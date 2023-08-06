# -*- coding: utf-8 -*-
"""
PyLinReg
==============================================================================
Linear Regression Model with only Python Standard Library based on
Ordinary Least Squares (OLS) Method
------------------------------------------------------------------------------
MIT License
Copyright (c) 2021 Richárd Ádám Vécsey Dr.
See accompanying file LICENSE.
"""

# constants
__author__ = 'Richárd Ádám Vécsey Dr.'
__copyright__ = "Copyright 2021, PyLinReg"
__credits__ = ['Richárd Ádám Vécsey Dr.']
__license__ = 'MIT'
__version__ = '1.0.0'
__status__ = 'Alpha'



# import section
# standard library
from datetime import datetime
from math import sqrt
from statistics import mean 



class LinearModel(object):
    """
    LinearModel object contains model data and calculates regression variables
    """
    
    def __init__(self, predictors=None, targets=None, replace_none=True):
        """
        Initialize the LinearModel object        
        =================================
        
        Attributes
        ----------
        predictors : list, tuple
            Values of predictor (independent) variables for linear regression 
            model calculation.
        targets : list, tuple
            Values of target (dependent) variables for linear regression model
            calculation.
        replace_none : boolean
            Whether to replace none value with the mean of data or not. If not,
            the exact pair, that contains None value, will be removed.
            Default: True
        
        Methods
        -------
        frompairs(pairs)
            Create linear regression model based on pairs of values instead of
            the two different lists for predictors and targets.
        
        Raises
        ------
        ValueError
            If the length of predictors and targets are not equal.
        """

        # Check the lengths of inputs of the model
        if len(predictors) != len(targets):
            raise ValueError('Length of predictors must be equal with the length of targets')
        
        self.__predictors = predictors
        self.__targets = targets
        self.__pairs = []       
        
        # Check None to replace or remove invalid values
        # This helps to avoid calculation errors
        if None in self.__predictors:
            if replace_none:
                _temp_predictors = []
                _replaceable_ids = []
                for idx, predictor in enumerate(self.__predictors):
                    if predictor is None:
                        _replaceable_ids.append(idx)
                    else:
                        _temp_predictors.append(predictor)
                _temp_mean = mean(_temp_predictors)
                for replace_id in _replaceable_ids:
                    self.__predictors[replace_id] = _temp_mean
                del _temp_predictors
                del _replaceable_ids
                del _temp_mean
            else:
                _removable_ids = []
                for idx, predictor in enumerate(self.__predictors):
                    if predictor is None:
                        _removable_ids.append(idx)
                for removable_id in _removable_ids:
                    self.__predictors.pop(removable_id)
                    self.__targets.pop(removable_id)
                del _removable_ids
                
        if None in self.__targets:
            if replace_none:
                _temp_targets = []
                _replaceable_ids = []
                for idx, target in enumerate(self.__targets):
                    if target is None:
                        _replaceable_ids.append(idx)
                    else:
                        _temp_targets.append(target)
                _temp_mean = mean(_temp_targets)
                for replace_id in _replaceable_ids:
                    self.__targets[replace_id] = _temp_mean
                del _temp_targets
                del _replaceable_ids
                del _temp_mean
            else:
                _removable_ids = []
                for idx, target in enumerate(self.__targets):
                    if target is None:
                        _removable_ids.append(idx)
                for removable_id in _removable_ids:
                    self.__targets.pop(removable_id)
                    self.__predictors.pop(removable_id)
                del _removable_ids
        
        self.__x_mean = mean(self.__predictors)
        self.__y_mean = mean(self.__targets)
        
        sum_x_diff_sqr = 0
        sum_x_y_diff_mult = 0
        sum_y_diff_sqr = 0
        
        # Create pairs and other important variables for regression calculation
        for pair in zip(self.__predictors, self.__targets):
            self.__pairs.append([pair[0], pair[1]])
            x_diff = pair[0] - self.__x_mean
            y_diff = pair[1] - self.__y_mean
            x_y_diff_mult = x_diff * y_diff
            sum_x_y_diff_mult += x_y_diff_mult
            x_diff_sqr = x_diff ** 2
            sum_x_diff_sqr += x_diff_sqr
            y_diff_sqr = y_diff ** 2
            sum_y_diff_sqr += y_diff_sqr
        
        # Regression calculation
        self.__slope = sum_x_y_diff_mult / sum_x_diff_sqr
        self.__intercept = self.__y_mean - (self.__slope * self.__x_mean)
        self.__r = sum_x_y_diff_mult / (sqrt(sum_x_diff_sqr) * sqrt(sum_y_diff_sqr))



    @property
    def details(self):
        """
        Print the model's most important variables such as:
        pedictors, targets, pairs, x_mean, y_mean, r-Person, slope, intercept
        """

        if self.__slope and self.intercept is not None:      
            if len(self.__predictors) > 10:
                print('{:>10}: {} (x)'.format('predictors', self.__predictors[:10]))
                print('{:>10}: {} (y)'.format('targets', self.__targets[:10]))
            else:
                print('{:>10}: (x) {}'.format('predictors', self.__predictors))
                print('{:>10}: (y) {}'.format('targets', self.__targets))
            print('{:>10}: {}'.format('pairs', self.__pairs[:5]))
            print('{:>10}: {:8.4f}'.format('x mean', self.__x_mean))
            print('{:>10}: {:8.4f}'.format('y mean', self.__y_mean))
            print('{:>10}: {:8.4f}'.format('r-Pearson', self.__r))
            print('{:>10}: {:8.4f}'.format('slope', self.__slope))
            print('{:>10}: {:8.4f}'.format('intercept', self.__intercept))
        else:
            print('{:>10}: (x) {}'.format('predictors', self.__predictors))
            print('{:>10}: (y) {}'.format('targets', self.__targets))
            print('{:>10}: {}'.format('pairs', self.__pairs[:5]))
            print('{:>10}: {}'.format('x mean', self.__x_mean))
            print('{:>10}: {}'.format('y mean', self.__y_mean))
            print('{:>10}: {}'.format('r-Pearson', self.__r))
            print('{:>10}: {}'.format('slope', self.__slope))
            print('{:>10}: {}'.format('intercept', self.__intercept))



    @property
    def intercept(self):
        """
        Return with the value of intercept.
        """
        
        return self.__intercept
    


    @property
    def pairs(self):
        """
        Return with the values of pairs.
        """       
        return self.__pairs



    @property
    def predictors(self):
        """
        Return with the values of predictors.
        """        
        
        return self.__predictors
    


    @property
    def r(self):
        """
        Return with the value of r.
        """
        
        return self.__r



    @property
    def slope(self):
        """
        Return with the value of slope.
        """        
        
        return self.__slope



    @property
    def targets(self):
        """
        Return with the values of targets.
        """           

        return self.__targets



    @property
    def x_mean(self):
        """
        Return with the mean value of x (predictors).
        """
        
        return self.__x_mean
    


    @property
    def y_mean(self):
        """
        Return with the mean value of y (targets).
        """
        
        return self.__y_mean

    
    
    @classmethod
    def frompairs(cls, pairs):
        """
        Create linear regression model based on pairs of values instead of
        the two different lists for predictors and targets.
        ==================================================================
        
        Parameters
        ----------
        pairs : list, tuple
            Array-like variable pairs, where each pair contains one predictor
            and one target value. Eg: [[1, 10], [2, 20], [3,30]]
            First value in the pair must be the predictor and the second value
            must be the target.
        
        Returns
        -------
        LinearModel object
        """
        
        predictors = []
        targets = []
        for pair in pairs:
            predictors.append(pair[0])
            targets.append(pair[1])   
        
        return cls(predictors, targets)



    def add_predictors(self, predictors, verbose=False):
        """
        Add new predictor values to the model
        =====================================

        Parameters
        ----------
        targets : list, tuple
            Values of predictor (independent) variables for linear regression 
            model calculation. It is same as the argument of LinearModel object
            with similar name.
        verbose : boolean
            Whether to print details about how many value is added and how many
            pair is created from the new predictors and old targets.
            Default: False

        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the length of new predictors and targets are not equal.          
        """
        
        self.__predictors = predictors
        if verbose:
            self.printout('{} value(s) added as predictors.'
                          .format(len(predictors)))
        if self.__targets != None:
            if len(self.__predictors) == len(self.__targets):           
                _pairs = zip(self.__predictors, self.__targets)
                for pair in _pairs:
                    self.__pairs.append([pair[0], pair[1]])
                if verbose:
                    self.printout('{} pair(s) created.'
                                  .format(len(self.__pairs)))
            else:
                raise ValueError('Length of predictors must be equal with the length of targets')



    def add_targets(self, targets, verbose=False):
        """
        Add new target values to the model
        ==================================
            
        Parameters
        ----------
        predictors : list, tuple
            Values of target (dependent) variables for linear regression model
            calculation. It is same as the argument of LinearModel object with
            similar name.
        verbose : boolean
            Whether to print details about how many value is added and how many
            pair is created from the new predictors and old targets.
            Default: False
        
        Returns
        -------
        None

        Raises
        ------
        ValueError
            If the length of new targets and predictors are not equal.
        """        
        self.__targets = targets
        if verbose:
            self.printout('{} value(s) added as targets.'
                          .format(len(targets)))
        if self.__predictors != None:
            if len(self.__predictors) == len(self.__targets):              
                _pairs = zip(self.__predictors, self.__targets)
                for pair in _pairs:
                    self.__pairs.append([pair[0], pair[1]])
                if verbose:
                    self.printout('{} pair(s) created.'
                                  .format(len(self.__pairs)))
            else:
                raise ValueError('Length of predictors must be equal with the length of targets')



    def make_prediction(self, predictor):
        """
        Make prediction based on the given predictor
        ============================================
            
        Parameters
        ----------
        predictor : int, float
            Predictor (independent) value for prediction    

        Returns
        -------
        prediction : float
            Value of prediction
        
        Raises
        ------
        ValueError
            If the slope or intercept values are None.

        Notes
        -----
        ValueError can occur when the LinearModel was resetted and there were
        no new calculation. For avoiding this error, it should be fill the
        LinearModel with new variables and make a new calculation.
        """          
        
        if self.__slope and self.intercept is not None:
            return (self.__slope * predictor) + self.__intercept
        else:
            raise ValueError('Slope and intercept values should not be None. Slope is {} and intercept is {}'
                             .format(self.__slope, self.__intercept))



    def printout(self, message):
        """
        Help to print verbose message with the actual and formatted timestamp
        """
        
        time = datetime.now().strftime('%Y.%m.%d %H:%M:%S.%f')
        
        print('[{}] {}'.format(time, message))



    def recalculate(self, replace_none=True):
        """
        Recalculate the linear regression model
        =======================================
        
        Parameters
        ----------
        replace_none : boolean
            Whether to replace none value with the mean of data or not. If not,
            the exact pair, that contains None value, will be removed.
            Default: True  

        Returns
        -------
        prediction : float
            Value of prediction       
        """

        # Check None to replace or remove invalid values
        # This helps to avoid calculation errors        
        if None in self.__predictors:
            if replace_none:
                _temp_predictors = []
                _replaceable_ids = []
                for idx, predictor in enumerate(self.__predictors):
                    if predictor is None:
                        _replaceable_ids.append(idx)
                    else:
                        _temp_predictors.append(predictor)
                _temp_mean = mean(_temp_predictors)
                for replace_id in _replaceable_ids:
                    self.__predictors[replace_id] = _temp_mean
                del _temp_predictors
                del _replaceable_ids
                del _temp_mean
            else:
                _removable_ids = []
                for idx, predictor in enumerate(self.__predictors):
                    if predictor is None:
                        _removable_ids.append(idx)
                for removable_id in _removable_ids:
                    self.__predictors.pop(removable_id)
                    self.__targets.pop(removable_id)
                del _removable_ids
                
        if None in self.__targets:
            if replace_none:
                _temp_targets = []
                _replaceable_ids = []
                for idx, target in enumerate(self.__targets):
                    if target is None:
                        _replaceable_ids.append(idx)
                    else:
                        _temp_targets.append(target)
                _temp_mean = mean(_temp_targets)
                for replace_id in _replaceable_ids:
                    self.__targets[replace_id] = _temp_mean
                del _temp_targets
                del _replaceable_ids
                del _temp_mean
            else:
                _removable_ids = []
                for idx, target in enumerate(self.__targets):
                    if target is None:
                        _removable_ids.append(idx)
                for removable_id in _removable_ids:
                    self.__targets.pop(removable_id)
                    self.__predictors.pop(removable_id)
                del _removable_ids

        self.__x_mean = mean(self.__predictors)
        self.__y_mean = mean(self.__targets)
        
        sum_x_diff_sqr = 0
        sum_x_y_diff_mult = 0
        sum_y_diff_sqr = 0

        # Create pairs and other important variables for regression calculation        
        for pair in zip(self.__predictors, self.__targets):
            self.__pairs.append([pair[0], pair[1]])
            x_diff = pair[0] - self.__x_mean
            y_diff = pair[1] - self.__y_mean
            x_y_diff_mult = x_diff * y_diff
            sum_x_y_diff_mult += x_y_diff_mult
            x_diff_sqr = x_diff ** 2
            sum_x_diff_sqr += x_diff_sqr
            y_diff_sqr = y_diff ** 2
            sum_y_diff_sqr += y_diff_sqr

        # Regression calculation            
        self.__slope = sum_x_y_diff_mult / sum_x_diff_sqr
        self.__intercept = self.__y_mean - (self.__slope * self.__x_mean)
        self.__r = sum_x_y_diff_mult / (sqrt(sum_x_diff_sqr) * sqrt(sum_y_diff_sqr))



    def reset(self, verbose=False):
        """
        Reset variables to None or default.
        ===================================
        
        Parameters
        ----------
        verbose : boolean
            Whether to print a message that variables are set to None or
            default correctly.
            Default: False
        
        Notes
        -----
        The following variables will be None:
            self.__predictors, self.__targets, self.__slope, self.__intercept,
            self.__x_mean, self.__y_mean, self.__r
        The following variables will be default (other than None):        
            self.__pairs : empty list
        
        Returns
        -------
        None
        """
        
        self.__predictors = None
        self.__targets = None
        self.__pairs = []
        self.__slope = None
        self.__intercept = None
        self.__x_mean = None
        self.__y_mean = None
        self.__r = None
        if verbose:
            self.printout('Variables are set to None or default.')



if __name__ == "__main__":
    # Handling error when not using as a module
    raise RuntimeError('This is a module, not a script!')
else:
    # This is a module, not a script!
    pass
