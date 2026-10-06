# Response compatibility review

The proposed `label` field breaks the supported strict consumer: its decoder
requires exactly `id` and `state`. The current response produces
`("item-1", "ready")`; the proposed response raises `ValueError` instead.

Keep the existing response for that supported consumer. An opt-in representation
or a consumer migration could permit the field, but no version/support policy was
provided, so this review does not prescribe a new version or deadline.

The fixture exercises actual provider serialization and consumer decoding in one
process. It establishes this compatibility failure, not HTTP transport, production
authorization, retry handling, generated SDK behavior, or security guarantees.
Review-only leaves provider and consumer source unchanged.
