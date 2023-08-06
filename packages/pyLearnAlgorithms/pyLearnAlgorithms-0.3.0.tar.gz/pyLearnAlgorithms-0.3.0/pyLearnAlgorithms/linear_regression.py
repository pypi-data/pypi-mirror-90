import numpy as np
from scipy import optimize

class LinearRegression():
    """class for building linear regression models"""

    def __init__(self, X, y):
        """stores predictive attributes and labels"""

        # predictive attributes
        self.X = X
        # values to be predicted
        self.y = y

        return None
    
    def linear_reg_cost_function(self, theta = [1, 1], lambda_= 0.0):
        """cost function for a varied hypothesis (with regularization)"""

        theta = np.array(theta)
        m = self.y.size 
        X_bias = np.concatenate([np.ones((m, 1)), self.X], axis=1)
        J = 0
        grad = np.zeros(theta.shape)
        h = X_bias.dot(theta)
        J = (1 / (2 * m)) * np.sum(np.square(h - self.y)) + (lambda_ / (2 * m)) * np.sum(np.square(theta[1:]))
        grad = (1 / m) * (h - self.y).dot(X_bias)
        grad[1:] = grad[1:] + (lambda_ / m) * theta[1:]

        return J, grad

    def train_linear_reg(self, lambda_ = 0.0, maxiter = 200):
        """training the model for minimizing the cost function and modifying theta parameters"""

        model = LinearRegression(self.X, self.y)
        m = self.y.size 
        X_bias = np.concatenate([np.ones((m, 1)), self.X], axis=1)
        teta_inicial = np.zeros(len(X_bias[0, :]))
        costFunction = lambda t: model.linear_reg_cost_function(t, lambda_)
        options = {'maxiter': maxiter}
        res = optimize.minimize(costFunction,teta_inicial,jac=True,method='TNC',options=options)

        return res

    def learning_curve(self, Xval, yval, lambda_= 0.0):
        """computes training error and validation error for different data extracts"""

        model = LinearRegression(self.X, self.y)
        m = self.y.size
        error_train = np.zeros(m)
        error_val = np.zeros(m)
        for i in range(1, m + 1):
            model = LinearRegression(self.X[:i], self.y[:i])
            teta_t = model.train_linear_reg()
            error_train[i-1],_ = model.linear_reg_cost_function(teta_t.x)
            model = LinearRegression(Xval, yval)
            error_val[i-1],_ = model.linear_reg_cost_function(teta_t.x)
        
        return error_train, error_val
    
    def predict(self, Xtest):
        """makes the prediction for the test values"""

        model = LinearRegression(self.X, self.y)
        optimized_values = model.train_linear_reg(lambda_= 0.0)
        X_bias = np.concatenate([np.ones((Xtest.size, 1)), Xtest], axis=1)
        pred = np.dot(X_bias, optimized_values.x)

        return pred
    
    def predict_normal_equation(self, Xtest):
        """makes the prediction for the test values with normal equation"""

        model = LinearRegression(self.X, self.y)
        _, grad = model.normal_equation()
        X_bias = np.concatenate([np.ones((Xtest.size, 1)), Xtest], axis=1)
        pred = np.dot(X_bias, grad)

        return pred
    
    def normal_equation(self):
        """computes the linear regression model using the normal equation (least quadratic)"""

        m = self.y.size 
        X_bias = np.concatenate([np.ones((m, 1)), self.X], axis=1)
        grad = np.linalg.inv((X_bias.T.dot(X_bias))).dot(X_bias.T.dot(self.y))
        model = LinearRegression(self.X, self.y)
        J, _ = model.linear_reg_cost_function(grad, lambda_ = 0.0)
    
        return J, grad

    
