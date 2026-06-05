# Git Workflow Simulator

A small repository that models a professional GitHub workflow for a 3-person team.

This project is built to demonstrate how modern engineering teams collaborate using:

- feature branches
- pull requests and code review
- merge conflict resolution
- protected branches and branch rules
- release tagging and version control

## Repository contents

- `README.md` — the complete workflow guide and usage instructions.
- `.github/PULL_REQUEST_TEMPLATE.md` — the PR quality checklist used by contributors.
- `.github/CODEOWNERS` — sample reviewer assignment for code ownership.
- `workflow-simulator.py` — a simple script that prints a sample team workflow.

## Goal

Show how a professional team can work together on GitHub by:

- creating and naming branches consistently
- submitting pull requests to `main`
- assigning reviewers and implementing feedback
- handling conflicts before merge
- tagging releases after changes land in `main`

## Recommended GitHub configuration

For a realistic team repository, configure the following for `main`:

- require pull requests before merge
- require at least one or two approving reviews
- require passing status checks before merge
- dismiss stale approvals when new commits are pushed
- restrict direct pushes to `main`
- require branches to be up to date before merging

## Workflow overview

### Branch strategy

Use clear branch names such as:

- `feature/123-add-user-guide`
- `bugfix/234-fix-typo`
- `hotfix/345-patch-build-error`

Create each branch from `main` and keep it focused on a single change.

### Typical roles

- Developer A: creates the feature branch and implements the change.
- Developer B: reviews the pull request and ensures quality.
- Release Manager: approves the final merge and tags the release.

### Example feature branch flow

```bash
git checkout main
git pull origin main
git checkout -b feature/102-add-user-guide
# make changes
git add .
git commit -m "Add contribution workflow guide"
git push origin feature/102-add-user-guide
```

1. Open a pull request from the feature branch into `main`.
2. Add a clear summary and link any issues.
3. Add reviewers and use the PR checklist.

### Pull request process

Reviewers should verify:

- the change solves the stated problem
- code is readable and maintainable
- tests or validation steps are included
- merge conflicts are resolved

After approval, merge the PR using the team-preferred strategy:

- `Squash and merge` for a clean history
- `Create a merge commit` when preserving branch history is desired

Delete the branch after merging to keep the repository tidy.

### Conflict resolution

If the feature branch is behind `main`, update it before merging:

```bash
git checkout feature/102-add-user-guide
git fetch origin
git merge origin/main
# or git rebase origin/main
```

Resolve conflicts in the affected files, then continue:

```bash
git add <resolved-files>
git commit
git push origin feature/102-add-user-guide
```

### Release tagging

After a successful merge into `main`, create a release tag:

```bash
git checkout main
git pull origin main
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

Use semantic versioning to track releases:

- `v1.0.0` — initial release
- `v1.1.0` — new functionality
- `v1.1.1` — bug fixes

## Running the simulator

Run the workflow simulator script to see the process steps:

```bash
python workflow-simulator.py
```

## Notes

This repository is a documentation-first sample for a GitHub team workflow. The README contains the full collaboration process instead of a separate contributing guide.
