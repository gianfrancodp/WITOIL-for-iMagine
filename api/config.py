"""Module to define CONSTANTS used across the DEEPaaS Interface.

This module is used to define CONSTANTS used across the API interface.
Do not misuse this module to define variables that are not CONSTANTS or
that are not used across the `api` package. You can use the `config.py`
file on your model package to define CONSTANTS related to your model.

By convention, the CONSTANTS defined in this module are in UPPER_CASE.
"""

import logging
import os
from importlib import metadata
from pathlib import Path

# Ensure that your model package has a config.py file with the following
# pylint: disable=unused-import
# from witoil_for_imagine.config import DATA_PATH, MODELS_PATH

# DEEPaaS can load more than one installed models. Therefore, to
# avoid conflicts, each default PATH environment variables should lead to
# a different folder. The current practice is to use the path from where the
# model source is located.
BASE_PATH = Path(__file__).resolve(strict=True).parents[1]

# Get AI model metadata
API_NAME = "witoil_for_imagine"
API_METADATA = metadata.metadata(API_NAME)  # .json

# Fix metadata for emails from pyproject parsing
_EMAILS = API_METADATA["Author-email"].split(", ")
_EMAILS = map(lambda s: s[:-1].split(" <"), _EMAILS)
API_METADATA["Author-emails"] = dict(_EMAILS)

# Fix metadata for authors from pyproject parsing
_AUTHORS = API_METADATA.get("Author", "").split(", ")
_AUTHORS = [] if _AUTHORS == [""] else _AUTHORS
_AUTHORS += API_METADATA["Author-emails"].keys()
API_METADATA["Authors"] = sorted(_AUTHORS)

# logging level across API modules can be setup via API_LOG_LEVEL,
# options: DEBUG, INFO(default), WARNING, ERROR, CRITICAL
ENV_LOG_LEVEL = os.getenv("API_LOG_LEVEL", default="INFO")
LOG_LEVEL = getattr(logging, ENV_LOG_LEVEL.upper())
