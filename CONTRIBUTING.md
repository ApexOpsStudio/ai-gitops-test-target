# Contributing

Thanks for helping improve `ai-gitops-test-target`. This repository is a small
Python CLI used for GitOps-style testing, so contributions should stay focused,
easy to review, and covered by tests when behavior changes.

## Local Setup

1. Install Python 3.11 or newer.
2. Clone the repository and enter the project directory.
3. Install the test dependency:

   ```bash
   python -m pip install pytest
   ```

4. Run the test suite:

   ```bash
   python -m pytest
   ```

The CLI stores local task data under `~/.local/share/task-cli/tasks.json` during
normal use. Tests should monkeypatch `Path.home()` or use `tmp_path` so they do
not touch a contributor's real home directory.

## Development Guidelines

- Keep command behavior simple and predictable.
- Add or update pytest coverage for user-visible behavior changes.
- Use standard-library modules unless a dependency is clearly justified.
- Keep command output stable because tests and automation may depend on it.
- Prefer small pull requests that address one issue at a time.

## Pull Request Checklist

Before opening a pull request:

- run `python -m pytest`
- run `git diff --check`
- describe the behavior change and any validation commands in the PR body
- link the related issue or bounty, if applicable

For CLI changes, include a short before/after example when that helps reviewers
understand the output.
