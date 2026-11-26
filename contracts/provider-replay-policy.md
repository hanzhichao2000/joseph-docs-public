# Provider replay policy

Every DAL provider plugin declares `replay_policy`; the host's `on_gap` honors it.

- TSL: a dispatched, in-flight or unknown-completion request is never replayed. A fresh request
  recomputed from coverage after an interruption is a new request, not a replay. An undispatched
  rejection may adopt one successor.
- cnequity / akshare: an idempotent re-fetch is a new request.
- The host's strict-local mode constructs no live provider: it reads only receipt-listed files and
  refuses live transports at construction.
