"""Utility functions.

"""
import numpy as np

def convert_pvals(df):
    """Converts the p-values in to significance levels.

    An example dataframe of p-values with a "sign" column:

    .. code-block:: text

        name,pval,sign
        Right Anterior,0.8,1
        Left Anterior,0.02,-1

    This dataframe will be converted into:

    .. code-block:: text

        name,value
        Right Anterior,0
        Left Anterior,-1

    Or without a "sign" column:

    .. code-block:: text

        name,pval
        Right Anterior,0.8
        Left Anterior,0.02

    This dataframe will be converted into:

    .. code-block:: text

        name,value
        Right Anterior,0
        Left Anterior,1

    Note:
        * The column name of p-values should be ``pval``.
        * The column name of the signs should be ``sign``. If there is no such
          column, the signs will not be applied to the converted p-values.

    Args:
        df (pandas.DataFrame): The dataframe with the p-values. It can also have
            a column to indicate the "sign" of the p-values. For example, this
            column can be used to indicate whether the correlations are positive
            (1) or negative (-1).

    Returns:
        pandas.DataFrame: The converted dataframe.

    """
    def func(pval):
        if pval > 0.05:
            return 0
        elif pval > 0.01:
            return 1
        elif pval > 0.001:
            return 2
        else:
            return 3
    values = df['pval'].apply(func)
    if 'sign' in df:
        values = np.sign(df['sign']) * values
    values = values.to_frame(name='value')
    return values
