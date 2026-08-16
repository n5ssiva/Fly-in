# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    drone.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: n5ssim <n5ssim@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/08/16 21:30:05 by n5ssim            #+#    #+#              #
#    Updated: 2026/08/16 21:30:42 by n5ssim           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

"""Drone model: state of an individial drone during the simulation."""

from dataclasses import dataclass
from enum import Enum


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
