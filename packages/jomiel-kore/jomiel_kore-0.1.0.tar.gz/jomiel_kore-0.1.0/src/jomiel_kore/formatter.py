#
# jomiel-kore
#
# Copyright
#  2019-2020 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""
from ujson import dumps


def json_pprint_formatter(json_object, indent=2, ensure_ascii=False):
    """Return the pretty representation of the given json object.

    This is a convenience "wrapper" function for printing json objects
    in a human-readable representation.

    Args:
        json_object (obj): the json object to use

        indent (int): the used indentation

        ensure_ascii (bool): if True, limits output to ASCII and escapes
            all extended characters above 127 (https://git.io/Jfh2q)

    Returns:
        the human-readable representation of the json object

    """
    return dumps(
        json_object,
        ensure_ascii=ensure_ascii,
        sort_keys=True,
        indent=indent,
    )


def json_pprint(json_object):
    """Pretty print the given json object to the stdout.

    Args:
        json_object: the json object to use

    Returns:

    """
    json_str = json_pprint_formatter(json_object)
    print(json_str)


# vim: set ts=4 sw=4 tw=72 expandtab:
