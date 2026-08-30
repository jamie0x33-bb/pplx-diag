# Contributing

## Reporting a bug

Run `pplx-diag check` in the environment where it happened and quote the `bd_` bundle id
in the issue. Without it a report is usually not actionable — the same traceback means
different things on different images, and the bundle is how that gets resolved.

## Running the tests

```bash
pip install -e '.[dev]'
pytest
```

CI runs the suite on Python 3.10 through 3.13.

## What CI cannot cover

CI has no Computer sandbox, so `SANDBOX_TYPE` is unset, runtime detection resolves to
`local`, and the upload path is skipped. Anything image-specific has to be confirmed by
hand from inside a sandbox.

## Adding a runtime

Image tags map to connector schema revisions in `src/pplx_diag/collect.py`. A new image
needs an entry there and a case in `tests/test_collect.py`.

## Style

Standard library only in the runtime package. `pytest` is the single dev dependency.
