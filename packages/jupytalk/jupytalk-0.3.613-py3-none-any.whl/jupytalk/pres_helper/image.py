"""
@file
@brief Helpers for presentations.
"""


def show_images(name1, name2=None, title1=None, title2=None, figsize=(12, 4)):
    """
    Uses :epkg:`matplotlib` to show images.

    @param      name1       name of the first image
    @param      name2       name of the second image
    @param      title1      title for the first image
    @param      title2      title for the second image
    @param      figsize     figure size
    @return                 ax
    """
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg

    img1 = mpimg.imread(name1)
    if name2 is None:
        _, ax = plt.subplots(1, 1, figsize=figsize)
        img2 = None
        ax.imshow(img1)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
        if title1 is not None:
            ax.set_title(title1)
    else:
        _, ax = plt.subplots(1, 2, figsize=figsize)
        img2 = mpimg.imread(name2)
        ax[0].imshow(img1)
        ax[0].get_xaxis().set_visible(False)
        ax[0].get_yaxis().set_visible(False)
        ax[1].imshow(img2)
        ax[1].get_xaxis().set_visible(False)
        ax[1].get_yaxis().set_visible(False)
        if title1 is not None:
            ax[0].set_title(title1)
        if title2 is not None:
            ax[1].set_title(title2)
    return ax
