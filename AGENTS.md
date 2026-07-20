# Repository Guidelines

## Build, Test, and Development Commands

- `python .claude/control-plane/scripts/inventory.py` prints a structural inventory of the control-plane files.
- `python .claude/control-plane/scripts/validate.py` checks required files, agent metadata, manifest settings, and schema validity.
- `python .claude/control-plane/scripts/estimate_context.py` estimates context size for the current scaffold.
- Optional dependency install for full validation: `python -m pip install jsonschema pyyaml`.

## Coding Style & Naming Conventions

- Use short, declarative Markdown with clear headings and minimal prose.
- Keep file names lower-case with hyphens or fixed control-plane names such as `manifest.yaml` and `change-plan.schema.json`.
- Prefer standard Python conventions in scripts: `snake_case` functions, `Path` for file handling, and stdlib first.
- Keep JSON and YAML deterministic: stable key order, explicit values, no placeholder fields.

## Testing Guidelines

- Treat `validate.py` as the primary repository check before and after edits.
- When changing routing, skills, rules, or workflows, update the matching eval file under `.claude/control-plane/evals/`.
- Non-trivial script changes should include a small runnable self-check or assertion-based smoke test.

## Commit & Pull Request Guidelines

- This checkout does not expose git history, so no local commit convention could be inferred.
- If you add commits, use concise imperative subjects such as `docs: add contributor guide`.
- PRs should describe the change, list validation commands run, and call out any files under `.claude/control-plane/` that changed.

## Security & Configuration Tips

- Do not edit forbidden roots in `manifest.yaml` without explicit approval.
- Keep generated run artifacts out of version control and preserve the append-only model for auditability.
  

IMPORTANT:  The entire control plane must be recursively self-improving using a dynamic workflow trigger which also updates itself based on it's latest improvement run(s) or it's last.  if there is no evidence of a last run, assume it is the first run ever and act accordingly and ask for approval if the latest run introduces changes that require the manifest.yaml to be modified. 
