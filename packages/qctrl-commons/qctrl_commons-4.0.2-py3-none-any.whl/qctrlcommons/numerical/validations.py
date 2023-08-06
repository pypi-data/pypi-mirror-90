# Copyright 2020 Q-CTRL Pty Ltd & Q-CTRL Inc. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#     https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.
"""Module for numeric validation."""
import logging
from typing import Optional

import numpy as np

from ..serializers import decode

LOGGER = logging.getLogger(__name__)

MAX_ARRAY_SIZE = 256
MAX_NUMERICAL_VALUE = 1e27
MIN_NUMERICAL_VALUE = 1e-27
MAX_SEGMENT_COUNT = 256
MIN_SEGMENT_COUNT = 1
MAX_CONTROLS = {"drive": 3, "shift": 3, "drift": 1}
MAX_NOISES = 2


def encoded_value_is_valid(value: Optional[dict]) -> bool:
    """Checks that the encoded value conforms to the limitations imposed by the
    numerical package.

    Parameters
    ----------
    value : Optional[dict]
        the encoded representation of an numpy array.


    Returns
    -------
    bool
        True if the validation succeeded, False otherwise.

    """
    if value is None:
        # None is allowed
        return True

    if not isinstance(value, (dict,)):
        LOGGER.error("The encoded value is not a dict, got %s", (type(value)))
        return False

    if "shape" not in value or "dtype" not in value:
        LOGGER.error(
            "The encoded value is not a valid complex array or number: %s", str(value)
        )
        return False

    try:
        decoded = decode(value)
    except ValueError as err:
        LOGGER.exception("An error has happened while decoding the value: %s", str(err))
        return False

    return is_valid_operator_value(decoded)


def is_valid_operator_value(decoded: np.ndarray) -> bool:
    """Performs standard checks on an operator matrix.

    Parameters
    ----------
    decoded : np.ndarray
        checks that the current numpy array conforms to the limits defined in the numerical package.

    Returns
    -------
    bool
        True if the validation succeeded, False otherwise.

    """
    if not isinstance(decoded, np.ndarray):
        LOGGER.error("The current value %s is not a valid" " numpy array", decoded)
        return False

    if hasattr(decoded, "shape") and decoded.shape:
        if decoded.shape[0] > MAX_ARRAY_SIZE or decoded.shape[1] > MAX_ARRAY_SIZE:
            LOGGER.error(
                "Allowed matrix dimensions up to (%d, %d)" ", got %s",
                MAX_ARRAY_SIZE,
                MAX_ARRAY_SIZE,
                decoded.shape,
            )
            return False

        if (decoded > MAX_NUMERICAL_VALUE).any():
            LOGGER.error(
                "Not all values of %d are less than %d", decoded, MAX_NUMERICAL_VALUE
            )
            return False

    return True


def is_hermitian(value: np.ndarray) -> bool:
    """Checks if the numpy array is an hermitian matrix.

    Parameters
    ----------
    value : np.ndarray
        the array we want to check.

    Returns
    -------
    bool
        True if the validation succeeded, False otherwise.

    """
    return np.all(np.isclose(value, value.T.conj()))


def is_not_hermitian(value: np.ndarray) -> bool:
    """

    Parameters
    ----------
    value : np.ndarray
        np.ndarray: the array we want to check.

    Returns
    -------
    bool
        True if the validation succeeded, False otherwise.

    """
    return not is_hermitian(value)


def is_unitary(value: np.ndarray) -> bool:
    """Checks if the array is unitary.

    Parameters
    ----------
    value : np.ndarray
        np.ndarray: the array we want to check.

    Returns
    -------
    bool
        True if the validation succeeded, False otherwise.

    """
    return np.allclose(value.dot(value.T.conj()), np.eye(value.shape[0]))
