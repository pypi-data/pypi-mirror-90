#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from typing import Iterable

from pinecone.functions.ranker import Ranker

import numpy as np


class EuclideanRanker(Ranker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def batch_euclidean(self, xx, uu):
        xx_normed_squared = np.einsum('ij,ij->i', xx, xx)
        uu_normed_sqaured = np.einsum('ij,ij->i', uu, uu)
        return - xx_normed_squared - uu_normed_sqaured + 2 * np.dot(xx, np.transpose(uu))
    

    def score(self, q: np.ndarray, vectors: np.ndarray, prev_scores: Iterable[float]) -> Iterable[float]:
        return self.batch_euclidean(q, vectors).flatten()
