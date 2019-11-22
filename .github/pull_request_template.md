Checklist for reviewer:

- [ ] Scan the PR and verify that no changes (particularly to `.circleci/config.yml`) will cause environment variables (particularly credentials) to be exposed in test logs
- [ ] Trigger the `integration` CI test by pushing this revision [as discussed in the README](https://github.com/mozilla-services/mozilla-pipeline-schemas#packaging-and-integration-tests-optional)

For glean changes:
- [ ] Update `include/glean/CHANGELOG.md`
