import math

import numpy as np
from scipy.ndimage import filters as scipy_filters

from . import dsift
from ..utils import rgb2gray, rgb_to_hsv


def phow(image, verbose=False, fast=True, sizes=(4, 6, 8, 10), step=2, color='gray',
         float_descriptors=False, magnification=6, window_size=1.5, contrast_threshold=0.005):
    r"""
    Extracts PHOW features from the ``image``. PHOW is simply dense
    SIFT applied at several resolutions.

    `descriptors` has the same format of `sift()` and `dsift()`. `frames[:,1:2]`
    are the x,y coordinates of the center of each descriptor, `frames[:,3]`
    is the contrast of the descriptor, as returned by `dsift()` (for
    colour variant, contrast is computed on the intensity channel).
    `frames[:,4]` is the size of the bin of the descriptor.

    By default, `phow()` computes the gray-scale variant of the descriptor. The
    `color` option can be used to compute the color variant instead.

    Unlike the  Matlab wrapper of vlfeat, the image
    is pre-smoothed at the desired scale level by gaussian filter provided
    by Scipy: ``scipy.ndimage.filters.gaussian_filter``.

    Parameters
    ----------
    image : [H, W] or [H, W, 1] `float32` `ndarray`
        A single channel, greyscale, `float32` numpy array (ndarray)
        representing the image to calculate descriptors for.
    fast : `bool`, optional
        If ``True``, use a piecewise-flat, rather than Gaussian,
        windowing function. While this breaks exact SIFT equivalence,
        in practice is much faster to compute.
    sizes : (`int`, `int`, `int`), optional
        Scales at which the dense SIFT features are extracted. Each
        value is used as bin size for the dsift() function.
    step : `int`, optional
        A SIFT descriptor is extracted every ``step`` pixels. This allows for
        sub-sampling of the image.
    color : `str`, optional
        Choose between 'gray', 'rgb', 'hsv', and 'opponent'.
    float_descriptors : `bool`, optional
        If ``True``, the descriptor are returned in floating point rather than
        integer format.
    magnification : `int`, optional
        Set the descriptor magnification factor. The scale of the keypoint is
        multiplied by this factor to obtain the width (in pixels) of the spatial
        bins. For instance, if there are there are 4 spatial bins along each
        spatial direction, the ``side`` of the descriptor is approximately ``4 *
        magnification``.
    window_size : `int`, optional
        Set the variance of the Gaussian window that determines the
        descriptor support. It is expressed in units of spatial bins.
    contrast_threshold : `float`, optional
        Contrast threshold below which SIFT features are mapped to
        zero. The input image is scaled to have intensity range in [0,1]
        (rather than [0,255]) and this value is compared to the
        descriptor norm as returned by dsift().
    verbose : bool`, optional
        If ``True``, be verbose.

    Returns
    -------
    frames : `(F, 4)` `float32` `ndarray`
        ``F`` is the number of keypoints (frames) used. This is the center
        of every dense SIFT descriptor that is extracted.
    descriptors : `(F, 128)` `uint8` or `float32` `ndarray`
        ``F`` is the number of keypoints (frames) used. The 128 length vectors
        per keypoint extracted. ``uint8`` by default.

    Examples
    --------
      >>> import numpy as np
      >>> from cyvlfeat.sift import phow
      >>> from scipy.misc import ascent
      >>> img = ascent().astype(np.float32)
      >>> frames, descriptors = phow(img, verbose=True)


    """

    # Standardize the image: The following block assumes that the user input
    # for argument color has somewhat more priority than
    # actual color space of I.
    # That is why the conversions are according to the value of variable 'color'
    # irrespective of actual color space to which I belongs.

    color_lower = color.lower()
    I = image.copy()

    # case where user inputs, color ='gray' and I is also greyscale.
    if color_lower == 'gray':
        num_channels = 1

        # case where user inputs, color ='gray' but I belongs to RGB space.
        if I.ndim == 3 and I.shape[2] > 1:
            I = rgb2gray(I)
    else:
        num_channels = 3

        # case where user inputs, color ='rgb' or 'hsv'or 'opponent' but I is greyscale.
        if I.shape[2] == 1:
            I = np.dstack([I, I, I])

        # case where user inputs, color ='rgb' and I also belongs to RGB space.
        elif color_lower == 'rgb':
            pass

        # case where user inputs, color ='opponent' and I belongs to RGB space.
        elif color_lower == 'opponent':

            # Note that the mean differs from the standard definition of opponent
            # space and is the regular intensity (for compatibility with
            # the contrast thresholding).
            # Note also that the mean is added pack to the other two
            # components with a small multipliers for monochromatic
            # regions.

            alpha = 0.01
            I = np.stack(
                (rgb2gray(I), (I[:, :, 0] - I[:, :, 1]) / math.sqrt(2) + alpha * rgb2gray(I),
                 I[:, :, 0] + I[:, :, 1] - 2 * I[:, :, 2] / math.sqrt(6) + alpha * rgb2gray(I)),
                axis=-1)
        # case when user inputs, color ='hsv' and I belongs to RGB space.
        elif color_lower == 'hsv':
            I = rgb_to_hsv(I)
        else:
            # case when user inputs, color ='hsv' and I belongs to RGB space.
            color_lower = 'hsv'
            I = rgb_to_hsv(I)
            print('Color space not recognized, defaulting to HSV color space.')

    if verbose:
        print('Color space: {}'.format(color))
        print('I size: {}x{}'.format(I.shape[0], I.shape[1]))
        print('Sizes: [{} {} {} {}]'.format(sizes[0], sizes[1], sizes[2], sizes[3]))

    temp_frames = []
    temp_descrs = []

    for si in range(0, len(sizes)):
        off = math.floor(1.0 + 3.0 / 2.0 * (max(sizes) - sizes[si]))

        # smooth I to the appropriate scale based on the size of the SIFT bins
        sigma = sizes[si] / magnification
        ims = scipy_filters.gaussian_filter(I, sigma)

        # extract dense SIFT features from all channels
        temp_all_results = []
        data = ims.copy()
        for k in range(num_channels):

            # The third dimension of an image matrix represent the no. of channels that are present.
            # In Matlab, size(I) returns: 256 x 256 which is same as the result returned by python's I.shape
            # where I is the numpy array of image. In Matlab, size(I,3) returns 1 for a greyscale
            # image but in Python, I.shape[2] raises an error -> tuple index out of range, simply because
            # there is no third channel. For RGB images I.shape[2] returns 3. The below if-else is a fix
            # for that.
            if ims.ndim == 2:
                # Since it is greyscale, we'd pass whole array (Dsift accepts only 2D arrays.)
                smoothed_image = data

            elif ims.ndim == 3:
                # Since it has 3 channels, i.e. could be split into 3 different channels(2D array) one by one.
                smoothed_image = data[:, :, k]
            else:
                raise ValueError('Image array not defined')

            temp_results = dsift(smoothed_image, step=step, size=sizes[si],
                                 bounds=np.array([off, off, image.shape[0] - 1, image.shape[1] - 1]),
                                 norm=True, fast=fast, float_descriptors=float_descriptors, verbose=verbose)

            temp_all_results.append(temp_results)
        f = []
        d = []
        for item in temp_all_results:
            f.append(item[0])
            d.append(item[1])

        # remove low contrast descriptors note that for color descriptors the V component is thresholded
        if color_lower in ['gray', 'opponent']:
            contrast = f[0][:, 2]
        elif color_lower == 'rgb':
            m = (f[0][:, 2], f[1][:, 2], f[2][:, 2])
            contrast = np.mean(m, axis=0)
        else:
            color_lower = 'hsv'
            contrast = f[2][:, 2]

        for k in range(num_channels):
            d[k][contrast < contrast_threshold] = 0

        temp_frames.append(np.column_stack([f[0][:, :3], sizes[si] * np.ones((f[0].shape[0], ), dtype=np.float32)]))
        temp_descrs.append(np.column_stack(d))
    frames = np.concatenate(temp_frames, axis=0)
    descriptors = np.concatenate(temp_descrs, axis=0)

    return frames, descriptors
