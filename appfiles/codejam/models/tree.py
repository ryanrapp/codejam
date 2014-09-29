#Defines decision tree model
from codejam.models import basemodel
from sklearn import tree
import pprint

class TreeModel(basemodel.BaseModel):
  """Uses decision tree to estimate next time to crawl"""
  description = "Tree Model"
  def __init__(self):
    self.clf = tree.DecisionTreeRegressor()
    self.results = []

  def train(self, X, y):
    self.clf.fit(X, y)

  def adjust_prediction(self, predicted_y):
    return max(predicted_y, 1)

  def predict_interval(self, result):
    y_hat = [1000]
    self.results.append(result)

    clf = tree.DecisionTreeRegressor()

    window_length = 2
    window = []
    X = []
    y = []

    for i in range(1, len(result)):
      delta = result[i][0] - result[i-1][0]
      window.append(delta)
      if len(window) > window_length:
        window.pop(0)

      x = window[:]
      x.extend([result[i][1], result[i][2]])

      if len(window) == window_length and i+1 < len(result):
        X.append(x)
        y.append(result[i+1][0] - result[i][0])

    if len(X) != len(y):
      raise Exception('X and y need to be same length')
    if len(X) > 3:
      clf.fit(X, y)
      y_hat = clf.predict(x)
      pprint.pprint({'y_hat':y_hat})

    return y_hat[0]
