import pprint
from codejam import trainer, basecrawler

class MockCrawler(basecrawler.BaseCrawler):
  """Performance optmized mock crawler that can only read training data"""
  # todo (rrapp): optimize for loose searching by adding indexes

  def __init__(self, trainer):
    super(MockCrawler, self).__init__()
    self.trainer = trainer
    self.training_data = self.trainer.get_data()

  def crawl(self, feed_id, seconds):
    super(MockCrawler, self).crawl(feed_id, seconds)

    last_ten = []
    #pprint.pprint(self.training_data)
    for post in self.training_data[feed_id]:
      # Maintain list of last ten

      if seconds <= post[0]:
        #print "seconds %d" % seconds
        #print "post seconds %d" % post[0]
        #Return a copy of the last ten articles observed
        return last_ten

      last_ten.append(post)
      if len(last_ten) > 10:
        last_ten.pop(0)

  def get_total_posts(self, feed_id):
    return len(self.training_data[feed_id])
