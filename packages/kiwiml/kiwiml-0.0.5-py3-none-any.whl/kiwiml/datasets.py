##### DATASETS #####
import numpy as np
import requests

DATASET_INFO = {
    'BOSTON' : {
        'URL' : 'http://lib.stat.cmu.edu/datasets/boston'
    },
    'BREAST_CANCER' : {
        'URL' : 'https://archive.ics.uci.edu/ml/machine-learning-databases/breast-cancer-wisconsin/wdbc.data',
        'TARGET_VALUES' : {'M': 0, 'B': 1}
    },
    'MNIST' : {
        'X_TRAIN_URL' : 'http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz',
        'X_TEST_URL' : 'http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz',
        'Y_TRAIN_URL' : 'http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz',
        'Y_TEST_URL' : 'http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz'
    }
}

##### LOAD THE MNIST DATASET #####
def load_digits():
  import gzip

  # to make the code less messy and more readable:
  X_TRAIN_URL = DATASET_INFO['MNIST']['X_TRAIN_URL']
  X_TEST_URL = DATASET_INFO['MNIST']['X_TEST_URL']
  Y_TRAIN_URL = DATASET_INFO['MNIST']['Y_TRAIN_URL']
  Y_TEST_URL = DATASET_INFO['MNIST']['Y_TEST_URL']

  # initialize the arrays:
  X_train = []
  X_test = []
  y_train = []
  y_test = []

  # fetch and decompress the data:
  def fetch_data(url):
    data = requests.get(url).content
    return np.frombuffer(gzip.decompress(data), dtype=np.uint8).copy()

  # reshape and process the data:
  X_train = fetch_data(X_TRAIN_URL)[0x10:].reshape((-1, 28, 28))
  X_test = fetch_data(X_TEST_URL)[0x10:].reshape((-1, 28, 28))
  y_train = fetch_data(Y_TRAIN_URL)[8:]
  y_test = fetch_data(Y_TEST_URL)[8:]

  # merge the training and testing data and return them:
  return np.append(X_train, X_test, axis=0), np.append(y_train, y_test)

##### LOAD THE BOSTON DATASET #####
def load_boston():
  # load the data:
  BOSTON_URL = DATASET_INFO['BOSTON']['URL']
  data = requests.get(BOSTON_URL).content
  data = str(data).split('\\n')[22:-1]

  # format and parse the data:
  it = iter(data)
  X = []
  y = []
  for x in it:
    # note: (x + next(it)) is the full space-separated line containing a single data point
    datapoint = [np.float64(i) for i in (x + next(it)).split()]
    y.append(datapoint.pop()) # append last element of datapoint, then remove it from datapoint
    X.append(np.array(datapoint)) # append the rest of the datapoints to X

  return np.array(X), np.array(y)

##### LOAD THE UCI BREAST CANCER DATASET #####
def load_breast_cancer():
  BREAST_CANCER_URL = DATASET_INFO['BREAST_CANCER']['URL']
  TARGET_VALUES = DATASET_INFO['BREAST_CANCER']['TARGET_VALUES']
  # get and comma-separate the data from the URL:
  data = requests.get(BREAST_CANCER_URL).content
  data = [i.split('\\n')[0] for i in str(data)[9:].split(',')] # [9:] because we ignore the first ID number

  # process the data:
  X = []
  y = []
  for i in data:
    # if i is a target value, append it to y:
    if i in TARGET_VALUES:
      y.append(TARGET_VALUES[i])
    # otherwise, append the data point as a float:
    else:
      X.append(np.float64(i))

  X = np.array(X).reshape(-1, 30)
  y = np.array(y)

  return X, y
