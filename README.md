# mozilla-pipeline-schemas: generated-schemas

This is the [generated-schemas](https://github.com/mozilla-services/mozilla-pipeline-schemas/commits/test-generated-schemas)
branch of [mozilla-pipeline-schemas](https://github.com/mozilla-services/mozilla-pipeline-schemas).
See the [mps-deploys](https://protosaur.dev/mps-deploys/) dashboard for deployment status of schemas
to [gcp-ingestion](https://github.com/mozilla/gcp-ingestion) and BigQuery.

## directory tree

```bash
schemas
├── accounts-backend
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── accounts-frontend
│   ├── deletion-request
│   └── events
├── activity-stream
│   ├── events
│   ├── impression-stats
│   ├── on-save-recs
│   ├── pocket-button
│   ├── sessions
│   └── spoc-fills
├── bedrock
│   ├── deletion-request
│   ├── events
│   ├── interaction
│   ├── non-interaction
│   └── page-view
├── burnham
│   ├── baseline
│   ├── deletion-request
│   ├── discovery
│   ├── events
│   ├── metrics
│   ├── space-ship-ready
│   └── starbase46
├── contextual-services
│   ├── quicksuggest-block
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
│   ├── crash
│   ├── deletion-request
│   ├── events
│   ├── first-startup
│   ├── fog-validation
│   ├── messaging-system
│   ├── metrics
│   ├── new-metric-capture-emulation
│   ├── newtab
│   ├── pageload
│   └── pseudo-main
├── firefox-desktop-background-tasks
│   ├── background-tasks
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── firefox-desktop-background-update
│   ├── background-update
│   ├── baseline
│   ├── crash
│   ├── deletion-request
│   ├── events
│   ├── fog-validation
│   ├── metrics
│   └── pageload
├── firefox-installer
│   └── install
├── firefox-launcher-process
│   └── launcher-process-failure
├── firefox-translations
│   ├── custom
│   ├── deletion-request
│   └── events
├── glean
│   └── glean
├── glean-dictionary
│   ├── deletion-request
│   ├── events
│   └── page-view
├── mdn-yari
│   ├── action
│   ├── deletion-request
│   ├── events
│   └── page
├── messaging-system
│   ├── cfr
│   ├── infobar
│   ├── moments
│   ├── onboarding
│   ├── personalization-experiment
│   ├── snippets
│   ├── spotlight
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
├── mlhackweek-search
│   ├── action
│   ├── baseline
│   ├── custom
│   ├── deletion-request
│   ├── events
│   └── metrics
├── mobile
│   └── activation
├── mozdata
│   └── event
├── mozilla-lockbox
│   ├── addresses-sync
│   ├── baseline
│   ├── bookmarks-sync
│   ├── creditcards-sync
│   ├── deletion-request
│   ├── events
│   ├── history-sync
│   ├── logins-sync
│   ├── metrics
│   ├── sync
│   └── tabs-sync
├── mozilla-mach
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   ├── metrics
│   └── usage
├── mozillavpn
│   ├── daemonsession
│   ├── deletion-request
│   ├── events
│   ├── main
│   └── vpnsession
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
│   ├── deletion-request
│   └── events
├── org-mozilla-connect-firefox
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── org-mozilla-fenix
│   ├── activation
│   ├── addresses-sync
│   ├── baseline
│   ├── bookmarks-sync
│   ├── client-deduplication
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── creditcards-sync
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── fog-validation
│   ├── history-sync
│   ├── installation
│   ├── logins-sync
│   ├── metrics
│   ├── migration
│   ├── pageload
│   ├── spoc
│   ├── startup-timeline
│   ├── sync
│   ├── tabs-sync
│   └── topsites-impression
├── org-mozilla-fenix-nightly
│   ├── activation
│   ├── addresses-sync
│   ├── baseline
│   ├── bookmarks-sync
│   ├── client-deduplication
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── creditcards-sync
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── fog-validation
│   ├── history-sync
│   ├── installation
│   ├── logins-sync
│   ├── metrics
│   ├── migration
│   ├── pageload
│   ├── spoc
│   ├── startup-timeline
│   ├── sync
│   ├── tabs-sync
│   └── topsites-impression
├── org-mozilla-fennec-aurora
│   ├── activation
│   ├── addresses-sync
│   ├── baseline
│   ├── bookmarks-sync
│   ├── client-deduplication
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── creditcards-sync
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── fog-validation
│   ├── history-sync
│   ├── installation
│   ├── logins-sync
│   ├── metrics
│   ├── migration
│   ├── pageload
│   ├── spoc
│   ├── startup-timeline
│   ├── sync
│   ├── tabs-sync
│   └── topsites-impression
├── org-mozilla-firefox
│   ├── activation
│   ├── addresses-sync
│   ├── baseline
│   ├── bookmarks-sync
│   ├── client-deduplication
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── creditcards-sync
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── fog-validation
│   ├── history-sync
│   ├── installation
│   ├── logins-sync
│   ├── metrics
│   ├── migration
│   ├── pageload
│   ├── spoc
│   ├── startup-timeline
│   ├── sync
│   ├── tabs-sync
│   └── topsites-impression
├── org-mozilla-firefox-beta
│   ├── activation
│   ├── addresses-sync
│   ├── baseline
│   ├── bookmarks-sync
│   ├── client-deduplication
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── creditcards-sync
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── fog-validation
│   ├── history-sync
│   ├── installation
│   ├── logins-sync
│   ├── metrics
│   ├── migration
│   ├── pageload
│   ├── spoc
│   ├── startup-timeline
│   ├── sync
│   ├── tabs-sync
│   └── topsites-impression
├── org-mozilla-firefox-vpn
│   ├── baseline
│   ├── daemonsession
│   ├── deletion-request
│   ├── events
│   ├── main
│   ├── metrics
│   └── vpnsession
├── org-mozilla-firefoxreality
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   ├── launch
│   └── metrics
├── org-mozilla-focus
│   ├── activation
│   ├── baseline
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── deletion-request
│   ├── events
│   ├── fog-validation
│   ├── metrics
│   └── pageload
├── org-mozilla-focus-beta
│   ├── activation
│   ├── baseline
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── deletion-request
│   ├── events
│   ├── fog-validation
│   ├── metrics
│   └── pageload
├── org-mozilla-focus-nightly
│   ├── activation
│   ├── baseline
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── deletion-request
│   ├── events
│   ├── fog-validation
│   ├── metrics
│   └── pageload
├── org-mozilla-ios-fennec
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── metrics
│   ├── temp-bookmarks-sync
│   ├── temp-clients-sync
│   ├── temp-history-sync
│   ├── temp-logins-sync
│   ├── temp-rust-tabs-sync
│   ├── temp-sync
│   ├── temp-tabs-sync
│   └── topsites-impression
├── org-mozilla-ios-firefox
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── metrics
│   ├── temp-bookmarks-sync
│   ├── temp-clients-sync
│   ├── temp-history-sync
│   ├── temp-logins-sync
│   ├── temp-rust-tabs-sync
│   ├── temp-sync
│   ├── temp-tabs-sync
│   └── topsites-impression
├── org-mozilla-ios-firefoxbeta
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── metrics
│   ├── temp-bookmarks-sync
│   ├── temp-clients-sync
│   ├── temp-history-sync
│   ├── temp-logins-sync
│   ├── temp-rust-tabs-sync
│   ├── temp-sync
│   ├── temp-tabs-sync
│   └── topsites-impression
├── org-mozilla-ios-firefoxvpn
│   ├── baseline
│   ├── daemonsession
│   ├── deletion-request
│   ├── events
│   ├── main
│   ├── metrics
│   └── vpnsession
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
├── org-mozilla-klar
│   ├── activation
│   ├── baseline
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── deletion-request
│   ├── events
│   ├── fog-validation
│   ├── metrics
│   └── pageload
├── org-mozilla-mozregression
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   ├── metrics
│   └── usage
├── org-mozilla-reference-browser
│   ├── baseline
│   ├── crash
│   ├── deletion-request
│   ├── events
│   └── metrics
├── org-mozilla-tv-firefox
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── org-mozilla-vrbrowser
│   ├── addresses-sync
│   ├── baseline
│   ├── bookmarks-sync
│   ├── creditcards-sync
│   ├── deletion-request
│   ├── events
│   ├── history-sync
│   ├── logins-sync
│   ├── metrics
│   ├── session-end
│   ├── sync
│   └── tabs-sync
├── pine
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   ├── fog-validation
│   ├── messaging-system
│   ├── metrics
│   ├── new-metric-capture-emulation
│   ├── newtab
│   ├── pageload
│   └── pseudo-main
├── pioneer-citp-news-disinfo
│   ├── deletion-request
│   ├── measurements
│   ├── pioneer-enrollment
│   └── rallymeasurements
├── pioneer-citp-news-disinfo-two
│   ├── deletion-request
│   ├── measurements
│   ├── pioneer-enrollment
│   └── rallymeasurements
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
├── pioneer-sgsb-beyond-the-paywall
│   ├── advertisement
│   ├── article-content
│   ├── deletion-request
│   ├── page-nav
│   ├── page-nav-sensitive
│   ├── pioneer-enrollment
│   └── total-timing
├── pocket
│   └── fire-tv-events
├── rally-attention-stream
│   ├── advertisements
│   ├── article-contents
│   ├── attribution
│   ├── deletion-request
│   ├── events
│   ├── study-enrollment
│   ├── tracking-pixel
│   ├── user-journey
│   ├── youtube-ads
│   ├── youtube-video-details
│   └── youtube-video-recommendations
├── rally-citp-search-engine-usage
│   ├── ballot-interaction
│   ├── deletion-request
│   ├── events
│   ├── modal-interaction
│   ├── notice-interaction
│   ├── online-service-navigation
│   ├── serp-visit
│   ├── study-enrollment
│   └── study-initialization
├── rally-core
│   ├── deletion-request
│   ├── demographics
│   ├── enrollment
│   ├── events
│   ├── study-enrollment
│   ├── study-unenrollment
│   ├── unenrollment
│   └── uninstall-deletion
├── rally-debug
│   ├── deletion-request
│   ├── demographics
│   ├── enrollment
│   ├── events
│   ├── study-enrollment
│   ├── study-unenrollment
│   └── uninstall-deletion
├── rally-markup-fb-pixel-hunt
│   ├── deletion-request
│   ├── events
│   ├── fbpixelhunt-event
│   ├── fbpixelhunt-journey
│   ├── fbpixelhunt-pixel
│   └── study-enrollment
├── rally-study-zero-one
│   ├── deletion-request
│   ├── events
│   ├── rs01-event
│   └── study-enrollment
├── rally-zero-one
│   ├── deletion-request
│   ├── measurements
│   └── pioneer-enrollment
├── regrets-reporter
│   └── regrets-reporter-update
├── regrets-reporter-ucs
│   ├── deletion-request
│   ├── events
│   ├── main-events
│   ├── regret-details
│   ├── video-data
│   └── video-index
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
├── treeherder
│   ├── classified
│   ├── deletion-request
│   └── events
├── viu-politica
│   ├── deletion-request
│   ├── events
│   ├── main-events
│   ├── regret-details
│   ├── video-data
│   └── video-index
└── webpagetest
    └── webpagetest-run

627 directories
```

