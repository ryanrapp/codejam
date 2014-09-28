# BaseModel for calculating

class BaseModel(object):
  """Abstract base model to estimate next interval"""
  description = "Unknown Model"
  do_last = True

  def predict_interval(self, result):
    raise NotImplementedError

  def adjust_prediction(self, predicted_y):
    raise NotImplementedError

  def get_interval(self, result):
    predicted_y = self.predict_interval(result)
    return self.adjust_prediction(predicted_y)
