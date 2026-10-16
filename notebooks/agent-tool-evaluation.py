# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#     "marimo==0.25.1",
#     "marimo-studio==0.3.0",
#     "marimo-export==0.1.4",
#     "scikit-learn==1.9.1"
# ]
#
# [tool.marimo-studio]
# default = "post"
#
# [tool.marimo-studio.cells]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="More tools, more ways to be wrong")


@app.cell
def imports():
    import ast
    import json
    import re
    from collections import Counter
    from html import escape
    from itertools import zip_longest

    import marimo as mo
    from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, multilabel_confusion_matrix

    return (
        Counter,
        accuracy_score,
        ast,
        classification_report,
        confusion_matrix,
        escape,
        json,
        mo,
        multilabel_confusion_matrix,
        re,
        zip_longest,
    )


@app.cell
def appearance(mo):
    mo.Html("""
    <style>
    .tool-scroll { max-width: 100%; overflow-x: auto; margin: 1rem 0; }
    .tool-table { width: 100%; min-width: 620px; border-collapse: collapse; font-size: .85rem; line-height: 1.6; }
    .tool-table caption { text-align: left; font-weight: 700; margin-bottom: .65rem; }
    .tool-table th, .tool-table td { text-align: left; padding: .6rem .5rem;
      border-bottom: 1px solid #ccd5da; vertical-align: top; }
    .tool-table thead th { background: #eef2f5; }
    .tool-table thead th[colspan] { border-bottom: 2px solid #9fb3bd; }
    .tool-table tbody th { font-weight: 500; }
    .tool-table code { white-space: normal; overflow-wrap: anywhere; }
    .tool-table td { font-variant-numeric: tabular-nums; }
    .tool-table mark { background: #fbe1d4; color: inherit; padding: .1rem .35rem; }
    .tool-label { font-weight: 700; margin: 1.6rem 0 .3rem; }
    .tool-full { width: 100%; min-width: 560px; border-collapse: collapse; font-variant-numeric: tabular-nums; }
    .tool-full th, .tool-full td { border: 1px solid #ccd5da; padding: .45rem .5rem; }
    .tool-full thead th { background: #eef2f5; font: .75rem/1.3 "Source Code Pro", monospace; text-align: left; vertical-align: bottom; }
    .tool-full tbody th { background: #f7f9fa; font: 400 .78rem/1.35 "Source Code Pro", monospace; text-align: left; }
    .tool-full td { text-align: center; font-size: 1rem; font-weight: 700; }
    .tool-full td.zero { color: #9aa9b0; font-weight: 400; }
    .tool-full td.agree { background: #dfece8; }
    .tool-full td.error { background: #fbe1d4; }
    .tool-full td.focus { box-shadow: inset 0 0 0 2px #b15a3c; }
    .tool-full .axis, .tool-full .none { font: italic .8rem/1.3 "Noto Sans", sans-serif; color: #495a65; }
    .tool-matrices { display: grid; grid-template-columns: repeat(auto-fill, minmax(144px, 1fr)); gap: .75rem; margin: .75rem 0 1.25rem; }
    .tool-matrix { margin: 0; padding: .6rem; border: 1px solid #ccd5da; }
    .tool-matrix.is-marked { border: 2px solid #b15a3c; }
    .tool-matrix figcaption { font: .8rem/1.35 "Source Code Pro", monospace; min-height: 2.7em; margin-bottom: .4rem; }
    .tool-matrix-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2px; }
    .tool-matrix-grid span { padding: .3rem .45rem; background: #f2f5f7; color: #495a65; font-size: .78rem; line-height: 1.3; }
    .tool-matrix-grid b { display: block; color: #213448; font-size: 1.25rem; font-variant-numeric: tabular-nums; }
    .tool-matrix-grid .agree { background: #dfece8; }
    .tool-matrix-grid .error { background: #fbe1d4; }
    .tool-matrix-grid .focus { box-shadow: inset 0 0 0 2px #b15a3c; }
    .tool-matrix p { margin: .45rem 0 0; font-size: .85rem; line-height: 1.5; font-variant-numeric: tabular-nums; }
    .tool-stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: .9rem 1.5rem; margin: 1rem 0 1.5rem; }
    .tool-stats div { border-top: 2px solid #547b8b; padding-top: .4rem; }
    .tool-stats .is-bad { border-top-color: #b15a3c; }
    .tool-stats dt { font-size: .85rem; line-height: 1.4; color: #495a65; }
    .tool-stats dd { margin: .2rem 0 0; font: 700 1.25rem/1.3 "Montserrat", sans-serif; font-variant-numeric: tabular-nums; }
    .tool-confusion { width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: .9rem; }
    .tool-confusion th, .tool-confusion td { border: 1px solid #ccd5da; padding: .7rem; text-align: left; vertical-align: top; }
    .tool-confusion thead th { background: #eef2f5; }
    .tool-confusion b { display: block; font-size: 1.4rem; font-variant-numeric: tabular-nums; }
    .tool-confusion .focus { background: #fff0e7; box-shadow: inset 0 0 0 2px #b15a3c; }
    .tool-routes { display: grid; grid-template-columns: max-content 1fr; gap: .7rem 1rem; align-items: center; margin: 1.25rem 0; }
    .tool-routes > p { margin: 0; font-weight: 700; }
    .tool-route { display: flex; flex-wrap: wrap; gap: .4rem; margin: 0; padding: 0; list-style: none; }
    .tool-route li { display: flex; align-items: center; gap: .4rem; margin: 0; }
    .tool-route li + li::before { content: "→"; color: #495a65; }
    .tool-route span { padding: .1rem .65rem; border: 1px solid #3f6676; border-radius: 999px; font: .85rem/1.6 "Source Code Pro", monospace; }
    .tool-route .write { background: #3f6676; color: #fff; }
    .tool-route .repeat { background: #b15a3c; border-color: #b15a3c; color: #fff; }
    .tool-record { border-left: 4px solid #b15a3c; padding: .2rem 0 .2rem 1.2rem; margin: 1.6rem 0; }
    .tool-record h3 { font: 500 1.15rem/1.4 "Montserrat", sans-serif; margin: .2rem 0 .8rem; }
    .tool-record-label { color: #934426; font-weight: 700; font-size: .8rem; letter-spacing: .04em; text-transform: uppercase; margin: 0; }
    .tool-trace { white-space: pre-wrap; overflow-wrap: anywhere; padding: .8rem 1rem; background: #f2f5f7;
      color: #213448; border: 1px solid #d9e0e3; font: .8rem/1.7 "Source Code Pro", monospace; margin: .3rem 0 .9rem; }
    .tool-trace-error { background: #fff0e7; border-color: #dbb8a8; }
    .tool-record p { margin: .7rem 0; }
    .tool-record blockquote, .tool-turn blockquote { margin: .3rem 0 .9rem; padding: .1rem 0 .1rem .9rem;
      border-left: 3px solid #ccd5da; font-style: italic; }
    .tool-scenario { font: 500 1.15rem/1.4 "Montserrat", sans-serif; margin: 2rem 0 .2rem; }
    .tool-turn { border-top: 1px solid #ccd5da; padding: .7rem 0; }
    .tool-turn summary { cursor: pointer; font-weight: 700; }
    .tool-turn summary:focus-visible { outline: 3px solid #b15a3c; outline-offset: 3px; }
    @media (max-width: 560px) {
      .tool-routes { grid-template-columns: 1fr; }
      .tool-full { min-width: 460px; }
      .tool-full th, .tool-full td { padding: .35rem .3rem; }
      .tool-confusion th, .tool-confusion td { padding: .5rem; font-size: .8rem; }
    }
    </style>
    """)
    return


@app.cell
def title(mo):
    mo.md(r"""
    # More tools, more ways to be wrong: evaluating an agent's workflow

    *Mateusz Kubaszek · October 16, 2026 · AI agents · Evaluation*
    """)
    return


@app.cell(hide_code=True, expand_output=True)
def tools_matrix_illustration(mo):
    # Embedded once in the Studio HTML; keep alt text and caption identical.
    mo.image(
        mo.notebook_location() / "assets/tool-evaluation/tools-matrix-sketch.webp",
        alt='Hand-drawn six-by-six matrix with Status, Records, Approve, Labs, Surgery and None on both the Expected and Called axes, beside a small robot.',
        caption='Expected tools down the rows, called tools across the columns. This is a sketch; the report below contains the recorded counts.',
        rounded=True,
    )
    return


@app.cell
def opening(mo):
    mo.md(r"""
    After my [post about the confusion matrix](/blog/agent-confusion-matrix/),
    someone asked: what happens when the agent has several functions? Five,
    ten, a few dozen? What else should we measure so that the numbers still
    tell us something useful?

    That post evaluated single decisions. Here, the agent works through a
    conversation with several tools and a sequence of actions. It can choose
    the right function and pass the wrong patient ID. It can call every
    expected function and still leave the wrong result. It can take a
    different route and arrive at the same result.

    I kept the hospital admissions example and built a marimo laboratory with
    five tools, a small golden set and a deliberately broken parser. What
    surprised me was how quickly the report pointed at the code around the model.

    We will build that report in layers: **which tools, how many calls,
    and what actually changed**.
    """)
    return


@app.cell
def golden_set_story(mo):
    mo.md(r"""
    ## 1. Turn the golden set into a conversation

    The [previous post ended with a golden set](/blog/agent-confusion-matrix/#improvement)
    of reviewed decisions. For a tool-calling agent, each reference case
    needs more context. A patient may already be on the ward, a test may
    have been ordered in an earlier turn, or missing documentation may
    mean the process should stop.

    I extend each case with the **starting state, consecutive user turns,
    expected calls and expected final state**. Now we can evaluate a whole
    business scenario and find the point where it diverged.

    Historical failures are useful here too. Keep the observed conversation
    and annotate the expected behaviour separately: which call was missing,
    which arguments needed correcting, which state should have stayed
    unchanged. A second model can help draft those annotations; I review
    them before a scenario enters the reference set.

    My laboratory uses five small, authored scenarios:

    - **Happy path:** admission, lab tests, surgery.
    - **Already on the ward:** no repeated admission approval.
    - **Senior patient:** tests before admission.
    - **On hold:** incomplete documentation, so check the status and stop.
    - **Full workflow:** a status check after each step.

    These are teaching fixtures with invented patient records. The same
    structure can hold reviewed conversations from a real system.
    """)
    return


@app.cell
def golden_record(mo):
    mo.md(r"""
    One turn from the laboratory looks like this:

    ```python
    Turn(
        prompt="Check the medical records of patient 12345 first, "
               "then assign lab CBC for patient 12345.",
        expected_calls=[
            ("search_patient_data", {"query": "12345"}),
            ("assign_patient_labs", {
                "lab_name": "CBC", "patient_id": "12345"
            }),
        ],
    )
    ```

    A full `Record` groups consecutive turns, a patient ID and a `snapshot`
    of the fields we expect at the end. Before each scenario, the evaluator
    resets the data. Within a scenario, it keeps the conversation history and
    the effects of earlier calls.

    If you write integration tests, this should feel familiar: start from a
    known state, run the interaction, inspect the result. The laboratory runs
    a real model against mocked tools; an end-to-end test can extend the same
    idea through the actual application and its integrations.
    """)
    return


@app.cell
def labels_story(mo):
    mo.md(r"""
    ## 2. Apply the matrix to each tool

    Our labels are now the functions available to the agent:

    ```python
    labels = [
        "get_patient_status",
        "search_patient_data",
        "approve_patient_request",
        "assign_patient_labs",
        "assign_patient_surgery",
    ]
    ```

    If every request needed exactly one tool, one larger matrix would be
    enough: expected tools on the rows, called tools on the columns, correct
    choices on the diagonal. But our example turn needs **two** tools.
    Several labels can be true for the same turn, so tool presence is a
    **multilabel** problem: each turn becomes a row of 0s and 1s, one column
    per tool.

    Here is that turn from the recorded run with the corrected parser. The
    model checked the patient's status instead of looking up the records,
    then ordered the lab. One turn produces all four outcomes:

    | Tool | Expected | Called | Outcome |
    |:---|:---:|:---:|:---|
    | `get_patient_status` | 0 | 1 | FP |
    | `search_patient_data` | 1 | 0 | FN |
    | `approve_patient_request` | 0 | 0 | TN |
    | `assign_patient_labs` | 1 | 1 | TP |
    | `assign_patient_surgery` | 0 | 0 | TN |

    The lab reads this in two matrices.

    **One matrix with all tools.** Rows are expected tools, columns are
    called tools. Matching names go on the diagonal. An expected name without
    a matching call goes to the *nothing called* column, an unexpected call
    to the *nothing expected* row. When both remain in one turn, the lab
    pairs them in order. Our turn puts the lab order on the diagonal and pairs
    the missing record lookup with the extra status check: row
    `search_patient_data`, column `get_patient_status`. That pairing shows
    where to look. It does not prove that the agent confused those two
    functions; the trace has to show that. This matrix counts call
    occurrences.

    **One 2×2 matrix per tool.**
    [scikit-learn's multilabel_confusion_matrix](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.multilabel_confusion_matrix.html)
    takes the 0/1 rows and returns TP, FP, FN and TN for each function: the
    matrix from the previous post, applied to each tool. Its unit is **one
    conversation turn**. A tool called three times in a turn still counts as
    present once; section 5 counts repetitions.
    """)
    return


@app.cell
def scoring_story(mo):
    mo.md(r"""
    ## 3. Read the scores across functions

    Under each tool's matrix we keep [precision and recall](/blog/agent-confusion-matrix/#metrics)
    from the previous post and add two numbers: **F1**, their harmonic mean,
    and **support**, the number of turns that expected the function (`TP + FN`).

    To summarise several tools, **micro F1** pools TP, FP and FN across tools
    before computing F1, so frequently expected tools weigh more. **Macro F1**
    computes F1 per tool and takes the unweighted mean, so a rarely used
    function counts as much as a common one. The
    [classification report documentation](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.classification_report.html)
    describes both averages.

    This lab uses `zero_division=0`, so a displayed zero can hide an undefined
    ratio. With the broken parser below, `assign_patient_labs` is never called:
    its precision is 0/0 and shows as 0.000. Read scores together with the
    counts and support.

    There is also a stricter question per turn: **did the entire set of tool
    names match?** With multilabel input,
    [accuracy_score](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html)
    reports this as **subset accuracy**. The turn above fails it, even though
    the lab order is right and three of its five tool decisions agree.

    I keep both views: per-tool matrices to locate the failing function, and
    whole-turn matches to see how often the agent produced the complete set.
    Neither checks arguments or call order yet.
    """)
    return


@app.cell
def parser_story(mo):
    mo.md(r"""
    ## 4. The report pointed at my parser

    While building this example, I asked AI to help write the code that
    exposes Python functions to the model and parses its tool calls. With the
    broken parser, every write function falls off the diagonal. All expected
    calls of `approve_patient_request`, `assign_patient_labs` and
    `assign_patient_surgery` land in the *nothing called* column, and their
    own columns stay empty.

    That gives us a specific function and the turns where it should have
    appeared. Between the model's answer and the function execution, there
    is more code than the model:

    ```text
    Python function → tool schema → model response → parser → execution
    ```

    The lab converts signatures and docstrings into schemas with
    `get_json_schema`. The parser reads a Python-style list of calls. Its
    broken version uses a regular expression that assumes one call inside
    the list. With several calls, it keeps the first function name and
    merges the remaining arguments into it.
    """)
    return


@app.cell(hide_code=True, expand_output=True)
def parser_workflow_illustration(mo):
    # Embedded once in the Studio HTML; keep alt text and caption identical.
    mo.image(
        mo.notebook_location() / "assets/tool-evaluation/parser-workflow-sketch.webp",
        alt='A robot sends record, laboratory and surgery symbols through a Parser funnel toward Tools; two symbols fall aside as a person checks a reference clipboard.',
        caption='A model response still has to pass through the parser before a tool can run.',
        rounded=True,
    )
    return


@app.cell
def parser_demonstration(
    build_observed_report,
    escape,
    format_calls,
    full_matrix,
    goldenset,
    mo,
    parse_tool_calls,
    parse_tool_calls_broken,
    run_traces,
):
    # Actual second turn of the first scenario, captured from lab0.app.run().
    broken_record = next(trace for trace in run_traces if trace["parser"] == "parse_tool_calls_broken" and trace["turn_index"] == 2)
    parser_sample = next(message["content"] for message in broken_record["messages"] if message["role"] == "assistant")
    parser_correct = parse_tool_calls(parser_sample)
    parser_broken = parse_tool_calls_broken(parser_sample)
    _error = next(message["content"] for message in broken_record["messages"] if message["role"] == "tool" and message["content"].startswith("Error:"))
    _final_reply = broken_record["messages"][-1]["content"]
    _expected = goldenset[0]["turns"][1]["expected_calls"]
    _report = build_observed_report("broken", 0)
    _writes = ("approve_patient_request", "assign_patient_labs", "assign_patient_surgery")
    mo.Html(
        f'<p class="tool-label">Broken-parser run: expected vs called tools, {_report["expected_total"]} expected calls in {_report["turns"]} turns</p>'
        + full_matrix(_report["pair_labels"], _report["pair_matrix"], focus={(name, "-") for name in _writes})
        + '<div class="tool-record" id="broken-record"><p class="tool-record-label">Happy path · turn 2 · patient 12345</p>'
        + '<h3>The lab order disappears between response and execution</h3>'
        + f'<blockquote>{escape(broken_record["prompt"])}</blockquote>'
        + '<b>Expected calls</b><pre class="tool-trace">' + escape(format_calls(_expected)) + '</pre>'
        + '<b>Raw model response</b><pre class="tool-trace">' + escape(parser_sample) + '</pre>'
        + '<b>Broken parser output</b><pre class="tool-trace tool-trace-error">' + escape(format_calls(broken_record["calls"])) + '</pre>'
        + '<b>Tool result</b><pre class="tool-trace tool-trace-error">' + escape(_error) + '</pre>'
        + '<b>Reply to the user</b><blockquote>' + escape(_final_reply) + '</blockquote>'
        + '<p>The model did emit <code>assign_patient_labs</code>. The parser dropped it and attached '
          '<code>lab_name</code> to <code>get_patient_status</code>, which rejected it. The reply still says the records '
          'were retrieved, although no call in this turn succeeded. At the end of the scenario, <code>assigned_labs</code> '
          'is <code>[]</code> instead of <code>["CBC"]</code>.</p>'
        + '<p>Separately, the model chose a status check where the reference expects a record lookup. That is a '
          'routing mistake; correct parsing does not fix it.</p></div>'
    )
    return


@app.cell
def parser_lesson(mo):
    mo.md(r"""
    The replacement uses `ast.parse` and `ast.literal_eval` for this limited
    call format. It keeps multiple calls, and parentheses or commas inside
    string arguments. Parsing a name does not validate the arguments, so we
    still need schema validation before dispatching a call.

    Read the matrix by rows. Expected calls that never happened sit in the
    *nothing called* column; in the tool's own 2×2 matrix they are **false
    negatives**, not true negatives. `assign_patient_labs` has 4 there, so FN 4.
    A row of zeros would mean the reference never expected the tool: its
    support is zero. That is a coverage gap in the scenarios, not evidence
    that the tool works.

    The cell `search_patient_data` → `get_patient_status` holds 5, in the same
    five turns, with either parser. That is the model choosing a status check
    instead of a record lookup, and fixing the parser does not move it.
    Switch the parser in the report below and watch which cells change.

    The matrices also count **attempts**. One of the three `get_patient_status`
    calls on the diagonal comes from the last turn of the full workflow, where
    the call failed with a `TypeError`. The right name in the right turn says
    nothing about execution.

    That is what I want from evaluation: a short route from “something looks
    wrong” to an input I can reproduce. The matrix narrows the search; the raw
    response, parsed calls and execution results establish the cause.

    Together, these counts and checks let me see whether an expected scenario
    actually played out and, if it did not, find the turn where execution
    diverged. The parser is only one possible source of trouble. A method
    might be called with the wrong patient ID or test name even when parsing
    succeeds and every expected tool appears in the report. Comparing expected
    and actual arguments, tool results and final state helps locate that error.

    That gives this approach a wide range of uses. The same pattern can check
    an order, a booking, a document-processing flow or a support conversation:
    define the expected actions and outcomes, count what happened, then inspect
    the mismatches. Each failed scenario becomes a concrete case to investigate
    and keep as a regression test.
    """)
    return


@app.cell
def outcomes_story(escape, mo, observed_data):
    _threshold = 0.85  # the lab report's illustrative cutoff
    _groups = {}
    for _scenario in observed_data["runs"]["correct"]["scenarios"]:
        _key = (_scenario["count_scores"]["fp"] == _scenario["count_scores"]["fn"] == 0, _scenario["final_state_score"] >= _threshold)
        _groups.setdefault(_key, []).append(_scenario["name"].split(":")[0])

    def _cell(key, focus=False):
        names = _groups.get(key, [])
        css = ' class="focus"' if focus else ''
        return f'<td{css}><b>{len(names)}</b>{escape(", ".join(names))}</td>'

    _crosstab = (
        '<table class="tool-confusion"><thead><tr><th scope="col">Scenarios</th>'
        '<th scope="col">Final state ≥ 0.85</th><th scope="col">Final state &lt; 0.85</th></tr></thead><tbody>'
        f'<tr><th scope="row">Call counts match</th>{_cell((True, True))}{_cell((True, False))}</tr>'
        f'<tr><th scope="row">Call counts differ</th>{_cell((False, True), focus=True)}{_cell((False, False))}</tr>'
        '</tbody></table>'
    )
    _broken = observed_data["runs"]["broken"]["scenarios"][0]
    mo.Html(mo.md(r"""
    ## 5. The calls matched. Did the result?

    Suppose every expected tool name appeared. Did we order the correct test
    for the correct patient? The laboratory checks three layers:

    | Layer | What we compare | What can still slip through |
    |:---|:---|:---|
    | Tool presence per turn | Sets of function names | Wrong arguments, repeated calls, wrong order |
    | Call counts per scenario | Counts of each function name | Wrong arguments or order; calls in the wrong turn |
    | Final state | Selected fields against the expected snapshot | Unchecked fields, bad intermediate actions, unnecessary reads |

    The scenario score uses `Counter`, so two lab orders count as two calls.
    Matched occurrences are TP, extra ones FP, missing ones FN. These
    **call-count metrics** have a different unit from the per-turn matrices,
    and no useful TN: there is no fixed set of absent occurrences.

    The final-state score is the fraction of expected snapshot fields that
    match exactly. The lab also checks that no other patient changed, so a
    correct target snapshot cannot hide an accidental change elsewhere.

    Crossing the two checks gives another small matrix. Following the lab's
    report, a scenario passes the state check at a score of 0.85 or more.
    For the corrected-parser run:
    """).text + _crosstab + mo.md(f"""
    Only one scenario matches the expected call counts, yet three more reach
    the expected state through different calls. Section 6 opens one of them.
    The 0.85 cutoff is illustrative: three matching fields establish only
    those three assertions, and for a critical field I would require an
    explicit pass.

    The lab also reports embedding similarity between the actual and the
    expected snapshot, using a Sentence Transformer. That measures
    [similarity between embeddings](https://www.sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html),
    not correctness. In the broken run, the happy-path snapshot scores
    **{_broken["snapshot_similarity"]:.3f}** while
    **{_broken["matched_fields"]}/{_broken["total_fields"]}** of its fields
    match. For structured state, compare the fields directly.
    """).text)
    return


@app.cell
def alternative_story(escape, goldenset, mo, observed_data):
    _record = goldenset[-1]
    _scenario = observed_data["runs"]["correct"]["scenarios"][-1]
    _short_names = {"search_patient_data": "records", "get_patient_status": "status", "assign_patient_labs": "labs", "approve_patient_request": "approve", "assign_patient_surgery": "surgery"}
    _reads = {"search_patient_data", "get_patient_status"}

    def _route(calls):
        seen, items = [], []
        for name, args in calls:
            css = "" if name in _reads else "repeat" if [name, args] in seen else "write"
            seen.append([name, args])
            items.append(f'<li><span class="{css}">{escape(_short_names.get(name, name))}</span></li>')
        return f'<ol class="tool-route">{"".join(items)}</ol>'

    _expected = [list(call) for turn in _record["turns"] for call in turn["expected_calls"]]
    _actual = [list(call) for calls in _scenario["turn_calls"] for call in calls]
    _routes = f'<div class="tool-routes"><p>Expected</p>{_route(_expected)}<p>Observed</p>{_route(_actual)}</div>'
    mo.Html(mo.md(r"""
    ## 6. A different route can reach the same state

    Here is the full-workflow scenario from the corrected-parser run. Filled
    steps write patient state, outlined steps only read it, and the orange
    step repeats an earlier write.
    """).text + _routes + mo.md(f"""
    The agent made **{_scenario['actual_count']} calls against {_scenario['expected_count']} expected**.
    Its call-count F1 is **{_scenario['count_scores']['f1']:.3f}**, while
    **{_scenario['matched_fields']}/{_scenario['total_fields']} final-state fields match**.
    The differences explain the gap:

    - It assigned the surgery twice. The mock tool overwrites the same field,
      so the snapshot cannot show the duplicate; the sequence can. In a real
      system, a repeated write can mean a second order.
    - It checked the status once, instead of after each step as the user
      asked. Status checks only read state, so the snapshot cannot show that
      either.
    - It looked up the records before every write. That follows the lab's
      system prompt: *“Before you call approve_patient_request,
      assign_patient_labs or assign_patient_surgery, always call
      search_patient_data with the patient ID first.”* The reference looks
      them up only once. Read strictly, the golden trace breaks that rule
      and needs review too.

    This is why I treat the agent as a small state machine, a graph of
    transitions. The golden trace is one route through it. Another route can
    be acceptable if it meets the required conditions; if it also reaches the
    same result with fewer calls, it is a candidate improvement. Here, the
    final state alone would have hidden the repeated write.
    """).text)
    return


@app.cell
def experiment_intro(mo):
    mo.md(r"""
    ### Inspect the recorded model runs

    Everything below comes from running the original `lab0.py` with
    `LiquidAI/LFM2-1.2B-Tool`: five scenarios and 11 turns, once with each
    parser. These are two recorded passes on teaching fixtures, not an
    estimate of performance on production traffic.

    With the parser fixed, every remaining presence error falls into two
    patterns. In five turns, the model checked the status where the reference
    expected a record lookup: the cell `search_patient_data` →
    `get_patient_status`, or FP 5 and FN 5 in the per-tool matrices. In the
    already-on-the-ward scenario, it looked up the records and never ordered
    the lab or the surgery.

    Choose a run and a scenario to find these in the turns. Which scenarios
    do not change between parsers? Where do call-count F1 and the final
    state disagree?
    """)
    return


@app.cell
def controls(goldenset, mo):
    parser_mode = mo.ui.dropdown(
        options={"Broken parser · results_broken": "broken", "Corrected parser · results": "correct"},
        value="Broken parser · results_broken", label="Recorded run", full_width=True,
    )
    scenario_choice = mo.ui.dropdown(
        options={record["name"]: index for index, record in enumerate(goldenset)},
        value=goldenset[0]["name"], label="Scenario", full_width=True,
    )
    mo.vstack([parser_mode, scenario_choice])
    return parser_mode, scenario_choice


@app.cell
def continuous_story(mo):
    mo.md(r"""
    ## 7. Put evaluation at the steps where decisions happen

    A final report says whether the scenario worked. In a longer conversation,
    I also want the first divergence: perhaps step two never ordered the test,
    so step three never had the result it needed.

    That needs **turn-level and call-level evidence** in the decision log from
    the previous post: relevant state, the raw model response, parsed calls,
    validated arguments, tool results and the state after execution. Store the
    schema and parser versions beside the model and prompt versions. Then each
    step can be compared with the same point in the golden scenario.

    Some checks can run immediately, both after a prompt or parser change and
    in a running system: schema validation, execution errors, the target
    patient, a required lookup before a write. Others need a delayed outcome
    or a person to annotate the conversation. Leave those labels pending until
    that evidence exists.

    Once the correctness checks pass, record calls, latency and cost as well.
    Then two acceptable routes can be compared by what they cost to execute.
    """)
    return


@app.cell
def learning_story(mo):
    mo.md(r"""
    ## 8. The agent changes. The evaluation set should grow too

    The review loop from the previous post gets another job: finding missing
    scenarios and acceptable routes through the workflow.

    A random sample of historical conversations shows ordinary traffic. Add
    targeted samples for failures that are easy to miss: rare functions,
    failed tool calls, human corrections and new paths through the workflow.
    Annotate whether the task succeeded, what should have happened and which
    transitions were required. A failed interaction becomes a regression case;
    a valid alternative path, after review, an accepted solution.

    Keep the production-like sample and the collection of difficult cases
    separate. A set filled with rare failures is useful for regression
    testing, but its pass rate does not estimate how often the system
    succeeds. Report case counts and per-tool support with every score: two
    successful examples are still only two examples.

    Keep the development/held-out split from the previous post, and version
    the scenario set so that two agent versions are compared on the same
    cases. When model outputs vary, repeat the runs and report the variation.

    That is the habit I want: pick a real scenario, inspect it, annotate it
    and put what we learned back into the tests. The next missing function
    should have somewhere to show up.
    """)
    return


@app.cell
def run_lab(mo):
    mo.md(r"""
    ## 9. Run the full laboratory

    [Download the marimo laboratory](/downloads/agent-tool-evaluation-lab.zip),
    unpack it and run in that folder:

    ```bash
    uv sync
    uv run marimo edit lab0.py
    ```

    It runs `LiquidAI/LFM2-1.2B-Tool` with MLX on Apple silicon, plus a
    Sentence Transformer for the similarity scores; the first run downloads
    both models. `scenarios.py` holds a wider catalogue of 20 scenarios;
    `lab0.py` evaluates its own five.

    Compare the two parser reports in this order: per-tool support, missing
    and extra calls, then the state checks. When the name scores look
    suspiciously good, read the arguments.

    The archive also contains the recorded `lab-observed.json` and
    `lab-traces.json` used on this page, and `capture-tool-evaluation.py`
    to record a fresh run:

    ```bash
    uv run python capture-tool-evaluation.py --lab . --output lab-observed.json
    ```

    This page recomputes every metric from those recorded calls. Its source
    is the [blog notebook](https://github.com/mkubasz/mkubasz.github.io/blob/main/notebooks/agent-tool-evaluation.py).
    """)
    return


@app.cell
def parsers_from_lab(ast, re):
    # The two original parser implementations, exercised on the same response.
    def parse_tool_calls(text: str) -> list[tuple[str, dict[str, str]]]:
        """'[a(x="1"), b(y=2)]' -> [('a', {'x': '1'}), ('b', {'y': '2'})]

        LFM2 returns calls as a Python-style list. Parsing with ast handles parentheses and commas inside strings.
        """
        match = re.search('\\[\\s*[a-zA-Z_]\\w*\\(.*\\)\\s*\\]', text, re.S)
        if not match:
            return []
        try:
            calls = ast.parse(match.group(), mode='eval').body.elts
            return [(c.func.id, {kw.arg: str(ast.literal_eval(kw.value)) for kw in c.keywords}) for c in calls]
        except (SyntaxError, ValueError, AttributeError):
            return []

    def parse_tool_calls_broken(text: str) -> list[tuple[str, dict[str, str]]]:
        """Intentionally broken exercise: compare its matrices with parse_tool_calls and find the bug."""
        match = re.search('\\[([a-zA-Z_]\\w*)\\((.*?)\\)\\]', text)
        if not match:
            return []
        name, args_str = match.groups()
        return [(name, {k: v1 or v2 for k, v1, v2 in re.findall('(\\w+)\\s*=\\s*(?:[\'\\"](.*?)[\'\\"]|([^\\s,]+))', args_str)})]

    return parse_tool_calls, parse_tool_calls_broken


@app.cell
def reference_data(json, mo):
    data_root = mo.notebook_location() / "assets/tool-evaluation"
    observed_data = json.loads((data_root / "lab-observed.json").read_text())
    run_traces = json.loads((data_root / "lab-traces.json").read_text())["turns"]
    goldenset = observed_data["records"]
    labels = observed_data["runs"]["correct"]["labels"]
    return goldenset, observed_data, run_traces


@app.cell
def scoring_functions(Counter):
    def score_tools(expected, actual):
        expected, actual = Counter(expected), Counter(actual)
        tp = sum((actual & expected).values())
        fp = sum((actual - expected).values())
        fn = sum((expected - actual).values())
        return {
            "tp": tp, "fp": fp, "fn": fn,
            "precision": tp / (tp + fp) if tp + fp else 0.0,
            "recall": tp / (tp + fn) if tp + fn else 0.0,
            "f1": 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else 0.0,
        }

    return (score_tools,)


@app.cell
def report_function(
    Counter,
    accuracy_score,
    classification_report,
    confusion_matrix,
    goldenset,
    multilabel_confusion_matrix,
    observed_data,
    run_traces,
    score_tools,
    zip_longest,
):
    def build_observed_report(mode, scenario_id):
        run = observed_data["runs"][mode]
        records = goldenset
        scenarios = run["scenarios"]
        all_labels = run["labels"]
        expected_turns = [[name for name, _ in turn["expected_calls"]] for record in records for turn in record["turns"]]
        actual_turns = [[name for name, _ in calls] for scenario in scenarios for calls in scenario["turn_calls"]]
        y_true = [[int(label in turn) for label in all_labels] for turn in expected_turns]
        y_pred = [[int(label in turn) for label in all_labels] for turn in actual_turns]
        stats = classification_report(y_true, y_pred, target_names=all_labels, zero_division=0, output_dict=True)
        matrices = multilabel_confusion_matrix(y_true, y_pred)
        rows = []
        for label, ((tn, fp), (fn, tp)) in zip(all_labels, matrices):
            s = stats[label]
            rows.append([label, int(tp), int(fp), int(fn), int(tn), s["precision"], s["recall"], s["f1-score"], int(s["support"])])
        pairs = []
        for expected_names, actual_names in zip(expected_turns, actual_turns):
            expected_counts, actual_counts = Counter(expected_names), Counter(actual_names)
            pairs.extend((name, name) for name in (actual_counts & expected_counts).elements())
            # As in lab0.py: pair leftover names in order; '-' marks a missing or extra call.
            pairs.extend(zip_longest((expected_counts - actual_counts).elements(), (actual_counts - expected_counts).elements(), fillvalue="-"))
        pair_labels = all_labels + ["-"]
        pair_matrix = confusion_matrix([e for e, _ in pairs], [a for _, a in pairs], labels=pair_labels)
        record = records[scenario_id]
        scenario = scenarios[scenario_id]
        actual = scenario["turn_calls"]
        expected = [turn["expected_calls"] for turn in record["turns"]]
        count_scores = score_tools([name for turn in expected for name, _ in turn], [name for turn in actual for name, _ in turn])
        parser_traces = sorted([trace for trace in run_traces if trace["parser"] == run["parser"]], key=lambda trace: trace["turn_index"])
        offset = sum(len(record["turns"]) for record in records[:scenario_id])
        scenario_traces = parser_traces[offset:offset + len(record["turns"])]
        errors = [message["content"] for trace in scenario_traces for message in trace["messages"] if message["role"] == "tool" and message["content"].startswith("Error:")]
        return {
            "mode": mode, "scenario_id": scenario_id, "name": record["name"],
            "tool_rows": rows, "stats": stats, "matrices": matrices.tolist(),
            "pair_labels": pair_labels, "pair_matrix": pair_matrix.tolist(), "expected_total": sum(map(len, expected_turns)),
            "subset_accuracy": float(accuracy_score(y_true, y_pred)),
            "turns": len(y_true), "expected": expected, "actual": actual,
            "count_scores": count_scores,
            "expected_count": sum(map(len, expected)), "actual_count": sum(map(len, actual)),
            "trajectory_matches": actual == expected,
            "state": {"snapshot": scenario["snapshot"], "other_patients_unchanged": scenario["other_patients_unchanged"], "errors": errors},
            "matched_fields": sum(scenario["snapshot"][key] == value for key, value in record["snapshot"].items()),
            "total_fields": len(record["snapshot"]), "expected_snapshot": record["snapshot"],
            "snapshot_similarity": scenario["snapshot_similarity"], "traces": scenario_traces,
        }

    return (build_observed_report,)


@app.cell
def calculation(build_observed_report, parser_mode, scenario_choice):
    selected_report = build_observed_report(parser_mode.value, scenario_choice.value)
    return (selected_report,)


@app.cell
def html_helpers(escape, json):
    def html_table(caption, headers, rows):
        """headers is a list of column names, or prebuilt <tr> rows for a grouped header."""
        head = headers if isinstance(headers, str) else '<tr>' + ''.join(f'<th scope="col">{escape(str(value))}</th>' for value in headers) + '</tr>'
        body = ''.join(f'<tr><th scope="row">{row[0]}</th>' + ''.join(f'<td>{value}</td>' for value in row[1:]) + '</tr>' for row in rows)
        return (
            f'<div class="tool-scroll" tabindex="0" role="region" aria-label="{escape(caption)}">'
            f'<table class="tool-table"><caption>{escape(caption)}</caption>'
            f'<thead>{head}</thead><tbody>{body}</tbody></table></div>'
        )

    def format_calls(calls):
        lines = [f'{name}({", ".join(f"{key}={json.dumps(value)}" for key, value in args.items())})' for name, args in calls]
        return "\n".join(lines) or "no calls"

    def stat_list(items):
        """items: (label, value, needs attention)."""
        stats = ''.join(f'<div class="{"is-bad" if bad else ""}"><dt>{escape(label)}</dt><dd>{value}</dd></div>' for label, value, bad in items)
        return f'<dl class="tool-stats">{stats}</dl>'

    def tool_matrices(tool_rows, focus=None):
        """One 2x2 presence matrix per tool; focus=(tool, outcome) outlines one cell."""
        figures = []
        for label, tp, fp, fn, tn, precision, recall, f1, support in tool_rows:
            cells = []
            for outcome, value, kind in (("TP", tp, "agree"), ("FP", fp, "error"), ("FN", fn, "error"), ("TN", tn, "")):
                css = " ".join(filter(None, [kind if value else "", "focus" if focus == (label, outcome) else ""]))
                cells.append(f'<span class="{css}">{outcome}<b>{value}</b></span>')
            marked = " is-marked" if focus and focus[0] == label else ""
            figures.append(
                f'<figure class="tool-matrix{marked}"><figcaption><code>{escape(label).replace("_", "_<wbr>")}</code></figcaption>'
                f'<div class="tool-matrix-grid">{"".join(cells)}</div>'
                f'<p><b>F1 {f1:.3f}</b><br>P {precision:.3f} · R {recall:.3f}<br>support {support}</p></figure>'
            )
        return f'<div class="tool-matrices">{"".join(figures)}</div>'

    def full_matrix(labels, matrix, focus=()):
        """Expected tools (rows) vs called tools (columns); the last label is '-', no pair."""
        names = [f'<code>{escape(label).replace("_", "_<wbr>")}</code>' for label in labels[:-1]]
        head = ''.join(f'<th scope="col">{name}</th>' for name in names) + '<th scope="col" class="none">nothing called</th>'
        body = []
        for i, (row_name, row) in enumerate(zip(names + ['<span class="none">nothing expected</span>'], matrix)):
            cells = []
            for j, value in enumerate(row):
                css = "zero" if not value else "agree" if i == j else "error"
                css += " focus" if (labels[i], labels[j]) in focus else ""
                cells.append(f'<td class="{css}">{value}</td>')
            body.append(f'<tr><th scope="row">{row_name}</th>{"".join(cells)}</tr>')
        return (
            '<div class="tool-scroll" tabindex="0" role="region" aria-label="Expected versus called tools">'
            f'<table class="tool-full"><thead><tr><th scope="col" class="axis">expected ↓<br>called →</th>{head}</tr></thead>'
            f'<tbody>{"".join(body)}</tbody></table></div>'
        )

    return format_calls, full_matrix, html_table, stat_list, tool_matrices


@app.cell
def recorded_report(
    escape,
    format_calls,
    full_matrix,
    html_table,
    mo,
    selected_report,
    stat_list,
    tool_matrices,
):
    _r = selected_report
    _scores = _r["count_scores"]
    _run = "Broken-parser run" if _r["mode"] == "broken" else "Corrected-parser run"
    _state_rows = [[
        f'<code>{escape(key)}</code>',
        f'<code>{escape(repr(_r["state"]["snapshot"][key]))}</code>',
        f'<code>{escape(repr(value))}</code>',
        'yes' if _r["state"]["snapshot"][key] == value else '<mark>no</mark>',
    ] for key, value in _r["expected_snapshot"].items()]
    _turn_html = []
    for _index, (_expected, _actual, _trace) in enumerate(zip(_r["expected"], _r["actual"], _r["traces"]), 1):
        _highlight = _r["mode"] == "broken" and _r["scenario_id"] == 0 and _index == 2
        _errors = sum(message["role"] == "tool" and message["content"].startswith("Error:") for message in _trace["messages"])
        _summary = f'Turn {_index} · {len(_actual)} called / {len(_expected)} expected'
        _summary += f' · {_errors} tool error{"s" if _errors > 1 else ""}' if _errors else ''
        _summary += ' · record from section 4' if _highlight else ''
        _raw = '\n\n'.join(message['role'].upper() + '\n' + message['content'] for message in _trace['messages'])
        _turn_html.append(
            f'<details class="tool-turn"{" open" if _highlight else ""}><summary>{_summary}</summary>'
            f'<blockquote>{escape(_trace["prompt"])}</blockquote>'
            f'<b>Expected calls</b><pre class="tool-trace">{escape(format_calls(_expected))}</pre>'
            f'<b>Parsed calls</b><pre class="tool-trace">{escape(format_calls(_actual))}</pre>'
            f'<b>Model and tool messages</b><pre class="tool-trace">{escape(_raw)}</pre></details>'
        )
    _subset_hits = round(_r["subset_accuracy"] * _r["turns"])
    mo.Html(
        f'<p class="tool-label">{_run}: expected vs called tools, {_r["expected_total"]} expected calls in {_r["turns"]} turns</p>'
        + full_matrix(_r["pair_labels"], _r["pair_matrix"])
        + '<p class="tool-label">The same run as one 2×2 matrix per tool</p>'
        + tool_matrices(_r["tool_rows"])
        + stat_list([
            ("Micro F1", f'{_r["stats"]["micro avg"]["f1-score"]:.3f}', False),
            ("Macro F1", f'{_r["stats"]["macro avg"]["f1-score"]:.3f}', False),
            ("Turns with the exact tool set", f'{_subset_hits}/{_r["turns"]}', _subset_hits < _r["turns"]),
        ])
        + f'<h3 class="tool-scenario">{escape(_r["name"])}</h3>'
        + stat_list([
            ("Calls, expected → actual", f'{_r["expected_count"]} → {_r["actual_count"]}', _r["expected_count"] != _r["actual_count"]),
            ("Matched · extra · missing", f'{_scores["tp"]} · {_scores["fp"]} · {_scores["fn"]}', _scores["fp"] + _scores["fn"] > 0),
            ("Call-count F1", f'{_scores["f1"]:.3f}', _scores["f1"] < 1),
            ("State fields matched", f'{_r["matched_fields"]}/{_r["total_fields"]}', _r["matched_fields"] < _r["total_fields"]),
            ("Other patients unchanged", 'yes' if _r["state"]["other_patients_unchanged"] else 'no', not _r["state"]["other_patients_unchanged"]),
            ("Tool errors", len(_r["state"]["errors"]), bool(_r["state"]["errors"])),
            ("Same calls, arguments, order", 'yes' if _r["trajectory_matches"] else 'no', not _r["trajectory_matches"]),
        ])
        + html_table('Final state', ['Field', 'Actual', 'Expected', 'Match'], _state_rows)
        + ''.join(_turn_html)
    )
    return


@app.cell
def observed_overview(escape, html_table, mo, observed_data):
    _correct = observed_data["runs"]["correct"]["scenarios"]
    _broken = observed_data["runs"]["broken"]["scenarios"]

    def _state(scenario):
        value = f'{scenario["matched_fields"]}/{scenario["total_fields"]}'
        return value if scenario["matched_fields"] == scenario["total_fields"] else f'<mark>{value}</mark>'

    _rows = [[
        escape(_good["name"]), _good["expected_count"], _good["actual_count"], _bad["actual_count"],
        f'{_good["count_scores"]["f1"]:.3f}', f'{_bad["count_scores"]["f1"]:.3f}', _state(_good), _state(_bad),
    ] for _good, _bad in zip(_correct, _broken)]
    _head = (
        '<tr><th scope="col" rowspan="2">Scenario</th><th scope="colgroup" colspan="3">Calls</th>'
        '<th scope="colgroup" colspan="2">Call-count F1</th><th scope="colgroup" colspan="2">State fields matched</th></tr>'
        '<tr>' + ''.join(f'<th scope="col">{name}</th>' for name in ['expected', 'corrected', 'broken', 'corrected', 'broken', 'corrected', 'broken']) + '</tr>'
    )
    mo.Html(html_table('Scenario results by parser', _head, _rows))
    return


if __name__ == "__main__":
    app.run()
