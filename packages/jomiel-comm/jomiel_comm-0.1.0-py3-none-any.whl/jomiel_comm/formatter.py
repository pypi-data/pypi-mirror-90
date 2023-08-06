#
# jomiel-comm
#
# Copyright
#  2019-2020 Toni Gündoğdu
#
#
# SPDX-License-Identifier: Apache-2.0
#
"""TODO."""


def to_json(message, minified=False, stream=None, **kwargs):
    """Returns the JSON of the given protobuf message.

    Args:
        Message (obj): The protobuf message to be converted

        minified (bool): If True, the resulting JSON will be minified,
            otherwise (default) a human-readable representation is
            returned.

        stream (obj): Unless None, write the json to stream

        **kwargs (list): arbitrary keyword args (to be passed as such to
            ujson.dumps)

    Supported arbitrary keyword args (kwargs):
        See the `ujson` documentation at <https://git.io/Jfhr7>.

    Returns:
        str: the resulting JSON -- unless stream is None, in which case
            the resulting JSON is written to the stream and nothing is
            returned

    Notes:
        - google.protobuf.json_format.MessageToJson returns a
          human-readable representation of the data

        - For a minified representation, use the ujson module

    """
    from google.protobuf.json_format import MessageToJson

    rval = MessageToJson(message)

    if minified:
        from ujson import loads, dumps

        loaded = loads(rval)
        rval = dumps(loaded, **kwargs)

    if stream:
        stream.write(rval)
    else:
        return rval


def to_yaml(message, stream=None):
    """Returns the YAML of the given protobuf message.

    Args:
        Message (obj): The protobuf message to be converted

    Returns:
        str: the resulting YAML

    """
    from google.protobuf.json_format import MessageToDict

    data = MessageToDict(message)

    from ruamel.yaml import YAML, round_trip_dump

    yaml = YAML(typ="safe")
    yaml.default_flow_style = False

    stream.write("---\n")
    return round_trip_dump(data, stream)


# vim: set ts=4 sw=4 tw=72 expandtab:
