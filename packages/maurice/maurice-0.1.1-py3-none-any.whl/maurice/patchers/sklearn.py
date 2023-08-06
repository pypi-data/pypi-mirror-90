import logging
from types import MethodType

import dill
import wrapt
from joblib import hashing
from sklearn.base import BaseEstimator
from sklearn.utils import all_estimators

from maurice.core import CACHE_DIR

logger = logging.getLogger(__name__)


def cached_fit(wrapped: MethodType, instance: BaseEstimator, args, kwargs) -> BaseEstimator:
    path_to_cache = CACHE_DIR.joinpath(
        # path to module
        *type(instance).__module__.split("."),
        # class name
        type(instance).__name__,
        # instance state hash
        hashing.hash(instance.__getstate__()),
        # instance method name
        wrapped.__name__,
        # args and kwargs hash
        hashing.hash("".join(map(hashing.hash, (args, kwargs)))),
        # file name
        "cache.dill",
    )

    if not path_to_cache.exists():
        result = wrapped(*args, **kwargs)
        logger.info(f"Saving cached state to: {path_to_cache}")
        path_to_cache.parent.mkdir(parents=True, exist_ok=False)
        path_to_cache.write_bytes(dill.dumps(result.__getstate__()))
        return result
    else:
        logger.info(f"Loading cached state from: {path_to_cache}")
        instance.__setstate__(state=dill.loads(path_to_cache.read_bytes()))
        return instance


def patch_sklearn_estimators() -> None:
    for estimator in tuple(zip(*all_estimators()))[1]:
        wrapt.wrap_function_wrapper(estimator.__module__, f"{estimator.__name__}.fit", cached_fit)
