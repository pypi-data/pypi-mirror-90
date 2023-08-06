import numpy as np
import pandas as pd

import json
from json import JSONEncoder

from zigzag import peak_valley_pivots
from sklearn.cluster import AgglomerativeClustering


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


class Builder:
    def __init__(
            self,
            peak_percent_delta,
            merge_distance,
            merge_percent,
            min_bars_between_peaks
    ):
        self._peak_percent_delta = peak_percent_delta / 100
        self._min_bars_between_peaks = min_bars_between_peaks
        self._merge_distance = merge_distance
        self._merge_percent = merge_percent

    def with_candles(self, candles):
        rows = []
        for candle in candles:
            rows.append(candle['close'])

        df = pd.DataFrame(rows)
        df.columns = ['Close']

        self._prices = df['Close'].values
        self._candles = candles

    def find_potential_level_candles(self):
        pivots = peak_valley_pivots(self._prices, self._peak_percent_delta, -self._peak_percent_delta)
        indexes = self._get_pivot_indexes(pivots)

        self._pivots = pivots

        return indexes

    def candles_to_levels(self, pivot_candles_indexes):
        prices = self._prices[pivot_candles_indexes]
        candles = self._candles[pivot_candles_indexes]
        pivots = self._pivots[pivot_candles_indexes]
        distance = self._get_distance(self._prices)

        return self._cluster_prices_to_levels(prices, candles, pivots, distance)

    def _get_pivot_indexes(self, pivots):
        indexes = np.where(np.abs(pivots) == 1)
        return self._filter_by_bars_between(indexes)

    def _filter_by_bars_between(self, indexes):
        indexes = np.sort(indexes).reshape(-1, 1)

        try:
            selected = [indexes[0][0]]
        except IndexError:
            return indexes

        pre_idx = indexes[0][0]
        for i in range(1, len(indexes)):
            if indexes[i][0] - pre_idx < self._min_bars_between_peaks:
                continue
            pre_idx = indexes[i][0]
            selected.append(pre_idx)

        return np.array(selected)

    def _get_distance(self, X):
        if self._merge_distance:
            return self._merge_distance

        mean_price = np.mean(X)
        return self._merge_percent * mean_price / 100

    def _cluster_prices_to_levels(self, prices, candles, pivots, distance):
        clustering = AgglomerativeClustering(distance_threshold=distance, n_clusters=None)
        try:
            clustering.fit(prices.reshape(-1, 1))
        except ValueError:
            return None

        candles = pd.DataFrame(data=candles, columns=('candles',))
        prices = pd.DataFrame(data=prices, columns=('price',))
        pivots = pd.DataFrame(data=pivots, columns=('pivot',))

        candles['cluster'] = clustering.labels_
        candles['pivots'] = pivots
        prices['cluster'] = clustering.labels_
        prices['pivots'] = pivots
        # pivots['cluster'] = clustering.labels_

        candles = candles.groupby(['cluster', 'pivots']).apply(np.array)
        prices = prices.groupby(['cluster', 'pivots']).agg({'price': 'mean'}).apply(np.array)

        data = np.column_stack([candles, prices])

        return data
