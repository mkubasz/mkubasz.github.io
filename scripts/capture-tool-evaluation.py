"""Run the supplied Marimo lab unchanged and save its observed model outputs.

Use the lab's Python environment:
    /path/to/eval_tools/.venv/bin/python scripts/capture-tool-evaluation.py --lab /path/to/eval_tools
"""

import argparse
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime, timezone
from functools import wraps
import hashlib
import importlib.util
from importlib.metadata import version
import json
from pathlib import Path
import platform
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lab", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "notebooks/assets/tool-evaluation/lab-observed.json")
    args = parser.parse_args()
    lab = args.lab.resolve()
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    traces_path = output.with_name("lab-traces.json")
    source_files = ["lab0.py", "agent_loop.py", "scenarios.py", "main.py", "pyproject.toml", "uv.lock"]
    hashes = {name: hashlib.sha256((lab / name).read_bytes()).hexdigest() for name in source_files}
    started = datetime.now(timezone.utc).isoformat()
    timer = time.perf_counter()
    sys.path.insert(0, str(lab))

    import agent_loop

    original_runner = agent_loop.run_agent
    traces = []
    counts = {}

    @wraps(original_runner)
    def observed_runner(messages, tools, model, tokenizer, *runner_args, **kwargs):
        mode = kwargs.get("parse", agent_loop.parse_tool_calls).__name__
        counts[mode] = counts.get(mode, 0) + 1
        turn = counts[mode]
        offset = len(messages)
        prompt = messages[-1]["content"]
        turn_started = time.perf_counter()
        print(f"{mode}: turn {turn}/11 started", flush=True)
        calls = original_runner(messages, tools, model, tokenizer, *runner_args, **kwargs)
        traces.append({
            "parser": mode, "turn_index": turn, "prompt": prompt,
            "calls": deepcopy(calls), "messages": deepcopy(messages[offset:]),
            "elapsed_seconds": round(time.perf_counter() - turn_started, 4),
        })
        traces_path.write_text(json.dumps({"started_at": started, "source_sha256": hashes, "turns": traces}, ensure_ascii=False, indent=2) + "\n")
        print(f"{mode}: turn {turn}/11 finished · {len(calls)} calls · {traces[-1]['elapsed_seconds']:.1f}s", flush=True)
        return calls

    agent_loop.run_agent = observed_runner
    spec = importlib.util.spec_from_file_location("supplied_eval_tools_lab", lab / "lab0.py")
    notebook = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = notebook
    spec.loader.exec_module(notebook)
    print("Running lab0.app.run(): real LFM2 inference and both original parser reports.", flush=True)
    outputs, values = notebook.app.run()
    records = values["goldenset"]
    labels = [tool.__name__ for tool in values["tools"]]
    runs = {}
    for key, result_name, parser_name in (
        ("correct", "results", "parse_tool_calls"),
        ("broken", "results_broken", "parse_tool_calls_broken"),
    ):
        results = values[result_name]
        scenarios = []
        for record, (turn_calls, snapshot, no_side_effects) in zip(records, results):
            expected = [name for turn in record.turns for name, _ in turn.expected_calls]
            actual = [name for calls in turn_calls for name, _ in calls]
            scores = values["score_tools"](expected, actual)
            matched = sum(snapshot[k] == value for k, value in record.snapshot.items())
            scenarios.append({
                "name": record.name, "turn_calls": turn_calls,
                "snapshot": snapshot, "other_patients_unchanged": no_side_effects,
                "count_scores": scores, "expected_count": len(expected), "actual_count": len(actual),
                "matched_fields": matched, "total_fields": len(record.snapshot),
                "final_state_score": matched / len(record.snapshot),
                "snapshot_similarity": values["similarity"](snapshot, record.snapshot),
            })
        all_labels = list(dict.fromkeys(labels + [name for scenario in scenarios for calls in scenario["turn_calls"] for name, _ in calls]))
        true = [[int(label in [name for name, _ in turn.expected_calls]) for label in all_labels] for record in records for turn in record.turns]
        pred = [[int(label in [name for name, _ in calls]) for label in all_labels] for scenario in scenarios for calls in scenario["turn_calls"]]
        stats = values["classification_report"](true, pred, target_names=all_labels, zero_division=0, output_dict=True)
        matrices = values["multilabel_confusion_matrix"](true, pred).tolist()
        runs[key] = {"parser": parser_name, "labels": all_labels, "scenarios": scenarios, "classification_report": stats, "matrices": matrices}
        print(json.dumps({"run": key, "micro_f1": stats["micro avg"]["f1-score"], "macro_f1": stats["macro avg"]["f1-score"], "scenarios": [{"name": s["name"], "calls": s["actual_count"], "count_f1": s["count_scores"]["f1"], "final_state": s["final_state_score"]} for s in scenarios]}), flush=True)

    assert hashes == {name: hashlib.sha256((lab / name).read_bytes()).hexdigest() for name in source_files}, "Lab source changed during capture"
    result = {
        "schema": 1, "kind": "observed_model_run",
        "started_at": started, "finished_at": datetime.now(timezone.utc).isoformat(),
        "elapsed_seconds": round(time.perf_counter() - timer, 4),
        "model": "LiquidAI/LFM2-1.2B-Tool",
        "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
        "python": platform.python_version(), "platform": platform.system(), "machine": platform.machine(),
        "packages": {name: version(name) for name in ["marimo", "mlx-lm", "mlx", "sentence-transformers", "transformers", "scikit-learn"]},
        "source_sha256": hashes,
        "generation": {"max_steps_per_turn": 8, "max_tokens_per_generation": 256, "sampling": "unchanged defaults in agent_loop.py", "seed": "not overridden"},
        "records": [asdict(record) for record in records],
        "runs": runs,
        "trace_file": "lab-traces.json",
        "executed_cells": len(outputs),
    }
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(f"Saved observed run: {output}", flush=True)


if __name__ == "__main__":
    main()
