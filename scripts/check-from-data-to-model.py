"""Check the article's fictional examples, not an LLM's performance.

Run from the repository root:
    uv run --with marimo-studio==0.3.0 --with marimo-export==0.1.4 python scripts/check-from-data-to-model.py
"""

import ast
import importlib.util
import itertools
import json
import re
from html.parser import HTMLParser
from pathlib import Path

import yaml


def main():
    root = Path(__file__).resolve().parents[1]
    path = root / "notebooks/from-data-to-model-1.py"
    spec = importlib.util.spec_from_file_location("from_data_to_model", path)
    notebook = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(notebook)
    outputs, values = notebook.app.run()

    rows = values["offer_rows"]
    split = values["split_report"]
    assert len(rows) == 12 and len({row["id"] for row in rows}) == 12
    assert len({row["group"] for row in rows}) == 6
    bad = split("Split individual rows")
    good = split("Keep groups and time")
    assert bad["crossed"] == ["H-FEB", "H-JAN", "K-FEB", "K-JAN", "T-FEB", "T-JAN"]
    assert len(bad["leaked_rows"]) == 6
    assert not bad["time_ordered"]
    assert {name: len(part) for name, part in bad["parts"].items()} == {"train": 6, "validation": 3, "test": 3}
    assert good["crossed"] == [] and good["leaked_rows"] == []
    assert good["time_ordered"]
    expected_groups = {"train": {"K-JAN", "H-JAN", "T-JAN"}, "validation": {"K-FEB"}, "test": {"H-FEB", "T-FEB"}}
    for name, expected in expected_groups.items():
        assert {row["group"] for row in good["parts"][name]} == expected
    assert {name: len(part) for name, part in good["parts"].items()} == {"train": 6, "validation": 2, "test": 4}
    for report in (bad, good):
        ids = [row["id"] for part in report["parts"].values() for row in part]
        assert sorted(ids) == sorted(row["id"] for row in rows)
        assert len(set(ids)) == len(ids)
        # The new process figure must show the same assignments as the report.
        class DiagramAssignments(HTMLParser):
            def __init__(self):
                super().__init__()
                self.assignments = []

            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                if "data-row-id" in attrs:
                    self.assignments.append((attrs["data-row-id"], attrs["data-part"]))

        diagram = DiagramAssignments()
        diagram.feed(report["diagram_html"])
        expected = {(row["id"], part) for part, records in report["parts"].items() for row in records}
        assert len(diagram.assignments) == 12 and set(diagram.assignments) == expected
        assert len(report["families"]) == 6
        assert [family["records"][0]["observed_at"] for family in report["families"]] == sorted(
            family["records"][0]["observed_at"] for family in report["families"]
        )

    # Time boundaries are checked independently of the report's flag.
    dates = {name: [row["observed_at"] for row in part] for name, part in good["parts"].items()}
    assert max(dates["train"]) < "2026-02-01" <= min(dates["validation"])
    assert max(dates["validation"]) < "2026-02-10" <= min(dates["test"])
    # Repeating a product in a genuinely different promotion is allowed.
    assert {row["group"] for row in rows if row["id"].startswith("K-")} == {"K-JAN", "K-FEB"}

    checkpoint = values["checkpoint_report"]
    expected_resumes = {"Successful variant": None, "Regression after SFT": "base-v1", "Incorrect training data": "data-v1"}
    for scenario, resume in expected_resumes.items():
        result = checkpoint(scenario)
        assert result["resume_from"] == resume
        assert result["html"].count('class="ft-node is-focus"') == 1
    assert checkpoint("Successful variant")["focus"] == "sft-a"

    # Verified encoding fixture: preserve exact pieces, IDs and source identity.
    encoding = values["tokenizer_example"]
    assert encoding["revision"] == "93efa2f097d58c2a74874c7e644dbc9b0cee75a2"
    assert encoding["tokenizer_sha256"] == "9ca9acddb6525a194ec8ac7a87f24fbba7232a9a15ffa1af0c1224fcd888e47c"
    assert not encoding["add_special_tokens"] and not encoding["chat_template_applied"]
    assert encoding["decoded"] == "".join(encoding["decoded_pieces"]) == encoding["text"]
    assert len(encoding["ids"]) == len(encoding["tokens"]) == len(encoding["offsets"]) == 10
    assert all(isinstance(token_id, int) and 0 <= token_id < encoding["model_config"]["vocab_size"] for token_id in encoding["ids"])
    assert [encoding["text"][start:end] for start, end in encoding["offsets"]] == encoding["decoded_pieces"]

    # Every available combination must be prepared, using frontend labels.
    states = yaml.safe_load((root / "notebooks/__marimo__/studio/from-data-to-model-1/post/states.yaml").read_text())
    actual = {(row["checkpoint_choice"][0], row["split_choice"][0]) for row in states["states"].values()}
    expected = set(itertools.product(expected_resumes, ("Split individual rows", "Keep groups and time")))
    assert actual == expected and len(states["states"]) == 6
    initial = states["states"][states["default_state"]]
    assert initial == {"checkpoint_choice": ["Regression after SFT"], "split_choice": ["Split individual rows"]}

    tree = ast.parse(path.read_text())
    prose = [node.args[0].value for node in ast.walk(tree) if isinstance(node, ast.Call)
             and isinstance(node.func, ast.Attribute) and node.func.attr == "md"
             and node.args and isinstance(node.args[0], ast.Constant)]
    print(json.dumps({
        "status": "passed", "executed_cells": len(outputs), "prepared_combinations": len(actual),
        "narrative_words": len(re.findall(r"\b[\w’–-]+\b", " ".join(prose))),
        "promotion_groups": 6, "crossing_groups": {"row_split": len(bad["crossed"]), "group_time_split": 0},
        "checks": "partition integrity, provenance groups, chronological cutoffs, retry ancestry, diagram assignments, tokenizer provenance and round trip, full Prepared state coverage",
    }, indent=2))


if __name__ == "__main__":
    main()
