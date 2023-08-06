from statistics import NormalDist
from pytest import approx
import math

from inventory_management import OrderUpToNormal


def test_OrderUpToNormal1():
    data = NormalDist(40, 20).samples(1000)
    model = OrderUpToNormal().fit(data)
    S = model.predict(0, 2, 1, 0.98)
    assert approx(S, 191.14, 0.1)
