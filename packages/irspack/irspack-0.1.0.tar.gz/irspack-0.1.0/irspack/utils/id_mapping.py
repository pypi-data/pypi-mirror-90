from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import scipy.sparse as sps

from irspack.definitions import DenseScoreArray, InteractionMatrix, UserIndexArray
from irspack.recommenders import BaseRecommender


class IDMappedRecommender:
    def __init__(
        self, recommender: BaseRecommender, user_ids: List[Any], item_ids: List[Any]
    ):
        if recommender.n_users != len(user_ids):
            raise ValueError(
                "The recommender and user_ids have inconsistent number of users."
            )

        if recommender.n_items != len(item_ids):
            raise ValueError(
                "The recommender and item_ids have inconsistent number of items."
            )
        self.recommender = recommender
        self.user_ids = user_ids
        self.item_ids = item_ids
        self.user_id_to_index = {user_id: i for i, user_id in enumerate(user_ids)}
        self.item_id_to_index = {item_id: i for i, item_id in enumerate(item_ids)}

    def _score_to_recommended_items(
        self,
        score: DenseScoreArray,
        cutoff: int,
        allowed_item_ids: Optional[List[Any]] = None,
        forbidden_item_ids: Optional[List[Any]] = None,
    ) -> List[Tuple[Any, float]]:
        high_score_inds = score.argsort()[::-1]
        recommendations: List[Tuple[Any, float]] = []
        for i in high_score_inds:
            i_int = int(i)
            score_this = score[i_int]
            item_id = self.item_ids[i_int]
            if np.isinf(score_this):
                continue
            if allowed_item_ids is not None:
                if item_id not in allowed_item_ids:
                    continue
            if forbidden_item_ids is not None:
                if item_id in forbidden_item_ids:
                    continue
            recommendations.append((item_id, float(score_this)))
            if len(recommendations) >= cutoff:
                break
        return recommendations

    def get_recommendation_for_known_user_id(
        self, user_id: Any, cutoff: int = 20
    ) -> List[Tuple[Any, float]]:
        if user_id not in self.user_ids:
            raise RuntimeError(f"User with user_id {user_id} not found.")
        user_index: UserIndexArray = np.asarray(
            [self.user_id_to_index[user_id]], dtype=np.int64
        )
        score = self.recommender.get_score_remove_seen([user_index])[0, :]
        high_score_inds = score.argsort()[::-1]
        recommendations: List[Tuple[Any, float]] = []
        for i in high_score_inds:
            i_int = int(i)
            score_this = score[i_int]
            if np.isinf(score_this):
                continue
            recommendations.append((self.item_ids[i_int], float(score_this)))
            if len(recommendations) >= cutoff:
                break
        return recommendations

    def get_recommendation_for_new_user(
        self, item_ids: List[Any], cutoff: int = 20
    ) -> List[Tuple[Any, float]]:
        interactions_with_known_items = sorted(
            [
                self.item_id_to_index[item_id]
                for item_id in self.item_ids
                if item_id in self.item_id_to_index
            ]
        )
        cols = np.asarray(interactions_with_known_items, dtype=np.int64)
        rows = np.zeros_like(cols)
        data = np.ones(cols.shape, dtype=np.float64)
        X_input = sps.csr_matrix((data, (rows, cols)), shape=(1, len(self.item_ids)))
        score = self.recommender.get_score_cold_user_remove_seen(X_input)
