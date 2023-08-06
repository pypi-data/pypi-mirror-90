import pandas as pd
import numpy as np
import warnings
from sklearn.base import BaseEstimator, TransformerMixin


class MapTransformer(BaseEstimator, TransformerMixin):
    """Class for the transformations of inputs into a useful representations 
    for the Decision Support Platform.

    Attributes
    ----------
    names_map : dict of {str: dict}
        contains column names as keys and values are dict's to be used
        as `pd.Series.map` argument.
    """

    def __init__(self, col_map_dict):
        self.col_map_dict = col_map_dict

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        """
        """
        # copy
        X_ = X.copy()

        for colname, map_dict in self.col_map_dict.items():

            X_[colname] = X_[colname].map(map_dict)

        return X_

class NameTransformer(BaseEstimator, TransformerMixin):
    """Class used to select and rename the columns of a DataFrame.

    Attributes
    ----------
    names_map : dict,
        defines how columns are renamed
    keep_features : list,
        defines columns which are kept with the original name
    """

    def __init__(self, names_map, keep_features):
        """
        Parameters
        ----------
        names_map : dict {str: str},
            defines how columns are renamed. Keys are original names and
            values, the new ones
        keep_features : list,
            defines columns which are kept with the original name.
        """

        intersection_ = set(names_map.keys()).intersection(keep_features)
        assert len(intersection_) == 0, \
            f"""The following columns are defined both in `keep_features` as in `names_map.keys()`:
            {intersection_}
            """

        self.names_map = names_map
        self.keep_features = keep_features


    def fit(self, X, y=None):

        return self


    def transform(self, X, y=None):
        """
        Transform dataset.
        Parameters
        ----------
        X : pandas DataFrame, shape=(n_samples, n_features)
            Input data to be transformed. Use ``dtype=np.float32`` for maximum
            efficiency.
        Returns
        -------
        X_transformed : pandas DataFrame, shape=(n_samples, n_out)
            Transformed dataset.
        """
        X_ = X[list(self.names_map.keys()) + self.keep_features].copy()
        X_ = X_.rename(self.names_map, axis=1)

        return X_




class SelectTransformerMixin:
    """Mixin class for applying `np.select` to DataFrames, using a dict as
    unique parameter

    Attributes
    ----------
    select_map: dict of {colname: dict of {`choicelist`: `condlist`}}
        where `choicelist` and `condlist` are the arguments of
        `np.select`. For setting `default` argument of `np.select`
         use the specific key `'default'` within the internal dict.
    """

    def __init__(self, select_map):

        self.select_map = select_map

    def select_transform(self, X):

        # copy
        X_ = X.copy()

        for col_name, conditions_dict in self.select_map.items():
            # debug = 'y_lab' in col_name

            # initialize np.select arguments
            default_value = conditions_dict.get('default')
            default_value = default_value(X_) if callable(default_value) else default_value
            cond_list = []
            choice_list = []

            #if debug:
                #affected = 0

            for k, func in conditions_dict.items():

                if k != 'default':

                    # collect conditions and choice labels
                    cond_list.append(func(X_))
                    # if debug:
                    #     affected += func(X_).sum()

                    if callable(k):
                        choice_list.append(k(X_))

                    else:
                        choice_list.append(k)
                    # print(k, func(X_).sum())
            # if debug:
            #     print(f'affected: {affected:,}')


            # insert new column
            X_.loc[:, col_name] = np.select(cond_list, choice_list, default=default_value)

        return X_


class SelectTransformer(SelectTransformerMixin, BaseEstimator, TransformerMixin):
    """
    Class for applying `np.select` to DataFrames, using a dict as
    unique parameter.
    Attributes
    ----------
    select_map: dict of {colname: dict of {`choicelist`: `condlist`}}
        where `choicelist` and `condlist` are the arguments of
        `np.select`. For setting `default` argument of `np.select`
         use the specific key `'default'` within the internal dict.
    """

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        # apply transform method
        return self.select_transform(X)


class AssignTransformerMixin:
    """Mixin class for applying `DataFrame.assign`, using a dict as
    unique parameter

    Attributes
    ----------
    assign_map : dict of {colname: udf},
        `udf` must return a series which will be stored on the
        dataframe on `colname` column.

    NOTE: `udf` must never modify input DataFrame. Pandas does not
    check this!
    """

    def __init__(self, assign_map):

        self.assign_map = assign_map

    def assign_transform(self, X):

        # copy
        X_ = X.copy()

        return X_.assign(**self.assign_map)


class AssignTransformer(AssignTransformerMixin, BaseEstimator, TransformerMixin):
    """Class for applying `np.select` to DataFrames, using a dict as
    unique parameter.

    Attributes
    ----------
    assign_map : dict of {colname: udf},
        `udf` must return a series which will be stored on the
        dataframe on `colname` column.

    NOTE: `udf` must never modify input DataFrame. Pandas does not
    check this!
    """

    def fit(self, X, y=None):
        return self

    def transform(self, X):

        # apply transform method
        return self.assign_transform(X)


class AssSelTransformer(
    BaseEstimator, TransformerMixin, SelectTransformerMixin,
    AssignTransformerMixin):
    '''Generates new cols by user DataFrame.assign and by np.select

    Parameters
    ----------
    select_map: dict of {colname: dict of {`choicelist`: `condlist`}}
        where `choicelist` and `condlist` are the arguments of
        `np.select`. For setting `default` argument of `np.select`
         use the specific key `'default'` within the internal dict.

    assign_map : dict {colname: udf},
        `udf` must return a series which will be stored on the
        dataframe on `colname` column
    '''


    def __init__(self, select_map, assign_map):

        warnings.warn(
            "The `AssSelTransformer` class will be deprecated. Prefer with `AssignTransformer` and/or "
            "`SelectTransformer`",
            DeprecationWarning, stacklevel=2)

        SelectTransformerMixin.__init__(self, select_map)
        AssignTransformerMixin.__init__(self, assign_map)


    def transform(self, X):
        '''Calls all transform methods'''

        # copy
        X_ = X.copy()

        # apply inherited transform methods
        X_ = self.select_transform(X_)
        X_ = self.assign_transform(X_)

        return X_











