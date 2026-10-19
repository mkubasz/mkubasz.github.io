# From data to a useful model — editorial plan

Audience: software engineers new to training LLMs. Language: English, with Polish
offer text and PLN retained. The fictional company collects and assesses deals.
All numerical examples are authored fixtures, not observed model results.

## Part 1 — Before we fine-tune: the process behind a good deal

Slug: `from-data-to-model-1`. Complete article in the matching marimo notebook.
Outcome: explain the iterative lifecycle, why evaluation starts before training,
how data and evidence define an offer decision, and how to preserve independence.
Two experiments: checkpoint ancestry and known promotion-group leakage.

## Part 2 — Teaching the model our domain and task

Planned slug: `from-data-to-model-2`; not a published route yet.

1. Resume with the same shopper, kettle, coupon and shipping examples. Establish
   what the existing checkpoint gets right and which failure needs adaptation.
2. Inspect the actual tokenizer on Polish titles, diacritics, currencies, coupon
   codes and numbers. Compute sequences rather than drawing invented tokens.
3. Compare candidate checkpoints under the same task/evidence/generation budget.
   Include instruction-tuned checkpoints and a no-training baseline. Report
   quality, throughput and memory together; do not select by model size alone.
4. Explain CPT's next-token objective on offer-domain text. An optional pilot
   compares domain improvement and regressions. DAPT/TAPT describe corpus choice;
   replay is a data-mixing technique and annealing is a learning-rate schedule.
5. Turn a reviewed decision into one SFT example. Show context, target response,
   chat template, EOS, truncation and which response tokens contribute to loss.
6. Compare sibling variants on fixed validation tasks. Explain a failure that
   requires data repair versus one that suggests a training-configuration change.
7. Discuss preference optimisation/RL only when a reliable preference or reward
   exists. A click proxy is not an independent measure of offer quality. Distil
   examples from a larger model only with provenance and review.
8. Save lineage, state and validation evidence; hand one candidate to part 3.

Visuals: measured token sequences for the same Polish title; raw corpus versus
instruction/answer pair; checkpoint branches reusing part 1's visual language.
Optional interactions should change one meaningful factor at a time.

Default: retain the checkpoint's tokenizer. A replacement or vocabulary expansion
requires explicit model compatibility work and separate quality evaluation.
Do not promise a CPT gain or give one fixed replay percentage as universal advice.

## Part 3 — Proving it works, then shipping it

Planned slug: `from-data-to-model-3`; not a published route yet.

1. Define labels and ranking judgements. Evaluate usefulness among top suggestions,
   missed good offers, invented conditions and format validity separately.
2. Compare the candidate with the baseline on validation, relevant product/source
   subgroups, Polish tasks and shared regressions. Report counts and uncertainty.
3. Inspect concrete disagreements, including stale offers and absent price evidence.
   Calibrate any LLM judge against human judgements. Avoid treating a generic
   benchmark rank as task performance.
4. Measure operating cost, latency and memory at a documented load on the actual
   target hardware. Include collection/retrieval and serving where applicable.
   Identify a break-even assumption rather than promising savings from size.
5. Compare original and converted/quantized artifacts before freezing the release.
   Choose one best validated candidate; weight merging is a separate hypothesis.
6. Run the independent final test under the recorded protocol. If results guide
   edits, document the previous use and use a fresh holdout for independence.
7. Publish the weights/adapter, compatible tokenizer, inference configuration and
   model card. Document intended uses, dataset provenance, limitations and access
   constraints. Reproduction requires artifacts beyond the model card.
8. Close the lifecycle with observed failures, drift and a new data version.
   Roll back to a known serving bundle when an operational regression occurs.

Visuals: quality versus operational cost; one table comparing artifacts; a release
bundle and feedback loop. Use measured runs with recorded provenance if execution
is later authorised, otherwise clearly labelled fixtures.

## Continuity and publication

Keep the voice, fonts, ink/pastel palette and 860px outer reading width of the
existing agent-evaluation posts. Illustrations introduce a concrete scene;
code-generated diagrams and tables carry quantities and scientific claims.
Announce later parts as planned text until their routes exist. No automatic push
or deployment is authorised by this editorial plan.
