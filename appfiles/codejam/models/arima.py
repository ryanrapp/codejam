#Define Arima Model
from codejam.models import basemodel

class ArimaModel(basemodel.BaseModel):
  """Uses ARIMA(p,q) to estimate next time to crawl"""
  description = "Arima Model"
  def __init__(self, p = 3, q = 10):
    self.arima_q = 10
    self.result_paces = []

  def adjust_prediction(self, predicted_y):
    return max(predicted_y * .2, 1)

  def predict_interval(self, result):
    interval = 100
    # if len(result) > 7:
    #   arima_result = result[6:]
    # else:
    arima_result = result

    result_diameter = float(
        arima_result[-1][0] - arima_result[0][0])

    if result_diameter > 0:
      result_pace = len(arima_result) / result_diameter

      interval = 1 / result_pace
    else:
      pass

    return interval
