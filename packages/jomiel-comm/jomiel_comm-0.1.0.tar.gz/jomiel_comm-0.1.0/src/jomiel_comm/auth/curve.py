#
# jomiel-comm
#
# Copyright
#  2019 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""


def exit_error():
    """Wraps the sys.exit call, exits with an error code (1)."""
    from sys import exit as _exit

    _exit(1)


def load_cert_file(path, logger=None):
    """Loads a certificate file from the given location.

    Notes:

        - Exits with an error if zmq.auth.load_certificate raised an
          IOError (e.g. file not found)

    """
    from zmq.auth import load_certificate
    from os.path import abspath

    keyfile = abspath(path)

    try:
        return load_certificate(keyfile)
    except OSError as message:
        if logger:
            logger.error(message)
        exit_error()


def setup(socket, curve, logger=None):
    """Load the CURVE certificates required for a secure client connection.

    Args:
        socket (obj): the zmq socket to use

        curve (obj): the named tuple containing the curve options

        logger (obj): the logger instance to use (or None)

    Raises:
        ValueError if any of the required kwarg values were unacceptable

    Returns:
        Nothing

    """
    (pubkey, seckey) = load_cert_file(curve.client_key_file, logger)

    socket.curve_secretkey = seckey
    socket.curve_publickey = pubkey

    (pubkey, _) = load_cert_file(curve.server_public_key_file, logger)
    socket.curve_serverkey = pubkey


# vim: set ts=4 sw=4 tw=72 expandtab:
