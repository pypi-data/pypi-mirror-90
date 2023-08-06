import numpy as np
from deepNets import KNearestNeighbor as knn 

# testing
def test_KNearestNeighbor():
    X_tst = np.random.randint(1000,size=(500,3073))
    X_trn = np.random.randint(10000,size=(5000,3073))
    y_trn = np.random.randint(10,size=(10000,))
    classifier = knn.KNearestNeighbor()
    classifier.train(X_trn,y_trn)
    y_test = classifier.predict(X_tst)
    print(y_test[:5])


# 'pytest-runner'
#   tests_require=['pytest==4.4.1'],
#   test_suite='tests',