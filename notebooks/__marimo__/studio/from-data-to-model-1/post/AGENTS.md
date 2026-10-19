# From data to a useful model · Part 1

English technical blog for software engineers without prior LLM training experience.
Use the installed marimo-studio skill for view lifecycle, projections and export.

## Ownership and style

The notebook owns article prose, fictional offer data, computations, controls and
experiment verdicts. The view projects named cells and repeats only the static
title/date/lead. Keep the title cell for standalone notebook reading, unprojected.

Match the author’s existing posts: Montserrat headings, Noto Sans body, Source
Code Pro, 860px outer reading width, off-white page and pastel blue header.
post.css owns the page; figures.css is shared with the standalone notebook’s
appearance cell. Native marimo outputs stay opaque. No new icon or CSS runtime
is needed. Keep authored hosts under #app-shell.

Four illustrations (market, sorting, data-split, CPT sketch) are embedded once
as data URLs in index.html. Keep PNG originals and WebP delivery copies of all
seven in notebooks/assets/from-data-to-model-1; model, tokenizer and the
inference sketch stay on disk but are no longer embedded anywhere.
Standalone notebook image cells stay unprojected to avoid repeating payloads
across Prepared states. Alt text must agree with those notebook cells.
The model, tokenizer and split illustrations are fictional metaphors. Captions
distinguish supplied evidence from retrieval, drawn paper fragments from actual
token boundaries, and promotion families from product categories. Exact split
counts and chronology remain in the notebook-generated interactive report.

Detailed explanations for model inference, tokenization and dataset splitting
are notebook-generated technical process figures, all inline. The view has no
details disclosures; the data-split scene sits inline above its control. Keep
all labels legible when the process switches to a vertical layout on phones.
The split figure derives all assignments from split_report and follows its
existing control, so states.yaml still has six combinations. Encoding uses the
offline tokenizer-example.json fixture, pinned to an immutable SmolLM2 revision.
scripts/refresh-from-data-tokenizer.py reproduces that fixture with tokenizers
0.22.1; browser/runtime rendering never downloads weights or tokenizer files.
Model dimensions illustrate configuration, not a measured inference result.

The handwritten CPT diagram is the only inline sketch; the HTML inference
process replaced the inference sketch. The CPT sketch follows its
prose before SFT. It distinguishes corpus vocabulary, next-token loss, gradient
updates and an adapted parameter snapshot. Words are not class labels or
assumed whole-word tokens. Graph nodes and edge thickness are conceptual, not
literal transformer architecture or measured weights. Keep this scope explicit
in notebook-owned captions and preserve image provenance in the asset manifest.
The CPT sketch has an Enlarge diagram button opening a native modal
with the full-resolution image. Its scrollable canvas is keyboard focusable;
Close and Escape dismiss it and native focus returns to the triggering button.
This is presentation-only interaction and adds no notebook control states.

## Teaching decisions

Use the fictional deal-finding company throughout. Polish offers remain Polish;
explanations and interface copy are English. No trained-model metrics or savings
were measured. The split report counts known promotion-group overlap, not model
performance or guaranteed absence of semantic leakage. Different promotions for
the same product are different groups. The fixture has no time-crossing groups.

The Git analogy explains ancestry, checkpoints and releases. A tag is not a
backup; a checkpoint is not a source diff; merging weights requires evaluation.
Data defects can require returning earlier than the preceding training stage.
Adaptation stages are optional. Fine-tuning normally preserves the checkpoint’s
tokenizer. Test feedback used for changes loses independent holdout status.

## Delivery and checks

Keep marimo 0.25.1, Studio 0.3.0 and marimo-export 0.1.4 compatible with the other
posts. Prepared delivery uses all six combinations in states.yaml. Controls are
independent inputs. Check scripts/check-from-data-to-model.py, then export and
inspect the actual HTTP-served export at desktop and mobile widths. Exercise all
states and keyboard navigation; check fragment links, readable diagrams and
horizontal overflow. Never edit generated .artifacts files.
