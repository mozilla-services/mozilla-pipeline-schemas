# mozilla-pipeline-schemas: generated-schemas

This is the [generated-schemas](https://github.com/mozilla-services/mozilla-pipeline-schemas/commits/test-generated-schemas)
branch of [mozilla-pipeline-schemas](https://github.com/mozilla-services/mozilla-pipeline-schemas).
See the [mps-deploys](https://protosaur.dev/mps-deploys/) dashboard for deployment status of schemas
to [gcp-ingestion](https://github.com/mozilla/gcp-ingestion) and BigQuery.

## directory tree

```bash
schemas
├── activity-stream
│   ├── events
│   ├── impression-stats
│   ├── on-save-recs
│   ├── pocket-button
│   ├── sessions
│   └── spoc-fills
├── burnham
│   ├── baseline
│   ├── deletion-request
│   ├── discovery
│   ├── events
│   ├── metrics
│   ├── space-ship-ready
│   └── starbase46
├── contextual-services
│   ├── quicksuggest-click
│   ├── quicksuggest-impression
│   ├── topsites-click
│   └── topsites-impression
├── coverage
│   └── coverage
├── default-browser-agent
│   └── default-browser
├── edge-validator
│   └── error-report
├── eng-workflow
│   ├── bmobugs
│   ├── build
│   └── hgpush
├── firefox-accounts
│   ├── activity-flow-metrics
│   └── amplitude-event
├── firefox-desktop
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   ├── fog-validation
│   └── metrics
├── firefox-desktop-background-update
│   ├── background-update
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── firefox-installer
│   └── install
├── firefox-launcher-process
│   └── launcher-process-failure
├── glean
│   └── glean
├── messaging-system
│   ├── cfr
│   ├── infobar
│   ├── moments
│   ├── onboarding
│   ├── personalization-experiment
│   ├── snippets
│   ├── undesired-events
│   └── whats-new-panel
├── metadata
│   ├── credentials
│   ├── decoded
│   ├── error
│   ├── metaschema
│   ├── pioneer-decoded
│   ├── pioneer-error
│   ├── pioneer-ingestion
│   ├── raw
│   ├── sources
│   ├── structured-ingestion
│   └── telemetry-ingestion
├── mobile
│   └── activation
├── mozdata
│   └── event
├── mozilla-lockbox
│   ├── baseline
│   ├── bookmarks-sync
│   ├── deletion-request
│   ├── events
│   ├── history-sync
│   ├── logins-sync
│   ├── metrics
│   └── sync
├── mozilla-mach
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   ├── metrics
│   └── usage
├── mozphab
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   ├── metrics
│   └── usage
├── mozza
│   └── event
├── org-mozilla-bergamot
│   ├── custom
│   └── deletion-request
├── org-mozilla-connect-firefox
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── org-mozilla-fenix
│   ├── activation
│   ├── baseline
│   ├── bookmarks-sync
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── history-sync
│   ├── installation
│   ├── logins-sync
│   ├── metrics
│   ├── migration
│   ├── startup-timeline
│   └── sync
├── org-mozilla-fenix-nightly
│   ├── activation
│   ├── baseline
│   ├── bookmarks-sync
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── history-sync
│   ├── installation
│   ├── logins-sync
│   ├── metrics
│   ├── migration
│   ├── startup-timeline
│   └── sync
├── org-mozilla-fennec-aurora
│   ├── activation
│   ├── baseline
│   ├── bookmarks-sync
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── history-sync
│   ├── installation
│   ├── logins-sync
│   ├── metrics
│   ├── migration
│   ├── startup-timeline
│   └── sync
├── org-mozilla-firefox
│   ├── activation
│   ├── baseline
│   ├── bookmarks-sync
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── history-sync
│   ├── installation
│   ├── logins-sync
│   ├── metrics
│   ├── migration
│   ├── startup-timeline
│   └── sync
├── org-mozilla-firefox-beta
│   ├── activation
│   ├── baseline
│   ├── bookmarks-sync
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── history-sync
│   ├── installation
│   ├── logins-sync
│   ├── metrics
│   ├── migration
│   ├── startup-timeline
│   └── sync
├── org-mozilla-firefoxreality
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   ├── launch
│   └── metrics
├── org-mozilla-ios-fennec
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── org-mozilla-ios-firefox
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── org-mozilla-ios-firefoxbeta
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── org-mozilla-ios-focus
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── org-mozilla-ios-klar
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── org-mozilla-ios-lockbox
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── org-mozilla-mozregression
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   ├── metrics
│   └── usage
├── org-mozilla-reference-browser
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── org-mozilla-tv-firefox
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── org-mozilla-vrbrowser
│   ├── baseline
│   ├── bookmarks-sync
│   ├── deletion-request
│   ├── events
│   ├── history-sync
│   ├── logins-sync
│   ├── metrics
│   ├── session-end
│   └── sync
├── pioneer-citp-news-disinfo
│   ├── deletion-request
│   ├── measurements
│   └── pioneer-enrollment
├── pioneer-citp-news-disinfo-two
│   ├── deletion-request
│   ├── measurements
│   └── pioneer-enrollment
├── pioneer-core
│   ├── deletion-request
│   ├── demographic-survey
│   ├── pioneer-enrollment
│   ├── probes
│   ├── survey
│   └── uninstall-deletion
├── pioneer-debug
│   ├── debug
│   ├── deletion-request
│   └── pioneer-enrollment
├── pioneer-meta
│   └── pioneer-enrollment
├── pocket
│   └── fire-tv-events
├── rally-debug
│   ├── deletion-request
│   ├── demographics
│   ├── enrollment
│   ├── study-enrollment
│   └── study-unenrollment
├── rally-zero-one
│   ├── deletion-request
│   ├── measurements
│   └── pioneer-enrollment
├── regrets-reporter
│   └── regrets-reporter-update
├── telemetry
│   ├── addon-install-blocked
│   ├── advancedtelemetry
│   ├── anonymous
│   ├── bhr
│   ├── block-autoplay
│   ├── certificate-checker
│   ├── core
│   ├── crash
│   ├── deletion
│   ├── deletion-request
│   ├── deployment-checker
│   ├── disable-sha1rollout
│   ├── dnssec-study-v1
│   ├── downgrade
│   ├── event
│   ├── first-shutdown
│   ├── flash-shield-study
│   ├── focus-event
│   ├── frecency-update
│   ├── ftu
│   ├── health
│   ├── heartbeat
│   ├── installation
│   ├── main
│   ├── malware-addon-states
│   ├── mobile-event
│   ├── mobile-metrics
│   ├── modules
│   ├── new-profile
│   ├── normandy-login-study
│   ├── optout
│   ├── outofdate-notifications-system-addon
│   ├── pioneer-study
│   ├── pre-account
│   ├── prio
│   ├── regrets-reporter-update
│   ├── saved-session
│   ├── searchvol
│   ├── searchvolextra
│   ├── shield-icq-v1
│   ├── shield-study
│   ├── shield-study-addon
│   ├── shield-study-error
│   ├── sync
│   ├── system-addon-deployment-diagnostics
│   ├── testpilot
│   ├── testpilottest
│   ├── third-party-modules
│   ├── tls-13-study
│   ├── tls-13-study-v1
│   ├── tls-13-study-v2
│   ├── tls-13-study-v3
│   ├── tls-13-study-v4
│   ├── tls13-middlebox-alt-server-hello-1
│   ├── tls13-middlebox-beta
│   ├── tls13-middlebox-draft22
│   ├── tls13-middlebox-ghack
│   ├── tls13-middlebox-repetition
│   ├── tls13-middlebox-testing
│   ├── uitour-tag
│   ├── uninstall
│   ├── untrusted-modules
│   ├── update
│   ├── voice
│   ├── voice-feedback
│   ├── x-contextual-feature-recommendation
│   └── xfocsp-error-report
└── webpagetest
    └── webpagetest-run

344 directories
```

