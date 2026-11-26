# Public architecture

The public authority for the joseph-* package family. Public packages may depend on public layers
only; a private layer may extend but never complete public evidence.

The public layer is deliberately thin: short canonical contracts in `../contracts/`, the shared
rules in `../rules/`, and this index. Full-length architecture documents, vendor material, research
programs and the control plane live in `joseph-docs-private`, which pins this repository as a
submodule. Do not copy long documents here; write the contract down in a few lines instead.

Two executable rules, enforced by CI (`../tools/check_public_layer.py`):

- every public markdown file is listed in `../public-layer.allow`;
- no public markdown file exceeds 200 lines.
