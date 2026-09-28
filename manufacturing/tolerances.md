# Tolerance strategy

The Clawbit assembly mixes CNC laser-cut parts (high precision, 2D) with 3D-printed parts (functional prototype, lower precision) across 15+ unique parts. The strategy below keeps the linkage pivots accurate where it matters.

## General rules

- **Laser-cut parts:** hold ±0.1 mm on critical pivot-hole spacing. Compensate kerf in the CAM step (typically 0.1–0.2 mm for acrylic/plywood) — draw holes undersize by half the kerf.
- **3D-printed parts:** expect ±0.2 mm and ~0.5% shrinkage on longer dimensions. Print pivot bores undersize and ream/drill to final size.
- **Pivot holes:** ream to a light press or running fit depending on the joint — never rely on as-printed or as-cut hole size for a bearing fit.

## Fit guidance

| Joint | Recommended fit | Why |
|---|---|---|
| Crank/rocker pivots on frame | Reamed hole + shoulder bolt, light running fit | Must rotate freely with no slop (slop → gate timing error) |
| Coupler pin joints | Press-fit pin into one link, running fit in the other | One fixed, one free — avoids over-constraint |
| Motor shaft to crank | Set screw on flat, or D-shaft | No slip under reversing torque |
| Gate/deflector mounts | Clearance holes + nyloc nuts | Field-adjustable during commissioning |

## Stack-up

The gate timing depends on the **pivot-to-pivot distances** (r1–r4), not on part outlines. Tolerance those four dimensions tightest; cosmetic edges can be looser. Verify the assembled r1–r4 with calipers and update `analysis/four_bar_kinematics.m` if they differ from CAD — then re-run the Grashof and transmission-angle checks.

## TODO

- [ ] Record measured pivot-to-pivot distances from the built prototype
- [ ] Note the actual kerf compensation used for the laser-cut parts
- [ ] List the print settings (material, layer height, infill) for the 3D-printed parts
