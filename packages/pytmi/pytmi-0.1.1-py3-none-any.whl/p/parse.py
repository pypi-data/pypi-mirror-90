import utils
from typing import Optional, Union, Dict, Any


__all__ = []


def parse_tmi_message(message: str) -> Dict[str, Any]:
    parsed = {}

    if message.startswith("@"):
        message = message[1:]
        parsed["tags"], message = message.split(" :", 1)

    parsed["endpoint"], message = message.split(" ", 1)
    parsed["command"] = message.split("\r\n", 1)[0].lstrip()

    return parsed


__all__.append(parse_tmi_message)


def parse_tmi_tags(tags: str) -> Dict[str, Any]:
    if not isinstance(tags, str):
        raise TypeError("Expect str")

    parsed = {}

    tag_list = tags.split(";")

    for tag in tag_list:
        name, value = tag.split("=", 1)

        norm = value

        if value.isascii() and value.isnumeric():
            norm = int(value)

        elif value.isspace() or value == '':
            norm = None

        elif value.startswith("#") and utils.ishex(value[1:]):
            norm = int(value[1:], 16)

        parsed[name] = norm

    return parsed


def parse_tmi_privmsg(parsed_message: Dict[str, Any]) -> Dict[str, Any]:
    parsed = {}

    tags = parsed_message.get("tags", None)

    parsed.update(parse_tmi_tags(tags))

    command = parsed_message.get("command", " : ")
    
    parsed["message"] = command.split(" :")[1]

    return parsed


__all__.append(parse_tmi_privmsg)


def parse_tmi_user(endpoint: str) -> str:
    return endpoint.split("!", 1)
