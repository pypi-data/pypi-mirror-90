import numpy as np
from pyLearnAlgorithms.linear_regression import LinearRegression 
from scipy import optimize

class PolynomialRegression():
    """class for building polynomial regression models"""
    
    def __init__(self, X, y):
        """stores predictive attributes and labels"""

        # predictive attributes
        self.X = X
        # values to be predicted
        self.y = y

        return None

    def poly_features(self, X, poly_degree = 1):
        """performs polynomial mapping on predictive attributes"""

        X_poly = np.zeros((X.shape[0], poly_degree))
        for i in range(poly_degree):
            X_poly[:, i] = X[:, 0] ** (i + 1)

        return X_poly
    
    def feature_normalize(self, X_poly):
        """performs normalization on predictive attributes by normal distribution"""
    
        mu = np.mean(X_poly, axis = 0)
        X_norm = (X_poly - mu)
        sigma = np.std(X_norm, axis = 0, ddof = 1)
        X_norm = X_norm / sigma
        m = self.y.size 
        X_norm = np.concatenate([np.ones((m, 1)), X_norm], axis=1)
        
        return X_norm, mu, sigma

    def prepare_extracts(self, X, y, mu, sigma, poly_degree):
        """performs normalization and polynomial mapping on other data extracts"""

        X_poly = self.poly_features(X, poly_degree)
        X_poly -= mu
        X_poly /= sigma
        X_poly = np.concatenate([np.ones((y.size, 1)), X_poly], axis=1)

        return X_poly

    def poly_reg_cost_function(self, X_poly, y, theta = [1,1], lambda_= 0.0):
        """cost function for a varied hypothesis (with regularization)"""

        theta = np.array(theta)
        m = y.size 
        J = 0
        grad = np.zeros(theta.shape)
        h = X_poly.dot(theta)
        J = (1 / (2 * m)) * np.sum(np.square(h - y)) + (lambda_ / (2 * m)) * np.sum(np.square(theta[1:]))
        grad = (1 / m) * (h - y).dot(X_poly)
        grad[1:] = grad[1:] + (lambda_ / m) * theta[1:]

        return J, grad

    def train_poly_reg(self, X_poly, y, lambda_ = 0.0, maxiter = 200):
        """training the model for minimizing the cost function and modifying theta parameters"""

        initial_theta = np.zeros(X_poly[0,:].size)
        costFunction = lambda t: self.poly_reg_cost_function(X_poly, y, t, lambda_)
        options = {'maxiter': maxiter}
        res=optimize.minimize(costFunction, initial_theta, jac = True, method = 'TNC', options = options)

        return res
    
    def learning_curve(self, X_poly, y, Xval, yval, lambda_ = 0.0, maxiter = 200):
        """computes training error and validation error for different data extracts"""
        
        m = y.size
        error_train = np.zeros(m)
        error_val   = np.zeros(m)
        for i in range(1, m + 1):
            theta_t = self.train_poly_reg(X_poly[:i], y[:i], lambda_, maxiter)
            error_train[i-1],_ = self.poly_reg_cost_function(X_poly[:i], y[:i],theta_t.x, lambda_)
            error_val[i - 1], _ = self.poly_reg_cost_function(Xval, yval, theta_t.x, lambda_)
            
        return error_train, error_val
    
    def validation_curve(self, X_poly, y, Xval, yval, lambda_vec):
        """analyzes the lambda values for the best normalization"""

        error_train = np.zeros(len(lambda_vec))
        error_val = np.zeros(len(lambda_vec))
        for i in range(len(lambda_vec)):
            lambda_try = lambda_vec[i]
            theta_t = self.train_poly_reg(X_poly, y, lambda_ = lambda_try)
            error_train[i], _ = self.poly_reg_cost_function(X_poly, y, theta_t.x, lambda_ = 0)
            error_val[i], _ = self.poly_reg_cost_function(Xval, yval, theta_t.x, lambda_ = 0)

        return error_train, error_val
    
    def predict(self, Xtest, X_poly, y, lambda_ = 0.0):
        """makes the prediction for the test values"""

        theta_t = self.train_poly_reg(X_poly, y, lambda_)
        pred = np.dot(Xtest, theta_t.x)

        return pred 
    



    