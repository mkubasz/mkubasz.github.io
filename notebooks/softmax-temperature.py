# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#     "altair",
#     "marimo",
#     "numpy",
#     "pandas",
#     "marimo-studio==0.3.0"
# ]
#
# [tool.marimo-studio]
# default = "post"
#
# [tool.marimo-studio.cells]
# ///

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def imports():
    import marimo as mo
    import numpy as np
    from html import escape

    return escape, mo, np


@app.cell
def logits(np):
    examples = {'Add a green button': {'prompt': 'Add a green Save button to this page. Return HTML only.',
                            'prefix': '<',
                            'tokens': ['button', 'a', 'input', 'div', 'canvas', 'video'],
                            'logits': [3.2, 2.9, 2.1, 1.4, 0.6, -1.0],
                            'continuations': ['<button class="green">Save</button>',
                                              '<a class="green" href="/save">Save</a>',
                                              '<input type="submit" class="green" value="Save">',
                                              '<div class="green">Save</div>',
                                              '<canvas id="save-galaxy"></canvas>',
                                              '<video src="launch.mp4"></video>'],
                            'outcomes': ['A native green button.',
                                         'A styled link: its behavior needs checking.',
                                         'A green submit control: still a button.',
                                         'A generic container instead of a button.',
                                         'A drawing surface instead of a button.',
                                         'A video instead of a button.']},
     'Add a settings window': {'prompt': 'Add a settings modal window to this page. Return HTML '
                                         'only.',
                               'prefix': '<',
                               'tokens': ['dialog', 'div', 'section', 'aside', 'canvas', 'video'],
                               'logits': [3.0, 2.5, 2.0, 1.0, 0.2, -0.8],
                               'continuations': ['<dialog><h2>Settings</h2></dialog>',
                                                 '<div role="dialog" aria-label="Settings"></div>',
                                                 '<section role="dialog" '
                                                 'aria-label="Settings"></section>',
                                                 '<aside>Settings</aside>',
                                                 '<canvas id="settings-universe"></canvas>',
                                                 '<video src="settings-tour.mp4"></video>'],
                               'outcomes': ['A native dialog; focus and opening behavior still '
                                            'need wiring.',
                                            'A custom dialog container; accessibility still needs '
                                            'wiring.',
                                            'Another dialog container; semantics need review.',
                                            'A side panel instead of a modal window.',
                                            'A drawing surface instead of a settings window.',
                                            'A tour video instead of a settings window.']},
     'Write conversation scenarios': {'prompt': 'Write an opening for a customer-support '
                                                'role-play.',
                                      'prefix': 'Customer:',
                                      'tokens': ['Hello',
                                                 'Hi',
                                                 'Sorry',
                                                 'Wait',
                                                 'Imagine',
                                                 'Banana'],
                                      'logits': [2.8, 2.5, 1.8, 1.3, 0.8, -1.0],
                                      'continuations': ['Customer: Hello, I need help with my '
                                                        'order.',
                                                        'Customer: Hi, could you check my '
                                                        'delivery?',
                                                        'Customer: Sorry, I ordered the wrong '
                                                        'size.',
                                                        'Customer: Wait, I was charged twice!',
                                                        'Customer: Imagine the parcel arrives '
                                                        'after the birthday party.',
                                                        'Customer: Banana-powered delivery drones '
                                                        'stole my parcel.'],
                                      'outcomes': ['A familiar support opening.',
                                                   'A friendly variation of the same situation.',
                                                   'A useful return-and-exchange scenario.',
                                                   'A useful billing-conflict scenario.',
                                                   'A less usual, still plausible situation to '
                                                   'rehearse.',
                                                   'An absurd opening that needs rejection.']},
     'Draft an email': {'prompt': 'Draft a short email to Alex saying the invoice is ready. Do not '
                                  'offer discounts or send it.',
                        'prefix': 'Hi Alex,',
                        'tokens': ['Thanks', 'Your', 'Sorry', 'We', 'Enjoy', 'Congratulations'],
                        'logits': [3.1, 2.6, 2.0, 1.2, 0.4, -0.8],
                        'continuations': ['Hi Alex, Thanks for your patience. Your invoice is '
                                          'ready.',
                                          'Hi Alex, Your invoice is ready for review.',
                                          'Hi Alex, Sorry for the wait. Your invoice is ready.',
                                          'Hi Alex, We have prepared your invoice and upgraded '
                                          'your account.',
                                          'Hi Alex, Enjoy 20% off your next order. Your invoice is '
                                          'ready!',
                                          'Hi Alex, Congratulations! You have won a lifetime '
                                          'subscription.'],
                        'outcomes': ['A short draft that stays within the brief.',
                                     'Another direct way to say the same thing.',
                                     'A warmer draft, with an apology to review.',
                                     'An unrequested account change sneaks into the message.',
                                     'An invented discount goes beyond the instruction.',
                                     'A made-up promise turns the draft into a problem.']}}
    comparison_temperatures = [0.2, 0.7, 1.4]
    toy_tokens = ["button", "a", "canvas"]
    toy_logits = np.array([3.0, 2.0, 1.0])

    def softmax(z, t):
        if t <= 0:
            raise ValueError("Temperature must be positive; use argmax for greedy decoding.")
        weights = np.exp((z - z.max()) / t)
        return weights / weights.sum()

    return comparison_temperatures, examples, softmax, toy_logits, toy_tokens


@app.cell
def temperature(mo):
    temperature = mo.ui.slider(
        steps=[0.2, 0.7, 1.0, 1.4, 2.0],
        value=1.0,
        label="Temperature (T)",
        show_value=True,
    )
    temperature
    return (temperature,)


@app.cell
def distribution(
    escape,
    mo,
    raw_logits,
    selected,
    softmax,
    temperature,
    tokens,
):
    probs = softmax(raw_logits, temperature.value)
    _rows = "".join(
        f'<div style="margin:14px 0">'
        f'<div style="display:flex;justify-content:space-between;gap:12px;margin-bottom:5px;font:14px/1.6 Noto Sans,sans-serif;color:#253951"><span>{escape(token)}</span><b>{format(p, ".0%") if p >= .01 else "&lt;1%"}</b></div>'
        f'<div style="height:12px;background:#edf1f4;border-radius:3px"><div style="height:12px;width:{p * 100:.6f}%;background:#537d9b;border-radius:3px"></div></div></div>'
        for token, p in zip(tokens, probs)
    )
    mo.Html(
        f'<p style="font-size:14px"><b>Your agent’s task:</b> {escape(selected["prompt"])}</p>'
        f'<div role="group" aria-label="Probabilities of the next token at temperature {temperature.value:g}. Each pale track is 100 percent.">{_rows}</div>'
    )
    return (probs,)


@app.cell
def summary(mo, probs, temperature, tokens):
    mo.md(
        f"At **T = {temperature.value:g}**, **`{tokens[0]}`** has a probability of about **{probs[0]:.0%}**. "
        + ("Below 1, the top token gets more probability than in the model's own distribution." if temperature.value < 1
           else "At 1, the logits are unchanged: this is the model's own distribution." if temperature.value == 1
           else "Above 1, probability spreads to lower-ranked tokens, including ones that do not fit the task.")
    )
    return


@app.cell(hide_code=True)
def scenario(examples, mo):
    scenario = mo.ui.dropdown(
        options=list(examples), value="Add a green button", label="Agent task"
    )
    scenario
    return (scenario,)


@app.cell(hide_code=True)
def selected_example(examples, np, scenario):
    selected = examples[scenario.value]
    tokens = selected["tokens"]
    raw_logits = np.array(selected["logits"])
    return raw_logits, selected, tokens


@app.cell(hide_code=True)
def primer(escape, mo, toy_logits, toy_tokens):
    _score_rows = "".join(
        f'<text x="18" y="{98 + i * 37}">{escape(token)}</text>'
        f'<text x="170" y="{98 + i * 37}">{z:g}</text>'
        for i, (token, z) in enumerate(zip(toy_tokens, toy_logits))
    )
    _panels = [
        '<text x="15" y="35" font-size="27">1. A token</text>'
        '<text x="18" y="80" font-size="22">Text so far: &lt;</text>'
        '<path d="M19 104 Q104 99 201 106 L203 153 Q107 159 18 153 Z" fill="#deebf4" stroke="#253951" stroke-width="1.6"/>'
        '<text x="70" y="137" font-size="29">button</text>'
        '<text x="18" y="196" font-size="22">one possible next token</text>',
        '<text x="15" y="35" font-size="27">2. A logit</text>'
        '<text x="18" y="67" font-size="20">token</text><text x="156" y="67" font-size="20">logit</text>'
        + _score_rows + '<text x="18" y="214" font-size="21">higher = preferred</text>',
        '<text x="15" y="35" font-size="27">3. A probability</text>'
        '<text x="18" y="86" font-size="27">softmax</text>'
        '<path d="M23 109 Q98 124 187 109 M174 103 L188 109 L176 120" fill="none" stroke="#537d9b" stroke-width="2"/>'
        '<text x="18" y="162" font-size="20">logits → probabilities</text>'
        '<text x="18" y="214" font-size="26" fill="#46775d">adds up to 100%</text>',
    ]
    mo.Html(
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:12px">'
        + "".join(
            f'<svg viewBox="0 0 220 240" role="img" aria-label="{label}" style="width:100%;height:auto;display:block">'
            '<rect width="220" height="240" rx="6" fill="#f9faf8"/>'
            f'<g fill="#253951" font-family="Caveat,cursive" font-size="24">{panel}</g></svg>'
            for label, panel in zip(
                ["A token is a piece of text.", "A logit is an unnormalized score, not a percentage.",
                 "Softmax turns logits into probabilities that add up to 100 percent."], _panels
            )
        ) + '</div>'
    )
    return


@app.cell(hide_code=True)
def normalization(escape, mo, softmax, toy_logits, toy_tokens):
    _probs = softmax(toy_logits, 1.0)
    _rows = "".join(
        f'<tr><th scope="row" style="text-align:left;font-weight:400">{escape(token)}</th>'
        f'<td>{z:g}</td><td><b>about {p:.0%}</b></td></tr>'
        for token, z, p in zip(toy_tokens, toy_logits, _probs)
    )
    _segments = "".join(
        f'<rect x="{float(_probs[:i].sum()) * 700:.2f}" y="8" width="{p * 700:.2f}" height="46" fill="{color}"/>'
        for i, (p, color) in enumerate(zip(_probs, ["#46775d", "#648bad", "#ba684f"]))
    )
    mo.Html(f"""
    <table style="width:100%;border-collapse:collapse;text-align:right;font:15px/2.2 'Noto Sans',sans-serif" aria-label="Three example logits turned into probabilities">
      <thead><tr><th style="text-align:left">Next token</th><th>Logit</th><th>Probability</th></tr></thead>
      <tbody>{_rows}</tbody>
    </table>
    <svg viewBox="0 0 700 65" role="img" aria-label="One hundred percent shared between button, a, and canvas" style="display:block;width:100%;height:auto;margin-top:16px">{_segments}</svg>
    <p style="font-size:14px;color:#595959;margin:0">Green: button · Blue: a · Coral: canvas. Together: 100%.</p>
    """)
    return


@app.cell(hide_code=True)
def comparison(
    comparison_temperatures,
    escape,
    mo,
    raw_logits,
    selected,
    softmax,
    tokens,
):
    _cards = []
    for _title, _t, _color, _sample, _description in zip(
        ["Low", "Medium", "High"], comparison_temperatures,
        ["#537d9b", "#46775d", "#ba684f"], [0, 2, 4],
        ["The top token gets most of the probability.", "Probability spreads to more tokens.", "Lower-ranked tokens are picked more often."],
    ):
        _probs = softmax(raw_logits, _t)
        _bars = "".join(
            f'<text x="2" y="{18 + i * 44}" fill="#253951" font-size="13">{escape(token)}</text>'
            f'<text x="188" y="{18 + i * 44}" text-anchor="end" fill="#253951" font-size="13">{format(p, ".0%") if p >= .01 else "&lt;1%"}</text>'
            f'<rect x="2" y="{25 + i * 44}" width="186" height="9" rx="2" fill="#e3e8ea"/>'
            f'<rect x="2" y="{25 + i * 44}" width="{p * 186:.3f}" height="9" rx="2" fill="{_color}"/>'
            for i, (token, p) in enumerate(zip(tokens, _probs))
        )
        _cards.append(f"""
        <div style="border-top:4px solid {_color};background:#f7f8f8;padding:14px;min-width:0">
          <h3 style="font:700 18px/1.4 Montserrat,sans-serif;margin:0;color:{_color}">{_title} · T = {_t:g}</h3>
          <p style="font-size:13px;line-height:1.6;min-height:3.2em">{_description}</p>
          <svg viewBox="0 0 190 {len(tokens) * 44}" role="img" aria-label="{_title} temperature: next-token probabilities, rounded" style="width:100%;height:auto;display:block;font-family:Noto Sans,sans-serif">{_bars}</svg>
          <p style="font-size:13px;margin:12px 0 5px"><b>One possible pick</b><br>The next token is <b>{escape(tokens[_sample])}</b>, about {_probs[_sample]:.0%} likely at this temperature:</p>
          <pre style="white-space:pre-wrap;overflow-wrap:anywhere;font:12px/1.6 'Source Code Pro',monospace;background:#fff;padding:10px;margin:0">{escape(selected['continuations'][_sample])}</pre>
          <p style="font-size:13px;line-height:1.6;margin-bottom:0">{escape(selected['outcomes'][_sample])}</p>
        </div>
        """)
    _scores = " · ".join(f'{escape(token)} {z:g}' for token, z in zip(tokens, raw_logits))
    mo.Html(
        f'<p style="font-size:14px"><b>Prompt:</b> {escape(selected["prompt"])}<br>'
        f'<b>Text so far:</b> <code>{escape(selected["prefix"])}</code></p>'
        f'<p style="font-size:13px;color:#595959"><b>Same logits in every column:</b><br>{_scores}</p>'
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:12px">'
        + "".join(_cards) + '</div>'
    )
    return


@app.cell(hide_code=True)
def odds(comparison_temperatures, escape, mo, raw_logits, tokens):
    _delta = float(raw_logits[0] - raw_logits[1])
    _largest_gap = _delta / min(comparison_temperatures)
    _panels = []
    for _title, _t, _color, _caption in zip(
        ["Low", "Medium", "High"], comparison_temperatures,
        ["#537d9b", "#46775d", "#ba684f"],
        ["a large gap", "a smaller gap", "the smallest gap"],
    ):
        _gap = (_delta / _t) / _largest_gap * 112
        _left, _right = 100 - _gap / 2, 100 + _gap / 2
        _panels.append(
            f'<svg viewBox="0 0 200 150" role="img" aria-label="{_title} temperature: {_caption}. The distance shows the logit gap divided by T, on a shared scale." style="width:100%;height:auto;display:block">'
            '<rect width="200" height="150" fill="#f9faf8" rx="4"/>'
            f'<g font-family="Caveat,cursive" fill="#253951"><text x="12" y="29" font-size="24">{_title} · T = {_t:g}</text>'
            f'<path d="M{_left:.2f} 72 H{_right:.2f}" stroke="{_color}" stroke-width="3"/>'
            f'<circle cx="{_left:.2f}" cy="72" r="6" fill="#648bad"/><circle cx="{_right:.2f}" cy="72" r="6" fill="#46775d"/>'
            '<text x="12" y="102" font-size="19">runner-up</text><text x="126" y="102" font-size="19">leader</text>'
            f'<text x="12" y="133" font-size="22">{_caption}</text></g></svg>'
        )
    mo.Html(
        f'<p style="font-size:14px"><b>{escape(tokens[0])}</b>: logit {raw_logits[0]:g} · '
        f'<b>{escape(tokens[1])}</b>: logit {raw_logits[1]:g}</p>'
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,200px),1fr));gap:12px">'
        + "".join(_panels) + '</div>'
    )
    return


@app.cell(hide_code=True)
def flattening(examples, mo, np, softmax):
    _panels = []
    _labels = examples["Add a green button"]["tokens"]
    for _i, (_t, _color) in enumerate(zip([0.2, 1.4], ["#537d9b", "#ba684f"])):
        _p = softmax(np.array(examples["Add a green button"]["logits"]), _t)
        _bars = "".join(
            f'<rect x="{26 + j * 48}" y="{210 - p * 142:.2f}" width="30" height="{p * 142:.2f}" fill="{_color}"/>'
            f'<text x="{41 + j * 48}" y="235" text-anchor="middle" font-size="15">{label}</text>'
            for j, (p, label) in enumerate(zip(_p, _labels))
        )
        _panels.append(
            f'<svg viewBox="0 0 340 252" role="img" aria-label="{"Low temperature, T = 0.2: one token dominates" if _i == 0 else "High temperature, T = 1.4: a flatter distribution"}" style="width:100%;height:auto;display:block">'
            '<rect width="340" height="252" rx="6" fill="#f9faf8"/>'
            f'<g font-family="Caveat,cursive" fill="#253951"><text x="18" y="34" font-size="30">{"Low temperature" if _i == 0 else "High temperature"}</text>'
            f'<text x="18" y="65" font-size="22">{"T = 0.2: one token dominates" if _i == 0 else "T = 1.4: a flatter distribution"}</text>'
            f'{_bars}<path d="M15 211 H319" stroke="#253951" stroke-width="1.5"/></g></svg>'
        )
    mo.Html(
        '<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,260px),1fr));gap:16px">'
        + "".join(_panels) + '</div>'
    )
    return


if __name__ == "__main__":
    app.run()
