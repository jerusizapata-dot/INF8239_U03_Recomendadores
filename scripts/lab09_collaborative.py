from __future__ import annotations

import json
from time import perf_counter

from sklearn.metrics import root_mean_squared_error

from inf8239_u03.config import MOVIELENS_DIR, ROOT
from inf8239_u03.data import load_movielens
from inf8239_u03.metrics import catalog_coverage, hit_rate_at_k
from inf8239_u03.recommenders import MatrixFactorization, temporal_leave_one_out

ratings, movies = load_movielens(MOVIELENS_DIR)
train, test = temporal_leave_one_out(ratings)
start = perf_counter()
model = MatrixFactorization(factors=20, seed=42).fit(train, epochs=12)
train_seconds = perf_counter() - start
evaluable = test[test["userId"].isin(model.user_index) & test["movieId"].isin(model.item_index)]
predictions = [model.predict(row.userId, row.movieId) for row in evaluable.itertuples()]
rmse = root_mean_squared_error(evaluable["rating"], predictions)
recommendations = {}
for user_id in evaluable["userId"].unique():
    seen = set(train.loc[train["userId"].eq(user_id), "movieId"])
    top = model.top_n(user_id, seen, 10)
    recommendations[int(user_id)] = top["movieId"].astype(int).tolist()
metrics = {
    "method": "colaborativo",
    "rmse": float(rmse),
    "hit_rate_at_10": hit_rate_at_k(recommendations, evaluable, 10),
    "catalog_coverage": catalog_coverage(recommendations, len(movies)),
    "train_seconds": train_seconds,
    "factors": 20,
    "epochs": 12,
    "seed": 42,
}
model_size_bytes = int(model.user_factors.nbytes + model.item_factors.nbytes)
metrics["model_size_bytes"] = model_size_bytes
metrics["model_size_mib"] = model_size_bytes / (1024 ** 2)
(ROOT / "reports").mkdir(exist_ok=True)
(ROOT / "reports/collaborative_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
print(json.dumps(metrics, indent=2))
