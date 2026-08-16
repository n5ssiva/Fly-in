# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    network.py                                         :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: n5ssim <n5ssim@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/08/16 21:30:52 by n5ssim            #+#    #+#              #
#    Updated: 2026/08/16 22:10:50 by n5ssim           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

"""Network model: holds all zones and connections for the simulation."""

from flyin.connection import Connection
from flyin.zone import Zone


class Network:
    """Holds all zones and connections, and the adjacency structure between them."""

    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.adjacency: dict[str, list[Connection]] = {}
        self.start_zone: str | None = None
        self.end_zone: str | None = None
        self.nb_drones: int = 0

    def add_zone(self, zone: Zone) -> None:
        """Register a zone in the network."""
        if zone.name in self.zones:
            raise ValueError(f"duplicate zone name: {zone.name!r}")
        self.zones[zone.name] = zone

    def add_connection(self, connection: Connection) -> None:
        """Register a connection and update the adjacency structure both ways."""
        if connection.zone_a not in self.zones:
            raise ValueError(f"unknown zone: {connection.zone_a!r}")
        if connection.zone_b not in self.zones:
            raise ValueError(f"unknown zone: {connection.zone_b!r}")

        for existing in self.adjacency.get(connection.zone_a, []):
            if existing.other_side(connection.zone_a) == connection.zone_b:
                raise ValueError(
                    f"duplicate connection: {connection.zone_a!r}-{connection.zone_b!r}"
                )
        self.connections.append(connection)
        self.adjacency.setdefault(connection.zone_a, []).append(connection)
        self.adjacency.setdefault(connection.zone_b, []).append(connection)

    def neighbors(self, zone_name: str) -> list[Connection]:
        """Return the connections reachable from a given zone."""
        return self.adjacency.get(zone_name, [])
