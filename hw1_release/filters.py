"""
CS131 - Computer Vision: Foundations and Applications
Assignment 1
Author: Donsuk Lee (donlee90@stanford.edu)
Date created: 07/2017
Last modified: 10/16/2017
Python Version: 3.5+
"""

import numpy as np


def conv_nested(image, kernel):
    """A naive implementation of convolution filter.

    This is a naive implementation of convolution using 4 nested for-loops.
    This function computes convolution of an image with a kernel and outputs
    the result that has the same shape as the input image.

    Args:
        image: numpy array of shape (Hi, Wi).
        kernel: numpy array of shape (Hk, Wk).

    Returns:
        out: numpy array of shape (Hi, Wi).
    """
    Hi, Wi = image.shape
    Hk, Wk = kernel.shape
    out = np.zeros((Hi, Wi))

    ### YOUR CODE HERE
    hstep, vstep = Hk//2, Wk//2
    for m in range(Hi):
        for n in range(Wi):
            for i in range(min(m+hstep+1, Hk)):
                for j in range(min(n+vstep+1, Wk)):
                    if not ((m+hstep-i >= Hi) or (n+vstep-j >= Wi)):
                        out[m][n] += (kernel[i][j]*image[m+hstep-i][n+vstep-j])
    ### END YOUR CODE

    return out

def zero_pad(image, pad_height, pad_width):
    """ Zero-pad an image.

    Ex: a 1x1 image [[1]] with pad_height = 1, pad_width = 2 becomes:

        [[0, 0, 0, 0, 0],
         [0, 0, 1, 0, 0],
         [0, 0, 0, 0, 0]]         of shape (3, 5)

    Args:
        image: numpy array of shape (H, W).
        pad_width: width of the zero padding (left and right padding).
        pad_height: height of the zero padding (bottom and top padding).

    Returns:
        out: numpy array of shape (H+2*pad_height, W+2*pad_width).
    """

    H, W = image.shape
    out = None

    ### YOUR CODE HERE
    out = np.hstack((np.zeros((H, pad_width)), image, np.zeros((H, pad_width))))
    out = np.vstack((np.zeros((pad_height, out.shape[1])), out, np.zeros((pad_height, out.shape[1]))))
    ### END YOUR CODE
    
    return out


def conv_fast(image, kernel):
    """ An efficient implementation of convolution filter.

    This function uses element-wise multiplication and np.sum()
    to efficiently compute weighted sum of neighborhood at each
    pixel.

    Hints:
        - Use the zero_pad function you implemented above
        - There should be two nested for-loops
        - You may find np.flip() and np.sum() useful

    Args:
        image: numpy array of shape (Hi, Wi).
        kernel: numpy array of shape (Hk, Wk).

    Returns:
        out: numpy array of shape (Hi, Wi).
    """
    Hi, Wi = image.shape
    Hk, Wk = kernel.shape
    out = np.zeros((Hi, Wi))

    ### YOUR CODE HERE
    kernel = np.flip(np.flip(kernel, axis=0), axis=1)
    image = zero_pad(image, Hk//2, Wk//2)
    
    for m in range(Hi):
        for n in range(Wi):
            out[m, n] = np.sum(image[m:m+Hk, n:n+Wk]*kernel)
            
    ### END YOUR CODE

    return out

def conv_faster(image, kernel):
    """
    Args:
        image: numpy array of shape (Hi, Wi).
        kernel: numpy array of shape (Hk, Wk).

    Returns:
        out: numpy array of shape (Hi, Wi).
    """
    Hi, Wi = image.shape
    Hk, Wk = kernel.shape
    out = np.zeros((Hi, Wi))

    ### YOUR CODE HERE
    image = zero_pad(image, Hk//2, Wk//2)
    kernel = np.flip(np.flip(kernel, 0), 1)
    # The trick is to lay out all the (Hk, Wk) patches and organize them into a (Hi*Wi, Hk*Wk) matrix.
    # Also consider the kernel as (Hk*Wk, 1) vector. Then the convolution naturally reduces to a matrix multiplication.
    mat = np.zeros((Hi*Wi, Hk*Wk))
    for i in range(Hi*Wi):
        row = i // Wi
        col = i % Wi
        mat[i, :] = image[row: row+Hk, col: col+Wk].reshape(1, Hk*Wk)
    out = mat.dot(kernel.reshape(Hk*Wk, 1)).reshape(Hi, Wi)
    ### END YOUR CODE

    return out

def cross_correlation(f, g):
    """ Cross-correlation of f and g.

    Hint: use the conv_fast function defined above.

    Args:
        f: numpy array of shape (Hf, Wf).
        g: numpy array of shape (Hg, Wg).

    Returns:
        out: numpy array of shape (Hf, Wf).
    """

    out = None
    
    ### YOUR CODE HERE
    g = np.flip(np.flip(g, axis=0), axis=1)
    out = conv_fast(f, g)
    ### END YOUR CODE

    return out

def zero_mean_cross_correlation(f, g):
    """ Zero-mean cross-correlation of f and g.

    Subtract the mean of g from g so that its mean becomes zero.

    Hint: you should look up useful numpy functions online for calculating the mean.

    Args:
        f: numpy array of shape (Hf, Wf).
        g: numpy array of shape (Hg, Wg).

    Returns:
        out: numpy array of shape (Hf, Wf).
    """

    out = None
    ### YOUR CODE HERE
    g = g - np.mean(g)
    out = cross_correlation(f, g)
    ### END YOUR CODE

    return out

def normalized_cross_correlation(f, g):
    """ Normalized cross-correlation of f and g.

    Normalize the subimage of f and the template g at each step
    before computing the weighted sum of the two.

    Hint: you should look up useful numpy functions online for calculating 
          the mean and standard deviation.

    Args:
        f: numpy array of shape (Hf, Wf).
        g: numpy array of shape (Hg, Wg).

    Returns:
        out: numpy array of shape (Hf, Wf).
    """

    Hf, Wf = f.shape
    Hg, Wg = g.shape
    out = np.zeros((Hf, Wf))

    ### YOUR CODE HERE
    f = zero_pad(f, Hg//2, Wg//2)
    g = (g - np.mean(g)) / np.std(g)
    
    for m in range(Hf):
        for n in range(Wf):
            curr_img = f[m:m+Hg, n:n+Wg]
            out[m, n] = np.sum(((curr_img-np.mean(curr_img))/np.std(curr_img))*g)

    return out
