---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.8.0
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Exploratory analysis and Baseline modeling

<!-- #region -->
## Summary

The aim is to evaluate a **RandomForestRegressor** like a baseline model to estimate PM10.
The following experiments are executed:
  * **Experiment 1:** Use all available data to train and evaluate a model
  * **Experiment 2:** Cross validation between stations
  * **Experiment 3:** Compare models by sensor frequency
  * **Experiment 4:** Compare models by satelite and frequency

Also, other models are evaluated to compare against **RandomForestRegressor**:
  * **KNRegressor**
  * **MLPRegressor**
  * **Linear SVR**
  * **XGBRegressor**
  
  
**Hypothesis**
  1. RandomForestRegressor is a good baseline model
  2. There is another model tath beats RandomForestRegressor
  
**Notes:**

The dataset can be downloaded [here](https://drive.google.com/file/d/1W3JmH32LGJti1jg6Zhq-DQZds21NTREM/view?usp=sharing)
<!-- #endregion -->

## Experiment

```python
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.core.display import HTML
from matplotlib import rcParams
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from typing import Any, Callable, Dict, Iterable, List

rcParams['figure.figsize'] = 12, 8
sns.set_theme()
```

```python
DATA_PATH = "Tabla_Entrenamiento_MAIAC_MERRA_VIIRS_DEM_PM.csv"
TARGET_COL = "PM10_valor"
FEATURES_COLS = [
    'valor_AOD', 'DEM_asnm', 'VIIRS_night_lights', 'ALBEDO', 'BCCMASS', 'CLDHGH', 
    'CLDLOW', 'DMSSMASS', 'DUSMASS', 'OCSMASS', 'PBLH', 'PRECTOT','PS', 'RH', 
    'SO2SMASS', 'SO4SMASS', 'SPEED', 'SPEEDMAX','SSSMASS', 'T', 'U', 'USTAR', 'V'
]
```

```python
def summary(df: pd.DataFrame, n_sample: int=5) -> None:
    """
    Show brief summary for a given Dataframe
    Args:
        df: Dataframe
        n_sample: number of sample to display
    """
    rows, columns = df.shape
    display(HTML(f'<b>Nº Rows:</b> {rows}'))
    display(HTML(f'<b>Nº Columns:</b> {columns}'))
    display(HTML(f'<b>Sample:</b>'))
    display(df.sample(n_sample))
    

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



def search_best_model(X: np.array, y:np.array, model: Any, param_grid: Dict) -> Any:
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
                n_iter = 100,
                cv = 3,
                verbose=2,
                random_state=42,
                n_jobs = -1
            )
    
    rs.fit(X, y)
    
    return rs
```

### Load data

```python
df = pd.read_csv(DATA_PATH)
summary(df)
```

### Remove NA values from target column

```python
df.dropna(subset=[TARGET_COL], inplace=True)
summary(df)
```

### Remove NA values from feature columns

```python
df.dropna(how='any', inplace=True)
summary(df)
```

### Get some distributions


#### Features

```python
df[FEATURES_COLS].describe()
```

#### Target (PM10)

```python
df[TARGET_COL].describe()
```

```python
sns.displot(df, x=TARGET_COL)
```

#### PM10 distribution by signal frequency

```python
df.groupby("AODnm")[TARGET_COL].describe()
```

#### PM10 distribution by sensor and signal frequency

```python
df.groupby(["AODnm", "Satelite"])[TARGET_COL].describe()
```

#### PM10 distribution by monitoring station

```python
df.groupby(["estacion_pm"])[TARGET_COL].describe()
```

### Random Forest


### Experiment 1:  Use all data


#### Split dataset

```python
X_train, X_test, y_train, y_test = train_test_split(df[FEATURES_COLS], df[TARGET_COL], test_size = 0.20, random_state = 42)
```

#### Set param grid

```python
# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start=200, stop=2000, num=10)]

# Number of features to consider at every split
max_features = ['auto', 'sqrt']

# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)

# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10]

# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 4]

# Method of selecting samples for training each tree
bootstrap = [True, False]

rf_param_grid =  {
    'n_estimators': n_estimators,
    'max_features': max_features,
    'max_depth': max_depth,
    'min_samples_split': min_samples_split,
    'min_samples_leaf': min_samples_leaf,
    'bootstrap': bootstrap
}
```

#### Model training

```python
# Get best params
display(HTML(f'<b>Randomized Search CV:</b>'))
rf =  RandomForestRegressor()
rf_random = search_best_model(X_train, y_train, rf, rf_param_grid)

display(HTML(f'<b>Best params:</b>'))
print(rf_random.best_params_)
```

```python
# Training RF estimator with the best parameters to get feature importances
rf.set_params(**rf_random.best_params_)
rf.fit(X_train, y_train)
```

#### Model evaluation

```python
# Training metrics
display(HTML(f'<b>Training metrics:</b>'))
print(get_metrics(np.array(y_train), rf.predict(X_train)))

# Test metrics
display(HTML(f'<b>Evaluation metrics:</b>'))
print(get_metrics(np.array(y_test), rf.predict(X_test)))
```

#### Observations

```python
ax = sns.scatterplot(x=y_test, y=rf.predict(X_test))
ax = ax.set(xlabel = "PM10", ylabel="Prediction")
```

```python
# Get feature importances
feature_importances = list(zip(FEATURES_COLS, np.round(rf.feature_importances_, 2)))
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)

_ = [print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances]
```

```python

```

### Experiment 2: Cross validation between stations

```python
station_metrics = {'train':{}, 'test':{}}
for station in pd.unique(df.estacion_pm):
    display(HTML(f'<b>Station to evaluate:</b> {station}'))
    mask = df.estacion_pm == station
    X_train = df[~mask][FEATURES_COLS]
    y_train = df[~mask][TARGET_COL]
    X_test = df[mask][FEATURES_COLS]
    y_test = df[mask][TARGET_COL]
    
    
    # Get best params
    display(HTML(f'<b>Randomized Search CV:</b>'))
    rf = search_best_model(X_train, y_train, RandomForestRegressor(), rf_param_grid)
    
    display(HTML(f'<b>Best params:</b>'))
    print(rf.best_params_)
    
    # Training metrics
    station_metrics['train'][station] = get_metrics(np.array(y_train), rf.predict(X_train))

    # Test metrics
    station_metrics['test'][station] = get_metrics(np.array(y_test), rf.predict(X_test))

```

```python
display(HTML(f'<b>Training metrics:</b>'))
display(pd.DataFrame(station_metrics['train']))
display(HTML(f'<b>Test metrics:</b>'))
display(pd.DataFrame(station_metrics['test']))
```

```python

```

### Experiment 3: Compare models by sensor frequency

```python
freq_metrics = {'train':{}, 'test':{}}
for freq in pd.unique(df.AODnm):
    display(HTML(f'<b>Frequency to evaluate:</b> {freq}'))
    freq_df = df[df.AODnm == freq]
    X_train, X_test, y_train, y_test = train_test_split(
                                                        freq_df[FEATURES_COLS],
                                                        freq_df[TARGET_COL],
                                                        test_size = 0.20,
                                                        random_state = 42
                                                    )
    
    # Get best params
    display(HTML(f'<b>Randomized Search CV:</b>'))
    rf = search_best_model(X_train, y_train, RandomForestRegressor(), rf_param_grid)
    
    display(HTML(f'<b>Best params:</b>'))
    print(rf.best_params_)
    
    # Training metrics
    freq_metrics['train'][freq] = get_metrics(np.array(y_train), rf.predict(X_train))

    # Test metrics
    freq_metrics['test'][freq] = get_metrics(np.array(y_test), rf.predict(X_test))
```

```python
display(HTML(f'<b>Training metrics:</b>'))
display(pd.DataFrame(freq_metrics['train']))
display(HTML(f'<b>Test metrics:</b>'))
display(pd.DataFrame(freq_metrics['test']))
```

```python

```

### Experiment 4: Compare models by satelite and frequency

```python
sat_freq_metrics = {'train':{}, 'test':{}}
for name, group  in df.groupby(["AODnm", "Satelite"]):
    freq, sat = name
    display(HTML(f'<b>Frequency to evaluate:</b> {freq}'))
    display(HTML(f'<b>Satelite to evaluate:</b> {sat}'))
    X_train, X_test, y_train, y_test = train_test_split(
                                                        group[FEATURES_COLS],
                                                        group[TARGET_COL],
                                                        test_size = 0.20,
                                                        random_state = 42
                                                    )
    
    # Get best params
    display(HTML(f'<b>Randomized Search CV:</b>'))
    rf = search_best_model(X_train, y_train, RandomForestRegressor(), rf_param_grid)
    
    display(HTML(f'<b>Best params:</b>'))
    print(rf.best_params_)
    
    
    # Training metrics
    sat_freq_metrics['train'][f'{sat}_{freq}'] = get_metrics(np.array(y_train), rf.predict(X_train))

    # Test metrics
    sat_freq_metrics['test'][f'{sat}_{freq}'] = get_metrics(np.array(y_test), rf.predict(X_test))
```

```python
display(HTML(f'<b>Training metrics:</b>'))
display(pd.DataFrame(sat_freq_metrics['train']))
display(HTML(f'<b>Test metrics:</b>'))
display(pd.DataFrame(sat_freq_metrics['test']))
```

```python

```

### Other models using all data


#### Split Data

```python
X_train, X_test, y_train, y_test = train_test_split(df[FEATURES_COLS], df[TARGET_COL], test_size = 0.20, random_state = 42)
```

#### KNRegressor

```python
from sklearn.neighbors import KNeighborsRegressor


kn_param_grid = {
    'n_neighbors': [5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    'weights': ['uniform', 'distance'],
    'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
    'leaf_size': [30, 40, 50],
    'p': [1,2]
    
}

# Get best params
display(HTML(f'<b>Randomized Search CV:</b>'))
kn = search_best_model(X_train, y_train, KNeighborsRegressor(), knn_param_grid)

display(HTML(f'<b>Best params:</b>'))
print(knn.best_params_)


# Get metrics
display(HTML(f'<b>Training metrics:</b>'))
print(get_metrics(np.array(y_train), kn.predict(X_train)))

display(HTML(f'<b>Test metrics:</b>'))
print(get_metrics(np.array(y_test), kn.predict(X_test)))
```

#### Linear Support Vector Regression

```python
from sklearn.svm import LinearSVR

svr_param_grid = {
    'loss': ['epsilon_insensitive', 'squared_epsilon_insensitive'] ,
    'fit_intercept': [True, False],
    'dual': [True, False],
}


svr = search_best_model(X_train, y_train, LinearSVR(), svr_param_grid)

display(HTML(f'<b>Best params:</b>'))
print(svr.best_params_)


# Get metrics
display(HTML(f'<b>Training metrics:</b>'))
print(get_metrics(np.array(y_train), svr.predict(X_train)))

display(HTML(f'<b>Test metrics:</b>'))
print(get_metrics(np.array(y_test), svr.predict(X_test)))
```

#### MLP Regressor

```python
from sklearn.neural_network import MLPRegressor


mlp_param_grid = {
    'hidden_layer_sizes': [(8, 8, 64), (16, 16, 128), (32, 32, 256), (64, 64, 512)] ,
    'activation': ['identity', 'logistic', 'tanh', 'relu'],
    'solver': ['lbfgs', 'adam'],
    'learning_rate': ['constant', 'invscaling', 'adaptive'],
    'alpha': [0.0001, 0.05],
    'max_iter': [1000],
}


nn = search_best_model(X_train, y_train, MLPRegressor(), mlp_param_grid)

display(HTML(f'<b>Best params:</b>'))
print(nn.best_params_)


# Get metrics
display(HTML(f'<b>Training metrics:</b>'))
print(get_metrics(np.array(y_train), nn.predict(X_train)))

display(HTML(f'<b>Test metrics:</b>'))
print(get_metrics(np.array(y_test), nn.predict(X_test)))
```

#### XGBRegressor

```python
from xgboost import XGBRegressor

xgb_param_grid = {
    'n_estimators': [5, 10, 50, 100, 300, 1000] ,
    'max_depth': [5, 10, 20, 50, 70, 100],
    'objective': ['reg:linear'],
    'booster': ['gbtree', 'gblinear', 'dart']
}


xgb = search_best_model(X_train, y_train, XGBRegressor(), xgb_param_grid)

display(HTML(f'<b>Best params:</b>'))
print(xgb.best_params_)


# Get metrics
display(HTML(f'<b>Training metrics:</b>'))
print(get_metrics(np.array(y_train), xgb.predict(X_train)))

display(HTML(f'<b>Test metrics:</b>'))
print(get_metrics(np.array(y_test), xgb.predict(X_test)))
```

```python
ax = sns.scatterplot(x=y_test, y=xgb.predict(X_test))
ax = ax.set(xlabel = "PM10", ylabel="Prediction")
```

```python

```

## Conclusions

* **RandomForestRegressor** is a good baseline model to estimate PM10
* **XGBRegressor** is the best approach outperforming Random Forest Regressor by ~ 1 percentage point, 94.84% and 93.62% accuracy respectively
