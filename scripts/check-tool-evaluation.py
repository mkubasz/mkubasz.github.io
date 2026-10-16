"""Verify the recorded lab output and the article's derived metrics.

Run from the repository root:
    uv run --with marimo-studio==0.3.0 --with marimo-export==0.1.4 --with scikit-learn==1.9.1 python scripts/check-tool-evaluation.py
"""

import hashlib
import importlib.util
import json
from math import isclose
from pathlib import Path
from zipfile import ZipFile


def main():
    root = Path(__file__).resolve().parents[1]
    path = root / "notebooks/agent-tool-evaluation.py"
    spec = importlib.util.spec_from_file_location("tool_evaluation", path)
    notebook = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(notebook)
    outputs, values = notebook.app.run()
    data = values["observed_data"]
    records = values["goldenset"]
    build = values["build_observed_report"]
    assert data["kind"] == "observed_model_run"
    assert len(records) == 5
    assert sum(len(record["turns"]) for record in records) == 11
    assert sum(len(turn["expected_calls"]) for record in records for turn in record["turns"]) == 24

    # Hand-counted presence outcomes from the captured calls: TP, FP, FN, TN.
    oracles = {
        "correct": [(3, 5, 0, 3), (4, 0, 5, 2), (2, 0, 0, 9), (3, 0, 1, 7), (3, 0, 1, 7)],
        "broken": [(3, 5, 0, 3), (3, 0, 6, 2), (0, 0, 2, 9), (0, 0, 4, 7), (0, 0, 4, 7)],
    }
    expected_counts = [6, 5, 6, 1, 6]
    observed_counts = {"correct": [6, 3, 6, 1, 7], "broken": [3, 3, 3, 1, 1]}
    matched_fields = {"correct": [3, 1, 3, 3, 3], "broken": [0, 1, 0, 3, 1]}
    count_f1 = {"correct": [1/2, 3/4, 2/3, 1, 8/13], "broken": [0, 3/4, 2/9, 1, 2/7]}
    for mode in ("correct", "broken"):
        report = build(mode, 0)
        assert [tuple(row[1:5]) for row in report["tool_rows"]] == oracles[mode]
        assert [row[8] for row in report["tool_rows"]] == [3, 9, 2, 4, 4]
        assert report["matrices"] == data["runs"][mode]["matrices"]
        assert report["stats"] == data["runs"][mode]["classification_report"]
        for index in range(5):
            current = build(mode, index)
            original = data["runs"][mode]["scenarios"][index]
            assert current["expected_count"] == expected_counts[index]
            assert current["actual_count"] == observed_counts[mode][index]
            assert current["matched_fields"] == matched_fields[mode][index]
            assert isclose(current["count_scores"]["f1"], count_f1[mode][index])
            assert current["state"]["snapshot"] == original["snapshot"]
            assert current["state"]["other_patients_unchanged"] == original["other_patients_unchanged"]
            for key, value in current["count_scores"].items():
                assert isclose(value, original["count_scores"][key])
            assert [trace["calls"] for trace in current["traces"]] == original["turn_calls"]
    assert isclose(build("correct", 0)["stats"]["micro avg"]["f1-score"], 5/7)
    assert isclose(build("broken", 0)["stats"]["micro avg"]["f1-score"], 4/11)
    assert isclose(build("correct", 0)["subset_accuracy"], 4/11)
    assert isclose(build("broken", 0)["subset_accuracy"], 2/11)
    assert [len(build("broken", i)["state"]["errors"]) for i in range(5)] == [3, 0, 3, 0, 1]

    # The marked record is an observed parser failure, with the exact TypeError.
    record = values["broken_record"]
    assert record["turn_index"] == 2 and record["parser"] == "parse_tool_calls_broken"
    assert record["calls"] == [["get_patient_status", {"patient_id": "12345", "lab_name": "CBC"}]]
    assert any("unexpected keyword argument 'lab_name'" in message["content"] for message in record["messages"])
    assert values["parser_correct"] == [
        ("get_patient_status", {"patient_id": "12345"}),
        ("assign_patient_labs", {"lab_name": "CBC", "patient_id": "12345"}),
    ]
    assert values["parser_broken"] == [("get_patient_status", {"patient_id": "12345", "lab_name": "CBC"})]
    # Expected (rows) vs called (columns) occurrences, paired as in lab0.py; the last row/column is '-'.
    assert build("broken", 0)["pair_matrix"] == [
        [3, 0, 0, 0, 0, 2], [5, 3, 0, 0, 0, 1], [0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 4], [0, 0, 0, 0, 0, 4], [0, 0, 0, 0, 0, 0],
    ]
    assert build("correct", 0)["pair_matrix"] == [
        [3, 2, 0, 0, 0, 0], [5, 4, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0], [0, 0, 0, 3, 0, 1], [0, 0, 0, 0, 3, 1], [0, 0, 0, 0, 1, 0],
    ]
    # Prose claims: the four-outcome turn, a TP from a failed call, and the calls-vs-state cross-tab.
    assert [name for name, _ in data["runs"]["correct"]["scenarios"][0]["turn_calls"][1]] == ["get_patient_status", "assign_patient_labs"]
    last_broken = build("broken", 4)["traces"][-1]
    assert [name for name, _ in last_broken["calls"]] == ["get_patient_status"]
    assert any(message["content"].startswith("Error:") for message in last_broken["messages"] if message["role"] == "tool")
    correct = data["runs"]["correct"]["scenarios"]
    assert [s["name"].split(":")[0] for s in correct if s["count_scores"]["fp"] == s["count_scores"]["fn"] == 0] == ["On hold"]
    assert sum(s["count_scores"]["fp"] + s["count_scores"]["fn"] > 0 and s["final_state_score"] >= 0.85 for s in correct) == 3
    assert build("broken", 0)["state"]["snapshot"]["assigned_labs"] == []
    assert build("correct", 0)["state"]["snapshot"]["assigned_labs"] == ["CBC"]

    fixture = json.loads((root / "notebooks/assets/tool-evaluation/lab-reference.json").read_text())
    assert data["source_sha256"] == fixture["sha256"]
    assert data["records"] == fixture["records"]
    traces = json.loads((root / "notebooks/assets/tool-evaluation/lab-traces.json").read_text())
    assert traces["source_sha256"] == data["source_sha256"]
    assert len(traces["turns"]) == 22
    with ZipFile(root / "public/downloads/agent-tool-evaluation-lab.zip") as archive:
        assert archive.testzip() is None
        for name, digest in data["source_sha256"].items():
            assert hashlib.sha256(archive.read("agent-tool-evaluation-lab/" + name)).hexdigest() == digest
        for name in ("lab-observed.json", "lab-traces.json"):
            assert archive.read("agent-tool-evaluation-lab/" + name) == (root / "notebooks/assets/tool-evaluation" / name).read_bytes()

    print(json.dumps({
        "status": "passed", "executed_cells": len(outputs), "observed_runs": 2,
        "parser_scenario_states": 10, "captured_turns": 22,
        "micro_f1": {mode: build(mode, 0)["stats"]["micro avg"]["f1-score"] for mode in ("correct", "broken")},
        "checks": "hand-counted observed matrices, original lab metric agreement, all scenario counts/states/traces, highlighted FN record, archive/source integrity",
    }, indent=2))


if __name__ == "__main__":
    main()
