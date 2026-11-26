# Public architecture

The public authority for the joseph-* package family. Public packages may depend on public
layers only; a private layer may extend but never complete public evidence.

- `FINAL_TARGET_ARCHITECTURE_V1.md`: the long-term target shape (draft), with the platform
  boundary profile landing as Section 16.
- `CORE_DEPENDENCY_DIRECTION.md`: the dependency-direction rule and the exception-list ratchet.
- The package map (six packages by runtime role, visibility and upstream delegation) is in
  `../contracts/repo-map.md`.

The public layer is a **whitelist**: every file here must be listed in `../public-layer.allow`,
enforced by CI. Vendor-specific, research-specific and control-plane material lives in
`joseph-docs-private`, which pins this repository as a submodule.
