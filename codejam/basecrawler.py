# Base crawler class

class BaseCrawler(object):
  """Abstract base crawler class."""

  def __init__(self):
    self.utilization_by_feed = {}
    self.latest_crawl_by_feed = {}

  def crawl(self, feed_id, seconds):
    if feed_id not in self.latest_crawl_by_feed:
      self.latest_crawl_by_feed[feed_id] = seconds
    elif seconds < self.latest_crawl_by_feed[feed_id]:
      raise ValueError('Time travel not supported.')

    if feed_id not in self.utilization_by_feed:
      self.utilization_by_feed[feed_id] = 0
    self.utilization_by_feed[feed_id] += 1
