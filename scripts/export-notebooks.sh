#!/bin/sh
# Export the "post" view of every marimo notebook to public/blog/<name>/.
# Prepared runtime: Python runs here, visitors get static states (see the view's states.yaml).
set -eu
for nb in notebooks/*.py; do
  name=$(basename "$nb" .py)
  uvx marimo-studio==0.3.0 view export post --target "$nb" --output "public/blog/$name" --force
done
