# -*- coding: utf-8 -*-
"""
@file
@brief
"""
import timeit
import pandas


def unit(x):
    """
    Optimizes the rendering of time.

    .. runpython::
        :showcode:

        from jupytalk.benchmark.mlprediction import unit

        print(unit(34))
        print(unit(3.4))
        print(unit(0.34))
        print(unit(0.034))
        print(unit(0.0034))
        print(unit(0.00034))
        print(unit(0.000034))
        print(unit(0.0000034))
        print(unit(0.00000034))
    """
    if x >= 1:
        return "%1.2f s" % x
    elif x >= 1e-3:
        return "%1.2f ms" % (x * 1000)
    elif x >= 1e-6:
        return "%1.2f µs" % (x * 1000**2)
    elif x >= 1e-9:
        return "%1.2f ns" % (x * 1000**3)
    else:
        return "%1.2g s" % x


def timeexec(legend, code, number=50, repeat=200, verbose=True, context=None):
    """
    Measures the time for a given expression.

    @param      legend      name of the experiment
    @param      code        code to measure (as a string)
    @param      number      number of time to run the expression
                            (and then divide by this number to get an average)
    @param      repeat      number of times to repeat the computation
                            of the above average
    @param      verbose     print the time
    @param      globals     context (usuable equal to ``globals()``)
    @return                 dictionary

    .. runpython::
        :showcode:

        from jupytalk.benchmark.mlprediction import timeexec

        code = "3 * 45535266234653452"
        print(timeexec("multiplication", code))
    """
    if context is None:
        context = globals()
    rep = timeit.repeat(code, number=number, repeat=repeat, globals=context)
    ave = sum(rep) / (number * repeat)
    std = (sum((x / number - ave)**2 for x in rep) / repeat)**0.5
    fir = rep[0] / number
    fir3 = sum(rep[:3]) / (3 * number)
    las3 = sum(rep[-3:]) / (3 * number)
    rep.sort()
    mini = rep[len(rep) // 20] / number
    maxi = rep[-len(rep) // 20] / number
    if verbose:
        print("Average: %s deviation %s (with %d runs) in [%s, %s]" % (
            unit(ave), unit(std), number, unit(mini), unit(maxi)))
    return dict(legend=legend, average=ave, deviation=std, first=fir, first3=fir3,
                last3=las3, repeat=repeat, min5=mini, max5=maxi, code=code, run=number)


def make_dataframe(labels, arrays):
    """
    Builds a dataframe from multiple arrays.

    @param  labels      list of labels
    @param  arrays      list of arrays (or one array)
    @return             dataframes
    """
    if labels is not None:
        df = [pandas.DataFrame(data={'Label': labels})]
    else:
        df = []
    if isinstance(arrays, list):
        for i, ar in enumerate(arrays):
            d = pandas.DataFrame(
                data=ar, columns=["F%d_%d" % (i, j) for j in range(ar.shape[1])])
            df.append(d)
    else:
        ar = arrays
        d = pandas.DataFrame(
            data=ar, columns=["F%d" % j for j in range(ar.shape[1])])
        df.append(d)
    return pandas.concat(df, axis=1)
