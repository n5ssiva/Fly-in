# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    connection.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: n5ssim <n5ssim@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/08/16 21:29:24 by n5ssim            #+#    #+#              #
#    Updated: 2026/08/16 21:30:32 by n5ssim           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

"""Connection model: the edges of the drone routing network."""

from dataclasses import dataclass, field


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
        """Check whether one more drone can traverse this connection right now."""
        return len(self.current_transits) < self.max_link_capacity
