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
app = marimo.App(width="medium", app_title="Why did the same LLM prompt give me a different answer?")


@app.cell
def imports():
    from base64 import b64encode
    from html import escape
    from math import exp
    from pathlib import Path
    from random import Random

    import marimo as mo

    return Path, Random, b64encode, escape, exp, mo


@app.cell
def example():
    quicksort_prompt = "Write QuickSort in Python."
    polite_quicksort_prompt = "Please write QuickSort in Python."
    repository_instruction = "Use the middle element as the pivot."
    example_items = (8, 2, 5, 1, 7)
    return example_items, polite_quicksort_prompt, quicksort_prompt, repository_instruction


@app.cell(hide_code=True)
def sketch_renderer(Path, b64encode, escape, mo):
    def render_sketch(filename, dimensions, alt, caption, *, loading="lazy", caption_above=False):
        asset = Path(__file__).parent / "assets/llm-determinism" / filename
        encoded = b64encode(asset.read_bytes()).decode("ascii")
        width, height = dimensions
        image = (
            f'<img src="data:image/webp;base64,{encoded}" width="{width}" height="{height}" '
            f'loading="{loading}" alt="{escape(alt)}">'
        )
        caption_html = f"<figcaption>{escape(caption)}</figcaption>"
        first, last = (caption_html, image) if caption_above else (image, caption_html)
        return mo.Html(f"""
        <figure class="handwritten-sketch">
          {first}
          {last}
        </figure>
        """)

    return (render_sketch,)


@app.cell
def title(mo):
    mo.md(r"""
    # Why did the same LLM prompt give me a different answer?

    *Mateusz Kubaszek · November 20, 2026 · LLMs · Inference*
    """)
    return


@app.cell(hide_code=True)
def black_box_sketch(quicksort_prompt, render_sketch):
    render_sketch(
        "black-box-sketch.webp",
        (1200, 800),
        "The request passes through a black box and a possible answer uses the middle item as the pivot.",
        f"Input: {quicksort_prompt}",
        loading="eager",
        caption_above=True,
    )
    return


@app.cell
def prompt_transition(mo):
    mo.md("""
    And we could add just one word that, in theory, shouldn't change the response.
    """)
    return


@app.cell(hide_code=True)
def polite_black_box_sketch(polite_quicksort_prompt, render_sketch):
    render_sketch(
        "please-black-box-sketch.webp",
        (1200, 800),
        "The request passes through a black box and a possible answer uses the last item as the pivot.",
        f"Input: {polite_quicksort_prompt}",
        caption_above=True,
    )
    return


@app.cell
def opening(mo):
    mo.md(r"""
    I would give a colleague the same task either way. A coding assistant might
    pick the middle item as the pivot in one answer and the last item in the
    other. Then I paste the *exact* first sentence into a fresh chat and get
    a third implementation. Which of those runs would you compare to test
    whether the model is deterministic?

    I'd start by asking what went into each run. The word *please* changes the
    input. Repeating the exact sentence gives us a better comparison, and even
    there we still need to know what the coding assistant actually sent, which
    checkpoint served it, and how it chose the next token.

    Let's follow that QuickSort request and open the box one step at a time.
    """)
    return


@app.cell
def weights(mo):
    mo.md(r"""
    ## 1. Put the box of numbers on the desk

    Think of a trained checkpoint as a box of numbers. Those are the weights.
    The model architecture tells us how to use them. In a conventional
    decoder-only language model, a forward pass takes a sequence of tokens and
    produces scores, or **logits**, for what could come next. In the mathematical
    model, with inference-time randomness disabled, the same weights and input
    give the same scores. An actual machine evaluates that function in finite
    precision, where the order of operations matters.

    ### The weights are frozen for inference

    During training, the optimizer updates the weights. During inference, the
    runtime holds the deployed checkpoint's weights fixed. The QuickSort prompt
    supplies the initial tokens. Each generated token extends that sequence, so
    the next forward pass can produce different scores with the very same weights.
    """)
    return


@app.cell(hide_code=True)
def frozen_weights_sketch(render_sketch):
    render_sketch(
        "frozen-weights-sketch.webp",
        (1200, 800),
        "A hand-drawn neural network with nodes and connections encased in a slab of blue ice.",
        "The ice represents a snapshot of the learned parameters, held fixed during inference.",
    )
    return


@app.cell
def checkpoint_variation(mo):
    mo.md(r"""
    Training is a different run. Start twice with the same architecture and
    dataset and you can still get two checkpoints. Random initialization, the
    order of minibatches and dropout can all affect the updates. A seed helps
    replay the random choices within a controlled setup. Reproducing the weights
    across library versions and hardware takes more than setting the seed.
    [PyTorch's reproducibility notes](https://docs.pytorch.org/docs/2.15/notes/randomness.html)

    Think of a recommendation system trained on a sample of shoppers. The
    question of whether its recommendations generalize belongs to evaluation on
    other shoppers or later data. The question of whether a training run can be
    repeated belongs to reproducibility. We can fix our seeds and still learn
    the wrong pattern from a narrow dataset.

    In practice, a short model name in an app can be a service alias. A second
    request under that name may reach an updated checkpoint or a different
    serving configuration. A fine-tuned checkpoint can have different weights,
    and a quantized build can represent and compute with them differently.
    For a comparison I can replay, I want the exact revision and runtime
    configuration. Self-hosting gives me more control over both.
    """)
    return


@app.cell
def request(mo):
    mo.md(r"""
    ## 2. What did the coding assistant send?

    *Write QuickSort in Python* and *Please write QuickSort in Python* express
    the same request to a person. A tokenizer works on the text it receives.
    Adding a word, changing case or adding a space can change the sequence
    of token IDs. Two different token sequences can lead to two different
    answers even when each run is perfectly repeatable.

    Now keep the visible sentence fixed. Imagine that on Monday the assistant
    sends the question on its own. On Tuesday it also includes a repository
    convention to use the middle element as the pivot. The convention may come
    from a file, a skill or a retrieval step. The same thing happens when a
    chat history grows or a system prompt changes between releases.
    """)
    return


@app.cell
def request_board(escape, mo, quicksort_prompt, repository_instruction):
    _prompt = escape(quicksort_prompt)
    _instruction = escape(repository_instruction)
    mo.Html(f"""
    <figure class="request-board">
      <dl class="request-flow">
        <div>
          <dt>What you see in chat</dt>
          <dd><span class="board-note">{_prompt}</span></dd>
        </div>
        <div>
          <dt>What the assistant sends</dt>
          <dd><span class="board-note">{_prompt}</span></dd>
          <dd><span class="board-note board-note-added"><strong>Repository guide</strong>{_instruction}</span></dd>
        </div>
      </dl>
      <figcaption>The chat still shows the same sentence. The assembled request now carries an extra instruction.</figcaption>
    </figure>
    """)
    return


@app.cell(hide_code=True)
def request_route_map(render_sketch):
    render_sketch(
        "request-route-map.webp",
        (1122, 1402),
        "A hand-drawn fantasy map follows the request from User Prompt through Agent Camp, API Gateway, "
        "Model Router, Chat Template, Tokenizer, and Serving Queue to Model Keep. "
        "The numbered stages are explained in order below.",
        "One route through a hosted coding-agent system. A local runtime can combine or bypass some of these stops.",
    )
    return


@app.cell
def request_route(mo):
    mo.md(r"""
    ### What happens at each stop?

    1. **User prompt.** The editor hands *Write QuickSort in Python* to the
       coding agent. This is the message I can see and copy from the chat.
    2. **Agent camp.** The agent assembles the conversation. It may include
       its own instructions, the repository rule about the pivot, chat
       history, retrieved files and results from earlier tool calls. In a
       chat API, the request can also carry the model name, generation
       settings and the definitions of available tools. A tool result from
       this turn can become context in a later request.
       [GitHub's guide to coding-agent context](https://docs.github.com/en/copilot/reference/customization-cheat-sheet)
       · [vLLM's chat API](https://docs.vllm.ai/en/stable/serving/online_serving/openai_compatible_server/)
    3. **API gateway.** The agent sends the request over HTTP. A hosted gateway
       can check credentials and usage limits before forwarding the request.
       [Envoy Gateway's rate-limiting guide](https://gateway.envoyproxy.io/docs/concepts/rate-limiting/)
    4. **Model router.** The service maps the requested name or alias to a
       deployment. It can then pick a replica, for example using current load.
       The deployment determines which checkpoint and serving configuration
       handle this run. The gateway and router can be part of the same service.
       [Kubernetes Inference Gateway's endpoint selection](https://gateway-api-inference-extension.sigs.k8s.io/api-types/inferencepool/)
    5. **Chat template.** The selected model's template formats the messages.
       It can mark who said what and where the assistant's turn should begin.
       [Hugging Face's guide to chat templates](https://huggingface.co/docs/transformers/chat_templating)
    6. **Tokenizer.** The formatted prompt becomes an ordered list of token IDs.
       This is where the exact spelling, spaces and added repository rule
       show up in the input. The assembled context also has to fit the model's
       token budget. An agent can trim or summarize earlier messages to make room.
    7. **Serving queue.** The runtime schedules the request. In a shared
       deployment it can process the prompt in a batch alongside other requests.
       [vLLM's architecture overview](https://docs.vllm.ai/en/stable/design/arch_overview/)
    8. **Model keep.** The model receives the token IDs and runs them through
       its frozen weights. The first forward pass gives us logits for the next
       token. The decoder makes the choice in the next section.

    When I investigate a mismatch, I compare the assembled messages and any
    context the agent supplied first. Then I check which deployment and
    tokenizer the request reached. Two identical lines in the chat can take
    different routes through the system.
    """)
    return


@app.cell
def decoding(mo):
    mo.md(r"""
    ## 3. Who picked the next token?

    The forward pass gives us scores. The decoder makes the choice. **Greedy
    decoding** takes the highest-scoring token, with a fixed rule for ties.
    **Sampling** draws a token from a distribution. Temperature reshapes that
    distribution, and the random draw chooses from it. Two draws can pick
    different tokens even when the scores and temperature match.
    [Transformers generation strategies](https://huggingface.co/docs/transformers/generation_strategies)

    The runtime appends the chosen token to the sequence, after the prompt and
    any tokens generated so far. The model uses that longer sequence to score
    the candidates for the next token. One small difference early on can give
    us a different function by the end.
    If you want to see how the probabilities move before any pick is made,
    try the charts in [What temperature does to a softmax](/blog/softmax-temperature/).

    A seed sets the starting state of a pseudorandom generator. To replay the
    draw, the sampler also needs to consume randomness the same way. Greedy
    decoding removes that draw entirely. Some interfaces expose it as
    `temperature=0`. The resulting token still depends on the scores the
    runtime computes for that request.

    The loop can stop when the model emits an end-of-sequence token or when
    generation reaches the configured token limit.
    [Transformers stopping criteria](https://huggingface.co/docs/transformers/internal/generation_utils#stoppingcriteria)
    """)
    return


@app.cell(hide_code=True)
def decoder_route_map(render_sketch):
    render_sketch(
        "decoder-route-map.webp",
        (1122, 1402),
        "A fantasy map leads from Model Keep to logits and then to the decoder. "
        "A side path feeds temperature and seed into the decoder when sampling. "
        "The decoder chooses the next token, which joins the sequence. A blue path takes the extended sequence "
        "back to Model Keep for another step, and the main path leads to the answer when generation stops.",
        "The blue road is the return path. Each chosen token becomes part of the context for the next prediction.",
    )
    return


@app.cell(hide_code=True)
def flow_sketch(quicksort_prompt, render_sketch, repository_instruction):
    render_sketch(
        "request-flow-sketch.webp",
        (1086, 1448),
        f'User types “{quicksort_prompt}” The system adds the rule “{repository_instruction}” '
        "The model reads tokens from both and returns logits. The decoder chooses the next token. "
        "When sampling, temperature shapes the probabilities and the seed sets the random sequence. "
        "One possible answer is QuickSort with a middle pivot.",
        "In the full QuickSort request, the repository rule reaches the model together with the user prompt.",
    )
    return


@app.cell
def runtime(mo):
    mo.md(r"""
    ## 4. Temperature is zero. What can still move?

    Say my QuickSort request reaches the same checkpoint with the same
    tokens and greedy decoding. A serving engine may process that request
    alone on one run and alongside other requests on the next. Some kernels
    use a different order of arithmetic for a different batch shape. With
    floating-point rounding, even a fixed calculation can give different
    results when its operations are grouped differently.
    """)
    return


@app.cell(hide_code=True)
def rounding_sketch(render_sketch):
    render_sketch(
        "rounding-sketch.webp",
        (1200, 800),
        "Cancel first: (10 to the 20th minus 10 to the 20th) plus 1 gives 1. "
        "Round first: 10 to the 20th plus (negative 10 to the 20th plus 1) gives 0.",
        "In double precision, adding 1 to −10²⁰ rounds back to −10²⁰. Cancel the large terms first and the 1 survives.",
    )
    return


@app.cell
def runtime_takeaway(mo):
    mo.md(r"""
    The sketch exaggerates rounding so we can see it. In inference, a tiny
    change is enough when two tokens have nearly tied scores. If their order
    flips, greedy decoding takes a different token and the next step begins
    from a different prefix. An engine with batch-invariant operations can
    remove this source of variation. [PyTorch's numerical accuracy notes](https://docs.pytorch.org/docs/2.15/notes/numerical_accuracy.html)
    · [Thinking Machines Lab's inference experiments](https://thinkingmachines.ai/blog/defeating-nondeterminism-in-llm-inference/)
    """)
    return


@app.cell
def lab_intro(mo):
    mo.md(r"""
    ## 5. Change one thing and run it again

    Follow the prompt and extra context through two runs of a tiny decoder.
    Each run chooses a rule for picking the **pivot**, the element QuickSort
    uses to split the list. The board marks which element that rule picks on
    the same example list. The scores are made up and the choices are computed
    locally. In the sampling case both runs sample at temperature 1, so only
    the seed changes.
    """)
    return


@app.cell
def controls(mo):
    comparison = mo.ui.dropdown(
        options=["Exact replay", "Prompt wording", "Repository context", "Sampling seed", "Serving arithmetic"],
        value="Exact replay",
        label="Change in run B",
    )
    comparison
    return (comparison,)


@app.cell
def experiment(Random, comparison, exp, polite_quicksort_prompt, quicksort_prompt, repository_instruction):
    _base = {"prompt": quicksort_prompt, "context": None, "scores": (1.00000010, 1.00000000), "seed": None}
    _changes = {
        "Exact replay": {},
        "Prompt wording": {"prompt": polite_quicksort_prompt, "scores": (0.80, 1.10)},
        "Repository context": {"context": repository_instruction, "scores": (0.25, 1.25)},
        "Sampling seed": {"seed": 2},
        "Serving arithmetic": {"scores": (0.99999990, 1.00000000)},
    }
    _explanations = {
        "Exact replay": "Both runs see the same scores and use the same greedy rule.",
        "Prompt wording": "Adding ‘Please’ changes the input. In this fixture the new scores favor the middle pivot.",
        "Repository context": "The displayed request matches. The extra repository instruction changes the input and the scores.",
        "Sampling seed": "Both runs use the same scores and probabilities. The draws land on opposite sides of the cutoff.",
        "Serving arithmetic": "The last-pivot score moves by 0.00000020 in this fixture. That is enough to reverse the ranking.",
    }
    _run_a = _base | ({"seed": 7} if comparison.value == "Sampling seed" else {})
    _run_b = _run_a | _changes[comparison.value]

    def _decode(run):
        last, middle = run["scores"]
        seed = run["seed"]
        if seed is None:
            choose_last = last >= middle
            decoding = "Greedy"
        else:
            probability = 1 / (1 + exp(middle - last))
            draw = Random(seed).random()
            choose_last = draw < probability
            decoding = f"Seed {seed} · draw {draw:.3f} · last-pivot probability {probability:.3f}"

        return {
            "prompt": run["prompt"],
            "context": run["context"],
            "last_score": f"{last:.8f}",
            "middle_score": f"{middle:.8f}",
            "decoding": decoding,
            "choose_last": choose_last,
        }

    run_a = _decode(_run_a)
    run_b = _decode(_run_b)
    explanation = _explanations[comparison.value]
    return explanation, run_a, run_b


@app.cell
def lab_report(escape, example_items, explanation, mo, run_a, run_b):
    def _run_panel(title, run):
        pivot_index = len(example_items) - 1 if run["choose_last"] else len(example_items) // 2
        pivot_label = "Last element" if run["choose_last"] else "Middle element"
        tiles = "".join(
            f'<span class="pivot-tile pivot-tile-selected">{value}</span>'
            if position == pivot_index else f'<span class="pivot-tile">{value}</span>'
            for position, value in enumerate(example_items)
        )
        context = escape(run["context"] or "None in this run")
        context_class = "run-context-added" if run["context"] else ""
        example_label = ", ".join(map(str, example_items))
        return f"""
        <div class="run-panel">
          <h3>{title}</h3>
          <div class="run-step run-input">
            <h4>What goes in</h4>
            <dl>
              <div><dt>Visible prompt</dt><dd>{escape(run["prompt"])}</dd></div>
              <div class="{context_class}"><dt>Extra context</dt><dd>{context}</dd></div>
            </dl>
          </div>
          <div class="run-step run-decision">
            <h4>Decoder</h4>
            <p>{escape(run["decoding"])}</p>
            <dl class="pivot-scores">
              <div><dt>Last-pivot score</dt><dd>{run["last_score"]}</dd></div>
              <div><dt>Middle-pivot score</dt><dd>{run["middle_score"]}</dd></div>
            </dl>
          </div>
          <div class="run-step run-output">
            <h4>What comes out</h4>
            <p class="pivot-result">{pivot_label} becomes the pivot ({example_items[pivot_index]}).</p>
            <div class="pivot-tiles" role="img" aria-label="Example list: {example_label}. Pivot: {example_items[pivot_index]}.">
              {tiles}
            </div>
          </div>
        </div>
        """

    mo.Html(f"""
    <figure class="run-comparison" aria-label="Decoder results">
      <div class="run-panels">
        {_run_panel("Run A", run_a)}
        {_run_panel("Run B", run_b)}
      </div>
      <figcaption>{escape(explanation)}</figcaption>
    </figure>
    """)
    return


@app.cell
def replay(mo):
    mo.md(r"""
    ## 6. What would I save for a replay?

    Suppose yesterday's QuickSort answer passed the tests and today's doesn't.
    Before changing the temperature, I'd save the two traces and ask three
    questions in order.

    1. **Did we send the same input?** Capture the assembled messages, tool
       schemas and any tool outputs or retrieved context used for generation.
       When the stack exposes them, compare the actual token IDs. Freeze the
       external data for a replay.
    2. **Did we run the same computation?** Record the checkpoint revision,
       tokenizer and chat template, quantization, serving engine and decoding
       settings. Keep the seed when sampling. If the provider only gives you a
       model name and request ID, record both and treat the replay as a test of
       the service you can observe.
    3. **Where do the two runs first disagree?** In a controlled environment,
       compare the first differing token and, if available, the scores at that
       step. If the agent served a cached final answer on one run, label that
       comparison separately. A response cache can return yesterday's text
       without a second generation.

    For regression tests, I'd keep the exact trace when I need to debug a
    change. For the QuickSort task itself, I'd run both implementations on
    empty input, repeated values and an already sorted list, checking that the
    result is sorted and preserves every element. Two implementations can
    differ line for line and both satisfy the contract.

    So, are LLMs deterministic? A deterministic forward pass and decoder can
    reproduce the same answer under fixed execution conditions. A user
    asking the same question twice has only fixed one part of that setup.
    If I want to compare answers, I start by deciding which parts of the run
    I can hold constant and which result I need to reproduce.
    """)
    return


if __name__ == "__main__":
    app.run()
