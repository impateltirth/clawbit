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

## Sorting sequence and control interface

The four-bar is the gate actuator; material classification is an upstream input
to that mechanism. A complete cycle has four explicit states:

1. **Acquire:** detect one ball in the sensing pocket and prevent a second ball
   from entering.
2. **Classify:** convert the selected sensor signal into a route identifier.
   Suitable sensors depend on the actual materials—for example inductive for
   metal/non-metal, optical for colour/reflectivity, or load-cell data for mass.
3. **Route:** command the motor to the crank angle associated with that route,
   allow the ball to clear the gate, and enforce a timeout.
4. **Home:** return to the known home switch before admitting the next ball.

The controller should reject ambiguous readings instead of guessing, and route
them to a reject bin. The actual sensor, thresholds, route angles, and cycle
time remain hardware-specific and must be recorded from the built prototype.

## Manufacturing

15+ unique parts across two processes — see `manufacturing/`:
- `BOM.csv` — part list template (fill in from SolidWorks)
- `tolerances.md` — tolerance strategy for laser-cut + 3D-printed assembly
- `../cad/` — SolidWorks exports (STEP/STL/DXF/PDF) go here
