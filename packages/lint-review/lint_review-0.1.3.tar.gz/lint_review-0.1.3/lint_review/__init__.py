# flake8: noqa
# type: ignore
try:
    from importlib import metadata
except ImportError:
    # Running on pre-3.8 Python; use importlib-metadata package
    import importlib_metadata as metadata
__version__ = metadata.version("lint_review")

from .__main__ import main
