# CAD exports

SolidWorks source files (`.sldprt` / `.sldasm`) live outside this repo. Export the manufacturing-ready files here:

| Export | Format | Purpose |
|---|---|---|
| Assembly + all parts | STEP AP214 (`.step`) | Archival, viewable anywhere |
| 3D-printed parts | STL (`.stl`), fine resolution | Slicing |
| Laser-cut parts | DXF (`.dxf`), 1:1 flat patterns | CAM / laser cutter |
| Fabrication drawing | PDF (`.pdf`) | The drawing with tolerances and notes |

Suggested naming: `clawbit-<part_no>-<rev>.<ext>`, matching `part_no` in `manufacturing/BOM.csv`.

**TODO:** add the exports for the 15+ unique parts.
