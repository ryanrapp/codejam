import pprint
from codejam.controllers import basecrawler

class MockCrawler(basecrawler.BaseCrawler):
  """Performance optmized mock crawler that can only read training data"""
  # todo (rrapp): optimize for loose searching by adding indexes

  def __init__(self, training_data):
    super(MockCrawler, self).__init__()
    self.training_data = training_data

  def crawl(self, feed_id, seconds):
    super(MockCrawler, self).crawl(feed_id, seconds)

    last_ten = []
    for post in self.training_data[feed_id]:
      if seconds <= post[0]:
        return last_ten

      last_ten.append(post)
      if len(last_ten) > 10:
        last_ten.pop(0)

  def get_total_posts(self, feed_id, start_time = None, end_time = None):
    if start_time is None:
      return len(self.training_data[feed_id])
    else:
      sum = 0
      for item in self.training_data[feed_id]:
        if item[0] >= start_time and item[0] <= end_time:
          sum += 1

      return sum
