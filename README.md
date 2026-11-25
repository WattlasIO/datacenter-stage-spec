# Data Center Stage & Evidence Specification (`datacenter-stage-spec`)

[![CI](https://github.com/WattlasIO/datacenter-stage-spec/actions/workflows/ci.yml/badge.svg)](https://github.com/WattlasIO/datacenter-stage-spec/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-F0561D.svg)](LICENSE)
[![Maintained by Wattlas](https://img.shields.io/badge/Maintained%20by-Wattlas-111315.svg)](https://wattlas.io)

An open **JSON Schema**, **7-stage lifecycle taxonomy** ([`STAGES.md`](STAGES.md)), and zero-dependency Python validator (`validate.py`) for tracking pre-operational data center projects with explicit filing proof and capacity basis.

## Problem this specification solves

Data center pipeline lists routinely mix press releases, interconnection queue placeholders, zoning applications, and active construction into a single undifferentiated megawatt total. This specification enforces two basic rules:

1. **No stage without qualifying proof:** A press release can prove `announced`, never `building_permit` or `under_construction`.
2. **No megawatt number without its basis:** Every disclosed MW value must declare whether it is `it_load_mw`, `utility_load_mw`, `interconnection_request_mw`, or `generation_nameplate_mw`.

## Stages at a glance

```text
announced -> zoning_filed -> zoning_approved -> site_permit -> building_permit -> under_construction -> energized
```

See [`STAGES.md`](STAGES.md) for the exact qualifying and non-qualifying records for each stage.

## Quick start

Requires Python 3.10+. Zero external packages.

```bash
# Validate the included example record
python3 validate.py examples/valid-permitted-campus.json

# Run the test suite
python3 -m unittest discover -v
```

## Schema & files

- [`schema/project-record.schema.json`](schema/project-record.schema.json) — JSON Schema (Draft 2020-12)
- [`STAGES.md`](STAGES.md) — Stage definitions, evidence rules, and capacity basis taxonomy
- [`validate.py`](validate.py) — Zero-dependency validator enforcing stage-to-evidence consistency
- [`examples/valid-permitted-campus.json`](examples/valid-permitted-campus.json) — Synthetic valid example

## FAQ

### Why separate `site_permit` from `building_permit`?
A site permit (site plan, grading, stormwater, or state environmental permit) approves land preparation and environmental compliance. A building permit authorizes vertical structure construction. Projects can stall for months or years between site permitting and vertical construction. See [Data center site permit vs building permit: the differences](https://wattlas.io/articles/data-center-site-permit-vs-building-permit).

### Why require a `capacity.basis` field?
An interconnection request MW figure, a utility service load figure, an IT load figure, and an air-permit backup generator nameplate figure are not interchangeable. Labelling the basis prevents double-counting and modeling errors. See [Data center megawatts: IT load vs utility load](https://wattlas.io/articles/data-center-megawatts-explained).

---

## Related open repositories from Wattlas

- [`WattlasIO/awesome-data-centers`](https://github.com/WattlasIO/awesome-data-centers) — Curated directory of data center infrastructure, grid, standards, DCIM tools, and research
- [`WattlasIO/datacenter-permit-sources`](https://github.com/WattlasIO/datacenter-permit-sources) — Official US public filing portal directory and strict-source validator CLI
- [`WattlasIO/datacenter-mw-calculator`](https://github.com/WattlasIO/datacenter-mw-calculator) — IT load, utility load (PUE), water (WUE), MVA, and backup generator sizing CLI

Built and maintained by **[Wattlas](https://wattlas.io)** — US data center pipeline intelligence tied to public records ([public directory](https://wattlas.io/projects) · [sample records](https://wattlas.io/sample)).

## License

MIT
