from typing import Any, Dict

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import RandomizedSearchCV


def get_metrics(forecast: np.array, ground_truth: np.array) -> Dict:
    """
    Calculate a set of metrics to measure the performance of the forecasting model
    Args:
        forecast: list of forecasted values
        ground_truth: list of real values
    Return:
        Dictionary of the main forcasting metrics
    """
    # Mean Absolute Percentage Error
    mape = np.mean(np.abs(forecast - ground_truth) / ground_truth)
    # Mean Absolute Error
    mae = mean_absolute_error(forecast, ground_truth)
    # Root Mean Square Error
    rmse = np.sqrt(mean_squared_error(forecast, ground_truth))
    # Mean Shortage Error
    mshe = np.nanmean(
        np.where(forecast < ground_truth, np.abs(forecast - ground_truth), np.nan)
    )
    # Mean Surplus Error
    msue = np.nanmean(
        np.where(forecast > ground_truth, np.abs(forecast - ground_truth), np.nan)
    )

    accuracy = None
    if mape <= 1:
        accuracy = (1 - mape) * 100

    return {
        "mape": mape,
        "accuracy": accuracy,
        "mae": mae,
        "mshe": mshe,
        "msue": msue,
        "rmse": rmse,
        "n_sample": len(ground_truth),
    }


def search_best_model(X: np.array, y: np.array, model: Any, param_grid: Dict) -> Any:
    """
    Randomized search on hyperparameters to get the best model

    Args:
        X: dataset to train
        y: targets to train
        model: model instance to fit
        param_grid: set of parameter to try
    Return:
        The best model fitted
    """
    # Random search of parameters, using 3 fold cross validation,
    # search across 100 different combinations, and use all available cores
    rs = RandomizedSearchCV(
        estimator=model,
        param_distributions=param_grid,
        n_iter=100,
        cv=3,
        verbose=2,
        random_state=42,
        n_jobs=-1,
    )

    rs.fit(X, y)

    return rs.best_estimator_


def get_param_grid() -> Dict:
    """
    Get hyperparameters grid
    """
    # Number of trees in random forest
    n_estimators = [int(x) for x in np.linspace(start=200, stop=2000, num=10)]
    # Number of features to consider at every split
    max_features = ["auto", "sqrt"]
    # Maximum number of levels in tree
    max_depth = [int(x) for x in np.linspace(10, 110, num=11)]
    max_depth.append(None)  # type: ignore
    # Minimum number of samples required to split a node
    min_samples_split = [2, 5, 10]
    # Minimum number of samples required at each leaf node
    min_samples_leaf = [1, 2, 4]
    # Method of selecting samples for training each tree
    bootstrap = [True, False]
    rf_param_grid = {
        "n_estimators": n_estimators,
        "max_features": max_features,
        "max_depth": max_depth,
        "min_samples_split": min_samples_split,
        "min_samples_leaf": min_samples_leaf,
        "bootstrap": bootstrap,
    }

    return rf_param_grid
