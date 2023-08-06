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
import logging as lgg


def read_input(**kwargs):
    """Reads input from, either, the command line (nargs returned by
    configargparse) or directly from stdin. The input is parsed for URIs
    -- and if requested, made sure that they are of proper standard.

    Defaults to stdin (if argv is empty or undefined).

    Ignores the comments, for example:

        # A comment line.
        https://foo     # Also ignored.

    Args:
        **kwargs: arbitrary keyword args

    Supported arbitrary keyword args (kwargs):

        nargs (list): As returned by ConfigArgParse, if none is given,
               the input is read from the stdin, instead

        validate_uri (bool): If True, validates that each item is an URI
            Default is False.

        rebuild_uri (bool): If True (default), each item is rebuilt as an URI.
            Useful if you want to make sure that the URIs look
            representable, fixes various URI string presentation issues
            (e.g. 'HtTpS' -> 'https').

            Ignored, unless used together with validate_uri. Default is
            True.

        components_only (bool): If True, each item is returned as a
            list of broken down URI components.

            Also, when True, forces validate_uri (True) and rebuild_uri
            (False). Default is False.

        unique_items_only (bool): If True (default), returns only the
            unique items. Default is True.

    Raises:
        ValueError if validation is enabled and fails (e.g. the input
        contains entries that do not appear to be HTTP URIs)

    Returns:
        list: Parsed values

    """
    unique_items_only = kwargs.get("unique_items_only", True)
    components_only = kwargs.get("components_only", False)
    validate_uri = kwargs.get("validate_uri", False)
    rebuild_uri = kwargs.get("rebuild_uri", True)
    nargs = kwargs.get("nargs")

    rebuild_uri = False if components_only else rebuild_uri
    validate_uri = True if components_only else validate_uri

    if validate_uri:
        # lgg.debug('validate input URIs')
        from urllib.parse import urlparse, urlunparse

    def parse():
        """Parse input for URIs."""

        def add(value):
            """Append a new value to the results."""

            # lgg.debug('input item <%s>' % value)

            if validate_uri:

                uri_components = urlparse(value)
                sch = uri_components.scheme

                if not sch.startswith("http"):
                    raise ValueError("%s: not a valid URI" % value)

                if rebuild_uri:
                    value = urlunparse(uri_components)

                if components_only:
                    value = uri_components

            result.append(value)

        result = []
        if nargs:
            # lgg.debug('parse from nargs')
            for narg in nargs:
                add(narg)
        else:
            # lgg.debug('parse from stdin')
            def read_stdin():
                """Read from stdin."""
                from sys import stdin

                while True:
                    line = stdin.readline().strip()
                    if not line:
                        break
                    line = line.split("#", 1)[0].strip()
                    if line:
                        add(line)

            read_stdin()
        return result

    result = parse()
    if unique_items_only:
        # lgg.debug('return unique items only')
        def unique_items(seq):  # https://stackoverflow.com/a/480227
            """Return unique items in the results, only."""
            seen = set()
            seen_add = seen.add
            return [s for s in seq if not (s in seen or seen_add(s))]

        return unique_items(result)
    return result


if __name__ == "__main__":

    def parse_opts():
        """Parse options."""

        from configargparse import get_parser

        parser = get_parser(add_config_file_help=False)

        parser.add(
            "-b",
            "--verbose",
            help="Enable DEBUG logging level",
            action="store_true",
        )

        parser.add(
            "-v",
            "--validate-uri",
            help="Validate each item as an URI",
            action="store_true",
        )

        parser.add(
            "-u",
            "--unique-items-only",
            help="Return unique items only",
            action="store_true",
        )

        parser.add(
            "-c",
            "--components-only",
            help="Return items as broken down components",
            action="store_true",
        )

        parser.add(
            "-r",
            "--rebuild_uri",
            help="Rebuild items as URIs",
            action="store_true",
        )

        parser.add("uri", nargs="*")
        return parser.parse()

    opts = parse_opts()

    def enable_debug():
        """Enable verbose logging."""
        level = lgg.DEBUG if opts.verbose else lgg.INFO
        lgg.basicConfig(
            level=level,
            format="[%(levelname)s] %(message)s",
        )

    enable_debug()

    try:
        items = read_input(
            unique_items_only=opts.unique_items_only,
            components_only=opts.components_only,
            validate_uri=opts.validate_uri,
            rebuild_uri=opts.rebuild_uri,
            nargs=opts.uri,
        )
        for item in items:
            lgg.info(item)
        lgg.info("total items %d", len(items))
    except ValueError as error:
        lgg.error(error)

# vim: set ts=4 sw=4 tw=72 expandtab:
