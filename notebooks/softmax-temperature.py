# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#     "altair",
#     "marimo",
#     "numpy",
#     "pandas",
#     "marimo-studio==0.3.0"
# ]
#
# [tool.marimo-studio]
# default = "post"
#
# [tool.marimo-studio.cells]
# ///

import marimo

app = marimo.App(width="medium")


@app.cell
def imports():
    import altair as alt
    import marimo as mo
    import numpy as np
    import pandas as pd

    return alt, mo, np, pd


@app.cell
def logits(np):
    tokens = ["the", "a", "model", "cat", "attention", "banana"]
    raw_logits = np.array([3.2, 2.9, 2.1, 1.4, 0.6, -1.0])
    return raw_logits, tokens


@app.cell
def temperature(mo):
    temperature = mo.ui.slider(
        steps=[0.25, 0.5, 1.0, 2.0, 4.0], value=1.0, label="Temperature $T$", show_value=True
    )
    temperature
    return (temperature,)


@app.cell
def distribution(alt, np, pd, raw_logits, temperature, tokens):
    def softmax(z, t):
        e = np.exp((z - z.max()) / t)
        return e / e.sum()

    probs = softmax(raw_logits, temperature.value)
    entropy = float(-(probs * np.log2(probs)).sum())
    chart = (
        alt.Chart(pd.DataFrame({"token": tokens, "p": probs}))
        .mark_bar(color="#253951")
        .encode(
            x=alt.X("token:N", sort=None, title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("p:Q", scale=alt.Scale(domain=[0, 1]), title="p(token)"),
            tooltip=["token", alt.Tooltip("p:Q", format=".3f")],
        )
        .properties(width="container", height=240)
    )
    chart
    return (entropy,)


@app.cell
def summary(entropy, mo, np, temperature, tokens):
    mo.md(
        f"At $T = {temperature.value}$ the entropy is **{entropy:.2f} bits** "
        f"(uniform over {len(tokens)} tokens: {np.log2(len(tokens)):.2f} bits)."
    )
    return


if __name__ == "__main__":
    app.run()
