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


def find_matching_files(find_filename, location=None):
    """Find all matching files (recursively) from the current working
    directory (default), or from the location specified.

    Args:
        find_filename (str): file name to look for (can be a mask)
        location (str): the location to search for matching files (None
            for cwd)

    Returns:
        list: of matching files

    """
    from os.path import join
    from glob import iglob
    from os import getcwd

    def match_files():
        pathname = join(location, "**", find_filename)
        result = []
        for filename in iglob(pathname, recursive=True):
            result.append(filename)
        return result

    location = location if location else getcwd()
    return match_files()


def put(msg):
    """Put a message to the stdout.

    Args:
        msg (str): the message to write

    """
    from sys import stdout

    stdout.write(msg)


def unlink_if(fpath, verbose=True):
    """Remove the specified file conditionally (exists).

    Args:
        fpath (str): the path to the file
        verbose (bool): If set to false, pipes down the chatter

    """
    from os.path import exists
    from os import unlink

    if exists(fpath):
        if verbose:
            put("Removing file %s\n" % fpath)
        unlink(fpath)


# vim: set ts=4 sw=4 tw=72 expandtab:
