#!/usr/bin/env python3
"""Simple workflow simulator for a 3-person Git team."""

steps = [
    "1. Developer A branches from main: git checkout -b feature/102-add-user-guide",
    "2. Developer A commits changes and pushes the feature branch.",
    "3. Developer A opens a PR to main and requests review from Developer B.",
    "4. Developer B reviews the code, leaves comments, and approves the PR.",
    "5. If main has changed, the branch is updated and conflicts are resolved.",
    "6. After approvals and checks, the feature branch is merged into main.",
    "7. Release Manager tags the merged commit on main: git tag -a v1.0.0 -m 'Release v1.0.0'.",
    "8. The team deletes the completed feature branch and updates local main.",
]

print("Git Workflow Simulator\n")
for line in steps:
    print(line)

print("\nThis simulation shows the collaborative steps used by a small professional team.")
