#!/usr/bin/env python3
# coding: utf-8

from math import *
from zencad import *


class GripStyle:

    _tech = 0.01

    def __init__(
            self,
            step_length: float = 8.0,
            slot_length_percentage: float = 0.5,
            slot_side_fillet: float = 0.4
    ):
        self._step_length = step_length
        self._slot_length_percentage = slot_length_percentage
        self._slot_side_fillet = slot_side_fillet
        self.depth = (step_length * slot_length_percentage) / 2

    def create_shape(
            self,
            radius: float,
            height: float
    ):
        steps_count = int(floor(radius * pi * 2 / self._step_length))
        step_angle = pi * 2 / steps_count
        result = cylinder(radius, height)
        bottom_top_chamfer = self.depth - self._tech
        max_bottom_top_chamfer = (height / 2) - self._tech
        bottom_top_chamfer = min(bottom_top_chamfer, max_bottom_top_chamfer)
        result = result.chamfer(bottom_top_chamfer, [(0, -radius, 0), (0, -radius, height)])
        sbtn = cylinder(self.depth, height + self._tech*8).down(self._tech*4)
        sbtn = sbtn.back(radius)
        sbtn = cylinder(radius+self._tech, height+self._tech*6).down(self._tech*3) - sbtn
        sbtn = sbtn.fillet(self._slot_side_fillet, [(self.depth, -radius, height/2), (-self.depth, -radius, height/2)])
        step_offset = sin(step_angle/2) * radius - self._tech
        sbtn_iscn = polysegment([(0, 0, 0), (-step_offset, -radius, 0), (step_offset, -radius, 0)], closed=True)
        sbtn_iscn = sbtn_iscn.fill()
        sbtn_iscn = sbtn_iscn.extrude(height+self._tech*2).down(self._tech)
        sbtn = sbtn_iscn - sbtn
        sbtns = union([sbtn.rotateZ(step_angle*i) for i in range(steps_count)])
        result -= sbtns
        return result


if __name__ == "__main__":
    style = GripStyle(
    )

    mask = halfspace().rotateX(pi / 2)

    screw_radius = 3.6
    screw_height = 12
    wall = 2.4

    grip = style.create_shape(
        radius=30,
        height=20
    )

    disp(grip, color(1, 0, 1))

    show()
