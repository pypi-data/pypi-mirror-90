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
from collections import namedtuple


def curve_opts_new(server_public_key_file, client_key_file):
    """Returns a namedtuple containing the curve options."""

    curve_opts = namedtuple(
        "curve_opts",
        "server_public_key_file, client_key_file",
    )

    return curve_opts(server_public_key_file, client_key_file)


def ssh_opts_new(
    ssh_server,
    ssh_key_file,
    ssh_password,
    ssh_timeout,
    ssh_paramiko,
):
    """Return a namedtuple containing the ssh options."""

    ssh_opts = namedtuple(
        "ssh_opts",
        "server, key_file, password, timeout, paramiko",
    )

    return ssh_opts(
        ssh_server,
        ssh_key_file,
        ssh_password,
        ssh_timeout,
        ssh_paramiko,
    )


def auth_opts_new(curve=None, ssh=None):
    """Return a namedtuple containing either curve or ssh options.

    You can use the `curve_opts_new` and `ssh_opts_new` functions with this
    function.

    Args:
        curve (obj): the namedtuple created with `curve_opts_new`
        ssh (obj): the namedtuple created with `ssh_opts_new`

    Notes:
        - You must set eithe curve(:arg:) or ssh(:arg:), not both or
          neither

    Raises:
        ValueError if any of the args are invalid

    Returns:
        obj: New namedtuple containing either curve or ssh options

    """
    if not curve and not ssh:
        raise ValueError("curve and ssh cannot both be None")

    elif curve and ssh:
        raise ValueError(
            "you can set only either curve or ssh, not both",
        )

    auth_opts = namedtuple("auth_opts", "curve, ssh")
    return auth_opts(curve, ssh)


# vim: set ts=4 sw=4 tw=72 expandtab:
