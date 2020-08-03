Checklist for reviewer:

- [ ] Commits should reference a bug or github issue, if relevant (if a bug is referenced, the pull request should include the bug number in the title)
- [ ] Scan the PR and verify that no changes (particularly to `.circleci/config.yml`) will cause environment variables (particularly credentials) to be exposed in test logs
- [ ] If the PR comes from a fork, trigger the `integration` CI test by pushing this revision [as discussed in the README](https://github.com/mozilla-services/mozilla-pipeline-schemas#packaging-and-integration-tests-optional) and review the report posted in the comments.

For glean changes:
- [ ] Update `templates/include/glean/CHANGELOG.md`
