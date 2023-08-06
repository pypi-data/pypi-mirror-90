#
# jomiel-comm
#
# Copyright
#  2019-2021 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""


class InquireError(Exception):
    """Failed to communicate with jomiel."""

    __slots__ = []


def connect(addr, no_linger=True, auth=None, logger=None):
    """Creates the connection socket and connects to jomiel.

    Args:
        addr (string): The endpoint address to connect to

        no_linger (bool): If True, sets the socket option LINGER to 0
            (disable). The default is True.

        auth (obj): The authentication options (if any). Use the
            curve_opts_new, ssh_opts_new and auth_opts_new functions from
            .auth

        logger (obj): The logger to use (if any)

    Returns:
        obj: the created socket

    TODO:
        - Depending on the --auth-mode value, apply whatever
            needs to be applied to establish the connection

    """
    from zmq import Context, REQ, LINGER

    ctx = Context.instance()
    sck = ctx.socket(REQ)
    skip_connect = False

    if auth:
        if auth.curve:
            # Setup CURVE
            from .auth.curve import setup

            setup(sck, auth.curve, logger=logger)
        elif auth.ssh:
            # Setup SSH
            from .auth.ssh import setup

            setup(sck, addr, auth.ssh)
            skip_connect = True

    if not skip_connect:
        sck.connect(addr)

    if no_linger:
        sck.setsockopt(LINGER, 0)

    return sck


def inquire(socket, input_uri, timeout=60):
    """Sends a new metadata inquiry message and awaits for a
    response.

    Exits if the connection attempt timeouts.

    Args:
        socket (obj): the connection socket to us

        input_uri (string): the input URI to inquire the metadata for

        timeout (int): Maximum time in seconds that the program should
            allow the connection to the service to take. Default is 60.

    Raises:
        InquireError if jomiel returned an error

    """

    def inquiry_new():
        """Create a new media inquiry message."""
        from jomiel_messages.protobuf.v1beta1.message_pb2 import (
            Inquiry,
        )

        inquiry = Inquiry()
        inquiry.media.input_uri = input_uri
        return Inquiry.SerializeToString(inquiry)

    def receive_response():
        """Receive a response message from jomiel.

        Returns:
            obj: The response message

        """
        from jomiel_messages.protobuf.v1beta1.message_pb2 import (
            Response,
        )
        from jomiel_messages.protobuf.v1beta1.status_pb2 import (
            STATUS_CODE_OK,
        )

        data = socket.recv()
        resp = Response()
        resp.ParseFromString(data)

        if resp.status.code != STATUS_CODE_OK:
            raise InquireError(
                "%s (status=%d, error=%d, http=%d)"
                % (
                    resp.status.message,
                    resp.status.code,
                    resp.status.error,
                    resp.status.http.code,
                ),
            )

        return resp

    inquiry = inquiry_new()
    socket.send(inquiry)

    from zmq import Poller, POLLIN

    poller = Poller()
    poller.register(socket, POLLIN)

    connect_timeout = int(timeout) * 1000  # to msec

    if poller.poll(connect_timeout):
        return receive_response()
    raise OSError("connection timed out")


# vim: set ts=4 sw=4 tw=72 expandtab:
