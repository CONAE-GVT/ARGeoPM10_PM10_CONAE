import pickle
from typing import no_type_check

from sklearn.ensemble import RandomForestRegressor

from empatia.model.exceptions import LoadModelException


class PM10Estimator(RandomForestRegressor):
    def save_model(self, path: str) -> None:
        with open(path, "wb") as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

    @classmethod
    @no_type_check
    def load_model(cls, path: str) -> "PM10Estimator":
        with open(path, "rb") as f:
            model = pickle.load(f)  # nosec
        if model.__class__ != cls:
            raise LoadModelException(
                f"Object loaded is instance of {model.__class__}."
                f" Expected instance of {cls}"
            )
        return model
