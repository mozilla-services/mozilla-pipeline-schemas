Checklist for reviewer:

- [ ] Commits should reference a bug or github issue, if relevant (if a bug is referenced, the pull request should include the bug number in the title)
- [ ] If adding a new field, the field should have a description (see #576 for an example)
- [ ] If coming from a fork, run integration tests: `./.github/push-to-trigger-integration <username>:<branchname>`

For glean changes:
- [ ] Update `templates/include/glean/CHANGELOG.md`

For modifications to schemas in restricted namespaces (see [`CODEOWNERS`](/CODEOWNERS)):
- [ ] Follow the [change control procedure](https://docs.google.com/document/d/1TTJi4ht7NuzX6BPG_KTr6omaZg70cEpxe9xlpfnHj9k/edit#heading=h.ttegrcfy18ck)
