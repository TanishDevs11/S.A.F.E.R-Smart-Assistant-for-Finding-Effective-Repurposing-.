import plotly.express as px
import numpy as np


def plot_pae_map(
    pae_matrix: np.ndarray,
    title: str,
):
    """
    Plot AlphaFold-style Predicted Aligned Error (PAE) map.

    Args:
        pae_matrix (np.ndarray): NxN PAE matrix (Å)
        title (str): Plot title

    Returns:
        plotly.graph_objects.Figure
    """

    fig = px.imshow(
        pae_matrix,
        origin="upper",
        aspect="equal",

        # AlphaFold-style green gradient
        # Low error (confident) = dark green
        # High error (uncertain) = light green
        color_continuous_scale=[
            [0.0, "#00441b"],
            [0.2, "#006d2c"],
            [0.4, "#31a354"],
            [0.6, "#74c476"],
            [0.8, "#c7e9c0"],
            [1.0, "#f7fcf5"],
        ],

        labels=dict(
            x="Scored residue",
            y="Aligned residue",
            color="Expected error (Å)"
        ),

        title=title,
    )

    # -----------------------------
    # High-quality interaction
    # -----------------------------
    fig.update_traces(
        hovertemplate=(
            "Scored residue: %{x}<br>"
            "Aligned residue: %{y}<br>"
            "Expected error: %{z:.2f} Å"
            "<extra></extra>"
        )
    )

    # -----------------------------
    # Layout tuning (sharp & clean)
    # -----------------------------
    fig.update_layout(
        height=720,
        width=720,
        title_x=0.5,
        coloraxis_colorbar=dict(
            title="Expected position error (Å)",
            thickness=14,
            len=0.85
        ),
        margin=dict(l=40, r=40, t=60, b=40),
    )

    return fig
