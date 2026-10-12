"""Verify the educational notebook against hand counts and a pairwise AUC oracle.

Run from the repository root:
    uvx --with marimo-studio==0.3.0 python scripts/check-agent-evaluation.py
"""

import importlib.util
import json
from pathlib import Path

import numpy as np


def main():
    path = Path(__file__).resolve().parents[1] / "notebooks/agent-confusion-matrix.py"
    spec = importlib.util.spec_from_file_location("agent_evaluation", path)
    notebook = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(notebook)
    outputs, values = notebook.app.run()
    counts = values["confusion_counts"]
    metrics = values["classification_metrics"]
    roc = values["roc_coordinates"]
    labels, scores = values["labels"], values["scores"]

    # Manually enumerable examples catch swapped rows and denominators.
    assert counts(labels, scores, .35) == {"TP": 18, "FP": 20, "FN": 2, "TN": 60}
    assert counts(labels, scores, .80) == {"TP": 8, "FP": 2, "FN": 12, "TN": 78}
    example = metrics({"TP": 5, "FP": 3, "FN": 2, "TN": 6})
    assert np.isclose(example["accuracy"], 11 / 16)
    assert np.isclose(example["recall"], 5 / 7)
    assert np.isclose(example["precision"], 5 / 8)
    assert np.isclose(example["fpr"], 3 / 9)

    assert counts(labels, scores, 0) == {"TP": 20, "FP": 80, "FN": 0, "TN": 0}
    rejected = counts(labels, scores, 1)
    assert rejected == {"TP": 0, "FP": 0, "FN": 20, "TN": 80}
    assert metrics(rejected)["precision"] is None
    assert counts([1, 0], [.5, .5], .5) == {"TP": 1, "FP": 1, "FN": 0, "TN": 0}

    # This independent definition checks integration, ties and curve direction.
    positives = scores[labels == 1]
    negatives = scores[labels == 0]
    pairs = positives[:, None] - negatives[None, :]
    pairwise_auc = float(np.mean((pairs > 0) + .5 * (pairs == 0)))
    fpr, tpr, auc = roc(labels, scores)
    assert np.isclose(auc, pairwise_auc)
    assert np.isclose(auc, .888125)
    assert (fpr[0], tpr[0]) == (0, 0)
    assert (fpr[-1], tpr[-1]) == (1, 1)
    assert np.all(np.diff(fpr) >= 0) and np.all(np.diff(tpr) >= 0)
    assert np.isclose(roc([1, 0], [.5, .5])[2], .5)
    assert np.isclose(roc([1, 0], [.9, .1])[2], 1)
    assert np.isclose(roc([1, 0], [.1, .9])[2], 0)

    previous = counts(labels, scores, 0)
    for threshold_percent in range(0, 101, 5):
        current = counts(labels, scores, threshold_percent / 100)
        assert sum(current.values()) == 100
        assert current["TP"] + current["FN"] == 20
        assert current["FP"] + current["TN"] == 80
        assert current["TP"] <= previous["TP"]
        assert current["FP"] <= previous["FP"]
        previous = current

    # Numbers quoted in the prose, the exercises and the lab answers.
    at = {t: metrics(counts(labels, scores, t / 100)) for t in range(0, 101, 5)}
    assert (at[35]["accuracy"], at[100]["accuracy"]) == (.78, .80)
    assert np.allclose([at[35]["precision"], at[80]["precision"], at[80]["recall"]], [18 / 38, .8, .4])
    assert max(t for t in at if at[t]["recall"] == 1) == 20 and np.isclose(at[20]["fpr"], .575)
    assert np.allclose([at[t]["precision"] for t in (85, 90, 95)], [6 / 7, .8, 1])
    assert [t for t in at if at[t]["accuracy"] >= .86] == [80]

    assert len(values["contexts"]) == 3
    print(json.dumps({
        "status": "passed", "executed_cells": len(outputs),
        "threshold_positions": 21, "interactive_scenarios": 1, "static_contexts": 3,
        "roc_auc": auc, "pairwise_auc": pairwise_auc,
        "checks": "hand counts, denominators, boundary rule, zero denominator, monotonicity, ROC endpoints and tie-aware independent AUC",
    }, indent=2))


if __name__ == "__main__":
    main()
