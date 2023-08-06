#
# Copyright (c) 2020-2021 Pinecone Systems Inc. All right reserved.
#

from typing import Iterable

from pinecone.functions.ranker import Ranker

import numpy as np


class CosineRanker(Ranker):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def batch_norm(self, xx):
        xx_row_norms = np.sqrt(np.einsum('ij,ij->i', xx, xx))
        xx_row_norms[xx_row_norms == 0] = 1  # don't normalize zero vectors
        return xx / np.broadcast_to(xx_row_norms, (xx.shape[1],) + xx_row_norms.shape).T

    def sim_cosine(self, x, u):
        norm_x = np.sqrt(np.einsum('i,i->', x, x))
        norm_u = np.sqrt(np.einsum('i,i->', u, u))
        ret = np.einsum('i,i->', x, u) / (norm_x * norm_u)
        return ret

    def batch_cosine(self, xx, uu):
        xx_normed = self.batch_norm(xx)
        uu_normed = self.batch_norm(uu)
        return np.einsum('ij,kj->ik', xx_normed, uu_normed)

    def score(self, q: np.ndarray, vectors: np.ndarray, prev_scores: Iterable[float]) -> Iterable[float]:
        return self.batch_cosine(vectors, q).flatten()
