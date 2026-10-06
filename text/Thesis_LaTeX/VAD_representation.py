"""Create a three-dimensional Valence-Arousal-Dominance illustration.

The axes use the normalized range employed in the thesis:

    X = valence, Y = arousal, Z = dominance, all in [-1, 1].

The emotion coordinates are schematic examples intended to make the geometry
of VAD space intuitive. They are not predictions from the thesis models or
empirical estimates for a particular dataset.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from mpl_toolkits.mplot3d import proj3d


HERE = Path(__file__).resolve().parent
OUTPUT_DIR = HERE / "media"
OUTPUT_DIR.mkdir(exist_ok=True)

PNG_PATH = OUTPUT_DIR / "vad_3d_emotion_space.png"
PDF_PATH = OUTPUT_DIR / "vad_3d_emotion_space.pdf"

# Illustrative VAD coordinates: (valence, arousal, dominance).
EMOTIONS = {
    "Joy": (0.85, 0.65, 0.65),
    "Excitement": (0.75, 0.90, 0.45),
    "Contentment": (0.75, -0.45, 0.45),
    "Calm": (0.45, -0.75, 0.25),
    "Anger": (-0.75, 0.80, 0.65),
    "Fear": (-0.80, 0.85, -0.70),
    "Sadness": (-0.75, -0.55, -0.65),
    "Boredom": (-0.35, -0.80, -0.45),
    "Surprise": (0.05, 0.90, 0.05),
}

# Colours group nearby examples visually; the positions carry the VAD meaning.
EMOTION_GROUPS = {
    "positive": {
        "members": {"Joy", "Excitement", "Contentment", "Calm"},
        "colour": "#0072B2",
        "label": "Positive-valence examples",
    },
    "negative_active": {
        "members": {"Anger", "Fear"},
        "colour": "#D55E00",
        "label": "Negative, high-arousal examples",
    },
    "negative_subdued": {
        "members": {"Sadness", "Boredom"},
        "colour": "#7A5195",
        "label": "Negative, low-arousal examples",
    },
    "mixed": {
        "members": {"Surprise"},
        "colour": "#6B7280",
        "label": "Valence-variable example",
    },
}

# Label offsets are in screen points and keep annotations away from markers.
LABEL_OFFSETS = {
    "Joy": (8, 7),
    "Excitement": (-8, 10),
    "Contentment": (8, -13),
    "Calm": (10, 13),
    "Anger": (-8, 10),
    "Fear": (-10, -18),
    "Sadness": (-8, -15),
    "Boredom": (8, -14),
    "Surprise": (8, 9),
}


def emotion_colour(name: str) -> str:
    """Return the display colour for an emotion."""
    for group in EMOTION_GROUPS.values():
        if name in group["members"]:
            return group["colour"]
    raise KeyError(f"No colour group is defined for {name!r}")


def build_figure() -> tuple[plt.Figure, plt.Axes]:
    """Build and return the VAD figure and its three-dimensional axes."""
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 10,
            "axes.titlesize": 14,
            "axes.labelsize": 11,
            "savefig.dpi": 300,
        }
    )

    fig = plt.figure(figsize=(9.2, 6.6), facecolor="white")
    ax = fig.add_subplot(111, projection="3d")
    fig.subplots_adjust(left=0.02, right=0.87, bottom=0.20, top=0.84)

    # The requested coordinate mapping.
    ax.set_xlabel("Valence (X)", labelpad=11, color="#005A8D", weight="bold")
    ax.set_ylabel("Arousal (Y)", labelpad=11, color="#A94A00", weight="bold")
    # A 2D label avoids a Matplotlib 3D clipping issue at the right page edge.
    ax.set_zlabel("")
    ax.text2D(
        1.12,
        0.52,
        "Dominance (Z)",
        transform=ax.transAxes,
        rotation=90,
        ha="center",
        va="center",
        color="#246B32",
        weight="bold",
        fontsize=11,
    )

    ticks = [-1, -0.5, 0, 0.5, 1]
    tick_labels = ["−1", "−0.5", "0", "0.5", "1"]
    for setter in (ax.set_xlim, ax.set_ylim, ax.set_zlim):
        setter(-1, 1)
    ax.set_xticks(ticks, tick_labels)
    ax.set_yticks(ticks, tick_labels)
    ax.set_zticks(ticks, tick_labels)
    ax.set_box_aspect((1, 1, 1))
    ax.view_init(elev=24, azim=-55)

    # Light panes and grids preserve the three-dimensional structure in print.
    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        axis.pane.set_facecolor((0.97, 0.97, 0.97, 1))
        axis.pane.set_edgecolor((0.72, 0.72, 0.72, 1))
        axis._axinfo["grid"]["color"] = (0.72, 0.72, 0.72, 0.45)
        axis._axinfo["grid"]["linewidth"] = 0.7

    # Coloured centre lines make the X/Y/Z mapping clear.
    ax.plot([-1, 1], [0, 0], [0, 0], color="#0072B2", linewidth=1.5)
    ax.plot([0, 0], [-1, 1], [0, 0], color="#D55E00", linewidth=1.5)
    ax.plot([0, 0], [0, 0], [-1, 1], color="#2E7D32", linewidth=1.5)
    ax.scatter([0], [0], [0], s=18, color="#222222", depthshade=False, zorder=6)

    # Plot all emotion points before projecting their annotations.
    for name, (valence, arousal, dominance) in EMOTIONS.items():
        ax.scatter(
            [valence],
            [arousal],
            [dominance],
            s=58,
            color=emotion_colour(name),
            edgecolor="white",
            linewidth=0.8,
            depthshade=False,
            zorder=8,
        )

    fig.suptitle(
        "Illustrative emotions in VAD space",
        x=0.47,
        y=0.965,
        fontsize=14,
        weight="bold",
    )
    fig.text(
        0.47,
        0.915,
        "X = valence   •   Y = arousal   •   Z = dominance",
        ha="center",
        va="center",
        color="#444444",
        fontsize=10,
    )

    legend_handles = [
        Patch(
            facecolor=group["colour"],
            edgecolor="none",
            label=group["label"],
        )
        for group in EMOTION_GROUPS.values()
    ]
    fig.legend(
        handles=legend_handles,
        loc="lower center",
        bbox_to_anchor=(0.5, 0.052),
        ncol=2,
        frameon=False,
        fontsize=9,
        columnspacing=2.0,
    )
    fig.text(
        0.5,
        0.018,
        "Emotion locations are schematic examples, not model predictions.",
        ha="center",
        va="bottom",
        fontsize=9,
        style="italic",
        color="#555555",
    )

    # Convert 3D locations to 2D display coordinates for crisp, offset labels.
    fig.canvas.draw()
    for name, (valence, arousal, dominance) in EMOTIONS.items():
        x_2d, y_2d, _ = proj3d.proj_transform(
            valence, arousal, dominance, ax.get_proj()
        )
        offset_x, offset_y = LABEL_OFFSETS[name]
        horizontal_alignment = "left" if offset_x >= 0 else "right"
        ax.annotate(
            name,
            xy=(x_2d, y_2d),
            xytext=(offset_x, offset_y),
            textcoords="offset points",
            ha=horizontal_alignment,
            va="center",
            fontsize=9,
            weight="semibold",
            color="#202020",
            bbox={
                "boxstyle": "round,pad=0.18",
                "facecolor": "white",
                "edgecolor": "none",
                "alpha": 0.82,
            },
        )

    return fig, ax


def main() -> None:
    """Render the figure to thesis-ready raster and vector files."""
    fig, _ = build_figure()
    fig.savefig(PNG_PATH, bbox_inches="tight", facecolor="white")
    fig.savefig(PDF_PATH, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved {PNG_PATH}")
    print(f"Saved {PDF_PATH}")


if __name__ == "__main__":
    main()
