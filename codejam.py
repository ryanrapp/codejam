import numpy as np

from codejam import trainer, dispatcher
from codejam import mockcrawler
from codejam import judge
from codejam.models import arima

mytrainer = trainer.Trainer()
mytrainer.train()

mytrainer.draw_hist('22425')

mycrawler = mockcrawler.MockCrawler(mytrainer)
myjudge = judge.Judge(mycrawler)
arima_model = arima.ArimaModel(3, 10)
d = dispatcher.Dispatcher(mycrawler, myjudge)

#d.process_feed('22425', arima_model)
d.process_feed('254130', arima_model)
#d.process_feed('649380', arima_model)



# # Create a random dataset
# rng = np.random.RandomState(2)
# X = np.sort(5 * rng.rand(80, 1), axis=0)
# y = np.sin(X).ravel()
# y[::5] += 3 * (0.5 - rng.rand(16))
#
# # Fit regression model
# from sklearn.tree import DecisionTreeRegressor
#
# clf_1 = DecisionTreeRegressor(max_depth=2)
# clf_2 = DecisionTreeRegressor(max_depth=3)
# clf_1.fit(X, y)
# clf_2.fit(X, y)
#
# # Predict
# X_test = np.arange(0.0, 5.0, 0.01)[:, np.newaxis]
# y_1 = clf_1.predict(X_test)
# y_2 = clf_2.predict(X_test)
#
# # Plot the results
# import matplotlib.pyplot as plt
#
# plt.figure()
# plt.scatter(X, y, c="k", label="data")
# #plt.plot(X_test, y_1, c="g", label="max_depth=2", linewidth=2)
# plt.plot(X_test, y_2, c="r", label="max_depth=3", linewidth=2)
# plt.xlabel("data")
# plt.ylabel("target")
# plt.title("Decision Tree Regression")
# plt.legend()
# plt.show()
