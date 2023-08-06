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

try:  # py38+
    from importlib.metadata import version as metadata_version
    from importlib.metadata import PackageNotFoundError
except ModuleNotFoundError:
    from importlib_metadata import version as metadata_version
    from importlib_metadata import PackageNotFoundError


def package_version(package_name, destination):
    """Returns the package version string

    Args:
        package_name (str): the package name to look up
        destination (list): the list to store the result (tuple) to

    """
    try:
        version = metadata_version(package_name)
    except PackageNotFoundError:
        version = "<unavailable>"

    if package_name == "pyzmq":
        from zmq import zmq_version

        version = "{} (libzmq version {})".format(
            version,
            zmq_version(),
        )

    destination.append((package_name, version))


# vim: set ts=4 sw=4 tw=72 expandtab:
