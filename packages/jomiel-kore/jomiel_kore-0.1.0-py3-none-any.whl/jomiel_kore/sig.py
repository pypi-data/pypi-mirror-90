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
from signal import getsignal
from signal import signal
from signal import SIGTERM


class GracefulExit:
    """Wraps SIGTERM handling in a with-statement compatible use."""

    __slots__ = ["orig_sigterm", "logger"]

    def __init__(self, logger=None):
        """Initializes the object.

        Args:
            logger (obj): the logger function used to save new entries
                            Can also be None, if logging is not needed.

        """
        self.orig_sigterm, self.logger = (None, logger)

    def __enter__(self):
        """Traps the SIGTERM."""

        self.log("<sigterm> trap signal handler")
        self.orig_sigterm = getsignal(SIGTERM)

        def sigterm_handler(signo, frame):
            """Our SIGTERM handler.

            For lack of a better solution, it currently raises SIGINT
            which we can handle cleanly.

            """
            self.log("<sigterm> signo=%d, frame=%s" % (signo, frame))
            raise KeyboardInterrupt

        signal(SIGTERM, sigterm_handler)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Restore the the SIGTERM handler back to its original state."""
        self.log("<sigterm> restore system handler")
        signal(SIGTERM, self.orig_sigterm)

    def log(self, text):
        """Save a new entry to the logger.

        Args:
            text (string): Text to be saved

        """
        if self.logger:
            self.logger(text)


# vim: set ts=4 sw=4 tw=72 expandtab:
