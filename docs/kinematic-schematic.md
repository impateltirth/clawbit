# Kinematic schematic

```mermaid
flowchart LR
    O2["Fixed pivot O₂"] -->|"r₂ crank / motor input"| A["Moving joint A"]
    A -->|"r₃ coupler"| B["Moving joint B"]
    B -->|"r₄ rocker / gate output"| O4["Fixed pivot O₄"]
    O2 ---|"r₁ ground link"| O4
```

The checked-in dimensions are demonstrative placeholders. Replace all four
link lengths with pivot-to-pivot measurements from the verified SolidWorks
assembly before using the computed rocker travel, transmission angle, or
clearance envelope for manufacturing decisions.
