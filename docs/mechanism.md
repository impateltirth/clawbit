# Clawbit mechanism notes

## What it does

Four-bar linkage ball sorting mechanism: a motor drives the crank through full revolutions, the rocker oscillates, and the linkage drives the sorting gate that routes balls by material into separate paths. The linkage was designed and prototyped in SolidWorks, with high-precision parts CNC laser cut and the functional prototype 3D printed.

## Link table

**TODO:** fill in measured lengths from the SolidWorks model, then run `analysis/four_bar_kinematics.m` to verify the Grashof type and transmission angle.

| Link | Role | Length (mm) | Notes |
|---|---|---|---|
| r1 | Ground (frame pivot to pivot) | | |
| r2 | Crank (input, motor-driven) | | Must be the shortest link for crank-rocker |
| r3 | Coupler | | |
| r4 | Rocker (output, drives gate) | | |

## Design checks (from the kinematics script)

- **Grashof:** s + l < p + q, with the crank shortest → crank-rocker, so the motor sees continuous rotation while the gate oscillates.
- **Transmission angle:** keep the minimum above ~40° over the cycle; below that, force transmission gets poor and the gate can bind.
- **Rocker swing:** max(ψ) − min(ψ) sets the gate travel — size the diverter to match.
- **Coupler curve:** the traced path of the coupler midpoint; use it to check clearances against the ball path.

## Sorting principle — TODO

Document how balls are differentiated by material here (e.g. size/weight sensing at the gate, diverter logic, throughput). The kinematics above cover the linkage; the sensing and gate sequencing still need to be written up.

## Manufacturing

15+ unique parts across two processes — see `manufacturing/`:
- `BOM.csv` — part list template (fill in from SolidWorks)
- `tolerances.md` — tolerance strategy for laser-cut + 3D-printed assembly
- `../cad/` — SolidWorks exports (STEP/STL/DXF/PDF) go here
