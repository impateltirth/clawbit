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
    ap.add_argument("--r1", type=float, default=R1, help="ground length, mm")
    ap.add_argument("--r2", type=float, default=R2, help="crank length, mm")
    ap.add_argument("--r3", type=float, default=R3, help="coupler length, mm")
    ap.add_argument("--r4", type=float, default=R4, help="rocker length, mm")
    ap.add_argument("--branch", type=int, choices=(-1, 1), default=1,
                    help="assembly branch")
    args = ap.parse_args()

    linkage = Linkage(args.r1, args.r2, args.r3, args.r4)
    phis = np.linspace(0, 2 * np.pi, 181)
    psis = np.array([rocker_angle(linkage, p, args.branch) for p in phis])

    print("links: r1=%.2f r2=%.2f r3=%.2f r4=%.2f mm | Grashof: %s"
          % (args.r1, args.r2, args.r3, args.r4,
             "yes" if linkage.grashof else "no"))

    O2 = np.array([0.0, 0.0])
    O4 = np.array([args.r1, 0.0])
    P2 = np.column_stack([args.r2 * np.cos(phis), args.r2 * np.sin(phis)])
    P3 = O4 + np.column_stack([args.r4 * np.cos(psis), args.r4 * np.sin(psis)])
    M = (P2 + P3) / 2  # coupler midpoint -> coupler curve

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_aspect("equal")
    ax.grid(True)
    pad = 20
    ax.set_xlim(P2[:, 0].min() - pad, O4[0] + args.r4 + pad)
    ax.set_ylim(-args.r2 - args.r4 - pad, args.r2 + args.r4 + pad)
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
