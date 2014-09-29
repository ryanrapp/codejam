#Define exponential model
from codejam.models import basemodel

class ExponentialModel(basemodel.BaseModel):
  """Uses exponential model with geometric discount factor d"""
  description = "Exponential Model"
  def __init__(self, d = .8, q = 10):
    self.d = d
    self.q = q

  def adjust_prediction(self, t, predicted_y):
    return max(predicted_y * 10,10)

  def predict_interval(self, t, results):
    results = results[len(results) - self.q:]
    if len(results) < self.q:
      return 1000

    exp_sum = 0
    scalar_sum = 0

    for i in range(1, len(results)):
      delta = results[i][0] - results[i-1][0]
      exp_sum += (self.d ** (len(results) - i)) * delta
      scalar_sum += self.d ** (len(results) - i)

    return exp_sum / scalar_sum
