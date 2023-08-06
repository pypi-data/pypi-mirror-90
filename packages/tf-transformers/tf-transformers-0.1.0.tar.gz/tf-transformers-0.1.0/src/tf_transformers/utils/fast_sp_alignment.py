def fast_sp_split(sentence, tokenizer, SPECIAL_PIECE):
    original_words = sentence.split()
    subwords = tokenizer.tokenize(sentence)

    # Convert text into main_words (list of list of subwords per word)
    sub_words_mapped = []
    temp_tokens = []
    for tok in subwords:
        if tok == SPECIAL_PIECE:
            if temp_tokens:
                sub_words_mapped.append(temp_tokens)
                temp_tokens = []
            sub_words_mapped.append([tok])

        else:
            if tok.startswith(SPECIAL_PIECE):
                if temp_tokens:
                    sub_words_mapped.append(temp_tokens)
                    temp_tokens = []
                temp_tokens.append(tok)
            else:
                temp_tokens.append(tok)

    if temp_tokens:
        sub_words_mapped.append(temp_tokens)
    return original_words, sub_words_mapped

def account_for_special_piece_local(
    word_tokens, sub_words_mapped
):
    # this loop is used to accout for extra SPECIAL_PIECE
    # if any
    special_counter = 0
    aligned_words = []
    orig_to_new_index = []
    for index, _sub_word in enumerate(sub_words_mapped):
        # this is some extra SPECIAL PIECE character
        # add it to original word
        if len(_sub_word) == 1 and _sub_word[0] == SPECIAL_PIECE:
            special_counter += 1
            aligned_words.append(_sub_word[0])
        else:
            pos = index - special_counter
            aligned_words.append(word_tokens[pos])
            orig_to_new_index.append(index) # whenever original words comes, we need old-new mapping
    return orig_to_new_index, aligned_words

def fast_sp_alignment(sentence, tokenizer, SPECIAL_PIECE):
    """Fast Sentence Piece Alignment

    A sentence will be split into tokens based on whitespace, then tokenize using
    sentence piece tokenizer (GPT2, Albert, etc).

    Args:
        sentence ([type]): [description]
        tokenizer ([type]): [description]
        SPECIAL_PIECE ([type]): [description]

    Returns:
        [orig_to_new_index]: [list: Old to new index mapping alignment]
        [aligned_words]: [list of string: Aligns words (by adding SPECIAL_PIECE) if required]
        [sub_words_mapped]: [list of list of subwords]
    """

    original_words, sub_words_mapped = fast_sp_split(sentence, tokenizer, SPECIAL_PIECE)
    # If they are of different length mostly due to
    # extra SPECIAL_PIECE or unicode characters
    if len(original_words) != len(sub_words_mapped):
        # Try to re-align if possible
        try:
            orig_to_new_index, aligned_words = account_for_special_piece_local(original_words, sub_words_mapped)
        except:
            # if re-align fails, then tokenize like word-piece tokenizer
            # biut, using sentence piece
            aligned_words = original_words
            sub_words_mapped = [tokenizer.tokenize(word) for word in original_words]
            orig_to_new_index = range(len(original_words))

        assert(len(aligned_words) == len(sub_words_mapped))
        return orig_to_new_index,  aligned_words, sub_words_mapped
    else:
        # If this mapping fails, logic fails
        orig_to_new_index = range(len(original_words))
        return orig_to_new_index, original_words, sub_words_mapped



# new_to_orig_dict = dict(zip(orig_to_new_index, range(len(orig_to_new_index))))
# # reverse mapping

# reverse_start_index_align = tok_to_orig_index[tok_start_position] # aligned index
# reverse_end_index_align   = tok_to_orig_index[tok_end_position]


# reverse_start_index_original = new_to_orig_dict[reverse_start_index_align] # original (doc_tokens) index
# reverse_start_index_stop = new_to_orig_dict[reverse_end_index_align]