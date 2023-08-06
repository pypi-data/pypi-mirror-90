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
from abc import ABCMeta
from abc import abstractmethod
from importlib import import_module
from sys import stdout

try:  # py37+
    from importlib.resources import path as resources_path
except ModuleNotFoundError:
    from importlib_resources import path as resources_path


class App(metaclass=ABCMeta):
    """A simple core class that wraps all-things-necessary to create
    command line interface application with very little effort."""

    __slots__ = [
        "_no_default_config_files",
        "_no_version_long_option",
        "_no_print_config_option",
        "_no_config_file_option",
        "_no_logger_options",
        "_config_module",
        "_logger_files",
        "_package_additional_search_paths",
        "_package_data_dir",
        "_package_name",
        "_version",
    ]

    def __init__(self, **kwargs):
        """Initializes the object.

        Args:
            **kwargs: arbitrary keyword args

        Supported arbitrary keyword args (kwargs):

            package_name (str): The package name to be used for
                package resource queries and building the XDG
                configuration file search paths.

                - The value will be used to determine the different XDG
                  configuration file paths

                - If None, the package resources queries will be skipped

                - If None, XDG configuration file path searches will be
                  skipped

                - Default search paths

                  - for application configuration files

                    /etc/xdg/{pkg_name}/{pkg_name}.yaml
                    ~/.config/{pkg_name}/{pkg_name}.yaml
                    ./{pkg_name}.yaml

                  - for logger configuration files

                    /etc/xdg/{pkg_name}/logger.yaml
                    ~/.config/{pkg_name}/logger.yaml
                    ./logger.yaml

                The value is typically set to __name__ by the caller.

            package_data_dir (str): The package data dir. This is
                package_name + package_data_dir. Be sure to set
                package_name, also.

            package_additional_search_paths (list): The _additional_
                package search paths to be added to the sys.path.

            config_module (str): Module path to the "configuration
                module" used throughout the application runtime
                life-cycle to access global _cached_ values.

            version (str): The program version string, or None.

            no_print_config_option (bool): If True, disable -D and -E
                options.

            no_default_config_files (bool): If True, skip the XDG paths
                in the configuration file search.

            no_version_long_option (bool): If True, disable
                --version-long option, altogether.

            no_config_file_option (bool): If True, disable the
                --config-file option.

            no_logger_options (bool): If True, disable all of the logger
                options (e.g. --logger-file, --logger-ident).

        """
        self._no_version_long_option = kwargs.get(
            "no_version_long_option",
            False,
        )
        self._no_print_config_option = kwargs.get(
            "no_print_config_option",
            False,
        )
        self._no_logger_options = kwargs.get("no_logger_options", False)
        self._config_module = kwargs.get("config_module")

        self._package_additional_search_paths = kwargs.get(
            "package_additional_search_paths",
        )
        self._package_data_dir = kwargs.get("package_data_dir")
        self._package_name = kwargs.get("package_name")

        self._no_default_config_files = kwargs.get(
            "no_default_config_files",
            False,
        )

        self._no_config_file_option = kwargs.get(
            "no_config_file_option",
            False,
        )

        def add_package_search_paths():
            """Append the additional package search paths to sys.path."""
            if self._package_additional_search_paths:
                from sys import path as sys_path

                for mod_path in self._package_additional_search_paths:
                    with resources_path(mod_path, "") as path:
                        sys_path.append(str(path))

        def determine_xdg_paths():
            """Return the XDG paths to configuration files."""

            pkg_name = self._package_name

            if not pkg_name or self._no_default_config_files:
                return ([], [])

            config_files = [
                "/etc/xdg/{0}/{0}.yaml".format(pkg_name),
                "~/.config/{0}/{0}.yaml".format(pkg_name),
                f"./{pkg_name}.yaml",
            ]

            logger_files = [
                f"/etc/xdg/{pkg_name}/logger.yaml",
                f"~/.config/{pkg_name}/logger.yaml",
                "./logger.yaml",
            ]

            if pkg_name:
                path_prefix = pkg_name

                if self._package_data_dir:
                    path_prefix = self._package_data_dir

                config_path = f"{path_prefix}.config.logger"
                config_fname = f"{pkg_name}.yaml"

                try:
                    with resources_path(config_path, config_fname) as p:
                        logger_files.insert(0, p)
                except FileNotFoundError:
                    pass

            return (config_files, logger_files)

        add_package_search_paths()

        (config_files, self._logger_files) = determine_xdg_paths()
        self._version = kwargs.get("version", "?")

        from configargparse import get_parser

        parser = get_parser(
            default_config_files=config_files,
            add_config_file_help=False,
        )

        parser.add(
            "--version",
            action="version",
            version="%(prog)s version " + self._version,
        )

        if not self._no_version_long_option:
            parser.add(
                "-v",
                "--version-long",
                help="""show version information about program's
                        environment and exit""",
                action="store_true",
            )

        if not self._no_config_file_option:
            parser.add(
                "--config-file",
                help="Read configuration from the specified file",
                is_config_file=True,
                metavar="FILE",
            )

        if not self._no_print_config_option:
            parser.add(
                "-D",
                "--print-config",
                help="Show the configuration values and exit",
                action="store_true",
            )

            parser.add(
                "-E",
                "--report-config",
                help="Report keys, values and where they were set",
                action="store_true",
            )

        def logger_group():
            """Add the logger option group."""
            grp = parser.add_argument_group("logger")

            grp.add(
                "--logger-config",
                help="Logger configuration file to read",
                metavar="FILE",
            )

            grp.add(
                "-L",
                "--logger-idents",
                help="Print logger identities and exit",
                action="store_true",
            )

            grp.add(
                "--logger-idents-verbose",
                help="Print logger identities in detail, "
                "use together with --logger-idents",
                action="store_true",
            )

            grp.add(
                "-l",
                "--logger-ident",
                help="Use the logger identity",
                metavar="IDENT",
                default="default",
            )

        if not self._no_logger_options:
            logger_group()

    @abstractmethod
    def run(self):
        """[Override] Runs the program."""

    def parse_opts(self, parser):
        """Parses the options.

        Notes:
            - Handles the -D and -E options gracefully

            - Applications subclassing this class, do not need to
              implement the support

            - Instead, the these are either disabled by the subclass or
              handled automagically by the superclass

        Args:
            parser (obj): configargparse parser instance

        """

        def handle_print_config():
            """Handle the -D and -E options."""

            if self._no_print_config_option:
                return

            def print_config_values(opts):
                """Prints the configuration values to stdout and
                terminate the program.

                Args:
                    opts (dict): configargparse returned options

                """
                data = {
                    "configuration": opts.__dict__,
                }
                dump_as_yaml(data)

            def print_report_config(parser):
                """Prints the configuration sources to stdout and
                terminates the program.

                Args:
                    parser (obj): configargparse parser instance

                """
                parser.print_values()
                exit_normal()

            if opts.print_config:
                print_config_values(opts)

            elif opts.report_config:
                print_report_config(parser)

        def handle_version_long():
            """Handle --version-long"""

            if self._no_version_long_option or not opts.version_long:
                return

            def version_long():
                """Return string to be printed with --version-long"""

                def package_versions():
                    """Return the package versions."""
                    from .version import package_version

                    required_packages = self.version_long_packages()
                    found_packages = []

                    for package_name in sorted(required_packages):
                        package_version(
                            package_name,
                            found_packages,
                        )

                    return [
                        {key: value} for key, value in found_packages
                    ]

                from sys import version as py_version

                return {
                    "version": self._version,
                    "python": {
                        "version": py_version.replace("\n", ""),
                        "packages": package_versions(),
                    },
                }

            yaml = version_long()
            dump_as_yaml(yaml)

        def setup_global_config():
            """Sets up the global config module with the parsed options."""

            if not self._config_module:
                return

            mod = import_module(self._config_module)

            if not self._no_logger_options:
                if opts.logger_config:
                    self._logger_files.insert(0, opts.logger_config)
                mod.logger_paths = self._logger_files

            mod.opts = opts

        opts = parser.parse()

        handle_print_config()
        handle_version_long()

        setup_global_config()

        return opts

    def version_long_packages(self):
        """[Override] Returns the required packages that we wish to check
        with --version-long and append to the output.

        Note:
            - Override this in your applications

        Returns:
            list: of package names (empty)

            Example:
                return ['requests', 'yaml', 'pyzmq']

        """
        return []


def subprocess_open(args):
    """Execute subprocess by using Popen."""
    from subprocess import Popen, PIPE

    chld = Popen(args, stdout=PIPE)
    data = chld.communicate()[0]
    return (chld.returncode, data.rstrip().decode("utf8"))


def exit_with(code):
    """Calls sys.exit with the exit status code."""
    from sys import exit as _exit

    _exit(code)


def exit_error():
    """Wraps the sys.exit call, exits with an error status code (1)."""
    exit_with(1)


def exit_normal():
    """Wraps the sys.exit call, exits with an OK status code (0)."""
    exit_with(0)


def round_trip_dump_yaml(data, stream=None):
    """Dump YAML.

    Args:
        data (dict): to be dumped as YAML
        stream (obj): to dump the YAML to

    """
    from ruamel.yaml import YAML, round_trip_dump

    yaml = YAML(typ="safe")
    yaml.default_flow_style = False
    round_trip_dump(data, stream)


def dump_as_yaml(yaml):
    """Dump the given data as YAML to stdout and exit process.

    Args:
        yaml (dict): data to be dumped

    """
    stdout.write("---\n")
    round_trip_dump_yaml(yaml, stdout)
    exit_normal()


def dump_logger_identities(loggers, detailed=False):
    """Dump the found logger identities to the stdout and exit.

    Args:
        loggers (dict): from the parsed .yaml to be dumped
        detailed (bool): be detailed

    """
    idents = loggers if detailed else [ident for ident in loggers]
    yaml = {"identities": idents}
    dump_as_yaml(yaml)


# vim: set ts=4 sw=4 tw=72 expandtab:
