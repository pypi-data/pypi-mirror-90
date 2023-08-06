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


def setup(socket, addr, ssh):
    """Tunnel zmq connection with SSH.

    Args:
        socket (obj): the zmq socket to use
        addr (string): connect to the address via ssh tunnel
        ssh (obj): the namedtuple containing the ssh options

    """
    from zmq.ssh import tunnel_connection

    tunnel_connection(
        socket,
        addr,
        ssh.server,
        keyfile=ssh.key_file,
        password=ssh.password,
        timeout=ssh.timeout,
        paramiko=ssh.paramiko,
    )


# vim: set ts=4 sw=4 tw=72 expandtab:
