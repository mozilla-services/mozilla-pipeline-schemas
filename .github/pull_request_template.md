Checklist for reviewer:

- [ ] Commits should reference a bug or github issue, if relevant (if a bug is referenced, the pull request should include the bug number in the title)
- [ ] Scan the PR and verify that no changes (particularly to `.circleci/config.yml`) will cause environment variables (particularly credentials) to be exposed in test logs
- [ ] Watch the results of the `integration` CI test and make sure the error rates do not increase without justification.

For glean changes:
- [ ] Update `include/glean/CHANGELOG.md`
