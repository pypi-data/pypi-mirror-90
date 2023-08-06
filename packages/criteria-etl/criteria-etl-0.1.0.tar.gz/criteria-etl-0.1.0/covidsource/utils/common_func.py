import pandas as pd
import numpy as np


def copy_docstring(sender):
    """Decorator for copying docstrings among functions.

    Parameters
    ----------
    sender: callable,
        where docstring will be copied from.
    receiver: callable,
        where dostring will be copied to.

    Example
    -------
    It can be used for different loader functions defined in each
    country source folder, normally in `utils.dataload`, by building
    wrappers of the agnostic functions defined in `covidsource.utils.
    dataload`.
    In the following example `sender=load_survey_data` and `receiver=
    load_survey_data_sv`:
    >>>@copy_docstring(load_survey_data)
    ...def load_survey_data_sv(path=SURVEY_DATA_PATH,
    ...                        load_func=LOCAL_LOAD_FUNC,
    ...                        columnnames_to_lower=True,
    ...                       ) -> pd.DataFrame:
    ...    return load_survey_data(
    ...        path, load_func,
    ...        columnnames_to_lower=columnnames_to_lower)

    source: https://softwareengineering.stackexchange.com/questions/
    386755/sharing-docstrings-between-similar-functions
    """

    def wrapper(receiver):
        receiver.__doc__ = sender.__doc__
        return receiver
    return wrapper


def bernoulli_on_rows(srs, row_bools, prob, seed = 300):
    '''Set values to zero using Bernoulli distribution on specific rows 
    of a Series.
    
    Parameters
    ----------
    srs : Series, 
        Series where specific rows are set as zero with probability `prob`.
    rows_bools: Series of bool
        specifies the columns where the values should be set to zero with
        probability `prob`.
    prob : float, 
        governs Bernoulli distribution.
    seed : random seed,
        used as argument of `np.random.seed` for ensuring replicability`.
    '''
    
    # generate bernoulli sample 
    np.random.seed(seed)
    bernoulli_srs = pd.Series(np.random.binomial(n = 1, p = prob, size =len(srs)))
    
    # exclude rows
    bernoulli_srs.loc[~ row_bools] = 1
    output = srs * bernoulli_srs.values
    
    return output
    

def uniform_decay(df, col, row_bools, decay):
    '''Apply uniform decay on column for specific rows. 
    
    Parameters
    ----------
    col : str,
        defines which is the column where this decay is applied.
    row_bools : Series of bool,
        define wich are the rows of `col` where uniform decay is  
        applied.
    decay : float,
        selected rows from `col` are multiplied by (1 - `decay`).
    '''
    unif_decay = row_bools.astype(float)
    unif_decay = unif_decay.replace(1, 1 - decay).replace(0, 1)
    output = df[col] * unif_decay
    return output
    

def proportional_cut(X, continuous_feature, threshold_col, n_buckets_threshold,
                     n_buckets_total, collapse_negative=False, **kwargs):
    """
    Transform continuous feature in binarized buckets proportional to a
    selected threshold.

    Parameters
    ----------
    X : pd.DataFrame,
        where columns are extracted.
    continuous_feature : column label,
        indicates wich columns is to be binarized.
    threshold_col : column label,
        indicates which column is used as threshold.
    n_buckets_threshold : int,
        number of bins to be used to reach threshold.
    n_buckets_total: int,
        total number of buckets. The rightmost bin will be unbounded,
        i.e. will contain which are greater than the seond last bin.
    collapse_negative : bool,
        whether negative values should be assigned to the leftmost bin.
        Default `False` (recommended).
    """

    bins = [i / n_buckets_threshold for i in range(0, n_buckets_total)]
    bins.append(np.inf)

    if collapse_negative:
        X.loc[X[continuous_feature] < 0, continuous_feature] = 0

    return pd.cut(
        X[continuous_feature] / X[threshold_col],
        bins=bins,
        labels=[i + 1 for i in range(n_buckets_total)],
        **kwargs
    )


def weighted_qcut(X, to_order_col, weights_col, q, **kwargs):
    """Return weighted quantile cuts from a given series, values.

    Parameters
    ----------
    X : pd.DataFrame,
        contains `to_order_col` and `weights_col`.
    to_order_col : column label,
        indicates the column according to which rows have to be ordered.
    weights_col : column label,
        indicates the column of weights.
    q : int,
        number of bins.
    """
    from pandas._libs.lib import is_integer

    if is_integer(q):
        quantiles = np.linspace(0, 1, q + 1)
    else:
        quantiles = q

    ordered_cum_sum = X[weights_col].iloc[X[to_order_col].argsort()].cumsum()
    bins = pd.cut(ordered_cum_sum / ordered_cum_sum.iloc[-1], quantiles,
                  **kwargs)
    return bins.sort_index()


def get_partition_bool_columns_dict(
        bool_cols, more_than_once, default, prefix='Solo ', suffix_to_remove='first'):
    """
    Returns dict to be used as `select_map` dict value on a
    `SelectTransformer` to partition a set of columns.

    The resulting partition first option will be two or more bool
    conditions from `bool_cols` followed by one per each bool column
    from `bool_cols` and if any bool condition is met from `bool_cols`,
    the default value will be used.

    Parameters
    ----------
    bool_cols : iterable of str,
        contains labels of columns where program `bool` observations
        will indicate whether or not the household is beneficiary of the
        program.
    more_than_once: str,
        used as choice when more than one bool condition is met on a
        row.
    default : str,
        used as default choice when no condition is met.
    prefix : str (optional),
        used as prefix on every choice which correspond to a single
        bool column from `bool_cols`. Default `'Solo '`
    suffix_to_remove : str (optional),
        to be removed from program cols on `choicelist`. Default
        `'first'`.
    """

    conditions = [
        lambda df, bool_cols=bool_cols:(df[bool_cols].sum(1) >= 2),
        * [(lambda df, col=col: df[col] == 1) for col in bool_cols
           ]]

    choices = [more_than_once, *[
        f'{prefix}{chn.replace(suffix_to_remove, "").replace("_", " ").strip()}'
        for chn in bool_cols
    ]]

    return {**dict(zip(choices, conditions)), **{'default': default}}


def new_poverty(original_poverty, modified_poverty):
    """
    Hardcoded function for getting `select_map` dict-value for computing
    new poverty.

    Parameters
    ----------
    original_poverty : column label,
        indicating the column of bools where reference poverty status
        needs to be taken.
    modified_poverty : column label,
        indicating column of bools where target poverty status  needs to
        be taken.
    """
    return {
        "Pobreza por COVID-19": lambda df, original_poverty=original_poverty,
        modified_poverty=modified_poverty: \
        (~ df[original_poverty]) & df[modified_poverty],
        "Se mantiene en pobreza": lambda df,
        original_poverty=original_poverty, modified_poverty=modified_poverty:
        df[original_poverty] & df[modified_poverty],
        "Se mantiene en no pobreza": lambda df,
        original_poverty=original_poverty, modified_poverty=modified_poverty:
        (~ df[original_poverty]) & (~ df[modified_poverty])
    }
