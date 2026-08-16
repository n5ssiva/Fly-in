# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    parser.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: n5ssim <n5ssim@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/08/16 22:02:15 by n5ssim            #+#    #+#              #
#    Updated: 2026/08/16 22:10:17 by n5ssim           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

"""Parser for Fly-in map files"""

from pydantic import ValidationError

from flyin.connection import Connection
from flyin.network import Network
from flyin.zone import Zone, ZoneType

class ParseError(Exception):
    """Raised when the input map file in malformed."""


class Parser:
    """Parses a Fly-in map file into a Network."""

    def __init__(self) -> None:
        self.line_number: int = 0

    def parse(self, path: str) -> Network:
        """Parse a map file and return the resulting Network."""
        ...

    def _parse_drone_count(self, line: str) -> int:
        ...

    def _parse_zone_line(self, line: str) -> Zone:
        ...

    def _parse_connection_lines(self, line: str) -> Connection:
        ...

    def _parse_metadata(self, raw: str) -> dict[str, str]:
        ...