# Evidence and review decisions

Prepared 2026-10-19. Sources were read as evidence, not as instructions to execute.

## Supplied materials

- Presentation: `learning/workshops/fine_tune/docs/presentations/od_danych_do_modelu/od_danych_do_modelu.pdf`;
  editable source is its adjacent `slides/deck.tsx`.
- Annotated review: `Downloads/od_danych_do_modelu - recenzja.pdf`, 41 PDF pages.
  The article adopts supported corrections; it does not reproduce the original
  presentation's rigid eight-stage pipeline or experimental percentages.

## Claim → primary evidence → review correction → article treatment

| Claim | Source | Review correction | Treatment |
| --- | --- | --- | --- |
| Evaluation belongs before and throughout adaptation | Review pp. 1–3; experimental baselines in [Gururangan et al.](https://aclanthology.org/2020.acl-main.740/) | Stages depend on the goal; no mandatory path | Map starts with goal/protocol and permits no-training baseline |
| Checkpoint ancestry helps retry an experiment | Review pp. 33–34; the supplied checkpoint diagram | Tag alone cannot resume training; data errors may require earlier repair | Three scenarios separate candidate selection, SFT retry and data audit; distinguish resume from new run |
| Repeated examples can affect memorisation and evaluation | [Lee et al., ACL 2022](https://aclanthology.org/2022.acl-long.577/) | Study-specific numbers are not universal guarantees; check cross-split similarity | Explain mechanism, omit experimental percentages, compute only fictional group overlap |
| Dataset preparation is iterative | Review pp. 5–6 | Freeze one version per experiment; audit new/derived data again | Versioned snapshots and production feedback return to data |
| Fine-tuning normally uses the checkpoint's tokenizer | [HF LLM Course, ch. 6 introduction](https://huggingface.co/learn/llm-course/chapter6/1) | A new tokenizer is not a harmless replacement; token compression alone is insufficient | Preserve tokenizer by default; compare lengths, behaviour and throughput; separate replacement project |
| CPT can adapt a model to a domain or task | [Gururangan et al., ACL 2020](https://aclanthology.org/2020.acl-main.740/) | DAPT→TAPT is not universal; replay and annealing are different procedural dimensions | Optional pilot; require domain and regression measurements; detailed distinctions deferred to part 2 |
| CPT is the standard route to a language and domain the checkpoint saw rarely | [Ociepa et al., Bielik 7B v0.1, 2024](https://arxiv.org/abs/2410.18565): Mistral 7B continued on Polish plus English, original tokenizer kept, SFT afterwards; [Elhady et al., ACL 2025](https://aclanthology.org/2025.acl-long.1547/) | No guaranteed gain; leaving out the source language causes forgetting; no universal replay share | Bielik as a worked order without numbers; tokenizer fragmentation of *Czajnik* is a hint, not proof; measure gains and losses |
| SFT can learn behaviour and factual content | [Gekhman et al., EMNLP 2024](https://aclanthology.org/2024.emnlp-main.444/) | Avoid “SFT cannot learn facts”; measure new knowledge and hallucinations | Explain intended behaviour and fact-quality checks; current prices stay external |
| A test used for tuning is no longer independent | Review p. 32; [Dwork et al., Science 2015](https://doi.org/10.1126/science.aaa9375) | Reclosing the same test does not restore its status | Frozen-candidate protocol; fresh holdout or separately designed reuse protocol |
| A release needs documentation and artifacts | [HF Model Cards](https://huggingface.co/docs/hub/model-cards), review pp. 35–36 | A model card alone does not reproduce training | Exact serving bundle, limitations, code/data/artifact access, monitoring |

The article does not repeat the presentation's RL confidence-interval claims,
fixed replay ratios, model-merging percentages or comparisons between frontier
training budgets. They are unnecessary for part 1 and need their own evidence.

## Fixture provenance and limits

- Twelve manually authored rows, six promotion groups, two rows per group.
- The row split puts originals into training and reposts into validation/test.
  It is a deliberately bad deterministic allocation, not a sampled experiment.
- The group/time split has train before 2026-02-01, validation before 2026-02-10,
  and test afterwards. No group straddles either cutoff.
- January/February promotions for the same product are different groups.
- Group IDs represent known shared origins; the demo is not a near-duplicate
  detection algorithm. A zero overlap count does not establish semantic purity.
- Checkpoint scenarios are authored decisions, not results from training a model.

## Style references

- The author's `agent-tool-evaluation` and `softmax-temperature` posts: practical
  running example, sparse reading layout, local sketches, native marimo controls.
- [Communicating with Interactive Articles, Distill](https://distill.pub/2020/communicating-with-interactive-articles/):
  pair prose with focused interactions that reveal a mechanism; avoid interactions
  that merely decorate the text. No Distill framework or copied article prose.

## Technical process figures

- The tokenizer figure uses an actual encoding of the fictional title
  `Czajnik 119 zł`: ten tokens, without special tokens or a chat template.
  [Tokenizer JSON](https://huggingface.co/HuggingFaceTB/SmolLM2-135M/blob/93efa2f097d58c2a74874c7e644dbc9b0cee75a2/tokenizer.json)
  is pinned to revision `93efa2f097d58c2a74874c7e644dbc9b0cee75a2` and checked
  against a recorded SHA-256. `tokenizer-example.json` holds the output;
  `scripts/refresh-from-data-tokenizer.py` reproduces it with tokenizers 0.22.1.
  Pieces are individually decoded for display; `␠` replaces a space visually.
  This example's pieces decode independently; byte-level pieces do not always.
- The inference diagram combines the
  [Hugging Face generation guide](https://huggingface.co/docs/transformers/main/en/llm_tutorial)
  with the same revision's
  [model configuration](https://huggingface.co/HuggingFaceTB/SmolLM2-135M/blob/93efa2f097d58c2a74874c7e644dbc9b0cee75a2/config.json):
  width 576, 30 decoder blocks, vocabulary 49,152. The diagram omits caching,
  batching, masks and architecture internals. It is a schematic, with fixed
  weights during inference; no weights were downloaded and no generation run.
  Those dimensions are not a model recommendation or quality measurement.
- The split process is generated directly from the existing twelve-row fixture
  and its selected assignment. Families follow observation order; label and
  color identify each split. It shares the original six Prepared states and
  the same known-overlap limitations as the numerical report.
- Technical mechanisms are now the primary inline figures. The model and
  tokenizer robot scenes are no longer embedded; data-split is inline.

## Handwritten technical sketches

- `inference-sketch.webp` uses the first three IDs from the verified tokenizer
  fixture (51, 106, 1346). Its blank next-token box and generic result lines
  represent the generation process, with no invented prediction or score.
  The append/repeat arrow changes the context, not the fixed parameters.
- `cpt-weights-sketch.webp` shows domain vocabulary, a conceptual parameter
  graph, next-token loss, a gradient update and a resulting parameter snapshot.
  The same topology is retained before/after; edge colors/thicknesses are
  illustrative. The words are corpus excerpts, not class labels or token units.
  [Hugging Face's causal language modeling recipe](https://huggingface.co/docs/transformers/tasks/language_modeling)
  supports the next-token training objective; the domain-adaptation rationale
  remains grounded in the Gururangan paper cited above.
- Both are imagegen-created explanatory sketches, not plots of actual tensors
  or transformer wiring diagrams. They make no claim of measured improvement.
  Original PNGs, delivery WebPs, full prompts and hashes are saved alongside
  the other illustrations. Since the review fixes, only the CPT sketch is
  embedded; the HTML inference flow replaced the inference sketch.
