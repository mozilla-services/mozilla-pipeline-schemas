Checklist for reviewer:

- [ ] Commits should reference a bug or github issue, if relevant (if a bug is referenced, the pull request should include the bug number in the title)
- [ ] If adding a new field, the field should have a description (see #576 for an example)
- [ ] Scan the PR and verify that no changes (particularly to `.circleci/config.yml`) will cause environment variables (particularly credentials) to be exposed in test logs

For glean changes:
- [ ] Update `templates/include/glean/CHANGELOG.md`
