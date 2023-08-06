from typing import Tuple

import tensorflow as tf
from tensorflow.python.ops import gen_array_ops


def decode_png(filename: str, channels: int = 1):
    """
    Read image from `filename` with `channels`.

    Parameters
    ----------
    filename : str
        A filename to read.
    channels : int, optional
        Number of channel. 3 for RGB, 1 for Grayscale, by default 1

    Returns
    -------
    tf.float32 `Tensor` of Image
        Image Tensor

    Examples
    --------
    >>> import tensorflow as tf
    >>> from utils import tf_images
    >>> sample_img = tf_images.decode_png("tests/test_resources/sample.png", 3)
    >>> tf.shape(sample_img)
    tf.Tensor([180 180   3], shape=(3,), dtype=int32)
    """
    bits = tf.io.read_file(filename)
    image = tf.image.decode_png(bits, channels)
    image = tf.cast(image, tf.float32)
    # image = tf.image.convert_image_dtype(image, dtype=tf.float32, saturate=False)
    return image


def save_img(tf_img, filename: str):
    """
    Save `Tensor` of `tf_img` to file.

    Parameters
    ----------
    tf_img : `Tensor`
        `Tensor` of image.
    filename : str
        File path to save.

    Examples
    --------
    >>> from utils import tf_images
    >>> tf_img = ...
    >>> tf_images.save_img(tf_img, "file_name.png")
    """
    tf.keras.preprocessing.image.save_img(filename, tf_img)


def tf_img_to_minmax(
    tf_img,
    threshold: float,
    min_max: Tuple[float, float] = (0.0, 1.0),
):
    """
    Convert grayscale `Tensor` of image, to `Tensor` of `min_max` value.

    Parameters
    ----------
    tf_img : `Tensor` of Image
        Should be grayscale image. (channel 1)
    threshold : float
        Threshold value to determine `min_max`
    min_max : Tuple[float, float], optional
        Min max value for `tf_img`, by default (0.0, 1.0)

    Returns
    -------
    `Tensor` of Image
        In image, exist only min_max values.

    Examples
    --------
    >>> import tensorflow as tf
    >>> from utils import tf_images
    >>> from tensorflow.python.ops import gen_array_ops
    >>> grayscale_sample_img = tf_images.decode_png("tests/test_resources/sample.png", 1)
    >>> min_maxed_grayscale_tf_image = tf_images.tf_img_to_minmax(
    ...     grayscale_tf_image, 127, (0, 255)
    ... )
    >>> reshaped_min_maxed_grayscale_tf_image = tf.reshape(
    ...     min_maxed_grayscale_tf_image, (-1, 1)
    ... )
    >>> print(gen_array_ops.unique_v2(reshaped_min_maxed_grayscale_tf_image, axis=[-2]))
    UniqueV2(y=<tf.Tensor: shape=(2, 1), dtype=float32, numpy=
    array([[255.],
        [  0.]], dtype=float32)>, idx=<tf.Tensor: shape=(32400,), dtype=int32, numpy=array([0, 0, 0, ..., 0, 0, 0], dtype=int32)>)
    >>> print(tf.math.count_nonzero(min_maxed_grayscale_tf_image))
    tf.Tensor(31760, shape=(), dtype=int64)
    """
    cond = tf.greater(tf_img, tf.ones_like(tf_img) * threshold)
    mask = tf.where(
        cond, tf.ones_like(tf_img) * min_max[1], tf.ones_like(tf_img) * min_max[0]
    )
    return mask


def tf_equalize_histogram(tf_img):
    """
    Tensorflow Image Histogram Equalization

    https://stackoverflow.com/questions/42835247/how-to-implement-histogram-equalization-for-images-in-tensorflow

    Parameters
    ----------
    tf_img : `Tensor` of image
        Input `Tensor` image `tf_img`

    Returns
    -------
    `Tensor` of image
        Equalized histogram image of input `Tensor` image `tf_img`.
    """
    values_range = tf.constant([0.0, 255.0], dtype=tf.float32)
    histogram = tf.histogram_fixed_width(tf.cast(tf_img, tf.float32), values_range, 256)
    cdf = tf.cumsum(histogram)
    cdf_min = cdf[tf.reduce_min(tf.where(tf.greater(cdf, 0)))]
    img_shape = tf.shape(tf_img)

    pix_cnt = img_shape[-3] * img_shape[-2]
    px_map = tf.round(
        tf.cast(cdf - cdf_min, tf.float32) * 255.0 / tf.cast(pix_cnt - 1, tf.float32)
    )
    px_map = tf.cast(px_map, tf.uint8)
    eq_hist = tf.expand_dims(tf.gather_nd(px_map, tf.cast(tf_img, tf.int32)), 2)
    return eq_hist


def remove_element(tensor, element):
    """
    Remove single element from 'tensor'.

    Parameters
    ----------
    tensor : `Tensor`
        Input `Tensor`
    element : `Tensor`
        Element to remove.

    Returns
    -------
    `Tensor`
        Tensor after remove element

    Examples
    --------
    >>> scs = remove_element(scs, [0, 0, 0])
    """
    check_element = tf.reduce_all(tf.equal(tensor, element), axis=-1)
    return tf.boolean_mask(tensor, tf.math.logical_not(check_element))


def tf_get_sorted_unique_color(tf_img):
    """
    Find unique colors in `tf_img`, and sort by number of colors.

    Parameters
    ----------
    tf_img : `Tensor` of image
        Input `Tensor` image `tf_img`. Should be color image.

    Returns
    -------
    `Tensor` array of colors
        All colors in `Tensor` image, sorted by number of colors.

    Examples
    --------
    >>> test_file_name: str = "lenna.png"
    >>> test_image_fullpath: str = os.path.join(
    ...     self.test_path, self.test_resource_folder_name, test_file_name
    ... )
    >>> tf_image = tf_images.decode_png(test_image_fullpath, 3)
    >>> #.
    >>> tf_images.tf_get_sorted_unique_color(tf_image)[:5]
    tf.Tensor(
    [[ 88.  18.  60.]
     [176.  67.  79.]
     [205.  96.  97.]
     [178.  69.  80.]
     [206. 100.  94.]], shape=(5, 3), dtype=float32)
    """
    scs = tf.reshape(tf_img, (-1, 3))
    scs, _, count = gen_array_ops.unique_with_counts_v2(scs, axis=[-2])
    scs_arg = tf.argsort(count, direction="DESCENDING")
    return tf.gather(scs, scs_arg)


def tf_get_all_colors(tf_img, black_first: bool = True):
    """
    Get all colors in `Tensor` image `tf_img`.
    The result always contains [0, 0, 0].

    Parameters
    ----------
    tf_img : `Tensor` of image
        Input `Tensor` image `tf_img`. Should be color image.
    black_first : bool, optional
        [description], by default True

    Returns
    -------
    `Tensor` array of colors
        All colors in `Tensor` image.

    Examples
    --------
    >>> import tensorflow as tf
    >>> from utils import tf_images
    >>> sample_img = tf_images.decode_png("tests/test_resources/sample.png", 3)
    >>> print(tf_images.tf_get_all_colors(sample_img))
    tf.Tensor(
    [[  0.   0.   0.]
     [245. 245. 245.]
     [ 71.  71.  71.]
     [255. 145.  77.]
     [ 72.  72.  72.]], shape=(5, 3), dtype=float32)
    """
    scs = tf_get_sorted_unique_color(tf_img)
    if black_first:
        scs = remove_element(scs, [0, 0, 0])
        scs = tf.cond(
            tf.reduce_any(tf.reduce_all(tf.equal(scs, [0, 0, 0]), axis=-1)),
            lambda: scs,
            lambda: tf.concat(
                [tf.constant([[0, 0, 0]], dtype=tf_img.dtype), scs], axis=-2
            ),
        )
    scs = tf.cast(scs, tf.float32)
    return scs


def tf_set_random_bucket(
    index, bin_size: int, shuffle_exclude_first: int = 0, seed: int = 42
):
    """
    Shuffle tensor in list.

    Parameters
    ----------
    index : `Tensor`
        Tensor will be shuffled.
    bin_size : int
        Result bin number
    shuffle_exclude_first : int, optional
        First `shuffle_exclude_first` elements will be excluded from shuffle, by default 0
    seed : int, optional
        Random seed value, by default 42

    Returns
    -------
    `Tensor`
        Shuffled array.

    Examples
    --------
    >>> ordered_index = tf.range(10, dtype=tf.int32)
    >>> tf_images.tf_set_random_bucket(
    ...     ordered_index, bin_size=5, shuffle_exclude_first=2
    ... )
    tf.Tensor([0 1 3 4 2], shape=(5,), dtype=int32)
    """
    bin_bucket = tf.range(
        start=shuffle_exclude_first, limit=bin_size, dtype=index.dtype
    )
    tf.random.set_seed(seed)
    shuffled_bin_bucket = tf.random.shuffle(bin_bucket)
    return tf.concat(
        [
            index[:shuffle_exclude_first],
            shuffled_bin_bucket[: bin_size - shuffle_exclude_first],
        ],
        axis=-1,
    )


def tf_generate_random_color_map(
    img, shuffle_exclude_first: int, bin_size: int, seed: int = 42
):
    """
    Get colors and random color index in image.

    Parameters
    ----------
    img : `Tensor`
        Tensor to generate color map.
    shuffle_exclude_first : int
        Random index calculate after this value.
    bin_size : int
        Result bin number
    seed : int, optional
        Random seed, by default 42

    Returns
    -------
    Tuple of `Tensor`
        (Tensor of map random index, Tensor of colors)

    Examples
    --------
    >>> test_file_name: str = "sample.png"
    >>> test_image_fullpath: str = os.path.join(
    ...     self.test_path, self.test_resource_folder_name, test_file_name
    ... )
    >>> tf_image = tf_images.decode_png(test_image_fullpath, 3)
    >>> #.
    >>> tf_images.tf_generate_random_color_map(
    ...     tf_image, shuffle_exclude_first=1, bin_size=5, seed=42
    ... )
    (<tf.Tensor: shape=(5,), dtype=float32, numpy=array([0., 4., 1., 2., 3.], dtype=float32)>, <tf.Tensor: shape=(5, 3), dtype=float32, numpy=
    array([[  0.,   0.,   0.],
        [245., 245., 245.],
        [255., 145.,  77.],
        [ 71.,  71.,  71.],
        [ 72.,  72.,  72.]], dtype=float32)>)
    """
    img_color_index, img_color = tf_generate_color_map(img)
    img_color_index = tf_set_random_bucket(
        img_color_index, bin_size, shuffle_exclude_first, seed=seed
    )
    return img_color_index, img_color


def tf_generate_color_map(img):
    """
    Get colors and color index in image.

    Parameters
    ----------
    img : `Tensor`
        Tensor to generate color map.

    Returns
    -------
    Tuple of `Tensor`
        (Tensor of map index, Tensor of colors)

    Examples
    --------
    >>> test_file_name: str = "sample.png"
    >>> test_image_fullpath: str = os.path.join(
    ...     self.test_path, self.test_resource_folder_name, test_file_name
    ... )
    >>> tf_image = tf_images.decode_png(test_image_fullpath, 3)
    >>> #.
    >>> tf_images.tf_generate_random_color_map(
    ...     tf_image, shuffle_exclude_first=1, bin_size=5, seed=42
    ... )
    (<tf.Tensor: shape=(5,), dtype=float32, numpy=array([0., 1., 2., 3., 4.], dtype=float32)>, <tf.Tensor: shape=(5, 3), dtype=float32, numpy=
    array([[  0.,   0.,   0.],
        [245., 245., 245.],
        [255., 145.,  77.],
        [ 71.,  71.,  71.],
        [ 72.,  72.,  72.]], dtype=float32)>)
    """
    img_color = tf_get_all_colors(img)
    img_color_index = tf.range(tf.shape(img_color)[-2], dtype=tf.float32)
    return img_color_index, img_color


def axis_converter(total_axis: int, axis: int):
    """
    Calculate axis using `total_axis`.
    For axis less than 0, and greater than 0.

    Parameters
    ----------
    total_axis : int
        Total axis num.
    axis : int
        Current axis num.

    Returns
    -------
    int
        Calculated current axis.
    """
    if axis < 0:
        return total_axis + axis
    else:
        return axis


def tf_change_channel_for_batch(img, index, axis: int):
    """
    Change channel by index. For batch(first channel).

    Parameters
    ----------
    img : `Tensor`
        Tensor to change order.
    index : `Tensor`
        Order array tensor consisting of `int`
    axis : int
        Change axis by

    Returns
    -------
    `Tensor`
        Order changed by index.

    Example
    -------
    >>> batch_sample_image_colors = [
    ...     [
    ...         [[0.0, 10.0, 20.0], [225.0, 235.0, 245.0]],
    ...         [[71.0, 41.0, 31.0], [255.0, 145.0, 77.0]],
    ...     ],
    ...     [
    ...         [[0.0, 10.0, 20.0], [225.0, 235.0, 245.0]],
    ...         [[71.0, 41.0, 31.0], [255.0, 145.0, 77.0]],
    ...     ],
    ... ]
    >>> new_order = [[2, 0, 1], [0, 2, 1]]
    >>> result = [
    ...     [
    ...         [[20.0, 0.0, 10.0], [245.0, 225.0, 235.0]],
    ...         [[31.0, 71.0, 41.0], [77.0, 255.0, 145.0]],
    ...     ],
    ...     [
    ...         [[0.0, 20.0, 10.0], [225.0, 245.0, 235.0]],
    ...         [[71.0, 31.0, 41.0], [255.0, 77.0, 145.0]],
    ...     ],
    ... ]
    >>> tf_images.tf_change_channel_for_batch(
    ...     batch_sample_image_colors, new_order, axis=3
    ... )
    """
    total_axis = tf.shape(tf.shape(img))[0]
    axis = axis_converter(total_axis, axis)

    b = tf.tile(index, [1, tf.reduce_prod(tf.shape(img)[1:axis])])
    b = tf.reshape(b, tf.shape(img)[: axis + 1])
    b = tf.cast(b, tf.int32)
    r = tf.gather_nd(tf.expand_dims(img, -1), tf.expand_dims(b, -1), batch_dims=axis)
    r = tf.squeeze(r, axis=-1)
    return r


def tf_change_channel(img, index, axis: int):
    """
    Change channel by index.

    Parameters
    ----------
    img : `Tensor`
        Tensor to change order.
    index : `Tensor`
        Order array tensor consisting of `int`
    axis : int
        Change axis by

    Returns
    -------
    `Tensor`
        Order changed by index.

    Example
    -------
    >>> batch_sample_image_colors = [
    ...     [[0.0, 10.0, 20.0], [225.0, 235.0, 245.0]],
    ...     [[71.0, 41.0, 31.0], [255.0, 145.0, 77.0]],
    ... ]
    >>> new_order = [[2, 0, 1]]
    >>> result = [
    ...     [[20.0, 0.0, 10.0], [245.0, 225.0, 235.0]],
    ...     [[31.0, 71.0, 41.0], [77.0, 255.0, 145.0]],
    ... ]
    >>> tf_images.tf_change_channel(
    ...     batch_sample_image_colors, new_order, axis=2
    ... )
    """
    total_axis = tf.shape(tf.shape(img))[0]
    axis = axis_converter(total_axis, axis)

    b = tf.tile(index, [1, tf.reduce_prod(tf.shape(img)[0:axis])])
    b = tf.reshape(b, tf.shape(img)[: axis + 1])
    b = tf.cast(b, tf.int32)
    r = tf.gather_nd(tf.expand_dims(img, -1), tf.expand_dims(b, -1), batch_dims=axis)
    r = tf.squeeze(r, axis=-1)
    return r


def tf_change_order(img, index):
    """
    Change channel by index. Simillar with `tf_change_channel()`.
    Works for TPU.

    Parameters
    ----------
    img : `Tensor`
        Tensor to change order.
    index : `Tensor`
        Order array tensor consisting of `int`

    Returns
    -------
    `Tensor`
        Order changed by index.

    Example
    -------
    >>> batch_sample_image_colors = [
    ...     [[0.0, 10.0, 20.0], [225.0, 235.0, 245.0]],
    ...     [[71.0, 41.0, 31.0], [255.0, 145.0, 77.0]],
    ... ]
    >>> new_order = [[2, 0, 1]]
    >>> result = [
    ...     [[[20.0], [0.0], [10.0]], [[245.0], [225.0], [235.0]]],
    ...     [[[31.0], [71.0], [41.0]], [[77.0], [255.0], [145.0]]],
    ... ]
    >>> tf_images.tf_change_order(batch_sample_image_colors, new_order)
    """
    b = tf.broadcast_to(index, tf.shape(img))
    b = tf.cast(b, tf.int32)
    r = tf.gather_nd(tf.expand_dims(img, -1), tf.expand_dims(b, -1), batch_dims=2)
    r = tf.squeeze(r)
    r = tf.expand_dims(r, -1)
    return r


def tf_image_detach_with_id_color_list(
    color_img, id_color_list, bin_num: int, mask_value: float = 1.0
):
    """
    Detach color image to `bin_num` size bucket.

    Don't do this for image which has many colors. (Too slow)

    Parameters
    ----------
    color_img : `Tensor`
        Tensor to detach by color. (Color image only)
    id_color_list : (`Tensor`, `Tensor`)
        Tuple of index, and color
    bin_num : int
        Detach bin number of image.
    mask_value : float, optional
        Masking value, by default 1.0

    Returns
    -------
    `Tensor`
        Tensor to detach by color

    Examples
    --------
    # 1) Get sample image as tf
    >>> test_file_name: str = "sample.png"
    >>> test_image_fullpath: str = os.path.join(
    ...     self.test_path, self.test_resource_folder_name, test_file_name
    ... )
    >>> tf_image = tf_images.decode_png(test_image_fullpath, 3)
    >>> #.
    >>> id_color_list = tf_images.tf_generate_color_map(tf_image)
    >>> #.
    >>> print(tf.shape(tf_image))
    tf.Tensor([180 180   3], shape=(3,), dtype=int32)
    >>> print(id_color_list)
    (<tf.Tensor: shape=(5,), dtype=float32, numpy=array([0., 1., 2., 3., 4.], dtype=float32)>, <tf.Tensor: shape=(5, 3), dtype=float32, numpy=
    array([[  0.,   0.,   0.],
        [245., 245., 245.],
        [255., 145.,  77.],
        [ 71.,  71.,  71.],
        [ 72.,  72.,  72.]], dtype=float32)>)
    >>> tf.shape(
    ...     tf_images.tf_image_detach_with_id_color_list(
    ...         tf_image, id_color_list=id_color_list, bin_num=30
    ...     )
    ... )
    tf.Tensor([180 180  30], shape=(3,), dtype=int32)
    """
    color_img = tf.cast(color_img, tf.float32)
    color_img = tf.expand_dims(color_img, axis=-2)
    color_num = tf.shape(id_color_list[1])[0]
    color_img = tf.broadcast_to(
        color_img,
        (
            tf.shape(color_img)[-4],
            tf.shape(color_img)[-3],
            color_num,
            tf.shape(color_img)[-1],
        ),
    )
    color_list_broad = tf.broadcast_to(
        id_color_list[1],
        (
            tf.shape(color_img)[-4],
            tf.shape(color_img)[-3],
            color_num,
            tf.shape(color_img)[-1],
        ),
    )
    r = tf.reduce_all(color_img == color_list_broad, axis=-1)
    result = tf.cast(r, tf.float32)
    result = tf.cond(
        bin_num > color_num,
        lambda: tf.concat(
            [
                result,
                tf.zeros(
                    (
                        tf.shape(color_img)[-4],
                        tf.shape(color_img)[-3],
                        bin_num - color_num,
                    )
                ),
            ],
            axis=-1,
        ),
        lambda: result,
    )
    return result


def tf_shrink3D(data, rows: int, cols: int, channels: int):
    """
    Shrink 3D `Tensor` data.

    Parameters
    ----------
    data : `Tensor`
        `Tensor` data to shrink. Shape should be 3-dimension.
    rows : int
        Number of rows
    cols : int
        Number of columns
    channels : int
        Number of channels

    Returns
    -------
    Shrinked `Tensor` array
        Shrinked 3d `Tensor`

    Examples
    --------
    >>> import tensorflow as tf
    >>> from utils import tf_images
    >>> a = tf.constant(
    ...     np.array(
    ...         [
    ...             [[1, 2], [3, 4]],
    ...             [[5, 6], [7, 8]],
    ...             [[9, 10], [11, 12]],
    ...             [[13, 14], [15, 16]],
    ...         ]
    ...     )
    ... )
    >>> print(shrink3D(a,2,1,2))
    tf.Tensor(
    [[[16 20]]  # [[[   1+3+5+7, 2+4+6+8]],
    [[48 52]]], shape=(2, 1, 2), dtype=int64)   #  [[9+11+13+15, 10+12+14+16]]]
    >>> print(shrink3D(a,2,1,1))
    tf.Tensor(
    [[[ 36]]    # [[[   1+3+5+7+2+4+6+8]],
     [[100]]], shape=(2, 1, 1), dtype=int64)    #  [[9+11+13+15+10+12+14+16]]]
    """
    return tf.reduce_sum(
        tf.reduce_sum(
            tf.reduce_sum(
                tf.reshape(
                    data,
                    [
                        rows,
                        tf.shape(data)[-3] // rows,
                        cols,
                        tf.shape(data)[-2] // cols,
                        channels,
                        tf.shape(data)[-1] // channels,
                    ],
                ),
                axis=1,
            ),
            axis=2,
        ),
        axis=3,
    )


def get_dynamic_size(_tensor):
    """
    Get dynamic batch size from 4d tensor.

    Parameters
    ----------
    _tensor : `Tensor`

    Returns
    -------
    Shape
        Dynamic tensor shape with batch size.
    """
    return tf.where([True, True, True, True], tf.shape(_tensor), [0, 0, 0, 0])


def tf_extract_patches(tf_array, ksize, img_wh, channel):
    """
    Extract Patches from `tf_array`.

    Other implementation of `tf.image.extract_patches`.

    Improved `tf_extract_patches`.

    - Conditions.
        - Padding is "SAME".
        - Stride is 1.
        - Width and Height are equal.

    Parameters
    ----------
    tf_array : `Tensor`
        Tensor array to extract patches. Shape should be (batch, height, width, channel).
    ksize : int
        Should be odd integer.
    img_wh : int
        Width and Height of square image.
    channel : int
        Number of channels.

    Returns
    -------
    `Tensor`
        Patch extracted `tf_array`
    """
    padding_size = max((ksize - 1), 0) // 2
    zero_padded_image = tf.keras.layers.ZeroPadding2D((padding_size, padding_size))(
        tf_array
    )
    # zero_padded_image = tf.pad(
    #     batch_image,
    #     [[0, 0], [padding_size, padding_size], [padding_size, padding_size], [0, 0]],
    # )

    b_size = get_dynamic_size(tf_array)
    batch_size = b_size[0]

    wh_indices = tf.range(ksize) + tf.range(img_wh)[:, tf.newaxis]

    a1 = tf.repeat(tf.repeat(wh_indices, ksize, axis=1), img_wh, axis=0)
    a2 = tf.tile(wh_indices, (img_wh, ksize))

    m = tf.stack([a1, a2], axis=-1)
    m = tf.expand_dims(m, axis=0)

    m1 = tf.repeat(m, batch_size, axis=0)
    m2 = tf.reshape(m1, (-1, img_wh, img_wh, ksize, ksize, 2))

    gg = tf.gather_nd(zero_padded_image, m2, batch_dims=1)
    gg2 = tf.reshape(gg, (-1, img_wh, img_wh, ksize * ksize * channel))

    return gg2
