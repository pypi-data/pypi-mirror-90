from typing import Dict, Any, Optional, Callable
import logging
import tensorflow as tf


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
stream = logging.StreamHandler()
logger.addHandler(stream)


class ModelScoreCallback(tf.keras.callbacks.Callback):

    def __init__(self, score_func: Callable, X, y):
        super().__init__()
        self._score_func = score_func
        self._X = X
        self._y = y

    def on_epoch_end(self, epoch: int, logs: Optional[Dict[str, Any]] = None):
        if self._X is None or self._y is None:
            return 
        score_df = self._score_func(self._X, self._y)
        row = score_df[score_df["class"] == "avg"]
        logger.info(row)
        for col in score_df.columns:
            if col == "support":
                continue
            logs[f"val_{col}"] = row[col].values.tolist()[0]
