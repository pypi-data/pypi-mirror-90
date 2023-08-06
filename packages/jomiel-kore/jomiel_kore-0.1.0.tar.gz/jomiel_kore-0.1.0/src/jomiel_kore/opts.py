#
# jomiel-kore
#
# Copyright
#  2019 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""


def check_if_positive_integer(argval):
    """Check that the given integer is a positive value."""
    from argparse import ArgumentTypeError

    try:
        value = int(argval)
    except ValueError:
        raise ArgumentTypeError(
            "invalid value type: %s (expected integer)" % argval,
        )
    if value < 1:
        raise ArgumentTypeError("the value must be a positive integer")
    return value


# vim: set ts=4 sw=4 tw=72 expandtab:
