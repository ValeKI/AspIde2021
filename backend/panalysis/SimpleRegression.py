import numpy as np
from numpy import ndarray
from sklearn.metrics import r2_score
from scipy.optimize import curve_fit, OptimizeWarning
import matplotlib.pyplot as plt
import backend.panalysis.FunctionsRegression as fr


# to calculate r^2
def rSquare(y_true: ndarray, y_pred: ndarray) -> float:
    return r2_score(y_true, y_pred)


# def residualSumOfSquares(y_true: ndarray, y_pred: ndarray) -> ndarray:
#     return np.mean((y_true - y_pred) ** 2)
#
# def meanAbsoluteError(y_true: ndarray, y_pred: ndarray):
#     return np.mean(np.absolute(y_true - y_pred))


# return a dictionary where:
#   the value of 'function' is the function of fr.regressionFunctions with the best r^2
#   the value of 'popt'     is an array with the optimize coefficients
#   the value of 'pcov'     is an array with the predictions of variance
def bestPrevision(x_true: ndarray, y_true: ndarray):
    max_x_true = max(x_true)
    max_y_true = max(y_true)

    x_norm = x_true/max_x_true
    y_norm = y_true/max_y_true

    bestRSquare = -5

    # 'function', 'popt', 'pcov'
    bestFunction = {}

    for function in fr.regressionFunctions:
        try:
            popt, pcov = curve_fit(function, x_norm, y_norm)
            y_pred = function(x_true, *popt)
            r2 = rSquare(y_true, y_pred)
            # print(f'R square: ${r2}')
            if r2 > bestRSquare:
                bestRSquare = r2
                bestFunction = \
                    {
                        'function'  : function,
                        'popt'      : popt,
                        'pcov'      : pcov
                    }
        # there are a group of errors due to calculate in curve_fit
        # in practice, the estimated coefficients are too large or negative or not suitable
        # for the function under consideration
        except RuntimeError:
            pass
        except ValueError:
            pass
        except KeyError:
            pass
        except RuntimeWarning:
            pass
        except OptimizeWarning:
            pass
        except TypeError:
            pass

    return bestFunction


def reduceData(xvalues, yvalues):
    xreduce = list(set(xvalues))
    yreduce = [None] * len(xreduce)
    for r in range(0, len(xreduce)):
        if yreduce[r] is None:
            for v in range(0, len(xvalues)):
                m = 0
                n = 0
                if xvalues[v] == xreduce[r]:
                    m += yvalues[v]
                    n = n + 1
                if n != 0:
                    yreduce[r] = m/n
    return xreduce, yreduce


def saveRegression(path, xvalues: list, yvalues: list, plotX='x', plotY='y') -> bool:
    if len(xvalues) != len(yvalues):
        return False

    plt.cla()

    # reducerData = reduceData(xvalues, yvalues)

    # xvalues = reducerData[0]
    # yvalues = reducerData[1]

    x = np.array(xvalues)
    y = np.array(yvalues)

    # set the x and y name of axis
    plt.xlabel(plotX)
    plt.ylabel(plotY)

    # bestFunction = {}
    # # find the best function
    # if len(xvalues) > 1:
    #     bestFunction = bestPrevision(x, y)

    # get the max value of x and y
    # max_x_true = max(x)
    # max_y_true = max(y)

    # if 'function' in bestFunction:
    #     # create normal value of a new x from 0 to 2. It uses to estimate double of data.
    #     # For example: if you insert 50 data (x,y), here the program generates 100 prediction data (x,y)
    #     newx = np.linspace(0, 2, 85)
    #     # multiplying the data with his maximum, they take on value in proportion to the entered data
    #     y_pred = bestFunction['function'](newx, bestFunction['popt'][0], bestFunction['popt'][1]) * max_y_true
    #     newx = newx * max_x_true
    #
    #     # plot the estimated data
    #     plt.plot(newx, y_pred, 'r', color='blue')

    # plot the real data
    plt.plot(x, y, 'ro', color='red')

    print(xvalues)
    print(yvalues)

    # plt.show()
    # save plot image in the path
    plt.savefig(path, bbox_inches='tight')
    return True
