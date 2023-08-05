"""
Staircase
==============

Staircase is a MIT licensed library, written in pure-Python, for
modelling step functions. See :ref:`Getting Started <getting_started>` for more information.
"""

#uses https://pypi.org/project/sortedcontainers/
from sortedcontainers import SortedDict, SortedSet
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytz
import math
import warnings
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from .docstrings.decorator import add_doc, append_doc
from .docstrings import stairs_class as SC_docs
from .docstrings import stairs_module as SM_docs
warnings.simplefilter('default')

origin = pd.to_datetime('2000-1-1')
tz_default = None
use_dates_default = False

class Default():
    pass
    
_default = Default()
    
    
def _set_default_timezone(tz=None):
    global tz_default
    tz_default = pytz.timezone(tz) if tz else None
    
def _get_default_timezone():
    return tz_default
    
def _get_default_use_dates():
    return use_dates_default
    
def _set_default_use_dates(use_dates):
    global use_dates_default
    assert type(use_dates) is bool
    use_dates_default = use_dates

def set_defaults(**kwargs):
    key_map = {
        "timezone": _set_default_timezone,
        "use_dates": _set_default_use_dates,
    }
    for key, val in kwargs.items():
        key_map[key](val)
        
def get_defaults():
    key_map = {
            "timezone": _get_default_timezone,
            "use_dates": _get_default_use_dates,
    }
    return {key: val() for key, val in key_map.items()}
    
def _verify_window(left_delta, right_delta, zero):
    assert left_delta <= zero, "left_delta must not be positive"
    assert right_delta >= zero, "right_delta must not be negative"
    assert right_delta - left_delta > zero, "window length must be non-zero"

def _convert_date_to_float(val, tz=_get_default_timezone()):
    if val is None:
        return None
    if hasattr(val, "__iter__"):
        if not isinstance(val, pd.Series):
            val = pd.Series(val)
        if val.dt.tz is None and tz is not None:
            val = val.dt.tz_localize(tz)
        deltas = pd.TimedeltaIndex(val - origin.tz_localize(tz))
        return list(deltas/pd.Timedelta(1, 'h'))
    if val.tz is None and tz is not None:
        val = val.tz_localize(tz)
    return (val - origin.tz_localize(tz))/pd.Timedelta(1, 'h')
    
def _convert_float_to_date(val, tz=_get_default_timezone()):
    if hasattr(val, "__iter__"):
        if not isinstance(val, np.ndarray):
            val = np.array(val)
        return list(pd.to_timedelta(val*3600, unit='s') + origin.tz_localize(tz))
    return pd.to_timedelta(val*3600, unit='s') + origin.tz_localize(tz)

def _from_cumulative(cumulative, use_dates=False, tz=None):
    return Stairs(dict(zip(cumulative.keys(),np.insert(np.diff(list(cumulative.values())), 0, [next(iter(cumulative.values()))]))), use_dates, tz)

def _min_pair(stairs1, stairs2):
    """
    Calculates the minimum of two Stairs objects.  It can be thought of as calculating the minimum of two step functions.

    Parameters:
        stairs1 (Stairs)
        stairs2 (Stairs)

    Returns:
        Stairs: the result of the calculation

    """
    assert isinstance(stairs1, Stairs) and isinstance(stairs2, Stairs), "Arguments to min must be both of type Stairs."
    assert stairs1.tz == stairs2.tz
    new_instance = stairs1-stairs2
    cumulative = new_instance._cumulative()
    for key,value in cumulative.items():
        if value > 0:
            cumulative[key] = 0
    deltas = [cumulative.values()[0]]
    deltas.extend(np.subtract(cumulative.values()[1:], cumulative.values()[:-1]))
    new_instance = Stairs(dict(zip(new_instance._keys(), deltas)), use_dates=stairs1.use_dates or stairs2.use_dates, tz=stairs1.tz)
    return new_instance + stairs2
    
def _max_pair(stairs1, stairs2):
    """
    Calculates the maximum of two Stairs objects.  It can be thought of as calculating the maximum of two step functions.

    Parameters:
        stairs1 (Stairs)
        stairs2 (Stairs)

    Returns:
        Stairs: the result of the calculation

    """
    assert isinstance(stairs1, Stairs) and isinstance(stairs2, Stairs), "Arguments to max must be both of type Stairs."
    assert stairs1.tz == stairs2.tz
    new_instance = stairs1-stairs2
    cumulative = new_instance._cumulative()
    for key,value in cumulative.items():
        if value < 0:
            cumulative[key] = 0
    deltas = [cumulative.values()[0]]
    deltas.extend(np.subtract(cumulative.values()[1:], cumulative.values()[:-1]))
    new_instance = Stairs(dict(zip(new_instance._keys(), deltas)), use_dates=stairs1.use_dates or stairs2.use_dates, tz=stairs1.tz)
    return new_instance + stairs2

def _compare(cumulative, zero_comparator, use_dates=False, tz=None):
    truth = cumulative.copy()
    for key,value in truth.items():
        new_val = int(zero_comparator(float(value)))
        truth[key] = new_val
    deltas = [truth.values()[0]]
    deltas.extend(np.subtract(truth.values()[1:], truth.values()[:-1]))
    new_instance = Stairs(dict(zip(truth.keys(), deltas)), use_dates, tz)
    new_instance._reduce()
    return new_instance

def _get_union_of_points(collection):
    
    def dict_common_points():
        return collection.values()
        
    def series_common_points():
        return collection.values
        
    def array_common_points():
        return collection
    
    for func in (dict_common_points, series_common_points, array_common_points):
        try:
            stairs_instances = func()
            points = []
            for stair_instance in stairs_instances:
                points += list(stair_instance._keys())
            return SortedSet(points)
        except (AttributeError, TypeError):
            pass
    raise TypeError('Collection should be a tuple, list, numpy array, dict or pandas.Series.')
    
    
    

def _using_dates(collection):

    def dict_use_dates():
        s = next(iter(collection.values()))
        return s.use_dates, s.tz
        
    def series_use_dates():
        s = collection.values[0]
        return s.use_dates, s.tz
        
    def array_use_dates():
        s = collection[0]
        return s.use_dates, s.tz
    
    for func in (dict_use_dates, series_use_dates, array_use_dates):
        try:
            return func()
        except:
            pass
    raise TypeError('Could not determine if Stairs collection is using dates.  Collection should be a tuple, list, numpy array, dict or pandas.Series.')
        
    
@append_doc(SM_docs.sample_example)
def sample(collection, points=None, how='right', expand_key=True):
    """
    Takes a dict-like collection of Stairs instances and evaluates their values across a common set of points.
    
    Technically the results of this function should be considered as :math:`\\lim_{x \\to z^{-}} f(x)`
    or :math:`\\lim_{x \\to z^{+}} f(x)`, when how = 'left' or how = 'right' respectively. See
    :ref:`A note on interval endpoints<getting_started.interval_endpoints>` for an explanation.
        
    
    Parameters
    ----------
    collection : dictionary or pandas.Series
        The Stairs instances at which to evaluate
    points : int, float or vector data
        The points at which to sample the Stairs instances
    how : {'left', 'right'}, default 'right'
        if points where step changes occur do not coincide with x then this parameter
        has no effect.  Where a step changes occurs at a point given by x, this parameter
        determines if the step function is evaluated at the interval to the left, or the right.
    expand_key: boolean, default True
        used when collection is a multi-index pandas.Series.  Indicates if index should be expanded from
        tuple to columns in a dataframe.
        
    Returns
    -------
    :class:`pandas.DataFrame`
        A dataframe, in tidy format, with three columns: points, key, value.  The column key contains
        the identifiers used in the dict-like object specified by 'collection'.
        
    See Also
    --------
    Stairs.sample
    """
    use_dates, tz = _using_dates(collection)
    #assert len(set([type(x) for x in collection.values()])) == 1, "collection must contain values of same type"
    if points is None:
        points = _get_union_of_points(collection)
        if use_dates:
            points.discard(float('-inf'))
            points = _convert_float_to_date(list(points), tz) #bugfix - pandas>=1.1 breaks with points as type SortedSet
    else:
        if not hasattr(points, "__iter__"):
            points = [points]
    points = list(points) #bugfix - pandas>=1.1 breaks with points as type SortedSet
    result = (pd.DataFrame({"points":points, **{key:stairs.sample(points, how=how) for key,stairs in collection.items()}})
        .melt(id_vars="points", var_name="key")
    )
    if isinstance(collection, pd.Series) and expand_key and len(collection.index.names) > 1:
        try:
            result = (result
                .join(pd.DataFrame(result.key.tolist(), columns=collection.index.names))
                .drop(columns='key')
            )
        except:
            pass
    return result

@append_doc(SM_docs.aggregate_example)
def aggregate(collection, func, points=None):
    """
    Takes a collection of Stairs instances and returns a single instance representing the aggregation.
    
    Parameters
    ----------
    collection : tuple, list, numpy array, dict or pandas.Series
        The Stairs instances to aggregate
    func: a function taking a 1 dimensional vector of floats, and returning a single float
        The function to apply, eg numpy.max
    points: vector of floats or dates
        Points at which to evaluate.  Defaults to union of all step changes.  Equivalent to applying Stairs.resample().
        
    Returns
    ----------
    :class:`Stairs`
    
    Notes
    -----
    The points at which to aggregate will include -infinity whether explicitly included or not.
    
    See Also
    --------
    staircase.mean, staircase.median, staircase.min, staircase.max
    """
    if isinstance(collection, dict) or isinstance(collection, pd.Series):
        Stairs_dict = collection
    else:
        Stairs_dict = dict(enumerate(collection))
    use_dates, tz = _using_dates(collection)
    df = sample(Stairs_dict, points, expand_key=False)
    aggregation = df.pivot_table(index="points", columns="key", values="value").aggregate(func, axis=1)
    if use_dates:
        aggregation.index = _convert_date_to_float(aggregation.index, tz=tz)
    aggregation[float('-inf')] = func([val._sample_raw(float('-inf')) for key,val in Stairs_dict.items()])
    step_changes = aggregation.sort_index().diff().fillna(0)
    #groupby.sum is necessary on next line as step_changes series may not have unique index elements
    return Stairs(dict(step_changes.groupby(level=0).sum()), use_dates=use_dates, tz=tz)._reduce()
    
@append_doc(SM_docs.mean_example)
def _mean(collection):
    """
    Takes a collection of Stairs instances and returns the mean of the corresponding step functions.
    
    Parameters
    ----------
    collection : tuple, list, numpy array, dict or pandas.Series
        The Stairs instances to aggregate using a mean function
    
    Returns
    -------
    :class:`Stairs`
    
    See Also
    --------
    staircase.aggregate, staircase.median, staircase.min, staircase.max
    """
    return aggregate(collection, np.mean)

@append_doc(SM_docs.median_example)
def _median(collection):
    """
    Takes a collection of Stairs instances and returns the median of the corresponding step functions.
    
    Parameters
    ----------
    collection : tuple, list, numpy array, dict or pandas.Series
        The Stairs instances to aggregate using a median function
    
    Returns
    -------
    :class:`Stairs`
    
    See Also
    --------
    staircase.aggregate, staircase.mean, staircase.min, staircase.max
    """
    return aggregate(collection,np.median)

@append_doc(SM_docs.min_example)
def _min(collection):
    """
    Takes a collection of Stairs instances and returns the minimum of the corresponding step functions.
    
    Parameters
    ----------
    collection : tuple, list, numpy array, dict or pandas.Series
        The Stairs instances to aggregate using a min function
    
    Returns
    -------
    :class:`Stairs`
    
    See Also
    --------
    staircase.aggregate, staircase.mean, staircase.median, staircase.max
    """
    return aggregate(collection, np.min)

@append_doc(SM_docs.max_example)
def _max(collection):
    """
    Takes a collection of Stairs instances and returns the maximum of the corresponding step functions.
    
    Parameters
    ----------
    collection : tuple, list, numpy array, dict or pandas.Series
        The Stairs instances to aggregate using a max function
    
    Returns
    -------
    :class:`Stairs`
    
    See Also
    --------
    staircase.aggregate, staircase.mean, staircase.median, staircase.min
    """
    return aggregate(collection, np.max)


def resample(container, x, how='right'):
    """
    Applies the Stairs.resample function to a 1D container, eg tuple, list, numpy array, pandas series, dictionary
    
    Returns
    -------
    type(container)
    
    See Also
    --------
    Stairs.resample
    """
    if isinstance(container, dict):
        return {key:s.resample(x, how) for key,s in container}
    if isinstance(container, pd.Series):
        return pd.Series([s.resample(x, how) for s in container.values], index=container.index)
    if isinstance(container, np.ndarray):
        return np.array([s.resample(x, how) for s in container])
    return type(container)([s.resample(x, how) for s in container])
    
@append_doc(SM_docs.hist_from_ecdf_example)
def hist_from_ecdf(ecdf, bin_edges=None, closed='left'):
    """
    Calculates a histogram from a Stairs instance corresponding to an
    `empirical cumulative distribution function <https://en.wikipedia.org/wiki/Empirical_distribution_function>`_.
    
    Such ecdf stair instances are returned from :meth:`Stairs.ecdf_stairs`.  This function predominantly exists
    to allow users to store the result of a ecdf stairs instance locally, and experiment with bin_edges without
    requiring the recalculation of the ecdf.

    Parameters
    ----------
    ecdf : :class:`Stairs`
        lower bound of the step-function domain on which to perform the calculation
    bin_edges : int, float, optional
        defines the bin edges for the histogram (it is the domain of the ecdf that is being binned).
        If not specified the bin_edges will be assumed to be the integers which cover the domain of the ecdf
    closed: {'left', 'right'}, default 'left'
        determines whether the bins, which are half-open intervals, are left-closed , or right-closed
          
    Returns
    -------
    :class:`pandas.Series`
        A Series, with a :class:`pandas.IntervalIndex`, representing the values of the histogram
        
    See Also
    --------
    Stairs.hist
    Stairs.ecdf_stairs
    """
    if bin_edges is None:
        round_func = math.floor if closed == 'left' else math.ceil
        bin_edges = range(round_func(min(ecdf.step_changes().keys()))-(closed=='right'), round_func(max(ecdf.step_changes().keys())) + (closed=='left') + 1)
    return pd.Series(
        data = [ecdf(c2, how=closed) - ecdf(c1, how=closed) for c1, c2 in zip(bin_edges[:-1], bin_edges[1:])],
        index = pd.IntervalIndex.from_tuples([(c1,c2) for  c1, c2 in zip(bin_edges[:-1], bin_edges[1:])], closed=closed),
        dtype='float64',
    )
        
def _pairwise_commutative_operation_matrix(collection, op, assume_ones_diagonal, **kwargs):
    series = pd.Series(collection)
    size = series.shape[0]
    vals = np.ones(shape=(size,size))
    for i in range(size):
        for j in range(i+assume_ones_diagonal,size):
            vals[i,j] = op(series.iloc[i], series.iloc[j], **kwargs)
            vals[j,i] = vals[i,j]
    return pd.DataFrame(
        vals,
        index=series.index,
        columns=series.index
    )
    
@append_doc(SM_docs.corr_example)
def corr(collection, lower=float('-inf'), upper=float('inf')):
    """
    Calculates the correlation matrix for a collection of :class:`Stairs` instances
    
    Parameters
    ----------
    collection: :class:`pandas.Series`, dict, or array-like of :class:`Stairs` values
        the stairs instances with which to compute the correlation matrix
    lower : int, float or pandas.Timestamp
        lower bound of the interval on which to perform the calculation
    upper : int, float or pandas.Timestamp
        upper bound of the interval on which to perform the calculation
          
    Returns
    -------
    :class:`pandas.DataFrame`
        The correlation matrix
        
    See Also
    --------
    Stairs.corr, staircase.cov
    """
    return(_pairwise_commutative_operation_matrix(collection, Stairs.corr, True, lower=lower, upper=upper))
 
@append_doc(SM_docs.cov_example)
def cov(collection, lower=float('-inf'), upper=float('inf')):
    """
    Calculates the covariance matrix for a collection of :class:`Stairs` instances
    
    Parameters
    ----------
    collection: :class:`pandas.Series`, dict, or array-like of :class:`Stairs` values
        the stairs instances with which to compute the covariance matrix
    lower : int, float or pandas.Timestamp
        lower bound of the interval on which to perform the calculation
    upper : int, float or pandas.Timestamp
        upper bound of the interval on which to perform the calculation
          
    Returns
    -------
    :class:`pandas.DataFrame`
        The covariance matrix
        
    See Also
    --------
    Stairs.cov, staircase.corr
    """
    return(_pairwise_commutative_operation_matrix(collection, Stairs.cov, False, lower=lower, upper=upper))
    
class Stairs:
    """
    An instance of a Stairs class is used to represent a :ref:`step function <getting_started.step_function>`.
    
    The Stairs class encapsulates a `SortedDict <http://www.grantjenks.com/docs/sortedcontainers/sorteddict.html>`_
    which is used to hold the points at which the step function changes, and by how much.
    
    See the :ref:`Stairs API <api.Stairs>` for details of methods.
    """
    
    def __init__(self, value=0, use_dates=_default, tz=_default):
        """
        Initialise a Stairs instance.
        
        Parameters
        ----------
        value : float, default 0
            The value of the step function at negative infinity.
        use_dates: bool, default False
            Allows the step function to be defined with `Pandas.Timestamp <https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html>`_.
        
        Returns
        -------
        :class:`Stairs`
        """
        if use_dates == _default:
            use_dates = _get_default_use_dates()
        if tz == _default:
            tz = _get_default_timezone()
        
        self._sorted_dict = SortedDict()
        if isinstance(value, dict):
            self._sorted_dict = SortedDict(value)
        else:
            self._sorted_dict = SortedDict()
            self._sorted_dict[float('-inf')] = value
        self.use_dates = use_dates
        self.tz = tz
        self.cached_cumulative = None
        
        #bypass date mapping
        if not use_dates:
            self.sample = self._sample
            self.resample = self._resample
            self.layer = self._layer
            self.get_integral_and_mean = self._get_integral_and_mean
            self.clip = self._clip
            self.values_in_range = self._values_in_range
            self.step_changes = self._step_changes
            
        
        self._get = self._sorted_dict.get
        self._items = self._sorted_dict.items
        self._keys = self._sorted_dict.keys
        self._values = self._sorted_dict.values
        self._pop = self._sorted_dict.pop
        self._len = self._sorted_dict.__len__
        self._popitem = self._sorted_dict.popitem
    
    # DO NOT IMPLEMENT __len__ or __iter__, IT WILL CAUSE ISSUES WITH PANDAS SERIES PRETTY PRINTING
       
    def __getitem__(self,*args, **kwargs):
        """
        f'{dict.__getitem__.__doc__}'
        """
        return self._sorted_dict.__getitem__(*args, **kwargs)
        
    def __setitem__(self, key, value):
        """
        f'{dict.__setitem__.__doc__}'
        """
        self._sorted_dict.__setitem__(key, value)
    
    def copy(self, deep=None):
        """
        Returns a deep copy of this Stairs instance
        
        Parameters
        ----------
        deep : None
            Dummy parameter to keep pandas satisfied.

        Returns
        -------
        :class:`Stairs`
        """
        new_instance = Stairs(use_dates=self.use_dates, tz=self.tz)
        for key,value in self._items():
            new_instance[key] = value
        return new_instance

    def plot(self, ax=None, **kwargs):
        """
        Makes a step plot representing the finite intervals belonging to the Stairs instance.
        
        Uses matplotlib as a backend.

        Parameters
        ----------
        ax : :class:`matplotlib.axes.Axes`, default None
            Allows the axes, on which to plot, to be specified
        **kwargs
            Options to pass to :function: `matplotlib.pyplot.step`
        
        Returns
        -------
        :class:`matplotlib.axes.Axes`
        """
        if ax is None:
            _, ax = plt.subplots()
                
        cumulative = self._cumulative()
        if self.use_dates:
            register_matplotlib_converters()
            x = list(cumulative.keys())
            x[0] = x[1]-0.00001
            ax.step(_convert_float_to_date(x, self.tz), list(cumulative.values()), where='post', **kwargs)
        else:
            ax.step(cumulative.keys(), cumulative.values(), where='post', **kwargs)
        return ax

    def _sample_raw(self, x, how='right'):
        """
        Evaluates the value of the step function at one, or more, points.

        Technically the results of this function should be considered as :math:`\\lim_{x \\to z^{-}} f(x)`
        or :math:`\\lim_{x \\to z^{+}} f(x)`, when how = 'left' or how = 'right' respectively. See
        :ref:`A note on interval endpoints<getting_started.interval_endpoints>` for an explanation.

        Parameters
        ----------
        x : int, float or vector data
            values at which to evaluate the function
        how : {'left', 'right'}, default 'right'
            if points where step changes occur do not coincide with x then this parameter
            has no effect.  Where a step changes occurs at a point given by x, this parameter
            determines if the step function is evaluated at the interval to the left, or the right.
            
        Returns
        -------
        float, or list of floats
        
        See Also
        --------
        staircase.sample
        """
        assert how in ("right", "left")
        if hasattr(x, "__iter__"):
            new_instance = self.copy()._layer_multiple(x, None, [0]*len(x))
            cumulative = new_instance._cumulative()
            if how == "right":
                return [cumulative[_x] for _x in x]
            else:
                shifted_cumulative = SortedDict(zip(cumulative.keys()[1:], cumulative.values()[:-1]))
                if float('-inf') in x:
                    vals = [self[float('-inf')]]
                else:
                    vals = []
                vals.extend([val for key,val in shifted_cumulative.items() if key in x])
                return vals
        elif x == float('-inf'):
            return self._values()[0]
        else:
            cumulative = self._cumulative()
            if how == "right":
                preceding_boundary_index = cumulative.bisect_right(x) - 1
            else:
                preceding_boundary_index = cumulative.bisect_left(x) - 1
            return cumulative.values()[preceding_boundary_index]

    
    def _sample_agg(self, x, window, aggfunc, lower_how='right', upper_how='left'):
        """
        Evaluates the aggregation of the step function over a window around one, or more, points.

        The window around each point is defined by two values paired into an array-like parameter called *window*.
        These two scalars are the distance from the point to the left boundary of the window, and the right boundary
        of the window respectively.
        
        
        Parameters
        ----------
        x : int, float or vector data
            values at which to evaluate the function
        aggfunc: {'mean', 'median', 'mode', 'max', 'min', 'std'}
            A string corresponding to the aggregating function
        window : array-like of int, float, optional
            Should be length of 2. Defines distances from focal point to window boundaries.
        lower_how: {'left', 'right'}, default 'right'
            Determines how the left window boundary should be evaluated.
            If 'left' then :math:`\\lim_{x \\to lower_how^{-}} f(x)` is included in the window.
        upper_how: {'left', 'right'}, default 'left'
            Determines how the right window boundary should be evaluated.
            If 'right' then :math:`\\lim_{x \\to upper_how^{+}} f(x)` is included in the window.
            
        Returns
        -------
        float, or list of floats
        
        See Also
        --------
        staircase.sample
        """
        assert len(window) == 2, "Window should be a array-like object of length 2."
        if isinstance(aggfunc, str):
            aggfunc = _stairs_methods[aggfunc]
        left_delta, right_delta = window
        _verify_window(left_delta, right_delta, 0)
        kwargs = {"lower_how":lower_how, "upper_how":upper_how} if aggfunc in [Stairs.min, Stairs.max] else {}
        if not hasattr(x, "__iter__"):
            return aggfunc(self, lower=x+left_delta, upper=x+right_delta, **kwargs)
        return [aggfunc(self, lower=point+left_delta, upper=point+right_delta, **kwargs) for point in x]
    
    @append_doc(SC_docs.sample_example)
    def _sample(self, x, how='right', aggfunc=None, window=(0,0), lower_how='right', upper_how='left'):
        """
        Evaluates the value of the step function at one, or more, points.

        This method can be used to directly sample values of the corresponding step function at the points
        provided, or alternatively calculate aggregations over some window around each point.  The first of these
        is performed when *aggfunc* is None.
        
        If *aggfunc* is None then the results of this function should be considered as :math:`\\lim_{x \\to z^{-}} f(x)`
        or :math:`\\lim_{x \\to z^{+}} f(x)`, when how = 'left' or how = 'right' respectively. See
        :ref:`A note on interval endpoints<getting_started.interval_endpoints>` for an explanation.
        
        If *aggfunc* is not None then a window, around each point x (referred to as the focal point), over which to aggregate is required.
        The window is defined by two values paired into an array-like parameter called *window*.
        These two scalars are the distance from the focal point to the left boundary of the window, and the right boundary
        of the window respectively.
        
        The function can be called using parentheses.  See example below.

        Parameters
        ----------
        x : int, float or vector data
            Values at which to evaluate the function
        how : {'left', 'right'}, default 'right'
            Only relevant if *aggfunc* is None.
            if points where step changes occur do not coincide with x then this parameter
            has no effect.  Where a step changes occurs at a point given by x, this parameter
            determines if the step function is evaluated at the interval to the left, or the right.
        aggfunc: {'mean', 'median', 'mode', 'max', 'min', 'std', None}.  Default None.
            A string corresponding to the aggregating function
        window : array-like of int, float or pandas.Timedelta, optional
            Only relevant if *aggfunc* is not None.  Should be length of 2. Defines distances from focal point to window boundaries.
        lower_how: {'left', 'right'}, default 'right'
            Only relevant if *aggfunc* is not None.  Determines how the left window boundary should be evaluated.
            If 'left' then :math:`\\lim_{x \\to lower_how^{-}} f(x)` is included in the window.
        upper_how: {'left', 'right'}, default 'left'
            Only relevant if *aggfunc* is not None.  Determines how the right window boundary should be evaluated.
            If 'right' then :math:`\\lim_{x \\to upper_how^{+}} f(x)` is included in the window.
            
        Returns
        -------
        float, or list of floats
        
        See Also
        --------
        staircase.sample
        """
        #not using dates
        if aggfunc is None:
            return self._sample_raw(x, how)
        else:
            return self._sample_agg(x, window, aggfunc, lower_how, upper_how)
    
    
    @add_doc(_sample.__doc__)
    def sample(self, x, how='right', aggfunc=None, window=(0,0), lower_how='right', upper_how='left'):
        #wrapper for dates
        x = _convert_date_to_float(x, self.tz)
        if aggfunc is not None:
            left_delta, right_delta = window
            if isinstance(left_delta, pd.Timedelta):
                left_delta = _convert_date_to_float(origin + left_delta, self.tz) - _convert_date_to_float(origin, self.tz) #convert to hrs
            if isinstance(right_delta, pd.Timedelta):
                right_delta = _convert_date_to_float(origin + right_delta, self.tz) - _convert_date_to_float(origin, self.tz) #convert to hrs
                window = (left_delta, right_delta)
        return self._sample(x,how,aggfunc,window,lower_how,upper_how)
    
    @append_doc(SC_docs.resample_example)
    def _resample(self, x, how='right', aggfunc=None, window=(0,0), lower_how='right', upper_how='left'):
        """
        Evaluates the value of the step function at one, or more, points and
        creates a new Stairs instance whose step changes occur at a subset of these
        points.  The new instance and self have the same values when evaluated at x.

        Parameters
        ----------
        x : int, float or vector data
            values at which to evaluate the function
        how : {'left', 'right'}, default 'right'
            if points where step changes occur do not coincide with x then this parameter
            has no effect.  Where a step changes occurs at a point given by x, this parameter
            determines if the step function is evaluated at the interval to the left, or the right.
        aggfunc: {'mean', 'median', 'mode', 'max', 'min', 'std', None}.  Default None.
            A string corresponding to the aggregating function
        window : array-like of int, float or pandas.Timedelta, optional
            Only relevant if *aggfunc* is not None.  Should be length of 2. Defines distances from focal point to window boundaries.
        lower_how: {'left', 'right'}, default 'right'
            Only relevant if *aggfunc* is not None.  Determines how the left window boundary should be evaluated.
            If 'left' then :math:`\\lim_{x \\to lower_how^{-}} f(x)` is included in the window.
        upper_how: {'left', 'right'}, default 'left'
            Only relevant if *aggfunc* is not None.  Determines how the right window boundary should be evaluated.
            If 'right' then :math:`\\lim_{x \\to upper_how^{+}} f(x)` is included in the window.
         
        Returns
        -------
        :class:`Stairs`
      
        See Also
        --------
        staircase.resample
        """
        if not hasattr(x, "__iter__"):
            x = [x,]
        new_cumulative = SortedDict({float('-inf'):self._sample(float('-inf'))})
        new_cumulative.update({point:self._sample(point, how, aggfunc, window, lower_how, upper_how) for point in x})
        return _from_cumulative(new_cumulative, self.use_dates, self.tz)

    @add_doc(_resample.__doc__)
    def resample(self, x, how='right', aggfunc=None, window=(0,0)):
        x = _convert_date_to_float(x, self.tz)
        if aggfunc is not None:
            assert len(window) == 2, "Window should be a array-like object of length 2."
            left_delta, right_delta = window
            if isinstance(left_delta, pd.Timedelta):
                left_delta = _convert_date_to_float(origin + left_delta) - _convert_date_to_float(origin) #convert to hrs
            if isinstance(right_delta, pd.Timedelta):
                right_delta = _convert_date_to_float(origin + right_delta) - _convert_date_to_float(origin) #convert to hrs
            window = (left_delta, right_delta)
        return self._resample(x, how, aggfunc, window, lower_how='right', upper_how='left')

    
    @append_doc(SC_docs.layer_example)
    def _layer(self, start=None, end=None, value=None):
        """
        Changes the value of the step function.
        
        
        Parameters
        ----------
        start : int, float or vector data, optional
            start time(s) of the interval(s)
        end : int, float or vector data, optional
            end time(s) of the interval(s)
        value: int, float or vector data, optional
            value(s) of the interval(s)
              
        Returns
        -------
        :class:`Stairs`
            The current instance is returned to facilitate method chaining
        
        """
        if hasattr(start, "__iter__") or hasattr(end, "__iter__"):
            layer_func = self._layer_multiple
        else:
            layer_func = self._layer_single
        return layer_func(start, end, value)

    @add_doc(_layer.__doc__)
    def layer(self, start=None, end=None, value=None):
        start = _convert_date_to_float(start, self.tz)
        if end is not None:
            end = _convert_date_to_float(end, self.tz)
        return self._layer(start, end, value)

        
    def _layer_single(self, start=None, end=None, value=None):
        """
        Implementation of the layer function for when start parameter is single-valued
        """
        if pd.isna(start):
            start = float('-inf')
        if pd.isna(value):
            value = 1
        self[start] = self._get(start,0) + value
        if start != float('-inf') and self[start] == 0:
            self._pop(start)
        
        if not pd.isna(end):
            self[end] = self._get(end,0) - value
            if self[end] == 0 or end == float('inf'):
                self._pop(end)
                
        self.cached_cumulative = None
        return self
                
    
    def _layer_multiple(self, starts=None, ends=None, values = None):
        """
        Implementation of the layer function for when start parameter is vector data
        """
        for vector in (starts, ends):
            if vector is not None and values is not None:
                assert len(vector) == len(values)
        
        if starts is None: starts = [float('-inf')]*len(ends)
        if ends is None: ends = []
        if values is None: values = [1]*max(len(starts), len(ends))
        
        for start, value in zip(starts, values):
            if pd.isna(start):
                start = float('-inf')
            self[start] = self._get(start,0) + value
        for end, value in zip(ends, values):
            if not pd.isna(end):
                self[end] = self._get(end,0) - value
        self.cached_cumulative = None
        return self

    @append_doc(SC_docs.step_changes_example)
    def _step_changes(self):
        """
        Returns a dictionary of key, value pairs of indicating where step changes occur in the step function, and the change in value
        
        Returns
        -------
        dictionary
        
        See Also
        --------
        Stairs.number_of_steps
        """
        return dict(self._items()[1:])
    
    @add_doc(_step_changes.__doc__)
    def step_changes(self):
        return dict(zip(_convert_float_to_date(self._keys()[1:], self.tz), self._values()[1:]))

    @append_doc(SC_docs.negate_example)
    def negate(self):
        """
        An operator which produces a new Stairs instance representing the multiplication of the step function by -1.
        
        Should be used as an operator, i.e. by utilising the symbol -.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing the multiplication of the step function by -1
            
        See Also
        --------
        Stairs.subtract
        """
        new_instance = self.copy()
        for key,delta in new_instance._items():
            new_instance[key] = -delta
        new_instance.cached_cumulative = None
        return new_instance
    
    @append_doc(SC_docs.add_example)
    def add(self, other):
        """
        An operator facilitating the addition of two step functions.
        
        Should be used as an operator, i.e. by utilising the symbol +.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing the addition of two step functions
            
        See Also
        --------
        Stairs.subtract
        """
        if not isinstance(other, Stairs):
            other = Stairs(other, self.use_dates, self.tz)
        new_instance = self.copy()
        for key, value in other._items():
            new_instance[key] = self._get(key,0) + value
        new_instance._reduce()
        new_instance.use_dates = self.use_dates or other.use_dates
        new_instance.cached_cumulative = None
        return new_instance
    
    @append_doc(SC_docs.subtract_example)
    def subtract(self, other):
        """
        An operator facilitating the subtraction of one step function from another.
        
        Should be used as an operator, i.e. by utilising the symbol -.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing the subtraction of one step function from another
        
        See Also
        --------
        Stairs.add
        """
        if not isinstance(other, Stairs):
            other = Stairs(other, self.use_dates, self.tz)
        other = -other
        return self + other
    
    def _mul_or_div(self, other, func):
        a = self.copy()
        b = other.copy()
        a_keys = a._keys()
        b_keys = b._keys()
        a._layer_multiple(b_keys, None, [0]*len(b_keys))
        b._layer_multiple(a_keys, None, [0]*len(a_keys))
        
        multiplied_cumulative_values = func(a._cumulative().values(), b._cumulative().values())
        new_instance = _from_cumulative(dict(zip(a._keys(), multiplied_cumulative_values)), use_dates=self.use_dates, tz=self.tz)
        new_instance._reduce()
        return new_instance
        
    @append_doc(SC_docs.divide_example)
    def divide(self, other):
        """
        An operator facilitating the division of one step function by another.

        The divisor should cannot be zero-valued anywhere.

        Should be used as an operator, i.e. by utilising the symbol /.  See examples below.

        Returns
        -------
        :class:`Stairs`
            A new instance representing the division of one step function by another
            
        See Also
        --------
        Stairs.multiply
        """
        if not bool(other.make_boolean()):
            raise ZeroDivisionError("Divisor Stairs instance must not be zero-valued at any point")
        
        return self._mul_or_div(other, np.divide)
    
    @append_doc(SC_docs.multiply_example)
    def multiply(self, other):
        r"""
        An operator facilitating the multiplication of one step function with another.
        
        Should be used as an operator, i.e. by utilising the symbol \*.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing the multiplication of one step function from another
        
        See Also
        --------
        Stairs.divide
        """
        return self._mul_or_div(other, np.multiply)
        
    def _cumulative(self):
        if self.cached_cumulative == None:
            self.cached_cumulative = SortedDict(zip(self._keys(), np.cumsum(self._values())))
        return self.cached_cumulative
    
    @append_doc(SC_docs.make_boolean_example)
    def make_boolean(self):
        """
        Returns a boolean-valued step function indicating where *self* is non-zero.
        
        Returns
        -------
        :class:`Stairs`
            A new instance representing where *self* is non-zero
        
        See Also
        --------
        Stairs.invert
        """
        new_instance = self != Stairs(0)
        return new_instance
    
    @append_doc(SC_docs.invert_example)
    def invert(self):
        """
        Returns a boolean-valued step function indicating where *self* is zero-valued.
        
        Equivalent to ~*self*
        
        Returns
        -------
        :class:`Stairs`
            A new instance representing where *self* is zero-valued
        
        See Also
        --------
        Stairs.make_boolean
        """
        new_instance = self.make_boolean()
        new_instance = Stairs(1, self.use_dates, self.tz) - new_instance
        return new_instance
    
    @append_doc(SC_docs.logical_and_example)
    def logical_and(self, other):
        """
        Returns a boolean-valued step function indicating where *self* and *other* are non-zero.
        
        Equivalent to *self* & *other*.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing where *self* & *other*
            
        See Also
        --------
        Stairs.logical_or
        """
        assert isinstance(other, type(self)), "Arguments must be both of type Stairs."
        self_bool = self.make_boolean()
        other_bool = other.make_boolean()
        return _min_pair(self_bool, other_bool)
    
    @append_doc(SC_docs.logical_or_example)
    def logical_or(self, other):
        """
        Returns a boolean-valued step function indicating where *self* or *other* are non-zero.
        
        Equivalent to *self* | *other*.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing where *self* | *other*
        
        See Also
        --------
        Stairs.logical_and
        """
        assert isinstance(other, type(self)), "Arguments must be both of type Stairs."
        self_bool = self.make_boolean()
        other_bool = other.make_boolean()
        return _max_pair(self_bool, other_bool)

    @append_doc(SC_docs.lt_example)
    def lt(self, other):
        """
        Returns a boolean-valued step function indicating where *self* is strictly less than *other*.
        
        Equivalent to *self* < *other*.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing where *self* < *other*
            
        See Also
        --------
        Stairs.gt, Stairs.le, Stairs.ge
        """
        if not isinstance(other, Stairs):
            other = Stairs(other, self.use_dates, self.tz)
        comparator = float(0).__lt__
        return _compare((other-self)._cumulative(), comparator, self.use_dates or other.use_dates, self.tz)    
    
    @append_doc(SC_docs.gt_example)
    def gt(self, other):
        """
        Returns a boolean-valued step function indicating where *self* is strictly greater than *other*.
        
        Equivalent to *self* > *other*.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing where *self* > *other*
            
        See Also
        --------
        Stairs.lt, Stairs.le, Stairs.ge
        """
        if not isinstance(other, Stairs):
            other = Stairs(other, self.use_dates, self.tz)
        comparator = float(0).__gt__
        return _compare((other-self)._cumulative(), comparator, self.use_dates or other.use_dates, self.tz)        
    
    @append_doc(SC_docs.le_example)
    def le(self, other):
        """
        Returns a boolean-valued step function indicating where *self* is less than, or equal to, *other*.
        
        Equivalent to *self* <= *other*.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing where *self* <= *other*
            
        See Also
        --------
        Stairs.lt, Stairs.gt, Stairs.ge
        """
        if not isinstance(other, Stairs):
            other = Stairs(other, self.use_dates, self.tz)
        comparator = float(0).__le__
        return _compare((other-self)._cumulative(), comparator, self.use_dates or other.use_dates, self.tz)        

    @append_doc(SC_docs.ge_example)
    def ge(self, other):
        """
        Returns a boolean-valued step function indicating where *self* is greater than, or equal to, *other*.
        
        Equivalent to *self* >= *other*.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing where *self* >= *other*
            
        See Also
        --------
        Stairs.lt, Stairs.gt, Stairs.le
        """
        if not isinstance(other, Stairs):
            other = Stairs(other, self.use_dates, self.tz)
        comparator = float(0).__ge__
        return _compare((other-self)._cumulative(), comparator, self.use_dates or other.use_dates, self.tz)                
    
    @append_doc(SC_docs.eq_example)
    def eq(self, other):
        """
        Returns a boolean-valued step function indicating where *self* is equal to *other*.
        
        Equivalent to *self* == *other*.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing where *self* == *other*
            
        See Also
        --------
        Stairs.ne, Stairs.identical
        """
        if not isinstance(other, Stairs):
            other = Stairs(other, self.use_dates, self.tz)
        comparator = float(0).__eq__
        return _compare((other-self)._cumulative(), comparator, self.use_dates or other.use_dates, self.tz)           
    
    @append_doc(SC_docs.ne_example)
    def ne(self, other):
        """
        Returns a boolean-valued step function indicating where *self* is not equal to *other*.
        
        Equivalent to *self* != *other*.  See examples below.
              
        Returns
        -------
        :class:`Stairs`
            A new instance representing where *self* != *other*
            
        See Also
        --------
        Stairs.eq, Stairs.identical
        """
        if not isinstance(other, Stairs):
            other = Stairs(other, self.use_dates, self.tz)
        comparator = float(0).__ne__
        return _compare((other-self)._cumulative(), comparator, self.use_dates or other.use_dates, self.tz)    
    
    @append_doc(SC_docs.identical_example)
    def identical(self, other):
        """
        Returns True if *self* and *other* represent the same step functions.
        
        Returns
        -------
        boolean
        
        See Also
        --------
        Stairs.eq, Stairs.ne
        """
        return bool(self == other)
    
    def _reduce(self):
        to_remove = [key for key,val in self._items()[1:] if val == 0]
        for key in to_remove:
            self._pop(key)
        return self
        
    def __bool__(self):
        """
        Return True if and only if step function has a value of 1 everywhere.
        
        Returns
        -------
        boolean
        """
        if self.number_of_steps() >= 2:
            return float((~self).integrate()) < 0.0000001
        return dict(self._sorted_dict) == {float('-inf'): 1}

    
    # def __bool__(self):
        # self._reduce()
        # if self._len() != 1:
            # return False
        # value = self._values()[0]
        # return value == 1
    
    @append_doc(SC_docs.integral_and_mean_example)
    def _get_integral_and_mean(self, lower=float('-inf'), upper=float('inf')):
        """
        Calculates the integral, and the mean of the step function.
        
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp
            upper bound of the interval on which to perform the calculation
              
        Returns
        -------
        tuple
            The area and mean are returned as a pair
            
        See Also
        --------
        Stairs.integrate, Stairs.mean
        """
        new_instance = self.clip(lower, upper)
        if new_instance.number_of_steps() < 2:
            return 0, np.nan
        if lower != float('-inf'):
            new_instance[lower] = new_instance._get(lower,0)
        if upper != float('inf'):
            new_instance[upper] = new_instance._get(upper,0)
        cumulative = new_instance._cumulative()
        widths = np.subtract(cumulative.keys()[2:], cumulative.keys()[1:-1])
        heights = cumulative.values()[1:-1]
        area = np.multiply(widths, heights).sum()
        mean = area/(cumulative.keys()[-1] - cumulative.keys()[1])
        return area, mean

    @add_doc(_get_integral_and_mean.__doc__)
    def get_integral_and_mean(self, lower=float('-inf'), upper=float('inf')):
        if isinstance(lower, pd.Timestamp):
            lower = _convert_date_to_float(lower, self.tz)
        if isinstance(upper, pd.Timestamp):
            upper = _convert_date_to_float(upper, self.tz)
        return self._get_integral_and_mean(lower, upper)
                
    @append_doc(SC_docs.integrate_example)
    def integrate(self, lower=float('-inf'), upper=float('inf')):
        """
        Calculates the integral of the step function.
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp
            upper bound of the interval on which to perform the calculation
              
        Returns
        -------
        float
            The area
            
        See Also
        --------
        Stairs.get_integral_and_mean
        """
        area, _ = self.get_integral_and_mean(lower, upper)
        return area
    
    @append_doc(SC_docs.mean_example)
    def mean(self, lower=float('-inf'), upper=float('inf')):
        """
        Calculates the mean of the step function.
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp
            upper bound of the interval on which to perform the calculation
              
        Returns
        -------
        float
            The mean
        
        See Also
        --------
        Stairs.rolling_mean, Stairs.get_integral_and_mean, Stairs.median, Stairs.mode
        """
        _, mean = self.get_integral_and_mean(lower, upper)
        return mean
    
    @append_doc(SC_docs.median_example)
    def median(self, lower=float('-inf'), upper=float('inf')):
        """
        Calculates the median of the step function.
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp
            upper bound of the interval on which to perform the calculation
              
        Returns
        -------
        float
            The median
            
        See Also
        --------
        Stairs.mean, Stairs.mode, Stairs.percentile, Stairs.percentile_Stairs
        """
        return self.percentile(50, lower, upper)
    
    @append_doc(SC_docs.var_example)
    def var(self, lower=float('-inf'), upper=float('inf')):
        """
        Calculates the variance of the step function.
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp
            upper bound of the interval on which to perform the calculation
              
        Returns
        -------
        float
            The variance of the step function
            
        See Also
        --------
        Stairs.std
        """
        percentile_minus_mean = (self.percentile_stairs(lower, upper) - self.mean(lower, upper))._cumulative()
        return (
            _from_cumulative(
                dict(zip(percentile_minus_mean.keys(), (val*val for val in percentile_minus_mean.values())))
            ).integrate(0,100)/100
        )
        
    @append_doc(SC_docs.std_example)
    def std(self, lower=float('-inf'), upper=float('inf')):
        """
        Calculates the standard deviation of the step function.
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp
            upper bound of the interval on which to perform the calculation
              
        Returns
        -------
        float
            The standard deviation of the step function
            
        See Also
        --------
        Stairs.var
        """
        return np.sqrt(self.var(lower, upper))
        
    @append_doc(SC_docs.describe_example)
    def describe(self, lower=float('-inf'), upper=float('inf'), percentiles=(25, 50, 75)):
        """
        Generate descriptive statistics.
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp
            upper bound of the interval on which to perform the calculation
        percentiles: array-like of float, default [25, 50, 70]
            The percentiles to include in output.  Numbers should be in the range 0 to 100.
              
        Returns
        -------
        :class:`pandas.Series`
            
        See Also
        --------
        Stairs.mean, Stairs.std, Stairs.min, Stairs.percentile, Stairs.max
        """
        percentilestairs = self.percentile_stairs(lower, upper)
        return pd.Series(
            {
                **{
                    "unique": percentilestairs.clip(0,100).number_of_steps()-1,
                    "mean": self.mean(lower, upper),
                    "std": self.std(lower, upper),
                    "min": self.min(lower, upper),
                },
                **{f'{perc}%': percentilestairs(perc) for perc in percentiles},
                **{
                    "max":self.max(lower, upper),
                }
            }
        )
        
    @append_doc(SC_docs.cov_example)
    def cov(self, other, lower=float('-inf'), upper=float('inf'), lag=0, clip='pre'):
        """
        Calculates either covariance, autocovariance or cross-covariance.

        The calculation is between two step functions described by *self* and *other*.
        If lag is None or 0 then covariance is calculated, otherwise cross-covariance is calculated.
        Autocovariance is a special case of cross-covariance when *other* is equal to *self*.
        
        Parameters
        ----------
        other: :class:`Stairs`
            the stairs instance with which to compute the covariance
        lower : int, float or pandas.Timestamp
            lower bound of the domain on which to perform the calculation
        upper : int, float or pandas.Timestamp
            upper bound of the domain on which to perform the calculation
        lag : int, float, pandas.Timedelta
            a pandas.Timedelta is only valid when using dates.
            If using dates and delta is an int or float, then it is interpreted as a number of hours.
        clip : {'pre', 'post'}, default 'pre'
            only relevant when lag is non-zero.  Determines if the domain is applied before or after *other* is translated.
            If 'pre' then the domain over which the calculation is performed is the overlap
            of the original domain and the translated domain.
            
        Returns
        -------
        float
            The covariance (or cross-covariance) between *self* and *other*
            
        See Also
        --------
        Stairs.corr, staircase.cov, staircase.corr
        """
        if lag != 0:
            assert clip in ['pre', 'post']
            if clip == 'pre' and upper != float('inf'):
                upper = upper - lag
            other = other.shift(-lag)
        return (self*other).mean(lower, upper) - self.mean(lower, upper)*other.mean(lower, upper)
    
    @append_doc(SC_docs.corr_example)
    def corr(self, other, lower=float('-inf'), upper=float('inf'), lag=0, clip='pre'):
        """
        Calculates either correlation, autocorrelation or cross-correlation.
        
        All calculations are based off the `Pearson correlation coefficient <https://en.wikipedia.org/wiki/Pearson_correlation_coefficient>`_.
        
        The calculation is between two step functions described by *self* and *other*.
        If lag is None or 0 then correlation is calculated, otherwise cross-correlation is calculated.
        Autocorrelation is a special case of cross-correlation when *other* is equal to *self*.
        
        Parameters
        ----------
        other: :class:`Stairs`
            the stairs instance with which to compute the correlation
        lower : int, float or pandas.Timestamp
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp
            upper bound of the interval on which to perform the calculation
        lag : int, float, pandas.Timedelta
            a pandas.Timedelta is only valid when using dates.
            If using dates and delta is an int or float, then it is interpreted as a number of hours.
        clip : {'pre', 'post'}, default 'pre'
            only relevant when lag is non-zero.  Determines if the domain is applied before or after *other* is translated.
            If 'pre' then the domain over which the calculation is performed is the overlap
            of the original domain and the translated domain.
            
        Returns
        -------
        float
            The correlation (or cross-correlation) between *self* and *other*
            
        See Also
        --------
        Stairs.cov, staircase.corr, staircase.cov
        """
        if lag != 0:
            assert clip in ['pre', 'post']
            if clip == 'pre' and upper != float('inf'):
                upper = upper - lag
            other = other.shift(-lag)
        return self.cov(other, lower, upper)/(self.std(lower, upper)*other.std(lower,upper))
    
    @append_doc(SC_docs.percentile_example)
    def percentile(self, x, lower=float('-inf'), upper=float('inf')):
        """
        Calculates the x-th percentile of the step function's values
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp
            upper bound of the interval on which to perform the calculation
              
        Returns
        -------
        float
            The x-th percentile
            
        See Also
        --------
        Stairs.median, Stairs.percentile_stairs
        """
        assert 0 <= x <= 100
        percentiles = self.percentile_stairs(lower, upper)
        return (percentiles(x, how='left') + percentiles(x, how='right'))/2

    @append_doc(SC_docs.percentile_stairs_example)
    def percentile_stairs(self, lower=float('-inf'), upper=float('inf')):
        """
        Calculates a percentile function (and returns a corresponding Stairs instance)
        
        This method can be used for efficiency gains if substituting for multiple calls
        to percentile() with the same lower and upper parameters
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp, optional
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp, optional
            upper bound of the interval on which to perform the calculation
              
        Returns
        -------
        :class:`Stairs`
            An instance representing a percentile function
            
        See Also
        --------
        Stairs.percentile
        """
        temp_df = (
            self.clip(lower,upper)
            .to_dataframe()
        )
        
        assert temp_df.shape[0] >= 3, "Step function composed only of infinite length intervals.  Provide bounds by 'lower' and 'upper' parameters"

        temp_df = (
            temp_df
            .iloc[1:-1]
            .assign(duration = lambda df: df.end-df.start)
            .groupby('value').sum()
            .assign(duration = lambda df: np.cumsum(df.duration/df.duration.sum()))
            .assign(duration = lambda df: df.duration.shift())
            .fillna(0)
        )
        percentile_step_func = Stairs()
        for start,end,value in zip(temp_df.duration.values, np.append(temp_df.duration.values[1:],1), temp_df.index):
            percentile_step_func.layer(start*100,end*100,value)
        #percentile_step_func._popitem()
        percentile_step_func[100]=0
        return percentile_step_func
        
    def percentile_Stairs(self, lower=float('-inf'), upper=float('inf')):
        """Deprecated.  Use Stairs.percentile_stairs."""
        warnings.warn(
            "Stairs.percentile_Stairs will be deprecated in version 2.0.0, use Stairs.percentile_stairs instead",
             PendingDeprecationWarning
        )
        return self.percentile_stairs(lower, upper)
        
    @append_doc(SC_docs.ecdf_stairs_example)
    def ecdf_stairs(self, lower=float('-inf'), upper=float('inf')):
        """
        Calculates an `empirical cumulative distribution function <https://en.wikipedia.org/wiki/Empirical_distribution_function>`_
        for the corresponding step function values (and returns the result as a Stairs instance)
       
        Parameters
        ----------
        lower : int, float or pandas.Timestamp, optional
            lower bound of the step-function domain on which to perform the calculation
        upper : int, float or pandas.Timestamp, optional
            upper bound of the step-function domain to perform the calculation
              
        Returns
        -------
        :class:`Stairs`
            An instance representing an empirical cumulative distribution function for the step function values
            
        See Also
        --------
        staircase.hist_from_ecdf
        Stairs.hist
        """
        def _switch_first_key_to_zero(d):
            d[0] = d.get(0,0) + d.pop(float('-inf'))
            return d

        _ecdf = _switch_first_key_to_zero(
            self.percentile_stairs(lower, upper)
            ._sorted_dict.copy()
        )
        
        return Stairs().layer(np.cumsum(list(_ecdf.values())[:-1]), None, np.diff(list(_ecdf.keys()))/100)
    
    @append_doc(SC_docs.hist_example)
    def hist(self, lower=float('-inf'), upper=float('inf'), bin_edges=None, closed='left'):
        """
        Calculates a histogram for the corresponding step function values
       
        Parameters
        ----------
        lower : int, float or pandas.Timestamp, optional
            lower bound of the step-function domain on which to perform the calculation
        upper : int, float or pandas.Timestamp, optional
            upper bound of the step-function domain to perform the calculation
        bin_edges : array-like of int or float, optional
            defines the bin edges for the histogram (remember it is the step-function range that is being binned).
            If not specified the bin_edges will be assumed to be the integers which cover the step function range
        closed: {'left', 'right'}, default 'left'
            determines whether the bins, which are half-open intervals, are left-closed , or right-closed
              
        Returns
        -------
        :class:`pandas.Series`
            A Series, with a :class:`pandas.IntervalIndex`, representing the values of the histogram
            
        See Also
        --------
        staircase.hist_from_ecdf
        Stairs.ecdf_stairs
        """
        _ecdf = self.ecdf_stairs(lower, upper)
        return hist_from_ecdf(_ecdf, bin_edges, closed)
        

    
    @append_doc(SC_docs.mode_example)
    def mode(self, lower=float('-inf'), upper=float('inf')):
        """
        Calculates the mode of the step function.
        
        If there is more than one mode only the smallest is returned
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp, optional
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp, optional
            upper bound of the interval on which to perform the calculation
              
        Returns
        -------
        float
            The mode
            
        See Also
        --------
        Stairs.mean, Stairs.median
        """
        df = (self.clip(lower,upper)
                .to_dataframe().iloc[1:-1]
                .assign(duration = lambda df: df.end-df.start)
        )
        return df.value.loc[df.duration.idxmax()]

    @append_doc(SC_docs.values_in_range_example)
    def values_in_range(self, lower=float('-inf'), upper=float('inf'), lower_how='right', upper_how='left'):
        """
        Returns the range of the step function as a set of discrete values.
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp, optional
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp, optional
            upper bound of the interval on which to perform the calculation
        lower_how: {'left', 'right'}, default 'right'
            Determines how the step function should be evaluated at *lower*.
            If 'left' then :math:`\\lim_{x \\to lower^{-}} f(x)` is included in the calculation.
        upper_how: {'left', 'right'}, default 'left'
            Determines how the step function should be evaluated at *upper*.
            If 'right' then :math:`\\lim_{x \\to upper^{+}} f(x)` is included in the calculation.
              
        Returns
        -------
        set of floats
        """
        if isinstance(lower, pd.Timestamp):
            lower = _convert_date_to_float(lower, self.tz)
        if isinstance(upper, pd.Timestamp):
            upper = _convert_date_to_float(upper, self.tz)
        return self._values_in_range(lower, upper, lower_how, upper_how)
        
    def _values_in_range(self, lower=float('-inf'), upper=float('inf'), lower_how='right', upper_how='left'):
        interior_points = [key for key in self._keys() if lower < key < upper]
        endpoint_vals = self._sample_raw([lower], how='right') + self._sample_raw([upper], how='left')
        if lower_how == 'left':
            endpoint_vals += self._sample_raw([lower], how='left')
        if upper_how == 'right':
            endpoint_vals += self._sample_raw([upper], how='right')
        return set(self._sample_raw(interior_points) + endpoint_vals)
    
    @append_doc(SC_docs.min_example)
    def min(self, lower=float('-inf'), upper=float('inf'), lower_how='right', upper_how='left'):
        """
        Calculates the minimum value of the step function
        
        If an interval which to calculate over is specified it is interpreted
        as a closed interval, with *lower_how* and *upper_how* indicating how the step function
        should be evaluated at the at the endpoints of the interval.
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp, optional
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp, optional
            upper bound of the interval on which to perform the calculation
        lower_how: {'left', 'right'}, default 'right'
            Determines how the step function should be evaluated at *lower*.
            If 'left' then :math:`\\lim_{x \\to lower^{-}} f(x)` is included in the calculation.
        upper_how: {'left', 'right'}, default 'left'
            Determines how the step function should be evaluated at *upper*.
            If 'right' then :math:`\\lim_{x \\to upper^{+}} f(x)` is included in the calculation.
              
        Returns
        -------
        float
            The minimum value of the step function
            
        See Also
        --------
        Stairs.max, staircase.min
        """
        return min(self.values_in_range(lower, upper, lower_how, upper_how))

    @append_doc(SC_docs.max_example)
    def max(self, lower=float('-inf'), upper=float('inf'), lower_how='right', upper_how='left'):
        """
        Calculates the maximum value of the step function
        
        If an interval which to calculate over is specified it is interpreted
        as a closed interval, with *lower_how* and *upper_how* indicating how the step function
        should be evaluated at the at the endpoints of the interval.
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp, optional
            lower bound of the interval on which to perform the calculation
        upper : int, float or pandas.Timestamp, optional
            upper bound of the interval on which to perform the calculation
        lower_how: {'left', 'right'}, default 'right'
            Determines how the step function should be evaluated at *lower*.
            If 'left' then :math:`\\lim_{x \\to lower^{-}} f(x)` is included in the calculation.
        upper_how: {'left', 'right'}, default 'left'
            Determines how the step function should be evaluated at *upper*.
            If 'right' then :math:`\\lim_{x \\to upper^{+}} f(x)` is included in the calculation.
              
        Returns
        -------
        float
            The maximum value of the step function
            
        See Also
        --------
        Stairs.min, staircase.max
        """
        return max(self.values_in_range(lower, upper, lower_how, upper_how))
     
    @append_doc(SC_docs.clip_example)
    def _clip(self, lower=float('-inf'), upper=float('inf')):
        """
        Returns a copy of *self* which is zero-valued everywhere outside of [lower, upper)
        
        Parameters
        ----------
        lower : int, float or pandas.Timestamp
            lower bound of the interval
        upper : int, float or pandas.Timestamp
            upper bound of the interval
              
        Returns
        -------
        :class:`Stairs`
            Returns a copy of *self* which is zero-valued everywhere outside of [lower, upper)
        """
        assert lower is not None and upper is not None, "clip function should not be called with no parameters."
        assert lower < upper, "Value of parameter 'lower' must be less than the value of parameter 'upper'"
        cumulative = self._cumulative()
        left_boundary_index = cumulative.bisect_right(lower) - 1
        right_boundary_index = cumulative.bisect_right(upper) - 1
        value_at_left = cumulative.values()[left_boundary_index]
        value_at_right = cumulative.values()[right_boundary_index]
        s = dict(self._items()[left_boundary_index+1:right_boundary_index+1])
        s[float('-inf')] = 0
        if lower != float('-inf'):
            s[float('-inf')] = 0
            s[lower] = value_at_left
        else:
            s[float('-inf')] = self[float('-inf')]
        if upper != float('inf'):
            s[upper] = s.get(upper,0)-value_at_right
        return Stairs(s, self.use_dates, self.tz)

    @add_doc(_clip.__doc__)
    def clip(self, lower=float('-inf'), upper=float('inf')):
        if isinstance(lower, pd.Timestamp):
            lower = _convert_date_to_float(lower, self.tz)
        if isinstance(upper, pd.Timestamp):
            upper = _convert_date_to_float(upper, self.tz)
        return self._clip(lower, upper)
    
    @append_doc(SC_docs.shift_example)
    def shift(self, delta):
        """
        Returns a stairs instance corresponding to a horizontal translation by delta
        
        If delta is positive the corresponding step function is moved right.
        If delta is negative the corresponding step function is moved left.
        
        Parameters
        ----------
        delta : int, float or pandas.Timedelta
            the amount by which to translate.  A pandas.Timedelta is only valid when using dates.
            If using dates and delta is an int or float, then it is interpreted as a number of hours.
              
        Returns
        -------
        :class:`Stairs`
        
        See Also
        --------
        Stairs.diff
        """
        if isinstance(delta, pd.Timedelta):
            assert self.use_dates, "delta is of type pandas.Timedelta, expected float"
            delta =  delta.total_seconds()/3600
        return Stairs(
            dict(zip(
                (key + delta for key in self._keys()),
                self._values()
            )),
            self.use_dates,
            self.tz,
        )
        
    @append_doc(SC_docs.diff_example)
    def diff(self, delta):
        """
        Returns a stairs instance corresponding to the difference between the step function corresponding to *self*
        and the same step-function translated by delta.
        
        Parameters
        ----------
        delta : int, float or pandas.Timedelta
            the amount by which to translate.  A pandas.Timestamp is only valid when using dates.
            If using dates and delta is an int or float, then it is interpreted as a number of hours.
              
        Returns
        -------
        :class:`Stairs`
        
        See Also
        --------
        Stairs.shift
        """
        return self-self.shift(delta)
        
    @append_doc(SC_docs.rolling_mean_example)
    def rolling_mean(self, window=(0,0), lower=float('-inf'), upper=float('inf')):
        """
        Returns coordinates defining rolling mean
        
        The rolling mean of a step function is a continous piece-wise linear function, hence it can
        be described by a sequence of x,y coordinates which mark where function changes gradient.  These
        x,y coordinates are returned as a :class:`pandas.Series` which could then be used with
        :meth:`matplotlib.axes.Axes.plot`, or equivalent, to visualise.
        
        A rolling mean requires a window around a point x (referred to as the focal point) to be defined.
        In this implementation the window is defined by two values paired into an array-like parameter called *window*.
        These two numbers are the distance from the focal point to the left boundary of the window, and the right boundary
        of the window respectively.  This allows for trailing windows, leading windows and everything between
        (including a centred window).
        
        If *lower* or *upper* is specified then only coordinates corresponding to windows contained within
        [lower, upper] are included.
        
        Parameters
        ----------
        window : array-like of int, float or pandas.Timedelta
            should be length of 2. Defines distances from focal point to window boundaries.
        lower : int, float, pandas.Timestamp, or None, default None
            used to indicate the lower bound of the domain of the calculation
        upper : int, float, pandas.Timestamp, or None, default None
            used to indicate the upper bound of the domain of the calculation
              
        Returns
        -------
        :class:`pandas.Series`
        
        See Also
        --------
        Stairs.mean
        """
        assert len(window) == 2, "Window should be a listlike object of length 2."
        left_delta, right_delta = window
        clipped = self.clip(lower, upper)
        if clipped.use_dates:
            left_delta = pd.Timedelta(left_delta, 'h')
            right_delta = pd.Timedelta(right_delta, 'h')
        change_points = list(SortedSet(
            [c - right_delta for c in clipped.step_changes().keys()] +
            [c - left_delta for c in clipped.step_changes().keys()]
        ))
        s = pd.Series(
            clipped.sample(change_points, aggfunc='mean', window=window),
            index = change_points,
        )
        if lower != float('-inf'):
            s = s.loc[s.index >= lower - left_delta]
        if upper != float('inf'):
            s = s.loc[s.index <= upper - right_delta]
        return s
    
    
    def to_dataframe(self):
        """
        Returns a pandas.DataFrame with columns 'start', 'end' and 'value'
        
        The rows of the dataframe can be interpreted as the interval definitions
        which make up the step function.
        
        Returns
        -------
        :class:`pandas.DataFrame`
        """
        starts = self._keys()
        ends = self._keys()[1:]
        if self.use_dates:
            starts = [pd.NaT] + _convert_float_to_date(np.array(starts[1:]), self.tz)
            ends = _convert_float_to_date(np.array(ends), self.tz) + [pd.NaT]
        else:
            ends.append(float('inf'))
        values = self._cumulative().values()
        df = pd.DataFrame({"start":list(starts), "end":list(ends), "value":list(values)}) #bugfix for pandas 1.1
        return df

    @append_doc(SC_docs.number_of_steps_example)
    def number_of_steps(self):
        """
        Calculates the number of step changes

        Returns
        -------
        int

        See Also
        --------
        Stairs.step_changes
        """
        return len(self._keys())-1
        
    def __str__(self):
        """
        Return str(self)
        """
        tzinfo = f", tz={self.tz}" if self.use_dates else ""
        return f"<staircase.Stairs, id={id(self)}, dates={self.use_dates}{tzinfo}>"

    def __repr__(self):
        """
        Return string representation of Stairs
        """
        return str(self)
    
        
    def __call__(self, *args, **kwargs):
        return self.sample(*args, **kwargs)
    
    __neg__ = negate
    __mul__ = multiply
    __truediv__ = divide
    __add__ = add
    __sub__ = subtract
    __or__ = logical_or
    __and__ = logical_and
    __invert__ = invert
    __eq__ = eq
    __ne__ = ne
    __lt__ = lt
    __gt__ = gt
    __le__ = le
    __ge__ = ge
    
_stairs_methods = {
    'mean':Stairs.mean,
    'median':Stairs.median,
    'mode':Stairs.mode,
    'max':Stairs.max,
    'min':Stairs.min,
}
