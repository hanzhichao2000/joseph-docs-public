# Runtime conventions

These rules apply to new Joseph packages and their hosts. Hosts own module discovery,
configuration, and presentation; the shared runtime registry provides generic declaration,
source, and redaction mechanics without import-time registration or diagnostics.

## Environment and configuration

- Hosts explicitly register module declarations and finalize the registry after composing modules,
  before resolving active configuration. Identical declarations for the same owner are idempotent;
  conflicting declarations, owners, or overlapping prefixes fail without exposing values.
- A host loading modules later must finalize the full existing and new declaration set before
  resolving newly activated configuration. A conflict prevents activation.
- Package variables use `JOSEPH_<PKG>_` prefixes. Shared variables are registered by exact name,
  initially `JOSEPH_PROGRESS`, not by an open shared prefix. Extensions register their own
  reservations and declarations during composition.
- Reservations are distinct from active declarations. Shared-file keys for reserved inactive
  packages remain inactive and do not trigger unknown-key warnings. Unknown keys in active
  namespaces, unregistered prefixes, and unknown shared names produce name-only diagnostics.
- Use `$XDG_CONFIG_HOME/joseph/.env` only when `XDG_CONFIG_HOME` is non-empty and absolute;
  otherwise use `~/.config/joseph/.env`. The working directory does not affect selection.
  Ordinary mode permits an absent file; controlled mode fails if its required file is absent.
- In ordinary mode declared environment values override file values, with a warning naming the
  variable and source kinds, never values. Controlled mode accepts only explicitly allowed sources
  and rejects disallowed inherited values, overrides, and missing required fields without fallback.
- Every shared file is checked, including files containing only inactive configuration. On POSIX it
  must be a regular file owned by the runtime account with permissions no broader than `0600`;
  `0700` is recommended for its directory. Open and validate through a file descriptor, rejecting
  links and avoiding check/open replacement races where supported. Unsafe, unreadable, or malformed
  files fail closed without automatic permission changes. Other platforms require equivalent
  access-control checks and fail closed if equivalence cannot be established.
- Declarations explicitly mark sensitive values. Redacted views hide them regardless of their names;
  name-based masking is only a fallback. Logs, exceptions, manifests, and receipts must not expose
  original sensitive values. Diagnostics never serialize configuration values or whole mappings.
- Each host owns its Settings model and uses only declared, resolved values and approved aliases.
  Registry-aware filtering precedes model validation so reserved inactive keys do not become model
  errors. Configuration included in a manifest must be serializable through the redacted view.
  New hosts do not require Hydra, OmegaConf, or Jinja2.

## Output and presentation

- A successful declared JSON-mode command writes exactly one complete JSON document to stdout,
  without banners, logs, progress, or additional documents. Unless a JSON error schema is registered,
  failure exits nonzero with empty stdout and safe diagnostics on stderr. Human-mode help, version,
  and tables are not required to emit JSON.
- Logs, diagnostics, and progress go to stderr; progress state does not enter manifests or receipts.
  Stream redirection must not capture machine stdout.
- Dynamic progress uses stderr's TTY status, not stdout's. It is disabled by default when stderr is
  non-TTY or execution is in CI; brief static stderr status is allowed. Piped stdout does not itself
  disable progress on terminal stderr. `JOSEPH_PROGRESS=off` disables progress.
- Non-empty `NO_COLOR` disables ANSI color by default; empty means unset. UX dependencies are optional
  host extras: base imports and machine output work without them, using standard logging, plain text,
  or no progress. Presentation resources and affected streams are restored on normal completion,
  handled exceptions, and handled interruption; untrappable termination is not covered.
