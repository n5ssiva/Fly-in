from dataclasses import dataclass, field
from enum import Enum


class ZoneType(Enum):
    NORMAL = "normal"
    BLOCKED = "blocked"
    RESTRICTED = "restricted"
    PRIORITY = "priority"

    def movement_cost(self) -> int:
        """Return the number of turns needed to move into a zone of this type."""
        match self:
            case ZoneType.NORMAL | ZoneType.PRIORITY:
                return 1
            case ZoneType.RESTRICTED:
                return 2
            case ZoneType.BLOCKED:
                raise ValueError("blocked zones have no movement cost")


@dataclass
class Zone:
    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = 1
    is_start: bool = False
    is_end: bool = False
    current_occupants: set[str] = field(default_factory=set)

    def has_capacity(self) -> bool:
        """Check whether one more drone can enter this zone right now."""
        if self.is_start or self.is_end:
            return True
        return len(self.current_occupants) < self.max_drones

    def add_drone(self, drone_id: str) -> None:
        """Register a drone as currently occupying this zone."""
        if not self.has_capacity():
            raise ValueError(f"zone {self.name!r} is at full capacity")
        self.current_occupants.add(drone_id)

    def remove_drone(self, drone_id: str) -> None:
        """Remove a drone from this zone's current occupants."""
        if drone_id not in self.current_occupants:
            raise ValueError(f"{drone_id} is not in the zone")
        self.current_occupants.remove(drone_id)


@dataclass
class Connection:
    zone_a: str
    zone_b: str
    max_link_capacity: int = 1
    current_transits: set[str] = field(default_factory=set)

    def other_side(self, zone_name: str) -> str:
        """Given one endpoint, return the zone name at the other end."""
        if zone_name == self.zone_a:
            return self.zone_b
        if zone_name == self.zone_b:
            return self.zone_a
        raise ValueError(f"{zone_name!r} is not an endpoint of this connection")

    def has_capacity(self) -> bool:
        """ Check whether one more drone can traverse this connection right now"""
        return len(self.current_transits) < self.max_link_capacity


class DroneStatus(Enum):
    WAITING = "waiting"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"


@dataclass
class Drone:
    drone_id: str
    current_zone: str | None
    status: DroneStatus = DroneStatus.WAITING
    transit_target: str | None = None
    transit_turns_remaining: int = 0


class Network:
    """Holds all zones and connections, and the adjacency structure between them."""

    def __init__(self) -> None:
        self.zones: dict[str, Zone] = {}
        self.connections: list[Connection] = []
        self.adjacency: dict[str, list[Connection]] = {}
        self.start_zone: str | None = None
        self.end_zone: str | None = None

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
