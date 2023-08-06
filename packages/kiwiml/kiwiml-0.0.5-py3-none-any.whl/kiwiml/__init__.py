"""
  _    _          _
 | | _(_)_      _(_)
 | |/ / \ \ /\ / / |
 |   <| |\ V  V /| |
 |_|\_\_| \_/\_/ |_|

------------------------
kiwi v0.0.5
written by ori yonay
------------------------

current features:
 - linear regression
 - logistic regression
 - single dimensional analysis
 - perceptron
 - naive bayes
 - KNN
 - autodiff
 - accuracy score
 - PCA
 - train_test_split
 - plot_cost_history
 - dataset importer (boston, breast cancer, MNIST)

TODO:
 - add laplace smoothing to naive bayes model
 - Error: add mean absolute deviation
 - SVM
 - Decision Tree
 - Random Forest
 - K-Means Clustering
 - Neural Network Library
     - fully-connected layer
     - convolutional layer
     - residual layer? idk
 - Error functions:
     - MAD
 - Autolearn

"""

import heapq # for KNN
import numpy as np
import random # for Utils.train_test_split

##### UTILITY FUNCTIONS #####
class Utils:
  def accuracy_score(y_true, pred):
    # make sure the lengths are the same:
    if len(y_true) != len(pred):
      raise Exception('(accuracy_score) error: length of y_true and pred must be equal.')

    return np.sum(y_true == pred) / len(y_true)

  def train_test_split(X, y, test_size=0.2):
    # calculate the holdout (index at which to split train/test data):
    holdout = int(test_size * len(X))

    # append the y-values to X:
    data = np.append(X, y[:, np.newaxis], axis=1)

    # split data into training and testing sets at random:
    random.shuffle(data)
    train = data[holdout:]
    test = data[:holdout]

    # split training and testing data into examples and labels:
    X_train = np.array([row[:-1] for row in train])
    y_train = np.array([row[-1] for row in train])
    X_test = np.array([row[:-1] for row in test])
    y_test = np.array([row[-1] for row in test])

    return X_train, X_test, y_train, y_test

  def plot_cost_history(model, **kwargs):
    # check if the model contains a cost history list:
    if hasattr(model, 'cost_history'):
      import matplotlib.pyplot as plt
      plt.plot(range(len(model.cost_history)), model.cost_history, **kwargs)
    else:
      raise Exception('(plot_cost_history): error: no cost history list found in model.')

  def PCA(X):
    means = np.mean(X.T, axis=1)
    centered_matrix = X - means
    covariance = np.cov(centered_matrix.T)
    values, vectors = np.linalg.eig(covariance)
    projected_data = vectors.T.dot(centered_matrix.T)
    return projected_data.T

  def standardize_data(x):
    mu = np.mean(x, 0)
    sigma = np.std(x, 0)
    x = (x - mu) / sigma
    return x, mu, sigma

  def sigmoid(x):
    return 1 / (1 + np.exp(-x))

  def step(x):
    return np.heaviside(x, 1).astype(int)

  def l2_norm(a, b):
    return np.sqrt(np.sum((a - b)**2))

##### ERROR FUNCTIONS #####
class Error:
  def MSE(X, y, predicted):
    # X not necessary as a parameter but left to keep things consistent with MSE_gradient
    return np.sum((predicted - y)**2) / (len(y))

  def MSE_gradient(X, y, predicted):
    return (2 / len(y)) * (X.T @ (predicted - y))

  def cross_entropy(y, predicted):
    zero_indices = np.argwhere(y==0).flatten()
    cost = -np.sum(np.log(1 - predicted[zero_indices]))
    one_indices = np.argwhere(y==1).flatten()
    cost -= np.sum(np.log(predicted[one_indices]))
    return cost / len(y)

  def cross_entropy_gradient(X, y, predicted):
    return (X.T @ (predicted - y)) / len(y)

  error_functions = {'l2' : Utils.l2_norm}

##### K-NEAREST-NEIGHBORS #####
class KNN:
  def __init__(self, n_neighbors=3, error_function='l2'):
    self.n_neighbors = n_neighbors

    if error_function not in Error.error_functions:
      raise Exception('(KNN) error: error function %s not found.' % error_function)
    self.error_function = Error.error_functions[error_function]

  def fit(self, X, y):
    self.X = X
    self.y = y
    return self

  def predict(self, X):
    pred = []
    for x in X:
      nearest_neighbors = []
      for point, label in zip(self.X, self.y):
        dist = self.error_function(point, x)
        if len(nearest_neighbors) < self.n_neighbors:
          heapq.heappush(nearest_neighbors, (-dist, label))
        else:
          heapq.heappushpop(nearest_neighbors, (-dist, label))
      votes = {}
      for neighbor in nearest_neighbors:
        if neighbor[1] in votes:
          votes[neighbor[1]] += 1
        else:
          votes[neighbor[1]] = 1
      pred.append(max(votes, key=votes.get))
    return np.array(pred)

##### LINEAR REGRESSION #####
class LinearRegressor:
  def __init__(self, normalize=True):
    self.normalize = normalize

  def fit(self, X, y, learning_rate=0.01, n_iters=50):
    if self.normalize:
      self.X, self.X_mu, self.X_sigma = Utils.standardize_data(X)
    else:
      self.X = X

    self.learning_rate = learning_rate
    self.y = y
    self.m, self.n = self.X.shape
    self.n_iters = n_iters
    self.w = np.random.RandomState(1).rand(self.n) # np.random.RandomState(1) is a random number generator
    self.b = 0

    # gradient descent:
    self.cost_history = []
    for _ in range(self.n_iters):
      predicted = self.predict(X)
      self.w -= self.learning_rate * Error.MSE_gradient(self.X, self.y, predicted)
      self.b -= self.learning_rate * np.sum(Error.MSE_gradient(np.ones(self.m), self.y, predicted))
      self.cost_history.append(Error.MSE(self.X, self.y, predicted))

    # return a pointer to itself for syntactic sugar like lr = LinearRegressor().fit(X, y):
    return self

  def predict(self, x):
    # if we trained the model on normalized data, we should also normalize any testing data
    # in the same way we did the training data:
    if self.normalize:
      x_copy = (x - self.X_mu) / self.X_sigma
    return (x_copy @ self.w) + self.b

##### LOGISTIC REGRESSION #####
class LogisticRegressor:
  def __init__(self, normalize=True):
    self.normalize = normalize

  def fit(self, X, y, learning_rate=0.01, n_iters=50):
    if self.normalize:
      self.X, self.X_mu, self.X_sigma = Utils.standardize_data(X)
    else:
      self.X = X

    self.learning_rate = learning_rate
    self.y = y
    self.m, self.n = self.X.shape
    self.w = np.zeros(self.n)
    self.b = 0

    self.cost_history = []
    for _ in range(n_iters):
      predicted = Utils.sigmoid((self.X @ self.w) + self.b)
      self.w -= self.learning_rate * Error.cross_entropy_gradient(self.X, self.y, predicted)
      self.b -= self.learning_rate * np.sum(Error.cross_entropy_gradient(np.ones(self.m), self.y, predicted))
      self.cost_history.append(Error.cross_entropy(self.y, predicted))

    return self

  def predict(self, x):
    # if we trained the model on normalized data, we should also normalize any testing data
    # in the same way we did the training data:
    if self.normalize:
      x_copy = (x - self.X_mu) / self.X_sigma
    return np.round(Utils.sigmoid((x_copy @ self.w) + self.b))

##### NAIVE BAYES #####
class NaiveBayes:
  def __init__(self):
    pass

  def fit(self, X, y):
    # setup:
    self.m, self.n = X.shape
    self.classes = np.unique(y)
    self.n_classes = len(self.classes)

    # calculate means, variances, and priors for each class:
    # note: priors = frequency of every class in our example set
    self.mu = np.zeros((self.n_classes, self.n), dtype=np.float64)
    self.var = np.zeros((self.n_classes, self.n), dtype=np.float64)
    self.priors = np.zeros(self.n_classes, dtype=np.float64)
    self.log_priors = np.zeros(self.n_classes, dtype=np.float64)

    for idx, c in enumerate(self.classes):
      X_c = X[y == c] # all examples of class c
      self.mu[idx, :] = X_c.mean(axis=0)
      self.var[idx, :] = X_c.var(axis=0)
      self.priors[idx] = len(X_c) / float(self.m)
      self.log_priors[idx] = np.log(self.priors[idx])

    return self

  def predict(self, X):
    pred = []
    for p in X:
      # calculate the conditional probabilities for each class:
      posteriors = []
      for idx, c in enumerate(self.classes):
        log_prior = self.log_priors[idx]
        class_conditional = np.sum(np.log(self._pdf(idx, p)))
        posterior = log_prior + class_conditional
        posteriors.append(posterior)

      # predict the class with the highest probability:
      pred.append(self.classes[np.argmax(posteriors)])

    return np.array(pred)

  def _pdf(self, class_idx, x):
    class_mu = self.mu[class_idx]
    class_var = self.var[class_idx]
    return np.exp(-(x - class_mu)**2 / (2 * class_var)) / np.sqrt(2 * np.pi * class_var)

##### PERCEPTRON #####
class Perceptron:
  def __init__(self, normalize=True):
    self.normalize = normalize

  def fit(self, X, y, learning_rate=0.01, n_iters=50):
    if self.normalize:
      self.X, self.X_mu, self.X_sigma = Utils.standardize_data(X)
    else:
      self.X = X

    self.learning_rate = learning_rate
    self.y = y
    self.m, self.n = self.X.shape
    self.w = np.zeros(self.n)
    self.b = 0

    # make sure y contains only 0s and 1s:
    y_ = np.heaviside(y, 0).astype(np.int)

    self.cost_history = []
    for _ in range(n_iters):
      predicted = Utils.step((self.X @ self.w) + self.b)
      self.w -= self.learning_rate * (predicted - y_) @ X
      self.b -= self.learning_rate * (np.sum(predicted - y_) / self.m)

      # here, the cost function is just (1 - average accuracy):
      self.cost_history.append(np.sum(predicted - y_) / self.m)

    return self

  def predict(self, x):
    # if we trained the model on normalized data, we should also normalize any testing data
    # in the same way we did the training data:
    if self.normalize:
      x_copy = (x - self.X_mu) / self.X_sigma
    return Utils.step((x_copy @ self.w) + self.b)

##### SINGLE DIMENSIONAL ANALYSIS #####
"""
the idea behind this approach is simple: find the optimal decision boundary for each
dimension along with its 'ratio' (a measure of separability of the data). we then
use this to calculate a weighted sum of the ratios (after they're normalized so their
sum equals 1) and their respective predictions.
"""
class SDA:
  def __init__(self):
    pass

  def fit(self, X, y):
    # make sure y contains only 0s and 1s:
    y_ = np.heaviside(y, 0).astype(np.int)

    # append the y-values to X:
    data = np.append(X, y_[:, np.newaxis], axis=1)

    self.m, self.n = X.shape
    num_ones = sum(y_)
    num_zeros = len(y_) - num_ones

    # for each dimension, calculate the optimal point of separation:
    self.model = []
    for dim in range(self.n):
      # sort the examples by this dimension:
      data = sorted(data, key = lambda i: i[dim])

      # find the optimal point of separation:
      zeros_on_left = 0
      zeros_on_right = num_zeros
      ones_on_left = 0
      ones_on_right = num_ones

      prev_threshold = data[0][dim]
      cur_threshold = data[0][dim]
      max_correct = max(num_zeros, num_ones)
      is_zol = num_ones > num_zeros

      for idx, p in enumerate(data):
        if int(p[-1]) == 0:
          zeros_on_left += 1
          zeros_on_right -= 1
        else:
          ones_on_left += 1
          ones_on_right -= 1

        correct = max(zeros_on_left + ones_on_right, zeros_on_right + ones_on_left)
        if correct >= max_correct:
          max_correct = correct
          is_zol = (zeros_on_left + ones_on_right > zeros_on_right + ones_on_left)
          prev_threshold = p[dim]
          if idx + 1 < len(data):
            cur_threshold = data[idx+1][dim]

      threshold = (prev_threshold + cur_threshold) / 2
      ratio = max_correct / len(data)

      self.model.append([threshold, ratio, is_zol])

    # standardize the ratios so they add up to 1:
    sum_ratios = sum(i[1] for i in self.model)
    for idx in range(self.n):
      self.model[idx][1] /= sum_ratios

    return self

  def predict(self, X):
    pred = []
    for p in X:
      weighted_sum = 0
      for x, b in zip(p, self.model):
        if (x > b[0] and b[2]) or (x < b[0] and not b[2]):
          weighted_sum += b[1]

      pred.append(round(weighted_sum))

    return np.array(pred, dtype=np.int8)
