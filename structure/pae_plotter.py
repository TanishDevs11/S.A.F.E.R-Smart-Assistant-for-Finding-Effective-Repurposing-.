import plotly.express as px
import numpy as np

def plot_pae_matrix(pae, title):
    pae = np.array(pae)

    fig = px.imshow(
        pae,
        color_continuous_scale="Greens",
        labels=dict(x="Residue", y="Residue", color="PAE (Å)"),
        title=title
    )

    fig.update_layout(
        height=600,
        coloraxis_colorbar=dict(title="Expected position error (Å)")
    )

    return fig
