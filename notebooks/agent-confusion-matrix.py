# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#     "marimo==0.25.1",
#     "marimo-studio==0.3.0",
#     "numpy>=2.0,<3"
# ]
#
# [tool.marimo-studio]
# default = "post"
#
# [tool.marimo-studio.cells]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="Four outcomes, different consequences")


@app.cell
def imports():
    import marimo as mo
    import numpy as np
    from html import escape

    return escape, mo, np


@app.cell
def appearance(mo):
    mo.Html("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Caveat:wght@500;600&display=swap');
    .eval-sketchboard { margin: 1.6rem 0; color: #253951; }
    .eval-sketchgrid { display: grid; grid-template-columns: repeat(auto-fit,minmax(min(100%,230px),1fr)); gap: 14px; }
    .eval-sketchgrid-four { grid-template-columns: repeat(2,minmax(0,1fr)); }
    .eval-sketchpanel { min-width: 0; }
    .eval-sketchpanel svg { display: block; width: 100%; max-width: 360px; height: auto; margin: auto; }
    .eval-sketchtitle { font: 600 1.65rem/1.3 Caveat,cursive; margin: 0 0 .7rem; }
    .eval-figure { margin: 1.5rem 0; padding: 1rem; border: 1px solid #ccd5da;
      background: #fff; color: #213448; border-radius: 3px; }
    .eval-figure svg { display: block; width: 100%; height: auto; }
    .eval-caption { font-size: .85rem; line-height: 1.65; color: #495a65; margin: .8rem 0 0; }
    .eval-scroll { overflow-x: auto; }
    .eval-matrix { border-collapse: collapse; width: 100%; font-size: .9rem; line-height: 1.5; }
    .eval-matrix caption { text-align: left; font-weight: 700; margin-bottom: 1rem; }
    .eval-matrix th, .eval-matrix td { padding: 1rem .7rem; border: 1px solid #ccd5da; vertical-align: top; }
    .eval-matrix thead th { background: #eef2f5; }
    .eval-matrix tbody th { width: 25%; text-align: left; font-weight: 500; }
    .eval-matrix td { width: 37.5%; }
    .eval-matrix .correct { background: #eef5f0; }
    .eval-matrix .error { background: #fff1e9; }
    .eval-matrix b { display: block; font-size: 1.1rem; margin-bottom: .35rem; }
    .eval-stats { display: grid; grid-template-columns: repeat(2, minmax(0,1fr)); gap: .7rem; margin: 1rem 0; }
    .eval-stat { border-top: 3px solid #547b8b; background: #f2f5f7; padding: .8rem; color: #213448; }
    .eval-stat strong { display: block; font-size: 1.5rem; font-variant-numeric: tabular-nums; }
    .eval-stat small { display: block; color: #495a65; font-variant-numeric: tabular-nums; }
    .eval-ledger { width: 100%; border-collapse: collapse; font-size: .8rem; }
    .eval-ledger th, .eval-ledger td { text-align: left; padding: .5rem; border-bottom: 1px solid #ccd5da; }
    .eval-ledger th[scope="row"] { white-space: nowrap; }
    @media(max-width: 560px) {
      .eval-sketchgrid-four { grid-template-columns: 1fr; }
      .eval-matrix { font-size: .78rem; }
      .eval-matrix th, .eval-matrix td { padding: .6rem .4rem; }
      .eval-stats { grid-template-columns: repeat(2,minmax(0,1fr)); }
      .eval-figure { padding: .6rem; }
    }
    </style>
    """)
    return


@app.cell
def title(mo):
    # The Studio view has this title in its static header; this cell is for the standalone notebook.
    mo.md(r"""
    # Four outcomes, different consequences: evaluating AI agents with a confusion matrix

    *Mateusz Kubaszek · October 12, 2026 · AI agents · Evaluation*
    """)
    return


@app.cell
def opening(mo):
    mo.md(r"""
    In the prehistoric days, before LLMs became everyone's favorite topic,
    we were already evaluating models. Classical machine learning, deep learning,
    statistics: there was a whole toolbox for checking whether a model was useful.

    IT has its cycles. We discover a new way to build systems, then rediscover
    some good old methods for checking them. We are doing that with AI agents.

    One of those methods is the **confusion matrix**. A small table. Four possible
    outcomes. Quite a lot of information about whether our agent makes the right
    decisions.

    Let's look at patients, email offers and investment proposals. In each case,
    the agent can say yes or no. But a wrong yes and a wrong no have very different
    consequences. **Which mistake hurts us, and how do we improve the system?**

    By the end, we will be able to name the four outcomes of an agent's decision,
    pick the metric that matches the expensive mistake, choose a threshold for it,
    and say what AUC does not settle.

    This continues the practical approach from
    [What temperature does to a softmax](/blog/softmax-temperature/).
    Here, we will change a decision threshold instead of sampling temperature.
    """)
    return


@app.cell
def four_outcomes(mo):
    mo.md(r"""
    ## 1. The agent did something. Was it supposed to?

    The agent admitted a patient, prepared an offer or called a tool. Fine.
    Activity alone does not tell us whether the decision was correct.

    We compare **what the agent decided** with **what should have happened**.
    That second answer is our reference label, often called **ground truth**.
    The agent's own explanation does not establish it.

    First, define the **positive class**: the condition we want to detect.
    Positive does not mean “good.” Here it means admission is needed, an offer
    is relevant, or a proposal passes a suitability check.

    | | Actually positive | Actually negative |
    |---|---|---|
    | **Agent says yes** | **True positive (TP):** correctly says yes | **False positive (FP):** incorrectly says yes |
    | **Agent says no** | **False negative (FN):** incorrectly says no | **True negative (TN):** correctly says no |

    A tool call can succeed technically and still be a false positive:
    the agent successfully did something it should never have done.
    """)
    return


@app.cell
def evaluation_functions(np):
    def confusion_counts(labels, scores, threshold):
        labels = np.asarray(labels, dtype=int)
        scores = np.asarray(scores, dtype=float)
        predicted = scores >= threshold
        actual = labels == 1
        return {
            "TP": int(np.sum(predicted & actual)),
            "FP": int(np.sum(predicted & ~actual)),
            "FN": int(np.sum(~predicted & actual)),
            "TN": int(np.sum(~predicted & ~actual)),
        }

    def classification_metrics(counts):
        def ratio(numerator, denominator):
            return numerator / denominator if denominator else None

        tp, fp, fn, tn = (counts[key] for key in ("TP", "FP", "FN", "TN"))
        return {
            "accuracy": ratio(tp + tn, tp + fp + fn + tn),
            "recall": ratio(tp, tp + fn),
            "precision": ratio(tp, tp + fp),
            "fpr": ratio(fp, fp + tn),
        }

    def roc_coordinates(labels, scores):
        # Every distinct score is a threshold; equal scores move together.
        thresholds = np.concatenate(([np.inf], np.unique(scores)[::-1]))
        points = [classification_metrics(confusion_counts(labels, scores, t)) for t in thresholds]
        fpr = np.array([point["fpr"] for point in points], dtype=float)
        tpr = np.array([point["recall"] for point in points], dtype=float)
        auc = float(np.trapezoid(tpr, fpr))
        return fpr, tpr, auc

    def percent(value):
        return "undefined" if value is None else f"{100 * value:.1f}%"

    return classification_metrics, confusion_counts, percent, roc_coordinates


@app.cell
def illustrative_data(np, roc_coordinates):
    # Intentionally invented, fixed scores. No patient, customer, or market data.
    positive_scores = np.array([
        .98, .95, .92, .90, .88, .85, .83, .80, .77, .74,
        .71, .68, .64, .60, .55, .50, .45, .40, .30, .20,
    ])
    negative_scores = np.concatenate((
        np.linspace(.02, .34, 60), np.linspace(.36, .78, 18), [.84, .93],
    ))
    scores = np.concatenate((positive_scores, negative_scores))
    labels = np.concatenate((np.ones(20, dtype=int), np.zeros(80, dtype=int)))
    roc_fpr, roc_tpr, ranking_auc = roc_coordinates(labels, scores)
    contexts = {
        "Patient admission": {
            "positive": "Admission needed", "negative": "Admission not needed",
            "yes": "Recommend admission", "no": "Do not recommend admission",
            "descriptions": {
                "TP": "Needed admission; correctly flagged.",
                "FP": "Did not need admission; flagged anyway.",
                "FN": "Needed admission; missed by the agent.",
                "TN": "Did not need admission; correctly not flagged.",
            },
            "suggested": .35,
            "priority": "Missed admission cases are the expensive mistake in this toy policy.",
        },
        "Email offers": {
            "positive": "Offer relevant", "negative": "Offer not relevant",
            "yes": "Recommend an offer", "no": "Skip the offer",
            "descriptions": {
                "TP": "Relevant offer; correctly recommended.",
                "FP": "Irrelevant offer; recommended anyway.",
                "FN": "Relevant offer; opportunity missed.",
                "TN": "Irrelevant offer; correctly skipped.",
            },
            "suggested": .80,
            "priority": "Unwanted offers are the expensive mistake. This pool has already passed the permission gate.",
        },
        "Investment proposals": {
            "positive": "Passes suitability check", "negative": "Fails suitability check",
            "yes": "Recommend for review", "no": "Skip the proposal",
            "descriptions": {
                "TP": "Suitable proposal; correctly flagged for review.",
                "FP": "Unsuitable proposal; incorrectly recommended.",
                "FN": "Suitable proposal; opportunity missed.",
                "TN": "Unsuitable proposal; correctly skipped.",
            },
            "suggested": .80,
            "priority": "Unsuitable proposals cost more here. A recommendation does not execute a trade.",
        },
    }
    return contexts, labels, ranking_auc, roc_fpr, roc_tpr, scores


@app.cell
def matrix_renderer(escape):
    def render_matrix(context, counts, caption):
        cells = {}
        for key in ("TP", "FP", "FN", "TN"):
            css = "correct" if key in ("TP", "TN") else "error"
            cells[key] = (
                f'<td class="{css}"><b>{key} · {counts[key]}</b></td>'
            )
        return (
            '<div class="eval-figure"><div class="eval-scroll">'
            '<table class="eval-matrix">'
            f'<caption>{escape(caption)}</caption><thead><tr><th scope="col">Agent decision ↓ / Reality →</th>'
            f'<th scope="col">{escape(context["positive"])}</th>'
            f'<th scope="col">{escape(context["negative"])}</th></tr></thead><tbody>'
            f'<tr><th scope="row">{escape(context["yes"])}</th>{cells["TP"]}{cells["FP"]}</tr>'
            f'<tr><th scope="row">{escape(context["no"])}</th>{cells["FN"]}{cells["TN"]}</tr>'
            '</tbody></table></div></div>'
        )

    return (render_matrix,)


@app.cell
def sketch_renderer(escape):
    def sketch_board(title, panels, caption, height=280):
        # The previous post's sketch vocabulary: Caveat, navy ink, irregular
        # strokes and pale blue/green/coral. All text and geometry stay here.
        cards = []
        for label, drawing, explanation in panels:
            cards.append(
                '<div class="eval-sketchpanel">'
                f'<svg viewBox="0 0 260 {height}" role="img" aria-label="{escape(label, quote=True)}" aria-description="{escape(explanation, quote=True)}">'
                f'<rect width="260" height="{height}" rx="5" fill="#f9faf8"/>'
                '<g fill="#253951" font-family="Caveat,cursive" font-size="23" '
                'stroke-linecap="round" stroke-linejoin="round">'
                f'{drawing}</g></svg></div>'
            )
        return (
            '<div class="eval-sketchboard">'
            f'<p class="eval-sketchtitle">{escape(title)}</p>'
            f'<div class="eval-sketchgrid{" eval-sketchgrid-four" if len(panels) == 4 else ""}">' + ''.join(cards) + '</div>'
            f'<p class="eval-caption">{escape(caption)}</p>'
            '</div>'
        )

    return (sketch_board,)


@app.cell
def patient_story(mo):
    mo.md(r"""
    ## 2. A patient needs admission. The agent says no.

    Imagine an agent helping a clinician decide which patients need admission.
    **Positive means admission is needed**, according to a reviewed clinical
    reference. In the drawings below, a cast is only our marker for those cases;
    a cast by itself does not decide whether somebody needs a ward bed.

    **Decision**

    - **TP — recommend admission:** the patient needs it. A correct flag.
    - **TN — do not recommend admission:** the patient does not need it. A correct rejection.
    - **FP — recommend admission:** the patient does not need it. An unnecessary review.
    - **FN — do not recommend admission:** the patient needs it. A missed case that could delay care.

    In this example, the missed case is the mistake we especially want to avoid.
    The four sketches show the difference. Then we count those outcomes across
    100 invented patients. The agent gives each case a score from 0 to 1 and
    says yes from 0.35 up; we return to that cut-off in section 6.
    """)
    return


@app.cell
def patient_comic(mo):
    # Alt and caption are repeated in the Studio view, which embeds this image statically.
    mo.image(
        mo.notebook_location() / "assets/agent-evaluation/patient.webp",
        alt="An AI triage robot tells a patient on crutches with a leg cast: You are perfectly healthy!",
        caption="A false negative, exaggerated: the agent says no to somebody who needs help.",
        rounded=True,
    )
    return


@app.cell
def patient_outcome_sketch(mo, sketch_board):
    _panels = []
    for _key, _yes, _needed, _explanation in [
        ("TP", True, True, "The reference says admission is needed. The agent flags the case."),
        ("FP", True, False, "The agent flags a case that does not need admission. An unnecessary review."),
        ("FN", False, True, "The agent says no to a case that needs admission. This is the missed case."),
        ("TN", False, False, "Admission is not needed, and the agent correctly says no."),
    ]:
        _color = "#46775d" if _key in ("TP", "TN") else "#ba684f"
        _fill = "#e5efe7" if _key in ("TP", "TN") else "#f7e6dd"
        _cast = (
            '<path d="M88 148 L107 172 L118 174 L115 181 L100 179 L80 160 Z" fill="#deebf4" stroke="#253951" stroke-width="1.8"/>'
            '<path d="M92 155 L103 152 M98 163 L109 160 M104 170 L115 167" fill="none" stroke="#537d9b" stroke-width="1.5"/>'
            '<path d="M54 104 L48 178 M43 115 L63 115 M44 178 L53 178" fill="none" stroke="#253951" stroke-width="2"/>'
        ) if _needed else '<path d="M82 144 L103 177 M104 177 L114 177" fill="none" stroke="#253951" stroke-width="2"/>'
        _drawing = (
            f'<text x="16" y="32" font-size="29">{_key}: agent says {"YES" if _yes else "NO"}</text>'
            '<path d="M16 44 Q129 49 241 43" fill="none" stroke="#253951" stroke-width="1.5"/>'
            '<circle cx="80" cy="83" r="17" fill="#fff" stroke="#253951" stroke-width="1.8"/>'
            '<path d="M78 101 Q73 123 82 144 M77 113 L57 135 M80 111 L100 130 M82 144 L72 179 M67 179 L79 179" fill="none" stroke="#253951" stroke-width="2"/>'
            + _cast +
            f'<path d="M135 80 Q185 75 234 81 L232 139 Q180 144 136 138 Z" fill="{_fill}" stroke="{_color}" stroke-width="1.8"/>'
            f'<text x="184" y="115" text-anchor="middle" font-size="29" fill="{_color}">{"flag" if _yes else "skip"}</text>'
            '<path d="M109 124 Q118 115 132 114 M124 108 L133 114 L125 120" fill="none" stroke="#253951" stroke-width="1.8"/>'
            '<text x="16" y="218" font-size="21">Independent reference:</text>'
            f'<text x="16" y="250" font-size="26">admission {"needed" if _needed else "not needed"}</text>'
        )
        _panels.append((f"{_key}: agent {'yes' if _yes else 'no'}, admission {'needed' if _needed else 'not needed'}", _drawing, _explanation))
    mo.Html(sketch_board(
        "The same yes/no action, four different stories", _panels,
        "Four invented cases. The label comes from the independent clinical reference, not from the agent.",
    ))
    return


@app.cell
def patient_matrix(confusion_counts, contexts, labels, mo, render_matrix, scores):
    _counts = confusion_counts(labels, scores, .35)
    mo.Html(render_matrix(contexts["Patient admission"], _counts, "100 patients, yes from a score of 0.35"))
    return


@app.cell
def metrics_intro(mo):
    mo.md(r"""
    ## 3. Four metrics, four different questions

    Each metric looks at a different group. Before dividing, ask whose cases
    belong in the denominator.

    The sketches circle three of those groups in our patient table. The same
    cases appear in more than one group because each metric asks a different
    question. The fourth metric, accuracy, uses all 100 cases.
    """)
    return


@app.cell
def denominator_sketch(classification_metrics, confusion_counts, labels, mo, percent, scores, sketch_board):
    _counts = confusion_counts(labels, scores, .35)
    _metrics = classification_metrics(_counts)
    _panels = []
    for _title, _keys, _numerator, _metric, _question, _explanation in [
        ("Recall", ("TP", "FN"), "TP", "recall", "All admission-needed cases", "Look at the actual positives. A missed patient stays in the denominator."),
        ("Precision", ("TP", "FP"), "TP", "precision", "All cases the agent flagged", "Look at the agent's yes decisions. Unnecessary flags stay in this denominator."),
        ("False positive rate", ("FP", "TN"), "FP", "fpr", "All admission-not-needed cases", "Look at the actual negatives. FPR uses this group, not all recommendations."),
    ]:
        _denominator = sum(_counts[k] for k in _keys)
        _dots = []
        _index = 0
        for _key in _keys:
            _color = {"TP": "#46775d", "FN": "#ba684f", "FP": "#ba684f", "TN": "#537d9b"}[_key]
            for _ in range(_counts[_key]):
                _x, _y = 24 + (_index % 12) * 19, 91 + (_index // 12) * 18
                _dots.append(f'<circle cx="{_x}" cy="{_y}" r="5" fill="{_color}"/>')
                _index += 1
        _drawing = (
            f'<text x="16" y="33" font-size="28">{_title}</text>'
            f'<text x="16" y="64" font-size="20">{_question}</text>'
            '<path d="M12 76 Q130 71 248 77 L246 216 Q129 222 13 216 Z" fill="#eef2ed" stroke="#253951" stroke-width="1.5"/>'
            + ''.join(_dots) +
            f'<text x="17" y="251" font-size="23">{_keys[0]} {_counts[_keys[0]]} + {_keys[1]} {_counts[_keys[1]]}</text>'
            '<path d="M21 264 Q124 272 234 264 M226 259 L236 264 L228 271" fill="none" stroke="#537d9b" stroke-width="1.8"/>'
            f'<text x="17" y="301" font-size="28">{_counts[_numerator]} / {_denominator} = {percent(_metrics[_metric])}</text>'
        )
        _panels.append((_title + ': ' + _question, _drawing, _explanation))
    mo.Html(sketch_board(
        "Before dividing, circle the right group", _panels,
        "The 100 patients from section 2. One dot is one case. Green: TP; coral: FP or FN, as labelled under each box; blue: TN.",
        height=325,
    ))
    return


@app.cell
def metrics_formulas(mo):
    mo.md(r"""
    ### Recall: how many needed cases did we find?

    $$\mathrm{Recall}=\mathrm{TPR}=\frac{TP}{TP+FN}$$

    Look at **every actual positive**, including the missed cases. For patients,
    that means everybody who needed admission. High recall matters when a missed
    case is costly. Saying yes to everybody finds every positive, but creates
    plenty of false positives too.

    ### False positive rate: how many negative cases did we flag?

    $$\mathrm{FPR}=\frac{FP}{FP+TN}$$

    Look at **every actual negative**. Of the patients who did not need admission,
    how many did we flag anyway? Lower is better when those unnecessary reviews
    are costly.

    ### Precision: when the agent says yes, how often is it right?

    $$\mathrm{Precision}=\frac{TP}{TP+FP}$$

    Look at **every yes from the agent**. How many were correct? Notice the
    difference from FPR: precision starts with the recommendations; FPR starts
    with the actual negatives.

    A selective agent can have high precision while missing many useful cases.
    We need recall beside it.

    ### Accuracy: how many decisions were correct overall?

    $$\mathrm{Accuracy}=\frac{TP+TN}{TP+TN+FP+FN}$$

    Count **both correct yes and correct no decisions**. Useful, but it treats
    the two mistakes equally.

    Our patients show the problem. At 0.35 the agent is right in 78 of the 100
    cases. Reject everybody instead: 80 correct, zero recall. A nicer percentage.
    A much poorer system.
    """)
    return


@app.cell
def email_story(mo):
    mo.md(r"""
    ## 4. An email offer has a different expensive mistake

    Now imagine an agent preparing offers. Among people we are allowed to
    contact, **positive means the offer is relevant**.

    **Decision**

    - **TP — recommend the offer:** it is relevant. A useful recommendation.
    - **TN — skip the offer:** it is irrelevant. A correct rejection.
    - **FP — recommend the offer:** it is irrelevant. An unwanted message.
    - **FN — skip the offer:** it is relevant. A lost opportunity.

    Here I would rather miss some opportunities than have the agent become
    annoyingly persistent. We care more about reliable recommendations and fewer
    false positives, so this agent says yes only from a score of 0.80, where the
    patient agent used 0.35.

    **Interest and permission are separate questions.** A recipient who has
    opted out is blocked before any relevance score and never enters this table.
    We return to that gate in section 7.

    The table counts relevance decisions among eligible recipients.
    """)
    return


@app.cell
def email_comic(mo):
    mo.image(
        mo.notebook_location() / "assets/agent-evaluation/email.webp",
        alt="An overeager sales robot launches an offer at a customer who has just pressed Unsubscribe.",
        caption="An unwanted message is this section's false positive. Ignoring an opt-out is a different failure: a permission rule, not a relevance score.",
        rounded=True,
    )
    return


@app.cell
def email_matrix(confusion_counts, contexts, labels, mo, render_matrix, scores):
    _counts = confusion_counts(labels, scores, .80)
    mo.Html(render_matrix(contexts["Email offers"], _counts, "100 eligible recipients, yes from a score of 0.80"))
    return


@app.cell
def email_check(mo):
    mo.md(r"""
    **Your turn.** Compute precision and recall from this table. Then compare
    them with the patients: precision 47.4%, recall 90.0%. What did the higher
    threshold buy, and what did it cost?

    /// details | Check your answer

    Precision = 8 / (8 + 2) = 80%. Recall = 8 / (8 + 12) = 40%.

    The higher threshold cut the false positives from 20 to 2. The price:
    12 relevant offers skipped, where the patient agent missed 2 cases.

    ///
    """)
    return


@app.cell
def investment_story(mo):
    mo.md(r"""
    ## 5. “We invested.” Fine. Should we have?

    An investment agent proposes an action. Counting completed trades tells us
    how active it is, but not whether its recommendations were appropriate.

    Define **positive as a proposal passing an agreed suitability check**, using
    information available when the decision was made.

    **Decision**

    - **TP — recommend the proposal:** it passes the suitability check. A correct recommendation.

    **Your turn.** We have filled this list twice already. Name the other three
    outcomes. Then a harder one: the agent recommends a proposal that fails the
    check, and the price later goes up. Which outcome is that?

    /// details | Check your answer

    - **TN — skip the proposal:** it fails the suitability check. A correct rejection.
    - **FP — recommend the proposal:** it fails the suitability check. An inappropriate recommendation.
    - **FN — skip the proposal:** it passes the suitability check. A missed suitable proposal.

    The harder one is still a **false positive**. The label was fixed when the
    decision was made, and a later gain does not change it.

    ///

    A suitable investment can lose money. An unsuitable one can make money.
    A lucky outcome does not repair a bad recommendation. Evaluate suitability
    against the agreed criteria and track later profit or loss separately.

    The classification also does not replace risk limits or approval to
    execute a trade.
    """)
    return


@app.cell
def investment_comic(mo):
    mo.image(
        mo.notebook_location() / "assets/agent-evaluation/investing.webp",
        alt="An investment robot celebrates high confidence beside a sharply falling stock chart.",
        caption="The price fell. That alone does not make the recommendation a false positive, just as high confidence does not make it a correct one.",
        rounded=True,
    )
    return


@app.cell
def suitability_sketch(mo, sketch_board):
    _panels = []
    for _key, _passes, _up, _explanation in [
        ("FP", False, True, "The proposal fails the agreed toy risk limit, yet the agent recommends it. A later gain does not repair that false positive."),
        ("TP", True, False, "The proposal passes the agreed toy suitability rule and is recommended. A later loss is recorded separately from that classification."),
    ]:
        _color = "#46775d" if _passes else "#ba684f"
        _price_path = "M37 215 L66 202 L91 211 L121 189 L151 198 L191 169 L226 161" if _up else "M37 164 L66 180 L91 172 L121 201 L151 191 L191 215 L226 225"
        _drawing = (
            f'<text x="16" y="32" font-size="28">{_key}: recommended</text>'
            '<text x="16" y="66" font-size="22">At decision time:</text>'
            f'<path d="M16 78 Q126 73 244 79 L242 119 Q127 125 17 120 Z" fill="{"#e5efe7" if _passes else "#f7e6dd"}" stroke="{_color}" stroke-width="1.6"/>'
            f'<text x="29" y="106" font-size="25" fill="{_color}">risk limit {"passed" if _passes else "failed"}</text>'
            '<text x="16" y="151" font-size="22">Later, the price:</text>'
            '<path d="M29 159 L30 234 L238 233" fill="none" stroke="#253951" stroke-width="1.5"/>'
            f'<path d="{_price_path}" fill="none" stroke="{"#46775d" if _up else "#ba684f"}" stroke-width="2.7"/>'
            f'<text x="16" y="274" font-size="25">{_key} stays {_key}. Log the P&amp;L.</text>'
        )
        _panels.append((f"{_key}: risk limit {'passed' if _passes else 'failed'}, later price {'rose' if _up else 'fell'}", _drawing, _explanation))
    mo.Html(sketch_board(
        "A lucky outcome is not a suitability label", _panels,
        "Two invented proposals; positive means passing the predefined suitability check. Later price movement is a separate outcome, never an input to the decision-time label.",
        height=300,
    ))
    return


@app.cell
def threshold_explained(mo):
    mo.md(r"""
    ## 6. A threshold turns a score into a decision

    Suppose the agent gives each case a score. Higher means stronger
    evidence for the positive class. **If the score reaches the threshold,
    the agent says yes. Otherwise, it says no.**

    Lower the threshold: find more positives, but accept more negatives too.
    Raise it: accept fewer cases, and miss more positives. This is the trade-off
    we saw with patients and offers.

    Where does an LLM agent get a score? It can be the probability of the yes
    token (the [previous post](/blog/softmax-temperature/) shows how logits
    become probabilities), a separate small classifier, or the share of yes
    answers across several runs. An agent with no score still gives us one
    confusion matrix and its metrics. We just cannot move a threshold.

    A score is not automatically a probability. An LLM saying “90% confident”
    still needs checking against labelled outcomes.
    """)
    return


@app.cell
def lab_intro(mo):
    mo.md(r"""
    ### Predict first, then move the threshold

    Here are our 100 invented patients again. The slider starts at 0.35,
    the table from section 2. Before you move it, predict:

    1. At a threshold of 0, what are recall and the false positive rate?
    2. How low must the threshold go before no patient is missed? What happens to the false positive rate there?
    3. Does precision always rise with the threshold? Try 0.85, 0.90 and 0.95.
    4. Which threshold gives the best accuracy? Would you run the patient agent there?
    """)
    return


@app.cell
def controls(mo):
    threshold = mo.ui.slider(start=0, stop=100, step=5, value=35, label="Threshold (%)", show_value=True, full_width=True)
    threshold
    return (threshold,)


@app.cell
def selected_result(classification_metrics, confusion_counts, contexts, labels, scores, threshold):
    active_context = contexts["Patient admission"]
    decision_threshold = threshold.value / 100
    active_counts = confusion_counts(labels, scores, decision_threshold)
    active_metrics = classification_metrics(active_counts)
    return active_context, active_counts, active_metrics, decision_threshold


@app.cell
def score_strip(active_context, active_counts, decision_threshold, escape, labels, mo, scores):
    _left, _width = 45, 380
    _x = lambda score: _left + _width * float(score)
    _marks = []
    for _score in scores[labels == 1]:
        _fill = "#35685e" if _score >= decision_threshold else "#b15a3c"
        _marks.append(f'<circle cx="{_x(_score):.1f}" cy="78" r="4.5" fill="{_fill}"/>')
    for _i, _score in enumerate(scores[labels == 0]):
        # Four staggered rows keep the 80 negatives from overlapping.
        _cx, _cy = _x(_score), 146 + (_i % 4) * 11
        _fill = "#b15a3c" if _score >= decision_threshold else "#547b8b"
        _marks.append(f'<path d="M{_cx - 4:.1f} {_cy} L{_cx:.1f} {_cy - 4} L{_cx + 4:.1f} {_cy} L{_cx:.1f} {_cy + 4} Z" fill="{_fill}"/>')
    _tx = _x(decision_threshold)
    _ticks = ''.join(
        f'<text x="{_x(_v):.1f}" y="222" text-anchor="middle">{_v:g}</text>' for _v in (0, .5, 1)
    )
    _c = active_counts
    mo.Html(f"""
    <figure class="eval-figure">
      <svg viewBox="0 28 470 257" role="img" aria-label="All 100 scores with the threshold at {decision_threshold:.2f}: {_c['TP']} true positives, {_c['FN']} false negatives, {_c['FP']} false positives, {_c['TN']} true negatives." xmlns="http://www.w3.org/2000/svg" style="font-family:system-ui,sans-serif;font-size:17px;max-width:560px;margin:auto">
        <g fill="#213448">
          <text x="{_left}" y="52" font-weight="700">{escape(active_context["positive"])}</text>
          <text x="{_left + _width}" y="52" text-anchor="end">FN {_c['FN']} · TP {_c['TP']}</text>
          <text x="{_left}" y="124" font-weight="700">{escape(active_context["negative"])}</text>
          <text x="{_left + _width}" y="124" text-anchor="end">TN {_c['TN']} · FP {_c['FP']}</text>
        </g>
        <path d="M{_left} 200h{_width}" stroke="#82909a"/>
        <g fill="#495a65">{_ticks}</g>
        {''.join(_marks)}
        <path d="M{_tx:.1f} 62V96 M{_tx:.1f} 134V200" stroke="#213448" stroke-width="2" stroke-dasharray="5 4"/>
        <text x="{min(max(_tx, _left + 62), _left + _width - 62):.1f}" y="250" text-anchor="middle" font-weight="700" fill="#213448">threshold {decision_threshold:.2f}</text>
        <text x="{_left}" y="275" fill="#495a65">← agent says no</text>
        <text x="{_left + _width}" y="275" text-anchor="end" fill="#495a65">agent says yes →</text>
      </svg>
      <figcaption class="eval-caption">One mark is one patient, placed by score. Circles needed admission; diamonds did not. Everything on or right of the dashed line gets a yes. Orange marks the two mistakes.</figcaption>
    </figure>
    """)
    return


@app.cell
def live_matrix(active_context, active_counts, mo, render_matrix):
    mo.Html(render_matrix(active_context, active_counts, "Your threshold, the same 100 patients"))
    return


@app.cell
def live_metrics(active_counts, active_metrics, mo, percent):
    _c = active_counts
    _cards = [
        ("Recall", "recall", _c["TP"], _c["TP"] + _c["FN"]),
        ("Precision", "precision", _c["TP"], _c["TP"] + _c["FP"]),
        ("False positive rate", "fpr", _c["FP"], _c["FP"] + _c["TN"]),
        ("Accuracy", "accuracy", _c["TP"] + _c["TN"], sum(_c.values())),
    ]
    _html = ''.join(
        f'<div class="eval-stat"><span>{_label}</span><strong>{percent(active_metrics[_key])}</strong>'
        f'<small>{_numerator} / {_denominator}</small></div>'
        for _label, _key, _numerator, _denominator in _cards
    )
    mo.Html(f'<div class="eval-stats" aria-live="polite">{_html}</div>')
    return


@app.cell
def lab_answers(mo):
    mo.md(r"""
    /// details | Check your predictions

    1. Both are 100%. The agent says yes to everybody.
    2. 0.20. Recall reaches 100% and the false positive rate is 57.5%: 46 of the 80 patients who did not need admission are flagged.
    3. No. Precision is 85.7% at 0.85, 80.0% at 0.90 and 100% at 0.95. With only a handful of yes decisions, one false positive moves it a lot. At 1.00 the agent says yes to nobody, so precision is undefined.
    4. 0.80, with 86% accuracy, where the agent misses 12 of the 20 patients who need admission. Accuracy treats both mistakes equally. We do not.

    ///
    """)
    return


@app.cell
def roc_explained(mo):
    mo.md(r"""
    ### ROC: what happens across thresholds?

    Sweep the threshold and plot **false positive rate horizontally** and
    **recall vertically**. That is the **ROC curve**. Every point is a different
    threshold applied to the same scores. Move the slider and the orange dot
    walks along it.

    Closer to the upper-left corner is better: more true positives, fewer false
    positives. Which point should we choose? That depends on which mistake hurts
    us and how many cases we can review.
    """)
    return


@app.cell
def roc_plot(active_metrics, decision_threshold, mo, ranking_auc, roc_fpr, roc_tpr):
    _left, _top, _size = 85, 60, 330
    _xy = lambda x, y: f"{_left + x * _size:.2f},{_top + (1 - y) * _size:.2f}"
    _points = " ".join(_xy(float(_x), float(_y)) for _x, _y in zip(roc_fpr, roc_tpr))
    _grid = ''.join(
        f'<path d="M{_left + _v * _size},{_top}v{_size} M{_left},{_top + (1-_v) * _size}h{_size}" stroke="#dce3e7"/>'
        f'<text x="{_left + _v * _size}" y="{_top + _size + 24}" text-anchor="middle">{_v:g}</text>'
        f'<text x="{_left - 12}" y="{_top + (1-_v) * _size + 5}" text-anchor="end">{_v:g}</text>'
        for _v in (0, .5, 1)
    )
    _cx = _left + active_metrics["fpr"] * _size
    _cy = _top + (1-active_metrics["recall"]) * _size
    mo.Html(f"""
    <figure class="eval-figure">
      <svg viewBox="0 0 470 475" role="img" aria-label="ROC curve, AUC {ranking_auc:.3f}. Current threshold {decision_threshold:.2f}; FPR {active_metrics['fpr']:.3f}; TPR {active_metrics['recall']:.3f}." xmlns="http://www.w3.org/2000/svg" style="font-family:system-ui,sans-serif;font-size:16px;max-width:560px;margin:auto">
        <text x="85" y="28" font-size="18" font-weight="700" fill="#213448">ROC · AUC {ranking_auc:.2f}</text>
        <g fill="#495a65">{_grid}</g>
        <polygon points="{_points} {_xy(1,0)}" fill="#dcece8" fill-opacity=".6"/>
        <path d="M{_xy(0,0)} L{_xy(1,1)}" fill="none" stroke="#82909a" stroke-dasharray="6 5" stroke-width="2"/>
        <polyline points="{_points}" fill="none" stroke="#35685e" stroke-width="3"/>
        <circle cx="{_cx}" cy="{_cy}" r="8" fill="#b15a3c" stroke="white" stroke-width="2"/>
        <text x="250" y="450" text-anchor="middle" fill="#213448">False positive rate (FPR) →</text>
        <text transform="translate(23,225) rotate(-90)" text-anchor="middle" fill="#213448">True positive rate (recall) →</text>
      </svg>
      <figcaption class="eval-caption">The orange dot follows your threshold. The curve and its area stay fixed.</figcaption>
    </figure>
    """)
    return


@app.cell
def auc_explained(mo):
    mo.md(r"""
    ### AUC: how well do the scores rank cases?

    **AUC is the area under the ROC curve.** It also answers a useful question:
    pick one actual positive and one actual negative. How often does the positive
    get the higher score? A tied pair counts as half.

    Perfect ranking gives AUC 1; chance-level ranking gives 0.5 in expectation.
    AUC describes the ranking, but it does not choose our threshold.

    **Move the threshold and the point moves. The curve and its AUC stay fixed.**
    """)
    return


@app.cell
def auc_pair_sketch(labels, mo, scores, sketch_board):
    _positives, _negatives = scores[labels == 1], scores[labels == 0]
    _panels = []
    for _title, _positive, _negative, _explanation in [
        ("A correctly ranked pair", float(_positives.max()), float(_negatives.max()), "One actual positive outranks one actual negative. This pair contributes 1 to the pairwise average."),
        ("A reversed pair", float(_positives.min()), float(_negatives.max()), "The negative outranks the positive. This pair contributes 0, even if both are accepted at a low threshold."),
    ]:
        _credit = float(_positive > _negative) + .5 * float(_positive == _negative)
        _px, _nx = 26 + 208 * _positive, 26 + 208 * _negative
        _drawing = (
            f'<text x="16" y="33" font-size="24">{_title}</text>'
            f'<text x="16" y="74" font-size="21" fill="#46775d">Actual positive: {_positive:.2f}</text>'
            '<path d="M25 95 Q130 91 235 96" fill="none" stroke="#253951" stroke-width="1.5"/>'
            f'<circle cx="{_px:.2f}" cy="95" r="7" fill="#46775d"/>'
            f'<text x="16" y="140" font-size="21" fill="#537d9b">Actual negative: {_negative:.2f}</text>'
            '<path d="M25 160 Q130 156 235 161" fill="none" stroke="#253951" stroke-width="1.5"/>'
            f'<path d="M{_nx-7:.2f} 160 L{_nx:.2f} 153 L{_nx+7:.2f} 160 L{_nx:.2f} 167 Z" fill="#537d9b"/>'
            '<text x="24" y="185" font-size="18">0</text><text x="231" y="185" font-size="18">1</text>'
            '<path d="M32 202 Q131 215 228 202 M219 197 L230 202 L222 210" fill="none" stroke="#253951" stroke-width="1.7"/>'
            f'<text x="16" y="246" font-size="30">Pair credit: {_credit:g}</text>'
        )
        _panels.append((_title, _drawing, _explanation))
    mo.Html(sketch_board(
        "AUC asks who gets the higher score", _panels,
        "AUC averages these comparisons across positive-negative pairs. Moving the decision threshold leaves the ranking unchanged.",
    ))
    return


@app.cell
def policy_sketch(contexts, mo, scores, sketch_board):
    _panels = []
    _case_score = float(scores[12])
    for _name in ("Patient admission", "Email offers"):
        _threshold = contexts[_name]["suggested"]
        _tx, _sx = 26 + 208 * _threshold, 26 + 208 * _case_score
        _drawing = (
            f'<text x="16" y="33" font-size="28">{"Patients" if _name == "Patient admission" else "Eligible email offers"}</text>'
            f'<text x="16" y="67" font-size="22">Same positive score: {_case_score:.2f}</text>'
            '<path d="M25 110 Q130 106 235 111" fill="none" stroke="#253951" stroke-width="1.7"/>'
            f'<circle cx="{_sx:.2f}" cy="110" r="7" fill="#46775d"/>'
            f'<path d="M{_tx:.2f} 88 Q{_tx-2:.2f} 111 { _tx:.2f} 143" fill="none" stroke="#ba684f" stroke-width="2" stroke-dasharray="4 4"/>'
            '<text x="23" y="137" font-size="18">0</text><text x="230" y="137" font-size="18">1</text>'
            f'<text x="16" y="177" font-size="26">Threshold {_threshold:.2f} → {"YES" if _case_score >= _threshold else "NO"}</text>'
            '<path d="M17 191 Q126 196 239 190" fill="none" stroke="#253951" stroke-width="1.5"/>'
            '<text x="16" y="224" font-size="26" fill="#537d9b">Same ranking</text>'
        )
        _panels.append((f"{_name} at threshold {_threshold:.2f}", _drawing, contexts[_name]["priority"]))
    mo.Html(sketch_board(
        "Same scores. Different expensive mistake.", _panels,
        "Two illustrative policies applied to the same 100 scored cases. The green dot is one actual positive. The coral line is the threshold; scores to its right, including equality, get a yes. These thresholds are examples, not universal optima.",
        height=245,
    ))
    return


@app.cell
def logs_and_labels(mo):
    mo.md(r"""
    ## 7. Collect evidence from day one

    We do not need to wait for fine-tuning to start measuring an agent.
    Define the decision, then keep its score, threshold and action. Record which
    prompt, model and **gateway** produced it. The gateway is the code around the
    agent that checks policy, adds useful information and validates actions.
    Keep human overrides and permission blocks visible too.

    A few rows from the email agent's log could look like this:
    """)
    return


@app.cell
def decision_log(mo):
    _rows = [
        ("r-101", "0.92", "draft offer", "relevant", "TP"),
        ("r-102", "0.84", "draft offer", "not relevant", "FP"),
        ("r-103", "0.64", "skip", "relevant", "FN"),
        ("r-104", "0.31", "skip", "unknown: no reply yet", "not counted yet"),
        ("r-105", "not scored", "blocked: opt-out", "none", "outside the matrix"),
    ]
    _body = ''.join(
        f'<tr><th scope="row">{_row[0]}</th>' + ''.join(f'<td>{_cell}</td>' for _cell in _row[1:]) + '</tr>'
        for _row in _rows
    )
    mo.Html(
        '<div class="eval-figure"><div class="eval-scroll"><table class="eval-ledger">'
        '<thead><tr><th scope="col">Case</th><th scope="col">Score</th><th scope="col">Action at 0.80</th>'
        '<th scope="col">Reference label</th><th scope="col">Counted as</th></tr></thead>'
        f'<tbody>{_body}</tbody></table></div>'
        '<p class="eval-caption">Invented rows. Each one also carries the prompt, model and gateway versions.</p></div>'
    )
    return


@app.cell
def reference_labels(mo):
    mo.md(r"""
    Attach a trusted reference label when it becomes available. Review accepted
    **and rejected** cases, otherwise we can miss the false negatives completely:
    the third row exists only because somebody reviewed a skipped recipient.
    Unknown labels should stay unknown: no reply to an offer does not establish
    that it was irrelevant.

    The last row never enters the matrix. A permission gate requires a valid
    opt-in and no active opt-out before scoring relevance. A high score cannot
    override an opt-out. Check permission again before sending, because it may
    have changed while the draft was waiting.
    """)
    return


@app.cell
def permission_flow(mo, sketch_board):
    _panels = [
        (
            "Opt-out blocks a recipient before relevance is scored",
            '<text x="16" y="32" font-size="28">1. First, permission</text>'
            '<path d="M24 58 L91 59 L93 101 L22 100 Z M24 59 L58 82 L91 59" fill="#deebf4" stroke="#253951" stroke-width="1.8"/>'
            '<path d="M103 81 Q144 73 186 81 M178 74 L188 81 L178 88" fill="none" stroke="#253951" stroke-width="1.8"/>'
            '<path d="M198 53 L223 53 L241 71 L241 95 L223 113 L198 113 L180 95 L180 71 Z" fill="#f7e6dd" stroke="#ba684f" stroke-width="1.8"/>'
            '<text x="209" y="90" text-anchor="middle" font-size="20" fill="#ba684f">STOP</text>'
            '<text x="16" y="148" font-size="25">Active opt-out?</text>'
            '<text x="16" y="180" font-size="26" fill="#ba684f">No contact. No score.</text>'
            '<path d="M19 192 Q122 197 227 191" fill="none" stroke="#ba684f" stroke-width="1.6"/>'
            '<text x="16" y="239" font-size="22">Log: permission block</text>',
            "A recipient fails the permission gate. This is not a relevance false negative.",
        ),
        (
            "An eligible recipient is scored, checked against the threshold and may receive a draft",
            '<text x="16" y="32" font-size="28">2. Then, relevance</text>'
            '<path d="M17 57 Q126 51 241 58 L240 116 Q127 122 18 116 Z" fill="#e5efe7" stroke="#253951" stroke-width="1.6"/>'
            '<text x="30" y="84" font-size="23">Valid opt-in; no opt-out</text>'
            '<text x="30" y="109" font-size="21" fill="#46775d">permission passed</text>'
            '<path d="M127 127 Q120 146 129 161 M122 153 L129 164 L136 153" fill="none" stroke="#253951" stroke-width="1.8"/>'
            '<text x="16" y="190" font-size="23">Toy score 0.92 ≥ 0.80</text>'
            '<text x="16" y="237" font-size="28" fill="#46775d">Prepare a draft</text>',
            "In this separate invented case, permission passes and the relevance score clears the threshold.",
        ),
        (
            "An opt-out after drafting prevents sending",
            '<text x="16" y="32" font-size="28">3. Before sending</text>'
            '<path d="M33 56 L162 59 L159 127 L31 124 Z" fill="#deebf4" stroke="#253951" stroke-width="1.6"/>'
            '<text x="49" y="85" font-size="23">Draft ready</text>'
            '<path d="M48 99 Q91 96 143 101 M48 111 Q91 107 120 112" fill="none" stroke="#537d9b" stroke-width="1.7"/>'
            '<path d="M175 93 Q203 109 211 136 M204 129 L211 139 L218 129" fill="none" stroke="#253951" stroke-width="1.8"/>'
            '<text x="16" y="167" font-size="24">A new opt-out arrived</text>'
            '<text x="16" y="199" font-size="23">Recheck permission</text>'
            '<text x="16" y="243" font-size="28" fill="#ba684f">Block the send</text>',
            "Permission may change while a draft waits. Recheck at execution time and record the block.",
        ),
    ]
    mo.Html(sketch_board(
        "Interested does not mean contactable", _panels,
        "The permission gate, relevance decision and send check are separate steps. A high relevance score never overrides an opt-out.",
    ))
    return


@app.cell
def dashboard_notes(mo):
    mo.md(r"""
    Now the dashboard can show the four outcomes, recall, precision and FPR.
    Compare meaningful groups and time periods. Track tool failures and
    permission violations separately; this small table measures one decision,
    rather than every part of an agent.

    If the agent sends difficult cases to a person, also show how much work it
    handles automatically. Handing everything over can make the metrics look
    excellent while leaving the whole job to somebody else.
    """)
    return


@app.cell
def improvement_loop(mo):
    mo.md(r"""
    ## 8. Now we have something we can improve

    Once we have reviewed mistakes, we can ask what was missing when the agent
    made its decision. There are several practical places to work.

    **The gateway and data.** A missing permission field or stale preference
    in the gateway may matter more than a new LLM. Fix the cause we actually
    found.

    **The prompt.** Use reviewed failure cases to clarify the task, classification
    rules and expected output. Whoever tunes the prompt, a person or an automatic
    prompt optimizer, needs a concrete objective: fewer missed patients within a
    reasonable review load, or fewer unwanted offers while still finding useful
    ones.

    **The model.** With enough reliable examples, fine-tune a model or train a
    smaller classifier. Then measure whether it improves the decisions we care
    about. More training does not establish that by itself.

    A **golden set** is a fixed collection of cases with trusted reference
    labels that every new version is evaluated against. Keep development cases
    separate from a held-out set for the final check. Tuning repeatedly on that
    final set turns it into development data.

    This gives us a useful loop: collect evidence, review mistakes, change the
    right component, test on fresh cases, then monitor the released version.
    Historical logs do not make a model learn by themselves.
    """)
    return


@app.cell
def improvement_flow(mo, sketch_board):
    _panels = [
        (
            "Inspect a traced permission failure before changing the system",
            '<text x="16" y="33" font-size="28">1. Find the cause</text>'
            '<path d="M24 59 L209 55 L214 200 L22 203 Z" fill="#deebf4" stroke="#253951" stroke-width="1.7"/>'
            '<text x="39" y="90" font-size="22">Trace: offer sent</text>'
            '<text x="39" y="122" font-size="22">Opt-out: active</text>'
            '<text x="39" y="154" font-size="22">Gate: missing</text>'
            '<path d="M37 165 Q114 170 189 164" fill="none" stroke="#ba684f" stroke-width="2"/>'
            '<text x="16" y="246" font-size="25">Review the evidence</text>',
            "This trace shows a permission failure. Keep it separate from the relevance confusion matrix.",
        ),
        (
            "Fix the identified permission gate and version the change",
            '<text x="16" y="33" font-size="28">2. Fix that component</text>'
            '<text x="16" y="79" font-size="23">Add the permission gate</text>'
            '<path d="M24 102 Q127 97 233 103 L231 165 Q126 171 25 165 Z" fill="#e5efe7" stroke="#253951" stroke-width="1.7"/>'
            '<text x="42" y="128" font-size="24">active opt-out?</text>'
            '<text x="42" y="154" font-size="25" fill="#ba684f">block before scoring</text>'
            '<path d="M128 178 Q119 192 129 209 M122 201 L129 212 L136 201" fill="none" stroke="#253951" stroke-width="1.8"/>'
            '<text x="16" y="246" font-size="25">Version the change</text>',
            "For this cause, repair the gateway rule and execution-time recheck. A prompt tweak cannot replace them.",
        ),
        (
            "Validate permission behavior and relevance metrics on held-out cases, then monitor",
            '<text x="16" y="33" font-size="28">3. Check fresh cases</text>'
            '<path d="M24 57 L205 61 L211 207 L21 204 Z" fill="#f9faf8" stroke="#253951" stroke-width="1.7"/>'
            '<path d="M38 83 L44 91 L57 74 M38 126 L44 134 L57 117 M38 170 L44 178 L57 161" fill="none" stroke="#46775d" stroke-width="2.3"/>'
            '<text x="66" y="90" font-size="21">Gate + send check</text>'
            '<text x="66" y="133" font-size="21">Held-out relevance</text>'
            '<text x="66" y="177" font-size="21">Agreed criteria</text>'
            '<text x="16" y="246" font-size="25">Release, then monitor</text>',
            "Test the repaired gate separately, evaluate relevance on held-out eligible cases, and monitor after release.",
        ),
    ]
    mo.Html(sketch_board(
        "One observed failure → one targeted repair → fresh evidence", _panels,
        "A concrete gateway example. For other error causes, inspect the labels and four outcomes before choosing enrichment, a prompt change or training. Version the prompt, model, gateway and policy.",
    ))
    return


@app.cell
def transfer_exercise(mo):
    mo.md(r"""
    ## 9. Your turn: an agent that issues refunds

    A support agent decides whether to call `refund_customer`. Nobody gave us
    a table this time. Before opening the answer, decide:

    1. What is the positive class, and where does the reference label come from?
    2. What is a false positive here? A false negative? Which one is expensive?
    3. Which metric would you watch first?
    4. What would you log from day one?

    /// details | One possible answer

    1. Positive: a refund is due under the refund policy. The label comes from a reviewer applying that policy. The agent's explanation does not establish it, and neither does a customer who stopped complaining.
    2. FP: a refund that was not due, so money leaves and abuse gets easier. FN: a refund that was due and got refused, so a customer is treated unfairly. For small amounts the refused customer usually hurts more; for large amounts the wrong payout does.
    3. Recall when refused customers are the expensive mistake, precision when wrong payouts are. Report the other one beside it.
    4. The request, the score if there is one, the threshold, the action and the policy version. Then the reviewer's label, including a sample of the refused requests.

    A limit above which a person must approve is a gateway rule, like the
    permission gate. It stays outside this table.

    ///
    """)
    return


if __name__ == "__main__":
    app.run()
