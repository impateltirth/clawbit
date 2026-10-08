#!/usr/bin/env python3
"""
Animate the Clawbit four-bar linkage and trace its coupler curve.

Same kinematics as analysis/four_bar_kinematics.m (Freudenstein's equation).

Usage:
    python3 four_bar_animate.py
    python3 four_bar_animate.py --save linkage.gif   # needs pillow
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from kinematics import Linkage, rocker_angle

# ---- Link lengths (mm): REPLACE with measurements from your SolidWorks model ----
R1 = 120.0  # ground (frame pivot to pivot)
R2 = 35.0   # crank (input, motor-driven)
R3 = 110.0  # coupler
R4 = 90.0   # rocker (output)


def solve_rocker(phi):
    """Rocker angle (rad) for crank angle phi (rad), open assembly branch."""
    return rocker_angle(Linkage(R1, R2, R3, R4), phi)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--save", help="save animation to file (e.g. linkage.gif)")
    ap.add_argument("--fps", type=int, default=30)
    args = ap.parse_args()

    phis = np.linspace(0, 2 * np.pi, 181)
    psis = np.array([solve_rocker(p) for p in phis])

    O2 = np.array([0.0, 0.0])
    O4 = np.array([R1, 0.0])
    P2 = np.column_stack([R2 * np.cos(phis), R2 * np.sin(phis)])
    P3 = O4 + np.column_stack([R4 * np.cos(psis), R4 * np.sin(psis)])
    M = (P2 + P3) / 2  # coupler midpoint -> coupler curve

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_aspect("equal")
    ax.grid(True)
    pad = 20
    ax.set_xlim(P2[:, 0].min() - pad, O4[0] + R4 + pad)
    ax.set_ylim(-R2 - R4 - pad, R2 + R4 + pad)
    ax.set_xlabel("x (mm)")
    ax.set_ylabel("y (mm)")
    ax.set_title("Clawbit four-bar linkage")

    (curve,) = ax.plot([], [], "k-", lw=1, alpha=0.6, label="coupler curve")
    (crank,) = ax.plot([], [], "b-o", lw=3, markersize=6, label="crank")
    (coupler,) = ax.plot([], [], "r-o", lw=3, markersize=6, label="coupler")
    (rocker,) = ax.plot([], [], "g-o", lw=3, markersize=6, label="rocker")
    ax.plot([O2[0], O4[0]], [O2[1], O4[1]], "ko", markersize=8)
    ax.legend(loc="best")

    def update(i):
        curve.set_data(M[: i + 1, 0], M[: i + 1, 1])
        crank.set_data([O2[0], P2[i, 0]], [O2[1], P2[i, 1]])
        coupler.set_data([P2[i, 0], P3[i, 0]], [P2[i, 1], P3[i, 1]])
        rocker.set_data([O4[0], P3[i, 0]], [O4[1], P3[i, 1]])
        return curve, crank, coupler, rocker

    anim = FuncAnimation(fig, update, frames=len(phis), interval=1000 / args.fps,
                         blit=True)
    if args.save:
        anim.save(args.save, fps=args.fps)
        print("saved", args.save)
    else:
        plt.show()


if __name__ == "__main__":
    main()
