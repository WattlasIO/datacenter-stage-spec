# Data Center Project Lifecycle Stage Taxonomy

This specification defines seven ordered stages for tracking data center projects from announcement through energization. A project advances to a stage **only when a primary record proves that milestone**.

| Order | Stage ID | What proves it | What does **not** prove it |
| --- | --- | --- | --- |
| 1 | `announced` | Developer press release, corporate filing, or economic development announcement naming a site or jurisdiction. | Anonymous rumors or speculative broker land listings. |
| 2 | `zoning_filed` | Formal rezoning, special exception, conditional use, or comprehensive plan amendment docket filed with local government. | Pre-application inquiries or news articles saying a developer "plans to file." |
| 3 | `zoning_approved` | Recorded vote, ordinance, or signed resolution approving land use for data center development. | Staff recommendations or planning commission hearings before final board approval. |
| 4 | `site_permit` | Approved site plan, grading/stormwater permit, wetlands permit, state environmental air/water permit, or utility service agreement docket. | Architectural registration alone or regional RTO load forecast adjustments. |
| 5 | `building_permit` | Issued vertical construction, foundation, shell, or electrical/mechanical building permit for a data hall or substation building. | Site clearing, demolition permits, or design-review registrations. |
| 6 | `under_construction` | Active vertical construction documented by issued building permits plus dated construction notice, inspection activity, or verified build progress. | Groundbreaking photo ops without permits or land grading alone. |
| 7 | `energized` | Certificate of occupancy, utility energization confirmation, or confirmed commercial operations. | Original target completion dates published years earlier. |

## Capacity basis rule

Whenever a megawatt (`mw`) figure is recorded, the schema requires an explicit `capacity.basis`:

- `it_load_mw` — Critical IT power delivered to servers and networking.
- `utility_load_mw` — Total facility electrical demand (`IT load × PUE`).
- `interconnection_request_mw` — Capacity requested in a utility or RTO queue (often speculative and subject to withdrawal).
- `generation_nameplate_mw` — Combined standby or onsite generator nameplate capacity from an environmental or power filing.
- `undisclosed` — Capacity not stated on public record (`mw` must be `null`).

For deeper background, see:
- [Announced isn't built: reading a datacenter's stage from the record](https://wattlas.io/articles/announced-isnt-built)
- [Phantom data centers: the record test](https://wattlas.io/articles/phantom-data-centers-record-test)
- [Data center site permit vs building permit: the differences](https://wattlas.io/articles/data-center-site-permit-vs-building-permit)
