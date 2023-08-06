import numpy as np

from cyvlfeat.quickshift.cyquickshift import cy_quickshift


def quickshift(image, kernel_size, max_dist=None,
               medoid=False, verbose=False,
               channel_first=False):
    r"""
    Quick shift is a mode seeking algorithm which links each pixel to
    its nearest neighbor which has an increase in the estimate of the
    density. These links form a tree, where the root of the tree is
    the pixel which correspond to the highest mode in the image.

    Parameters
    ----------
    image : [H, W] or [H, W, 1] `float64` `ndarray`
        A single channel, greyscale, `float64` numpy array (ndarray).
    kernel_size : ``double``
        The bandwidth parameter for density estimation.
    max_dist : ``double``, optional
        The maximum distance to a neighbor which increases
        the density. Since searching over all pixels for the nearest
        neighbor which increases the density would be prohibitively
        expensive, ``max_dist`` controls the maximum L2 distance between neighbors
        that should be linked.
    medoid : `bool`, optional
        If ``True``, run medoid shift instead of quick shift.
    verbose : `bool`, optional
        If ``True``, be verbose.

    Returns
    -------
    map : [H, W] `float64` `ndarray`. Array of the same size of I.
        Each element (pixel) of ``map`` is an index to the parent
        element in the forest.
    gaps: [H, W] `float64` `ndarray`. Array of the same size of I.
        ``gaps`` contains the corresponding branch length.
        Pixels which are at the root of their respective
        tree have MAP(x) = x and GAPS(x) = inf.
    estimate: [H, W] `float64` `ndarray`, optional
        The estimate of the density. Only returned if
        ``max_dist`` is not ``None``.
        
    Example
    -------
    >>> import numpy as np
    >>> from cyvlfeat.quickshift.quickshift import quickshift
    >>> from scipy.misc import ascent
    >>> img = ascent().astype(np.float64)
    >>> maps, gaps, estimate = quickshift(img, kernel_size=2, max_dist=10)
    >>> # medoid segmentation
    >>> maps, gaps, estimate = quickshift(img, kernel_size=2, max_dist=10, medoid=True)
    """

    # check for None
    if image is None or kernel_size is None:
        raise ValueError('A required input is None')

    # vlfeat requires image in channel-first style
    if image.ndim == 3:
        if not channel_first:
            image = image.transpose([2, 0, 1])
    # Add a channels axis
    if image.ndim == 2:
        image = np.expand_dims(image, axis=0)

    # Validate image size
    if image.ndim != 3:
        raise ValueError('Only 2D arrays with a channels axis are supported')

    compute_estimate = True

    if max_dist is None:
        compute_estimate = False
        # uses a default max_dist of kernel_size * 3
        max_dist = kernel_size * 3

    # Ensure types are correct before passing to Cython
    image = np.require(image, dtype=np.float64, requirements='C')

    result = cy_quickshift(image, kernel_size, max_dist, compute_estimate, medoid, verbose)

    return result
