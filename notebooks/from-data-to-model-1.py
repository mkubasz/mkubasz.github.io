# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#     "marimo==0.25.1",
#     "marimo-studio==0.3.0",
#     "marimo-export==0.1.4"
# ]
#
# [tool.marimo-studio]
# default = "post"
#
# [tool.marimo-studio.cells]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", app_title="Before we fine-tune")


@app.cell
def imports():
    import json
    from collections import defaultdict
    from html import escape
    from pathlib import Path

    import marimo as mo

    return Path, defaultdict, escape, json, mo


@app.cell
def appearance(Path, mo):
    _css = Path(__file__).parent / "__marimo__/studio/from-data-to-model-1/post/figures.css"
    mo.Html(f"<style>{_css.read_text()}</style>")
    return


@app.cell
def title(mo):
    mo.md("""
    # Before we fine-tune: the process behind a good deal

    *Mateusz Kubaszek · October 19, 2026 · From data to a useful model · Part 1*
    """)
    return


@app.cell(hide_code=True)
def market_illustration(Path, mo):
    mo.image(
        Path(__file__).parent / "assets/from-data-to-model-1/market.webp",
        alt="A small robot compares kettles, a coupon and a delivery parcel at a market stall.",
    )
    return


@app.cell
def opening(mo):
    mo.md("""
    Imagine we run a website for people who enjoy finding a good deal. A little
    like Pepper, a Polish deals community: offers arrive, people compare them,
    and the useful ones rise to the top. We add an AI assistant to help with
    the flood of listings. It reads the conditions, checks a shopper's
    preferences and explains which offers deserve attention. Then the
    invoice arrives.

    Every small decision has become a call to a large model. The website is
    busy all day, and the bill keeps growing while we sleep. I would like a
    smaller model that can run on an affordable machine and do this particular
    job well. That is a goal to measure, though: smaller weights alone do not
    tell us the cost of operating the whole service.

    Before opening a training notebook, I want to know what the work actually
    involves. Where do the examples come from? How do we recognise an
    improvement? What happens when the third experiment makes things worse?
    This first article builds that process, then spends most of its time on
    the ingredient every later experiment depends on: the data.

    **The company, offers and outcomes here are fictional.** The two interactive
    examples calculate properties of teaching fixtures; they do not report a
    trained model's performance or a measured saving. You need no training
    experience to follow along. Familiarity with tests and Git will help.
    """)
    return


@app.cell
def process_story(mo):
    mo.md("""
    ## 1. Training is one step in a loop of evidence

    A training run feels like the main event. In practice, it sits between
    decisions about evidence. We decide what success means, assemble examples,
    measure a starting solution, change something and check the result.
    A disappointing result sends us back to the cause, which may be the data,
    the starting model or the training configuration.

    Here is the map I would put on the wall. The route through adaptation is
    optional: a smaller existing model with a good prompt might already meet
    our requirements. Each change gets its own relevant checks, alongside
    shared regression tasks. Publication starts another round of observation.
    """)
    return


@app.cell
def process_map(mo):
    mo.Html("""
    <figure class="ft-process" aria-labelledby="process-caption">
      <ol class="ft-board">
        <li><span>01</span><b>Set the goal</b><small>Tasks, measures, budget</small></li>
        <li><span>02</span><b>Prepare the data</b><small>Sources, labels, split</small></li>
        <li><span>03</span><b>Measure a baseline</b><small>Checkpoint + tokenizer</small></li>
        <li class="ft-optional"><span>04 · optional</span><b>Adapt the model</b><small>CPT, SFT or another method</small></li>
        <li><span>05</span><b>Choose a candidate</b><small>Validation + regressions</small></li>
        <li><span>06</span><b>Test the frozen bundle</b><small>Independent final evaluation</small></li>
        <li><span>07</span><b>Publish and serve</b><small>Model, report, configuration</small></li>
        <li class="ft-feedback"><span>08 → 01 / 02</span><b>Observe and revise</b><small>Failures → next data version</small></li>
      </ol>
      <figcaption id="process-caption">Check data when they change; validate after each adaptation and after conversion or quantization. A failed check sends us to its cause.</figcaption>
    </figure>
    """)
    return


@app.cell
def git_story(mo):
    mo.md("""
    ## 2. Treat experiments like branches in Git

    Suppose two developers branch from the same commit. One change passes
    review; another breaks a test. We keep their common parent and try again
    from a known point. Training experiments benefit from the same habit.

    A **checkpoint** saves model state at a point in training. Two kinds of
    training appear below: supervised fine-tuning (SFT) trains on reviewed
    example answers, and continued pretraining (CPT) does more next-token
    training on domain text. We can start several SFT variants from the
    same parent and compare them on the same validation tasks. A tag is a
    useful name for that snapshot. It does not contain the snapshot, just as
    writing a commit hash on a sticky note does not back up a repository.

    To resume a run faithfully, keep the model and relevant optimizer,
    scheduler and random-number states, plus the data version, code,
    configuration and environment. Starting a new fine-tuning run from saved
    weights is a different operation from resuming an interrupted run.

    Try the three situations below. Where would you return? These are
    illustrative review decisions, with no invented benchmark scores.
    """)
    return


@app.cell
def checkpoint_cases():
    cases = {
        "Successful variant": {
            "kind": "success", "focus": "sft-a", "resume_from": None,
            "action": "Freeze sft-a as the candidate",
            "reason": "The variant meets the planned validation criteria and shared regression checks. Package it for the independent final test.",
        },
        "Regression after SFT": {
            "kind": "regression", "focus": "base-v1", "resume_from": "base-v1",
            "action": "Start another SFT variant from base-v1",
            "reason": "sft-b formats answers correctly but loses the coupon condition. The reviewed data and parent are sound in this scenario; investigate the SFT configuration before another run.",
        },
        "Incorrect training data": {
            "kind": "data", "focus": "data-v1", "resume_from": "data-v1",
            "action": "Audit the labels and create data-v2",
            "reason": "Both variants inherited examples labelled free delivery when delivery cost 30 zł. Returning to another weight snapshot cannot repair those labels. Recheck the data, then rebuild affected descendants from a sound parent.",
        },
    }
    return (cases,)


@app.cell
def checkpoint_control(cases, mo):
    checkpoint_choice = mo.ui.dropdown(
        options=list(cases), value="Regression after SFT", label="Experiment outcome", full_width=True,
    )
    checkpoint_choice
    return (checkpoint_choice,)


@app.cell
def checkpoint_logic(cases, escape):
    def checkpoint_report(choice):
        case = cases[choice]
        def node(name, description):
            current = " is-focus" if case["focus"] == name else ""
            return f'<div class="ft-node{current}"><code>{name}</code><span>{description}</span></div>'
        diagram = (
            '<figure class="ft-checkpoint" aria-label="Experiment branches with a shared parent">'
            '<div class="ft-trunk">'
            + node("data-v1", "Reviewed dataset snapshot")
            + '<span class="ft-arrow" aria-hidden="true">→</span>'
            + node("base-v1", "Starting weights + tokenizer")
            + '</div><div class="ft-branches">'
            + node("sft-a", "Variant A · same parent")
            + node("sft-b", "Variant B · same parent")
            + '</div><figcaption>CPT is omitted in this example. The outline marks the snapshot or data version involved in the next decision.</figcaption></figure>'
        )
        return {**case, "html": diagram + f'<div class="ft-verdict" role="status"><b>{escape(case["action"])}</b><p>{escape(case["reason"])}</p></div>'}
    return (checkpoint_report,)


@app.cell
def checkpoint_output(checkpoint_choice, checkpoint_report, mo):
    mo.Html(checkpoint_report(checkpoint_choice.value)["html"])
    return


@app.cell
def git_limits(mo):
    mo.md("""
    The analogy has limits. Model weights are not readable source diffs,
    and merging weights is not the equivalent of merging two independent
    bug fixes. A merged model needs its own evaluation. Even the best point
    to return to depends on what failed. Git gives us a useful way to think
    about ancestry and releases, not a recipe for combining capabilities.
    """)
    return


@app.cell
def goal_story(mo):
    mo.md("""
    ## 3. Decide what a good deal means

    Our shopper wants a new electric kettle, delivered in Poland, for at most
    **150 zł including delivery**. They do not have the shop's membership.
    Three listings arrive:

    | Offer | What the headline leaves out | Decision for this shopper |
    | :--- | :--- | :--- |
    | “Czajnik 119 zł!” | Delivery costs 30 zł; total 149 zł | Within budget; compare with current alternatives |
    | “Czajnik 99 zł z kodem” | The coupon requires a paid membership; ordinary price is 159 zł | Reject for this shopper |
    | “Czajnik 129 zł, dostawa gratis” | The promotion expired yesterday | Reject as unavailable |

    These decisions use information we supplied. A price under 150 zł makes
    an offer eligible; it does not establish that it is a bargain. For that,
    we also need a trustworthy comparison with equivalent products, their
    captured prices and the time of the comparison. Missing evidence should
    lead to review, rather than a confident story about a discount.

    The **system** fetches listings and price evidence through feeds, APIs or
    collection jobs. The **model** interprets the supplied information and
    returns a decision with reasons. Fresh prices stay in that external
    information: we cannot train tomorrow's promotion into yesterday's
    weights. Retrieval or tools can supply it when the model is called.

    Before changing the model, I write a small evaluation plan with named
    measures. **Precision@10 against reviewed judgements**: how many of the
    first ten suggestions are useful? **Rate of invented conditions**: how
    often does the explanation invent a condition or ignore delivery?
    What are the latency, memory use and cost at the expected request load?
    We record a baseline under the same conditions and choose acceptance
    criteria before seeing the new results. The previous
    [confusion-matrix article](/blog/agent-confusion-matrix/)
    explains why a single accuracy number can hide expensive mistakes.

    The cost comparison includes the serving machine, energy, collection and
    maintenance, plus training cost spread over the model's useful lifetime.
    Measure at realistic traffic, including busy periods. A small model that
    takes too long to assess each offer may need more machines than expected.
    """)
    return


@app.cell
def data_story(mo):
    mo.md("""
    ## 4. Turn listings into examples we can trust

    Think of the offers as receipts arriving at an accounting desk. Some are
    copies, some omit a line, and some describe a different transaction despite
    having a similar title. Putting them in a neat spreadsheet is useful,
    but it does not make their contents correct.

    I would keep the original snapshot and produce a structured version.
    Here is an abbreviated record for the first kettle:

    ```json
    {
      "offer_id": "kettle-jan-01",
      "promotion_group": "shop-a-kettle-january",
      "observed_at": "2026-01-05T09:00:00+01:00",
      "title": "Czajnik 119 zł!",
      "price_pln": 119,
      "shipping_pln": 30,
      "conditions": "No membership required",
      "source_snapshot": "fictional/shop-a/2026-01-05"
    }
    ```

    Observation time and expiry time answer different questions. Seeing a
    page today does not prove that its promotion is still valid. The full
    dataset should preserve availability, expiry, missing fields and the
    evidence behind each normalised value. Do not turn “delivery unknown”
    into zero just because the output schema expects a number.

    The raw snapshot also lets us investigate a bad annotation later. Perhaps
    the model learned the wrong rule; perhaps our parser dropped the line
    that said “members only”. Those require different fixes.
    """)
    return


@app.cell(hide_code=True)
def sorting_illustration(Path, mo):
    mo.image(
        Path(__file__).parent / "assets/from-data-to-model-1/sorting.webp",
        alt="A robot sorts illustrated offer cards on a desk, keeping two copies together with a paperclip.",
    )
    return


@app.cell
def quality_story(mo):
    mo.md("""
    ### Keep provenance, then check the collection

    For each source, record where the material came from, when it was captured,
    its permitted use and the version or hash of the snapshot. An accessible
    web page is not automatically a dataset we can redistribute. Remove
    unnecessary personal information from comments or account details.

    Then inspect both individual records and the collection. Are prices in
    the right currency? Do decimal commas survive parsing? Have we collected
    only highly upvoted electronics, while the site also handles groceries
    and local pickup? A large collection of easy examples may leave the
    conditions we actually care about almost unrepresented.

    Repeated offers deserve particular attention. A shop feed, a forum post
    and a shortened affiliate title may all describe the same promotion.
    Exact hashes find identical text; near-duplicate checks and source
    relationships help find rewritten copies. Preserve these relationships
    as groups before assigning examples to different splits. Cleaning ten
    thousand copies into ten thousand nicely formatted rows still gives the
    same promotion ten thousand opportunities to influence training.

    [Lee and colleagues](https://aclanthology.org/2022.acl-long.577/)
    studied how deduplication affects memorised output and train–test overlap.
    Their measured improvements belong to their experimental settings.
    The practical question for our collection is whether repeated examples
    distort learning or make our evaluation easier than the future task.

    ### Label the decision with the context that makes it true

    A useful supervised example contains the offer, the relevant shopper
    preferences, supporting evidence and the reviewed target response.
    For our 119 zł kettle, the response could be:

    > Eligible: 119 zł + 30 zł delivery = 149 zł, within the shopper's budget.
    > Whether it is a bargain still needs comparable current prices.

    A second reviewer should be able to follow the same reasoning. If two
    reviewers disagree, inspect the rule or mark the case for review. Forum
    votes can be a useful signal, but popularity is not automatically a
    correct label for every shopper. A deal can be popular because it arrived
    at a busy hour or appeals to a different audience.

    For ranking, also annotate which of two eligible offers this shopper
    should see first, using the same captured comparison evidence. Keep
    eligibility and recommendation quality separate: the 149 zł total may
    satisfy the budget while another equivalent kettle is better value.
    These judgements connect our examples to the order of the final suggestions.

    Synthetic examples can fill a gap: vary the coupon conditions or create
    a case with missing delivery information. Keep their parent examples and
    generation provenance. Review the outputs, and keep all descendants in
    their parent's split. An evaluation example must not quietly become the
    prompt used to manufacture training data.
    """)
    return


@app.cell
def split_story(mo):
    mo.md("""
    ## 5. Practise on yesterday, evaluate on something new

    Imagine studying with flashcards and then sitting an exam containing
    paraphrases of those same cards. A high score might reflect memory of the
    cards rather than the skill the examiner wanted to measure.

    Our copies create that problem. If the shop description goes into
    training and its forum repost goes into validation, the model has already
    encountered much of the evidence. This is **data leakage**: information
    crosses a boundary that the evaluation assumes is independent.

    The three collections have different jobs. **Training** supplies learning
    examples. **Validation** helps us choose models and configurations.
    **Test** supplies an independent final assessment of the frozen candidate.
    Their sizes should follow the statistical precision (how narrow each
    estimate must be) and the coverage we need; there is no universally
    correct percentage split.

    For a service receiving new promotions, time matters too. I want to know
    whether examples from earlier periods help with later offers. Keep copies
    and derivatives of a promotion together, while respecting that temporal
    boundary. If a promotion straddles a cutoff, explicitly exclude the
    crossing group or apply a documented boundary policy; do not move future
    observations into training just to preserve a convenient group size.

    Below are twelve rows: six promotions, each with an original and a
    repost. The first split separates rows without protecting promotion
    groups. A random row split would leak only some of the groups; this one
    deliberately sends every original to training and every repost to
    validation or test, the worst case. The second uses earlier groups for
    training and later groups for validation and test. No group in this
    fixture straddles its time cutoffs.
    """)
    return


@app.cell(hide_code=True)
def split_illustration(Path, mo):
    mo.vstack([
        mo.image(
            Path(__file__).parent / "assets/from-data-to-model-1/data-split.webp",
            alt="A robot keeps matching offer cards clipped together in three trays arranged along a timeline, with a closed envelope in the test tray.",
        ),
        mo.md("*Clipped cards are one promotion family and stay together. The trays follow the timeline: learn from training, choose with validation, then open the sealed test envelope once to assess the frozen candidate.*"),
    ])
    return


@app.cell
def offer_data():
    promotions = [
        ("K-JAN", "2026-01-05", "2026-01-06", "Czajnik 119 zł", "119 zł za czajnik", 119),
        ("H-JAN", "2026-01-12", "2026-01-13", "Słuchawki z kodem", "Kod na słuchawki", 89),
        ("T-JAN", "2026-01-19", "2026-01-20", "Toster, odbiór osobisty", "Toster tylko lokalnie", 79),
        ("K-FEB", "2026-02-05", "2026-02-06", "Czajnik dla klubowiczów", "Klub: oferta na czajnik", 99),
        ("H-FEB", "2026-02-12", "2026-02-13", "Słuchawki, darmowa dostawa", "Dostawa gratis: słuchawki", 109),
        ("T-FEB", "2026-02-19", "2026-02-20", "Toster 69 zł do piątku", "Piątkowa promocja: toster", 69),
    ]
    offer_rows = []
    for group, first, second, original, repost, price in promotions:
        for index, (observed_at, text) in enumerate(((first, original), (second, repost))):
            offer_rows.append({
                "id": f"{group}-{index + 1}", "group": group, "observed_at": observed_at,
                "text": text, "price_pln": price, "source": "shop" if index == 0 else "repost",
            })
    return (offer_rows,)


@app.cell
def split_control(mo):
    split_choice = mo.ui.dropdown(
        options=["Split individual rows", "Keep groups and time"],
        value="Split individual rows", label="Dataset split", full_width=True,
    )
    split_choice
    return (split_choice,)


@app.cell
def split_logic(defaultdict, offer_rows):
    def split_report(mode):
        parts = {"train": [], "validation": [], "test": []}
        for row in offer_rows:
            if mode == "Split individual rows":
                part = "train" if row["source"] == "shop" else (
                    "validation" if row["observed_at"] < "2026-02-01" else "test"
                )
            else:
                part = "train" if row["observed_at"] < "2026-02-01" else (
                    "validation" if row["observed_at"] < "2026-02-10" else "test"
                )
            parts[part].append(row)
        memberships = defaultdict(set)
        for part, rows in parts.items():
            for row in rows:
                memberships[row["group"]].add(part)
        crossed = sorted(group for group, locations in memberships.items() if len(locations) > 1)
        train_groups = {row["group"] for row in parts["train"]}
        leaked_rows = [row for part in ("validation", "test") for row in parts[part] if row["group"] in train_groups]
        ordered = (
            max(row["observed_at"] for row in parts["train"])
            < min(row["observed_at"] for row in parts["validation"])
            and max(row["observed_at"] for row in parts["validation"])
            < min(row["observed_at"] for row in parts["test"])
        )
        status = "Chronological boundaries hold" if ordered else "Training includes observations later than validation"
        families = []
        assignments = {row["id"]: part for part, rows in parts.items() for row in rows}
        for group in dict.fromkeys(row["group"] for row in offer_rows):
            records = sorted((row for row in offer_rows if row["group"] == group), key=lambda row: row["observed_at"])
            families.append({"group": group, "crossed": group in crossed, "records": [
                {**row, "part": assignments[row["id"]]} for row in records
            ]})
        family_columns = []
        for family in families:
            cards = []
            for row in family["records"]:
                cards.append(
                    f'<div class="ft-assignment ft-part-{row["part"]}" data-row-id="{row["id"]}" data-part="{row["part"]}">'
                    f'<small>{row["source"]}</small><b>{row["part"].title()}</b></div>'
                )
            first, last = family["records"][0], family["records"][-1]
            style = " is-crossed" if family["crossed"] else ""
            family_columns.append(
                f'<li class="ft-family{style}" data-group="{family["group"]}">'
                f'<div class="ft-family-heading"><b>{family["group"]}</b>'
                f'<small>{first["observed_at"][5:]} / {last["observed_at"][5:]}</small></div>'
                + cards[0] + '<span class="ft-family-link" aria-hidden="true">↓</span>' + cards[1] + '</li>'
            )
        diagram_html = (
            '<figure class="ft-technical" data-process="split" aria-labelledby="split-process-title">'
            '<header><p class="ft-kicker">Data boundaries · earlier to later</p>'
            '<h3 id="split-process-title">Follow each promotion family through the split</h3></header>'
            '<p class="ft-small">Each column is one promotion, with its shop record and repost. '
            'Labels name the assigned split. Dates are month-day in 2026.</p>'
            '<ol class="ft-families">' + ''.join(family_columns) + '</ol>'
            f'<figcaption>Fictional records, computed assignments. {len(crossed)} of {len(families)} promotion families cross a split boundary. '
            + ('Training reaches into February while validation contains January reposts.' if not ordered else
               'January families train the model; later February families are reserved for validation and test.')
            + '</figcaption></figure>'
        )
        html = (
            '<div class="ft-split-report">'
            f'<dl class="ft-counts"><div><dt>Promotion groups crossing splits</dt><dd>{len(crossed)}</dd></div>'
            f'<div><dt>Evaluation rows with a group seen in training</dt><dd>{len(leaked_rows)} / {len(parts["validation"]) + len(parts["test"])}</dd></div></dl>'
            f'<p class="ft-time-status">{status}.</p>'
            '<p class="ft-small">Matching group IDs identify known copies; terracotta outlines mark groups crossing a split.</p></div>'
        )
        return {"parts": parts, "crossed": crossed, "leaked_rows": leaked_rows, "time_ordered": ordered,
                "families": families, "diagram_html": diagram_html, "html": html}
    return (split_report,)


@app.cell
def split_process(mo, split_choice, split_report):
    mo.Html(split_report(split_choice.value)["diagram_html"])
    return


@app.cell
def split_output(mo, split_choice, split_report):
    mo.Html(split_report(split_choice.value)["html"])
    return


@app.cell
def split_lesson(mo):
    mo.md("""
    Notice that a product can appear again without being the same promotion.
    January's kettle and February's members-only kettle belong to different
    groups. Grouping every kettle together would answer a different question:
    can the model handle unseen products? Choose the boundary that matches
    the intended use, and report that choice.

    The counter measures known group overlap, not model accuracy. Zero here
    is a necessary property of this split, not proof that all semantic leakage
    has disappeared. A real audit also checks external benchmarks, generated
    derivatives and other sources of contamination.

    Once reviewed, freeze the dataset for an experiment. Record counts before
    and after filtering, source coverage, exclusions and split rules. New
    observations create a new version and another audit. Data preparation
    returns throughout the project; it is not a box we tick once.
    """)
    return


@app.cell
def training_story(mo):
    mo.md("""
    ## 6. Choose the adaptation that solves the observed problem

    Now we can ask whether training helps. First, evaluate smaller existing
    checkpoints with the intended prompt and evidence. Compare a simple
    rules-based solution where appropriate: adding price and delivery needs
    arithmetic, not a newly trained language model. The interesting model
    work is interpreting conditions and applying the shopper's criteria.

    The starting checkpoint may be a base language model or an already
    instruction-tuned model. That choice affects the work still needed.
    We will measure candidates on our tasks instead of selecting by parameter
    count or a general leaderboard alone. Training from scratch is outside
    this company's plan.

    It helps to see what the weights do before we change them. The figure
    below follows one generation step. The output head produces **logits**,
    one number per token ID: logits are unnormalised scores over the
    vocabulary. Generation picks the next token from them and repeats.
    """)
    return


@app.cell
def tokenizer_fixture(Path, json):
    tokenizer_example = json.loads(
        (Path(__file__).parent / "assets/from-data-to-model-1/tokenizer-example.json").read_text()
    )
    return (tokenizer_example,)


@app.cell
def model_process(mo, tokenizer_example):
    _config = tokenizer_example["model_config"]
    _source = f'https://huggingface.co/{tokenizer_example["repo"]}/blob/{tokenizer_example["revision"]}/config.json'
    mo.Html(f"""
    <figure class="ft-technical" data-process="model" aria-labelledby="model-process-title">
      <header><p class="ft-kicker">Inference · weights stay fixed</p>
        <h3 id="model-process-title">From supplied evidence to generated tokens</h3></header>
      <div class="ft-io"><span>System prepares the input</span>
        <p>Instructions + shopper criteria + freshly fetched offer evidence → formatted prompt</p></div>
      <ol class="ft-generation">
        <li><span class="ft-step">01 · encode</span><b>Tokenizer</b>
          <p>Prompt text → token IDs</p><code>input_ids: [n]</code></li>
        <li class="ft-forward"><span class="ft-step">02 · forward pass</span><b>Language model</b>
          <p>Embedding lookup<br>→ {_config["num_hidden_layers"]} causal decoder blocks<br>→ output head</p>
          <code>[n, {_config["hidden_size"]}] → last-position logits [{_config["vocab_size"]}]</code></li>
        <li><span class="ft-step">03 · select</span><b>Next token</b>
          <p>Greedy selection or sampling, according to the generation settings.</p><code>one token ID</code></li>
        <li><span class="ft-step">04 · append</span><b>Continue</b>
          <p>Add the ID to the sequence. Stop at an end token or configured limit.</p><code>n → n + 1</code></li>
      </ol>
      <div class="ft-generation-loop"><span aria-hidden="true">↶</span><p>Repeat steps 02–04 while generation continues. New tokens extend the context; they do not update the weights.</p></div>
      <div class="ft-io ft-io-output"><span>System handles the output</span>
        <p>Decode generated IDs → check response format and evidence → recommend or send for review</p></div>
      <figcaption>Simplified decoder-only generation; n is the current sequence length. Caching and batching are omitted.
        Shapes use the <a href="{_source}">SmolLM2-135M configuration</a> as a concrete example.
        See the <a href="https://huggingface.co/docs/transformers/main/en/llm_tutorial">generation guide</a>.</figcaption>
    </figure>
    """)
    return


@app.cell
def tokenizer_story(mo):
    mo.md("""
    ### Text arrives through the model's tokenizer

    A **tokenizer** converts text into the token IDs the model consumes.
    For “dostawa gratis” and Polish product descriptions, we can inspect the
    sequence lengths, encoding behaviour and actual throughput. But a
    pretrained model learned associations with its own token IDs. We normally
    keep its tokenizer when fine-tuning. Training a replacement is a separate
    adaptation project, not swapping a dictionary file. The
    [Hugging Face course](https://huggingface.co/learn/llm-course/chapter6/1)
    makes this distinction between fine-tuning and training from scratch.
    """)
    return


@app.cell
def tokenizer_process(escape, mo, tokenizer_example):
    _example = tokenizer_example
    _tiles = []
    _word = 0
    for _position, (_piece, _token_id) in enumerate(zip(_example["decoded_pieces"], _example["ids"]), start=1):
        _word += _piece.startswith(" ")  # a leading space opens the next word
        _display = _piece.replace(" ", "␠")
        _tiles.append(
            f'<li class="ft-word-{_word}"><span class="ft-token-position">{_position:02}</span>'
            f'<code lang="pl">{escape(_display)}</code><small>ID {_token_id}</small></li>'
        )
    _repo_url = f'https://huggingface.co/{_example["repo"]}/blob/{_example["revision"]}/tokenizer.json'
    _n = len(_example["ids"])
    _d = _example["model_config"]["hidden_size"]
    mo.Html(f"""
    <figure class="ft-technical" data-process="tokenizer" aria-labelledby="tokenizer-process-title">
      <header><p class="ft-kicker">Real encoding · fictional offer</p>
        <h3 id="tokenizer-process-title">One title becomes {_n} token IDs</h3></header>
      <div class="ft-io"><span>01 · title text</span><p lang="pl">{escape(_example["text"])}</p></div>
      <p class="ft-encoding-arrow"><span aria-hidden="true">↓</span> <code>encode(add_special_tokens=False)</code></p>
      <ol class="ft-token-strip" aria-label="Decoded token pieces and their IDs in sequence">{''.join(_tiles)}</ol>
      <p class="ft-small">␠ marks a space and colours group the pieces by word.
        <span lang="pl">Czajnik</span> takes four tokens, the number three plus a space token, <span lang="pl">zł</span> two.
        Tiles show individually decoded pieces; the tokenizer's byte-level vocabulary uses different spellings for some characters.</p>
      <div class="ft-embedding-flow"><code>{_n} IDs</code><span aria-hidden="true">→</span>
        <b>Embedding lookup</b><span aria-hidden="true">→</span><code>[{_n}, {_d}] vectors</code></div>
      <figcaption>Computed with the <a href="{_repo_url}">{escape(_example["repo"])}</a> tokenizer,
        revision <code>{_example["revision"][:8]}</code>. Decoding the complete ID sequence returns the original title.
        No special tokens or chat template are included; a full request contains more text.
        This is an encoding example, not a quality result or a production model choice.</figcaption>
    </figure>
    """)
    return


@app.cell
def adaptation_methods(mo):
    mo.md("""
    ### Adapt only where the baseline falls short

    **Continued pretraining (CPT)** continues the language-model training
    objective on a selected corpus. If the model struggles with the language
    of offers, domain-adaptive pretraining could be worth testing.
    [Gururangan and colleagues](https://aclanthology.org/2020.acl-main.740/)
    studied domain and task adaptation; their results support experiments,
    not a requirement that every project pass through the same sequence.
    Check both domain improvement and loss of previous capabilities.
    """)
    return


@app.cell(hide_code=True)
def cpt_sketch(Path, mo):
    mo.vstack([
        mo.image(
            Path(__file__).parent / "assets/from-data-to-model-1/cpt-weights-sketch.webp",
            alt="Hand-drawn CPT: domain text containing offer, promo, coupon and delivery is tokenized; next-token loss drives a gradient update from base weights W to adapted weights W-prime with the same graph topology.",
        ),
        mo.md("*CPT uses a domain corpus to continue the language-model objective. The same token sequence supplies shifted next-token targets; gradients guide an optimizer's updates to trainable parameters. Here, ‘offer’, ‘promo’, ‘coupon’ and ‘delivery’ are excerpts of corpus language, not class labels or assumed whole-word tokens. Edge thickness and colour are a conceptual picture of changed parameters.*"),
    ])
    return


@app.cell
def supervised_methods(mo):
    mo.md("""
    **Supervised fine-tuning (SFT)** trains on examples of the behaviour we
    want: an instruction, relevant context and a target response. Our kettle
    decision is one example. SFT can teach task behaviour and factual content,
    but factual learning and hallucinations need separate measurement.
    [Gekhman and colleagues](https://aclanthology.org/2024.emnlp-main.444/)
    examined risks when introducing new knowledge through fine-tuning.
    None of this makes training weights a suitable live price feed.

    Preference optimisation or reinforcement learning may become useful if
    we have reliable comparisons or rewards. Rewarding clicks alone could
    favour sensational headlines over good offers. We would need an
    independent check of actual task success. For now, these are possible
    later experiments, not compulsory stops after SFT.
    """)
    return


@app.cell
def release_story(mo):
    mo.md("""
    ## 7. Ship a version we can explain and revisit

    Imagine SFT improves our reviewed validation cases while keeping the
    other checks acceptable. We choose a candidate, record its lineage and
    package the exact weights, tokenizer, prompt or chat template and
    inference settings. If we convert or quantize it for the target machine,
    we validate that resulting artifact too. The serving format is part of
    what users will actually experience.

    The independent final test evaluates the frozen candidate under the
    recorded protocol. If we use its result to guide changes, that set has
    influenced development. Closing the file again does not restore its
    independence ([Dwork and colleagues, 2015](https://doi.org/10.1126/science.aaa9375));
    a later independent assessment needs a fresh holdout or a separately
    designed reuse protocol.

    Publication includes a model card describing intended uses, data,
    evaluation and limitations. [Hugging Face's model-card documentation](https://huggingface.co/docs/hub/model-cards)
    gives the structure. Reproducing training additionally requires the
    relevant artifacts, code and accessible data; a well-written card alone
    cannot supply them.

    Finally, watch the deployed service. Shops change their coupon wording.
    Delivery charges move. A new product category appears. Capture reviewed
    failures and operational measurements, then decide whether the next fix
    belongs in collection, parsing, prompting, data or training. The next
    iteration starts with that evidence and a new version, not another run
    launched because the previous one finished.
    """)
    return


@app.cell
def next_parts(mo):
    mo.md("""
    ## Next in this series

    We now have something more useful than a list of training methods: a
    purpose for each experiment, examples we can inspect, a starting solution
    to beat and saved versions we can return to. In the next article, we will
    use those pieces to decide what the model actually needs to learn.

    1. **Before we fine-tune: the process behind a good deal** — this article.
    2. **Teaching the model our domain and task** — planned. Tokenization,
       checkpoint selection, CPT, SFT and controlled comparisons.
    3. **Proving it works, then shipping it** — planned. Evaluation,
       uncertainty, operating cost, quantization and publication.
    """)
    return


if __name__ == "__main__":
    app.run()
