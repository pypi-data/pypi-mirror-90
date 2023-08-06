import json
import tensorflow as tf
import time
import collections

from absl import logging
from tf_transformers.utils.tokenization import _is_whitespace
from tf_transformers.utils import fast_sp_alignment
logging.set_verbosity("INFO")

def read_squad_examples(
    input_file, is_training, version_2_with_negative, translated_input_folder=None
):
    """Read a SQuAD json file into a list of SquadExample."""
    del version_2_with_negative
    with tf.io.gfile.GFile(input_file, "r") as reader:
        input_data = json.load(reader)["data"]

    if translated_input_folder is not None:
        translated_files = tf.io.gfile.glob(
            os.path.join(translated_input_folder, "*.json")
        )
        for file in translated_files:
            with tf.io.gfile.GFile(file, "r") as reader:
                input_data.extend(json.load(reader)["data"])

    examples = []
    for entry in input_data:
        for paragraph in entry["paragraphs"]:
            paragraph_text = paragraph["context"]

            for qa in paragraph["qas"]:
                qas_id = qa["id"]
                question_text = qa["question"]
                start_position = None
                orig_answer_text = None
                is_impossible = False

                if is_training:
                    is_impossible = qa.get("is_impossible", False)
                    if (len(qa["answers"]) != 1) and (not is_impossible):
                        raise ValueError(
                            "For training, each question should have exactly 1 answer."
                        )
                    if not is_impossible:
                        answer = qa["answers"][0]
                        orig_answer_text = answer["text"]
                        start_position = answer["answer_start"]
                    else:
                        start_position = -1
                        orig_answer_text = ""


                example = {
                    "qas_id": qas_id,
                    "question_text": question_text,
                    "paragraph_text": paragraph_text,
                    "orig_answer_text": orig_answer_text,
                    "start_position": start_position,
                    "is_impossible": is_impossible,
                }
                examples.append(example)
    return examples



def _improve_answer_span(
    doc_tokens, input_start, input_end, tokenizer, orig_answer_text
):
    """Returns tokenized answer spans that better match the annotated answer."""

    # The SQuAD annotations are character based. We first project them to
    # whitespace-tokenized words. But then after WordPiece tokenization, we can
    # often find a "better match". For example:
    #
    #   Question: What year was John Smith born?
    #   Context: The leader was John Smith (1895-1943).
    #   Answer: 1895
    #
    # The original whitespace-tokenized answer will be "(1895-1943).". However
    # after tokenization, our tokens will be "( 1895 - 1943 ) .". So we can match
    # the exact answer, 1895.
    #
    # However, this is not always possible. Consider the following:
    #
    #   Question: What country is the top exporter of electornics?
    #   Context: The Japanese electronics industry is the lagest in the world.
    #   Answer: Japan
    #
    # In this case, the annotator chose "Japan" as a character sub-span of
    # the word "Japanese". Since our WordPiece tokenizer does not split
    # "Japanese", we just use "Japanese" as the annotation. This is fairly rare
    # in SQuAD, but does happen.
    tok_answer_text = " ".join(tokenizer.tokenize(orig_answer_text))

    for new_start in range(input_start, input_end + 1):
        for new_end in range(input_end, new_start - 1, -1):
            text_span = " ".join(doc_tokens[new_start : (new_end + 1)])
            if text_span == tok_answer_text:
                return (new_start, new_end)

    return (input_start, input_end)


def post_clean_train_squad(train_examples, basic_tokenizer, is_training=True):
    if is_training:
        start_time = time.time()
        train_examples_updated = []
        failed_examples = []
        for example in train_examples:
            paragraph_text = example['paragraph_text']
            orig_answer_text = example['orig_answer_text']
            start_position = example['start_position']

            paragraph_text_original = paragraph_text[:]
            paragraph_text = basic_tokenizer._clean_text(paragraph_text)

            if len(paragraph_text) == len(paragraph_text_original):
                _answer_mod = paragraph_text[start_position: (start_position) + len(orig_answer_text)]
                _answer_old = paragraph_text_original[start_position: (start_position) + len(orig_answer_text)]
                # assert(_answer_mod == _answer_old)
                # mostly unicode error , ignore
                if _answer_mod != _answer_old:
                    failed_examples.append(example)
                else:
                    example['paragraph_text'] = paragraph_text
                    train_examples_updated.append(example)
            else:
                # even if length varies, answer positions might remain same
                # because, the modifications might been occur after answer indexes
                _answer_mod = paragraph_text[start_position: start_position + len(orig_answer_text)]
                _answer_old = paragraph_text_original[start_position: start_position + len(orig_answer_text)]
                if _answer_mod != _answer_old:
                    new_pos_found = False
                    difference = len(paragraph_text_original) - len(paragraph_text)
                    for i in range(1, difference+1):
                        answer = paragraph_text[start_position-i: (start_position-i) + len(orig_answer_text)]
                        if answer == orig_answer_text:
                            start_position = start_position-i
                            new_pos_found = True
                            example['start_position'] = start_position
                            example['paragraph_text'] = paragraph_text
                            train_examples_updated.append(example)
                            break
                    if not new_pos_found:
                        failed_examples.append(example)
                else:
                    example['paragraph_text'] = paragraph_text
                    train_examples_updated.append(example)
        end_time = time.time()
        logging.info('Time taken {}'.format(end_time-start_time))
        return train_examples_updated, failed_examples
    else:
        for example in train_examples:
            example['paragraph_text'] = basic_tokenizer._clean_text(example['paragraph_text'])
        return train_examples



def convert_single_example_to_feature_fast_sp(tokenizer,
    example, is_training, max_seq_length, max_query_length, doc_stride, SPECIAL_PIECE="▁"
):
    # Convert text to tokens
    doc_tokens = []
    char_to_word_offset = []
    prev_is_whitespace = True
    for c in example["paragraph_text"]:
        if _is_whitespace(c):
            prev_is_whitespace = True
        else:
            if prev_is_whitespace:
                doc_tokens.append(c)
            else:
                doc_tokens[-1] += c
            prev_is_whitespace = False
        char_to_word_offset.append(len(doc_tokens) - 1)

    # Get start and end span

    orig_answer_text = example["orig_answer_text"]
    answer_offset = example["start_position"]
    answer_length = len(orig_answer_text)
    start_position = char_to_word_offset[answer_offset]
    end_position = char_to_word_offset[answer_offset + answer_length - 1]

    # Fast Alignment for subwords

    subwords = tokenizer.tokenize(example["paragraph_text"])
    orig_to_new_index, aligned_words, sub_words_mapped = fast_sp_alignment(
        example["paragraph_text"], tokenizer, SPECIAL_PIECE
    )

    # means a SPECIAL PIECE has been added
    if len(aligned_words) > len(doc_tokens):
        new_start_position = orig_to_new_index[start_position]
        new_end_position = orig_to_new_index[end_position]
    else:
        # same as before
        new_start_position = start_position
        new_end_position = end_position

    # Assertion
    temp_tokens = aligned_words[new_start_position : new_end_position + 1]
    temp_tokens = [token for token in temp_tokens if token != SPECIAL_PIECE]
    assert (
        temp_tokens
        == doc_tokens[start_position : end_position + 1]
    )

    # mapping
    tok_to_orig_index = []
    orig_to_tok_index = []
    all_doc_tokens = []
    for (i, token) in enumerate(aligned_words):
        orig_to_tok_index.append(len(all_doc_tokens))
        sub_tokens = sub_words_mapped[i]
        for sub_token in sub_tokens:
            tok_to_orig_index.append(i)
            all_doc_tokens.append(sub_token)

    # Get better positions
    tok_start_position = None
    tok_end_position = None
    if is_training and example["is_impossible"]:
        tok_start_position = -1
        tok_end_position = -1
    if is_training and not example["is_impossible"]:
        tok_start_position = orig_to_tok_index[new_start_position]
        if new_end_position < len(aligned_words) - 1:
            tok_end_position = orig_to_tok_index[new_end_position + 1] - 1
        else:
            tok_end_position = len(all_doc_tokens) - 1

    (tok_start_position, tok_end_position) = _improve_answer_span(
        all_doc_tokens,
        tok_start_position,
        tok_end_position,
        tokenizer,
        example["orig_answer_text"],
    )

    query_tokens = tokenizer.tokenize(example["question_text"])[:max_query_length]
    # The -3 accounts for [CLS], [SEP] and [SEP]
    max_tokens_for_doc = max_seq_length - len(query_tokens) - 3

    # We can have documents that are longer than the maximum sequence length.
    # To deal with this we do a sliding window approach, where we take chunks
    # of the up to our max length with a stride of `doc_stride`.
    _DocSpan = collections.namedtuple(  # pylint: disable=invalid-name
        "DocSpan", ["start", "length"]
    )
    doc_spans = []
    start_offset = 0
    while start_offset < len(all_doc_tokens):
        length = len(all_doc_tokens) - start_offset
        if length > max_tokens_for_doc:
            length = max_tokens_for_doc
        doc_spans.append(_DocSpan(start=start_offset, length=length))
        if start_offset + length == len(all_doc_tokens):
            break
        start_offset += min(length, doc_stride)

    all_results = []
    for (doc_span_index, doc_span) in enumerate(doc_spans):
        span_is_impossible = example["is_impossible"]
        start_position = None
        end_position = None
        if is_training and not span_is_impossible:
            # For training, if our document chunk does not contain an annotation
            # we throw it out, since there is nothing to predict.
            doc_start = doc_span.start
            doc_end = doc_span.start + doc_span.length - 1
            out_of_span = False
            if not (tok_start_position >= doc_start and tok_end_position <= doc_end):
                out_of_span = True
            if out_of_span:
                # continue
                start_position = 0
                end_position = 0
                span_is_impossible = True
                continue
            else:
                doc_offset = len(query_tokens) + 2  # for CLS   , SEP
                start_position = tok_start_position - doc_start + doc_offset
                end_position = tok_end_position - doc_start + doc_offset

                input_ids = (
                    [tokenizer.cls_token]
                    + query_tokens
                    + [tokenizer.sep_token]
                    + all_doc_tokens[doc_start : doc_end + 1]
                    + [tokenizer.sep_token]
                )

                result = {}
                result["input_ids"] = input_ids
                result["start_position"] = start_position
                result["end_position"] = end_position
                result["qas_id"] = example["qas_id"]
                all_results.append(result)
    return all_results


def convert_single_example_to_feature_fast_sp_test(tokenizer,
    example, is_training, max_seq_length, max_query_length, doc_stride, SPECIAL_PIECE="▁"
):
    # Convert text to tokens
    doc_tokens = []
    char_to_word_offset = []
    prev_is_whitespace = True
    for c in example["paragraph_text"]:
        if _is_whitespace(c):
            prev_is_whitespace = True
        else:
            if prev_is_whitespace:
                doc_tokens.append(c)
            else:
                doc_tokens[-1] += c
            prev_is_whitespace = False
        char_to_word_offset.append(len(doc_tokens) - 1)


    # Fast Alignment for subwords
    subwords = tokenizer.tokenize(example["paragraph_text"])
    orig_to_new_index, aligned_words, sub_words_mapped = fast_sp_alignment(
        example["paragraph_text"], tokenizer, SPECIAL_PIECE
    )

    # mapping
    tok_to_orig_index = []
    orig_to_tok_index = []
    all_doc_tokens = []
    for (i, token) in enumerate(aligned_words):
        orig_to_tok_index.append(len(all_doc_tokens))
        sub_tokens = sub_words_mapped[i]
        for sub_token in sub_tokens:
            tok_to_orig_index.append(i)
            all_doc_tokens.append(sub_token)

    query_tokens = tokenizer.tokenize(example["question_text"])[:max_query_length]
    # The -3 accounts for [CLS], [SEP] and [SEP]
    max_tokens_for_doc = max_seq_length - len(query_tokens) - 3

    # We can have documents that are longer than the maximum sequence length.
    # To deal with this we do a sliding window approach, where we take chunks
    # of the up to our max length with a stride of `doc_stride`.
    _DocSpan = collections.namedtuple(  # pylint: disable=invalid-name
        "DocSpan", ["start", "length"]
    )
    doc_spans = []
    start_offset = 0
    while start_offset < len(all_doc_tokens):
        length = len(all_doc_tokens) - start_offset
        if length > max_tokens_for_doc:
            length = max_tokens_for_doc
        doc_spans.append(_DocSpan(start=start_offset, length=length))
        if start_offset + length == len(all_doc_tokens):
            break
        start_offset += min(length, doc_stride)

    all_results = []
    for (doc_span_index, doc_span) in enumerate(doc_spans):
        doc_start = doc_span.start
        doc_end = doc_span.start + doc_span.length - 1

        doc_offset = len(query_tokens) + 2  # for CLS   , SEP
        input_ids = (
            [tokenizer.cls_token]
            + query_tokens
            + [tokenizer.sep_token]
            + all_doc_tokens[doc_start : doc_end + 1]
            + [tokenizer.sep_token]
        )

        result = {}
        result["input_ids"] = input_ids
        result["qas_id"] = example["qas_id"]
        all_results.append(result)
    return all_results

def example_to_features_using_fast_sp_alignment(tokenizer,
    examples, is_training, max_seq_length, max_query_length, doc_stride, SPECIAL_PIECE):
    count_pos_list = []
    count_neg_list = []
    count_pos = 0
    count_neg = 0
    example_counter = 0
    for example in examples:
        if is_training:
            result_list = convert_single_example_to_feature_fast_sp(tokenizer, example, is_training, max_seq_length, max_query_length, doc_stride, SPECIAL_PIECE
                )
        else:

        # no valid examples
        if result_list == []:
            count_neg_list.append(example['qas_id'])
            count_neg += 1
        else:
            count_pos_list.append({example['qas_id']: len(result_list)})
            count_pos += len(result_list)
            for result in result_list:
                yield result
        example_counter += 1

        if example_counter % 1000 == 0:
            logging.info("Wrote {} pos and {} neg examples".format(count_pos, count_neg))
