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


def log_init(config_paths):
    """Initializes the logger.

    Reads the configuration from a (YAML) file.

    Args:
        config_paths: the list of configuration files (YAML) to read
            Stops at the first existing file.

    Returns:
        str, dict (tuple): the path to the read config file, the
            dictionary holding the identities parsed from the YAML file

    """
    from os.path import expanduser
    import logging.config as lc
    from glob import glob
    from ruamel.yaml import YAML

    # Try to find one of the specified logger config files and load it.
    for path in map(expanduser, config_paths):
        for found in glob(path):
            with open(found) as handle:
                yaml = YAML(typ="safe")
                data = yaml.load(handle)
                lc.dictConfig(data)
                return (found, data["loggers"])

    def set_fallback():
        """Set the fallback logger (if none the config files were found)."""
        from logging import basicConfig, INFO, info

        basicConfig(level=INFO, format="[%(levelname)s] %(message)s")

        info("unable to find %s", config_paths)
        info("using basic logging configuration instead")

        return ("<stdlib:basic>", [])

    return set_fallback()


if __name__ == "__main__":

    def parse_opts():
        """Parse options."""

        from configargparse import get_parser

        parser = get_parser(add_config_file_help=False)

        parser.add(
            "-f",
            "--logger-config",
            help="Logger configuration file to read",
            metavar="FILE",
            required=True,
        )

        parser.add(
            "-l",
            "--logger-ident",
            help="Specify the logger identity to use",
            choices=[
                "default",
                "debug",
                "stderr_file",
                "syslog",
                "file",
                "timed_file",
            ],
            metavar="IDENT",
            default="default",
        )

        return parser.parse()

    opts = parse_opts()
    log_init([opts.logger_config])

    def lg():
        """Return the logger."""
        import logging as lg

        return lg.getLogger(opts.logger_ident)

    lg().debug("Debug level message")
    lg().info("Info level message")

# vim: set ts=4 sw=4 tw=72 expandtab:
