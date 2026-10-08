"""Dependency-free four-bar geometry used by the analysis tools."""

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class Linkage:
    ground: float
    crank: float
    coupler: float
    rocker: float

    def __post_init__(self):
        if min(self.ground, self.crank, self.coupler, self.rocker) <= 0:
            raise ValueError("all link lengths must be greater than zero")

    @property
    def grashof(self):
        lengths = sorted((self.ground, self.crank, self.coupler, self.rocker))
        return lengths[0] + lengths[3] <= lengths[1] + lengths[2]


def rocker_point(linkage, crank_angle, branch=1):
    """Return the coupler/rocker joint using a circle intersection.

    ``branch`` selects one of the two assembly configurations (+1 or -1).
    """
    if branch not in (-1, 1):
        raise ValueError("branch must be +1 or -1")

    ax = linkage.crank * math.cos(crank_angle)
    ay = linkage.crank * math.sin(crank_angle)
    dx = linkage.ground - ax
    dy = -ay
    distance = math.hypot(dx, dy)
    if distance == 0:
        raise ValueError("coincident pivots produce an indeterminate assembly")
    if distance > linkage.coupler + linkage.rocker or distance < abs(
        linkage.coupler - linkage.rocker
    ):
        raise ValueError(
            "linkage cannot assemble at %.1f degrees" % math.degrees(crank_angle)
        )

    along = (
        linkage.coupler**2 - linkage.rocker**2 + distance**2
    ) / (2 * distance)
    height_sq = max(0.0, linkage.coupler**2 - along**2)
    height = math.sqrt(height_sq)
    ux, uy = dx / distance, dy / distance
    px = ax + along * ux - branch * height * uy
    py = ay + along * uy + branch * height * ux
    return px, py


def rocker_angle(linkage, crank_angle, branch=1):
    px, py = rocker_point(linkage, crank_angle, branch)
    return math.atan2(py, px - linkage.ground)
