from gustave.patchers.keras import patch_keras_models
from gustave.patchers.sklearn import patch_sklearn_estimators


def patch() -> None:
    patch_sklearn_estimators()
    patch_keras_models()
