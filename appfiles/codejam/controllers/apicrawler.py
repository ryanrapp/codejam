import pprint
import requests
from codejam.controllers import basecrawler
from codejam import utils

class APICrawler(basecrawler.BaseCrawler):
  """
  Requests data from API and renders as datapoints
  """
  # todo (rrapp): optimize for loose searching by adding indexes

  def __init__(self, dataview, endpoint='http://codejam.airpr.com/poll'):
    super(APICrawler, self).__init__()
    self.dateutil = utils.CJDateUtil()
    self.endpoint = endpoint
    self.dataview = dataview

  def crawl(self, feed_id, seconds):
    super(APICrawler, self).crawl(feed_id, seconds)

    poll_time = self.dateutil.from_seconds_to_datetime(seconds)

    print "Crawling time: %s" % poll_time

    params = {'feed_id': str(feed_id), 'poll_time': poll_time.isoformat()}
    r = requests.get(self.endpoint, params=params)
    datapoints = self.dataview.render_datapoints(feed_id, r.json().get('article_times', []))

    return datapoints

  def get_total_posts(self, feed_id):
    return len(self.training_data[feed_id])
