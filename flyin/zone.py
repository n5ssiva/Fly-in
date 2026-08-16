# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    zone.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: n5ssim <n5ssim@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/08/16 21:29:36 by n5ssim            #+#    #+#              #
#    Updated: 2026/08/16 21:53:01 by n5ssim           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

"""Zone model: the nodes of the drone routing network."""

from enum import Enum
from pydantic import BaseModel, Field


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


class Zone(BaseModel):
    name: str
    x: int
    y: int
    zone_type: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = 1
    is_start: bool = False
    is_end: bool = False
    current_occupants: set[str] = Field(default_factory=set)

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
