# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = ["tokenizers==0.22.1"]
# ///
"""Reproduce the article's tokenizer fixture; download no model weights.

Run: uv run scripts/refresh-from-data-tokenizer.py
The notebook reads the saved JSON offline and needs no extra dependency.
"""

import hashlib
import json
from pathlib import Path
from urllib.request import urlopen

import tokenizers
from tokenizers import Tokenizer


def main():
    repo = "HuggingFaceTB/SmolLM2-135M"
    revision = "93efa2f097d58c2a74874c7e644dbc9b0cee75a2"
    url = f"https://huggingface.co/{repo}/resolve/{revision}"
    with urlopen(f"{url}/tokenizer.json", timeout=30) as response:
        raw = response.read()
    digest = hashlib.sha256(raw).hexdigest()
    assert digest == "9ca9acddb6525a194ec8ac7a87f24fbba7232a9a15ffa1af0c1224fcd888e47c"
    with urlopen(f"{url}/config.json", timeout=30) as response:
        config = json.load(response)
    tokenizer = Tokenizer.from_str(raw.decode())
    text = "Czajnik 119 zł"
    encoding = tokenizer.encode(text, add_special_tokens=False)
    pieces = [tokenizer.decode([token_id]) for token_id in encoding.ids]
    # This title's individual tokens decode cleanly; byte fragments need not.
    assert "".join(pieces) == text == tokenizer.decode(encoding.ids)
    assert tokenizer.get_vocab_size() == config["vocab_size"]
    fixture = {
        "repo": repo, "revision": revision,
        "tokenizer_sha256": digest, "tokenizers_version": tokenizers.__version__,
        "text": text, "add_special_tokens": False, "chat_template_applied": False,
        "tokens": encoding.tokens, "ids": encoding.ids,
        "decoded_pieces": pieces, "offsets": encoding.offsets,
        "decoded": tokenizer.decode(encoding.ids),
        "model_config": {key: config[key] for key in ("model_type", "hidden_size", "num_hidden_layers", "vocab_size")},
        "scope": "Real tokenizer encoding of a fictional offer title. Config shapes are schematic; no model weights, inference or quality measurements.",
    }
    destination = Path(__file__).resolve().parents[1] / "notebooks/assets/from-data-to-model-1/tokenizer-example.json"
    destination.write_text(json.dumps(fixture, indent=2, ensure_ascii=False) + "\n")
    print(f"Saved {len(encoding.ids)} verified tokens to {destination}")


if __name__ == "__main__":
    main()
