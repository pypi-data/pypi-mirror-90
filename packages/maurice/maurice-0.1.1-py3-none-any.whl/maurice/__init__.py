from maurice.patchers.sklearn import patch_sklearn_estimators


def patch() -> None:
    patch_sklearn_estimators()
