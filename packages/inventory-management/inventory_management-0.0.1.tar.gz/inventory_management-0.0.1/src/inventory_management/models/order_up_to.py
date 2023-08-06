from statistics import NormalDist
import dataclasses
from typing import Iterable

import numpy as np


class OrderUpToNormal:
    def fit(self, demand: Iterable):
        self.normal_distribution = NormalDist.from_samples(demand)
        return self

    def predict(
        self,
        current_inventory: int,
        lead_time: int,
        inventory_period: int,
        service_level: float = 0.999,
    ) -> float:
        t = lead_time + inventory_period
        service_point = (
            self.normal_distribution.inv_cdf(service_level)
            - self.normal_distribution.mean
        )
        desired_inventory = (self.normal_distribution.mean * t) + (
            service_point * np.sqrt(t)
        )
        return desired_inventory - current_inventory
