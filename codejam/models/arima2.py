#Calculate Arima Model
from codejam.models import basemodel

class Arima2Model(basemodel.BaseModel):
  """Uses ARIMA(p,q) to estimate next time to crawl"""
  description = "Arima Model"
  def __init__(self, p = 3, q = 10):
    self.arima_q = 10
    self.result_paces = []

  def adjust_prediction(self, predicted_y):
    return predicted_y

  def predict_interval(self, result):
    interval = 100
    arima_result = result[0:min(self.arima_q, len(result))]
    result_diameter = float(
        arima_result[-1][0] - arima_result[0][0])

    if result_diameter > 0:
      result_pace = round(len(result) / result_diameter,8)
      self.result_paces.append(result_pace)

      interval = 1 / result_pace
    else:
      pass

    return interval
