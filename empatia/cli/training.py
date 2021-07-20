import datetime as dt
import json

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from empatia.model.estimator import PM10Estimator
from empatia.model.utils import get_metrics, get_param_grid, search_best_model
from empatia.settings import MODEL_DATA_PATH, TRAINING_DATA_PATH
from empatia.settings.constants import (
    DEFAULT_DATE_FORMAT,
    DEFAULT_FREQ,
    FEATURES_COLS,
    TARGET_COL,
)
from empatia.settings.log import logger


def train() -> None:
    """
    Train PM10 model
    """
    metadata = {}
    today = dt.datetime.strftime(dt.datetime.today(), DEFAULT_DATE_FORMAT)
    model_path = MODEL_DATA_PATH / f"model_{today}.pkl"
    log_file = MODEL_DATA_PATH / f"model_metadata_{today}.txt"

    metadata["model_name"] = "PM10Estimator"
    metadata["model_path"] = str(model_path)

    df = pd.read_csv(TRAINING_DATA_PATH)
    df.dropna(how="any", inplace=True)
    data = df[df.AODnm == DEFAULT_FREQ]
    X_train, X_test, y_train, y_test = train_test_split(
        data[FEATURES_COLS], data[TARGET_COL], test_size=0.20, random_state=42
    )
    logger.info("Searching best model...")
    rf = search_best_model(X_train, y_train, PM10Estimator(), get_param_grid())

    metadata["training_metrics"] = get_metrics(
        np.array(y_train), rf.predict(X_train)
    )  # type: ignore
    metadata["test_metrics"] = get_metrics(
        np.array(y_test), rf.predict(X_test)
    )  # type: ignore
    metadata["model_params"] = rf.get_params()

    with open(log_file, "w") as outfile:
        json.dump(metadata, outfile, indent=4)

    rf.save_model(model_path)
    logger.info(f"Saved model: {model_path}")
