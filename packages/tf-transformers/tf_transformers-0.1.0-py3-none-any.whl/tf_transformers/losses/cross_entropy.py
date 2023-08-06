import tensorflow as tf


def cross_entropy_loss(logits, labels, label_weights=None):
    """
    logits: 2D ((batch_size x num_words) x vocab_size)
    labels: 2D (batch_size x num_words )
    label_weights: 2D (batch_size x num_words) an array of either 0 or 1 or both
    """
    if logits.ndim == 3:
        logits = tf.reshape(logits, (-1, tf.shape(logits)[2]))
    log_probs = tf.nn.log_softmax(logits, axis=-1)
    vocab_size = tf.shape(logits)[1]
    label_ids = tf.reshape(labels, [-1])
    if label_weights is None:
        label_weights = tf.ones_like(label_ids)
    label_weights = tf.cast(tf.reshape(label_weights, [-1]), logits.dtype)
    one_hot_labels = tf.one_hot(label_ids, depth=vocab_size, dtype=tf.float32)

    # The `positions` tensor might be zero-padded (if the sequence is too
    # short to have the maximum number of predictions). The `label_weights`
    # tensor has a value of 1.0 for every real prediction and 0.0 for the
    # padding predictions.
    per_example_loss = log_probs * one_hot_labels
    per_example_loss = -tf.reduce_sum(per_example_loss, axis=[-1])
    numerator = label_weights * per_example_loss
    numerator = tf.reduce_sum(numerator)
    denominator = tf.reduce_sum(label_weights) + 1e-5
    loss = numerator / denominator
    return loss


def cross_entropy_loss_fast(labels, logits, label_weights=None):
    """
    logits: (.. , vocab_size)
    labels: (.. ) rank should be less than logits
    label_weights: labels shape

    Faster than above implementation
    """

    per_example_loss = tf.nn.sparse_softmax_cross_entropy_with_logits(logits=logits, labels=labels)

    if label_weights is None:
        label_weights = tf.ones_like(labels)
    per_example_loss = per_example_loss * tf.cast(label_weights, per_example_loss.dtype)
    numerator = tf.reduce_sum(per_example_loss)
    denominator = tf.cast(tf.reduce_sum(label_weights), numerator.dtype)
    denominator = tf.reduce_sum(label_weights)
    loss = tf.math.divide_no_nan(numerator, tf.cast(denominator, numerator.dtype))
    return loss
