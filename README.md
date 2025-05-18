# mozilla-pipeline-schemas: generated-schemas

This is the [generated-schemas](https://github.com/mozilla-services/mozilla-pipeline-schemas/commits/test-generated-schemas)
branch of [mozilla-pipeline-schemas](https://github.com/mozilla-services/mozilla-pipeline-schemas).
See the [mps-deploys](https://protosaur.dev/mps-deploys/) dashboard for deployment status of schemas
to [gcp-ingestion](https://github.com/mozilla/gcp-ingestion) and BigQuery.

## directory tree

```bash
schemas
├── accounts-backend
│   ├── accounts-events
│   └── events
├── accounts-cirrus
│   ├── baseline
│   ├── deletion-request
│   ├── enrollment
│   ├── enrollment-status
│   ├── events
│   ├── metrics
│   └── startup
├── accounts-frontend
│   ├── accounts-events
│   ├── deletion-request
│   └── events
├── activity-stream
│   ├── events
│   ├── impression-stats
│   ├── on-save-recs
│   ├── pocket-button
│   ├── sessions
│   └── spoc-fills
├── ads-backend
│   ├── events
│   ├── interaction
│   └── request-stats
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
├── debug-ping-view
│   ├── deletion-request
│   └── events
├── default-browser-agent
│   └── default-browser
├── eng-workflow
│   ├── bmobugs
│   ├── build
│   └── hgpush
├── firefox-accounts
│   ├── activity-flow-metrics
│   └── amplitude-event
├── firefox-crashreporter
│   ├── baseline
│   ├── crash
│   ├── deletion-request
│   ├── events
│   └── metrics
├── firefox-desktop
│   ├── baseline
│   ├── bounce-tracking-protection
│   ├── broken-site-report
│   ├── captcha-detection
│   ├── context-id-deletion-request
│   ├── crash
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── first-startup
│   ├── fog-validation
│   ├── fx-accounts
│   ├── hang-report
│   ├── heartbeat
│   ├── messaging-system
│   ├── metrics
│   ├── new-metric-capture-emulation
│   ├── newtab
│   ├── newtab-content
│   ├── nimbus-targeting-context
│   ├── onboarding-opt-out
│   ├── pageload
│   ├── pocket-button
│   ├── prototype-no-code-events
│   ├── pseudo-main
│   ├── quick-suggest
│   ├── quick-suggest-deletion-request
│   ├── search-with
│   ├── serp-categorization
│   ├── spoc
│   ├── top-sites
│   ├── urlbar-keyword-exposure
│   ├── urlbar-potential-exposure
│   ├── usage-deletion-request
│   ├── usage-reporting
│   ├── use-counters
│   └── user-characteristics
├── firefox-desktop-background-defaultagent
│   ├── baseline
│   ├── default-agent
│   ├── deletion-request
│   ├── events
│   └── metrics
├── firefox-desktop-background-tasks
│   ├── background-tasks
│   ├── baseline
│   ├── crash
│   ├── default-agent
│   ├── deletion-request
│   ├── events
│   ├── heartbeat
│   ├── metrics
│   └── nimbus-targeting-context
├── firefox-desktop-background-update
│   ├── background-update
│   ├── baseline
│   ├── bounce-tracking-protection
│   ├── broken-site-report
│   ├── captcha-detection
│   ├── crash
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── fog-validation
│   ├── hang-report
│   ├── metrics
│   ├── pageload
│   ├── use-counters
│   └── user-characteristics
├── firefox-installer
│   └── install
├── firefox-launcher-process
│   └── launcher-process-failure
├── firefox-translations
│   ├── custom
│   ├── deletion-request
│   └── events
├── glam
│   ├── deletion-request
│   └── events
├── glean
│   └── glean
├── glean-dictionary
│   ├── deletion-request
│   ├── events
│   └── page-view
├── gleanjs-docs
│   ├── deletion-request
│   └── events
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
│   ├── raw
│   ├── sources
│   ├── structured-ingestion
│   └── telemetry-ingestion
├── mobile
│   └── activation
├── monitor-backend
│   └── events
├── monitor-cirrus
│   ├── baseline
│   ├── deletion-request
│   ├── enrollment
│   ├── enrollment-status
│   ├── events
│   ├── metrics
│   └── startup
├── monitor-frontend
│   ├── deletion-request
│   └── events
├── moso-mastodon-backend
│   └── events
├── moso-mastodon-web
│   ├── deletion-request
│   └── events
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
│   ├── baseline
│   ├── daemonsession
│   ├── deletion-request
│   ├── events
│   ├── extensionsession
│   ├── main
│   ├── metrics
│   └── vpnsession
├── mozillavpn-backend-cirrus
│   ├── baseline
│   ├── deletion-request
│   ├── enrollment
│   ├── enrollment-status
│   ├── events
│   ├── metrics
│   └── startup
├── mozphab
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   ├── metrics
│   └── usage
├── net-thunderbird-android
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── net-thunderbird-android-beta
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── net-thunderbird-android-daily
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
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
│   ├── adjust-attribution
│   ├── baseline
│   ├── bookmarks-sync
│   ├── bounce-tracking-protection
│   ├── broken-site-report
│   ├── captcha-detection
│   ├── client-deduplication
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── creditcards-sync
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── fog-validation
│   ├── font-list
│   ├── fx-suggest
│   ├── hang-report
│   ├── history-sync
│   ├── home
│   ├── installation
│   ├── logins-sync
│   ├── metrics
│   ├── migration
│   ├── nimbus
│   ├── onboarding-opt-out
│   ├── pageload
│   ├── play-store-attribution
│   ├── spoc
│   ├── startup-timeline
│   ├── sync
│   ├── tabs-sync
│   ├── topsites-impression
│   ├── usage-deletion-request
│   ├── usage-reporting
│   ├── use-counters
│   └── user-characteristics
├── org-mozilla-fenix-nightly
│   ├── activation
│   ├── addresses-sync
│   ├── adjust-attribution
│   ├── baseline
│   ├── bookmarks-sync
│   ├── bounce-tracking-protection
│   ├── broken-site-report
│   ├── captcha-detection
│   ├── client-deduplication
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── creditcards-sync
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── fog-validation
│   ├── font-list
│   ├── fx-suggest
│   ├── hang-report
│   ├── history-sync
│   ├── home
│   ├── installation
│   ├── logins-sync
│   ├── metrics
│   ├── migration
│   ├── nimbus
│   ├── onboarding-opt-out
│   ├── pageload
│   ├── play-store-attribution
│   ├── spoc
│   ├── startup-timeline
│   ├── sync
│   ├── tabs-sync
│   ├── topsites-impression
│   ├── usage-deletion-request
│   ├── usage-reporting
│   ├── use-counters
│   └── user-characteristics
├── org-mozilla-fennec-aurora
│   ├── activation
│   ├── addresses-sync
│   ├── adjust-attribution
│   ├── baseline
│   ├── bookmarks-sync
│   ├── bounce-tracking-protection
│   ├── broken-site-report
│   ├── captcha-detection
│   ├── client-deduplication
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── creditcards-sync
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── fog-validation
│   ├── font-list
│   ├── fx-suggest
│   ├── hang-report
│   ├── history-sync
│   ├── home
│   ├── installation
│   ├── logins-sync
│   ├── metrics
│   ├── migration
│   ├── nimbus
│   ├── onboarding-opt-out
│   ├── pageload
│   ├── play-store-attribution
│   ├── spoc
│   ├── startup-timeline
│   ├── sync
│   ├── tabs-sync
│   ├── topsites-impression
│   ├── usage-deletion-request
│   ├── usage-reporting
│   ├── use-counters
│   └── user-characteristics
├── org-mozilla-firefox
│   ├── activation
│   ├── addresses-sync
│   ├── adjust-attribution
│   ├── baseline
│   ├── bookmarks-sync
│   ├── bounce-tracking-protection
│   ├── broken-site-report
│   ├── captcha-detection
│   ├── client-deduplication
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── creditcards-sync
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── fog-validation
│   ├── font-list
│   ├── fx-suggest
│   ├── hang-report
│   ├── history-sync
│   ├── home
│   ├── installation
│   ├── logins-sync
│   ├── metrics
│   ├── migration
│   ├── nimbus
│   ├── onboarding-opt-out
│   ├── pageload
│   ├── play-store-attribution
│   ├── spoc
│   ├── startup-timeline
│   ├── sync
│   ├── tabs-sync
│   ├── topsites-impression
│   ├── usage-deletion-request
│   ├── usage-reporting
│   ├── use-counters
│   └── user-characteristics
├── org-mozilla-firefox-beta
│   ├── activation
│   ├── addresses-sync
│   ├── adjust-attribution
│   ├── baseline
│   ├── bookmarks-sync
│   ├── bounce-tracking-protection
│   ├── broken-site-report
│   ├── captcha-detection
│   ├── client-deduplication
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── creditcards-sync
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── fog-validation
│   ├── font-list
│   ├── fx-suggest
│   ├── hang-report
│   ├── history-sync
│   ├── home
│   ├── installation
│   ├── logins-sync
│   ├── metrics
│   ├── migration
│   ├── nimbus
│   ├── onboarding-opt-out
│   ├── pageload
│   ├── play-store-attribution
│   ├── spoc
│   ├── startup-timeline
│   ├── sync
│   ├── tabs-sync
│   ├── topsites-impression
│   ├── usage-deletion-request
│   ├── usage-reporting
│   ├── use-counters
│   └── user-characteristics
├── org-mozilla-firefox-vpn
│   ├── baseline
│   ├── daemonsession
│   ├── deletion-request
│   ├── events
│   ├── extensionsession
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
│   ├── bounce-tracking-protection
│   ├── broken-site-report
│   ├── captcha-detection
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── fog-validation
│   ├── hang-report
│   ├── metrics
│   ├── pageload
│   ├── usage-deletion-request
│   ├── usage-reporting
│   ├── use-counters
│   └── user-characteristics
├── org-mozilla-focus-beta
│   ├── activation
│   ├── baseline
│   ├── bounce-tracking-protection
│   ├── broken-site-report
│   ├── captcha-detection
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── fog-validation
│   ├── hang-report
│   ├── metrics
│   ├── pageload
│   ├── usage-deletion-request
│   ├── usage-reporting
│   ├── use-counters
│   └── user-characteristics
├── org-mozilla-focus-nightly
│   ├── activation
│   ├── baseline
│   ├── bounce-tracking-protection
│   ├── broken-site-report
│   ├── captcha-detection
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── fog-validation
│   ├── hang-report
│   ├── metrics
│   ├── pageload
│   ├── usage-deletion-request
│   ├── usage-reporting
│   ├── use-counters
│   └── user-characteristics
├── org-mozilla-ios-fennec
│   ├── addresses-sync
│   ├── baseline
│   ├── bookmarks-sync
│   ├── creditcards-sync
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── fx-suggest
│   ├── history-sync
│   ├── logins-sync
│   ├── metrics
│   ├── nimbus
│   ├── onboarding-opt-out
│   ├── sync
│   ├── tabs-sync
│   ├── temp-baseline
│   ├── temp-bookmarks-sync
│   ├── temp-clients-sync
│   ├── temp-credit-cards-sync
│   ├── temp-history-sync
│   ├── temp-logins-sync
│   ├── temp-rust-tabs-sync
│   ├── temp-sync
│   ├── temp-tabs-sync
│   ├── topsites-impression
│   ├── usage-deletion-request
│   └── usage-reporting
├── org-mozilla-ios-firefox
│   ├── addresses-sync
│   ├── baseline
│   ├── bookmarks-sync
│   ├── creditcards-sync
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── fx-suggest
│   ├── history-sync
│   ├── logins-sync
│   ├── metrics
│   ├── nimbus
│   ├── onboarding-opt-out
│   ├── sync
│   ├── tabs-sync
│   ├── temp-baseline
│   ├── temp-bookmarks-sync
│   ├── temp-clients-sync
│   ├── temp-credit-cards-sync
│   ├── temp-history-sync
│   ├── temp-logins-sync
│   ├── temp-rust-tabs-sync
│   ├── temp-sync
│   ├── temp-tabs-sync
│   ├── topsites-impression
│   ├── usage-deletion-request
│   └── usage-reporting
├── org-mozilla-ios-firefoxbeta
│   ├── addresses-sync
│   ├── baseline
│   ├── bookmarks-sync
│   ├── creditcards-sync
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── first-session
│   ├── fx-suggest
│   ├── history-sync
│   ├── logins-sync
│   ├── metrics
│   ├── nimbus
│   ├── onboarding-opt-out
│   ├── sync
│   ├── tabs-sync
│   ├── temp-baseline
│   ├── temp-bookmarks-sync
│   ├── temp-clients-sync
│   ├── temp-credit-cards-sync
│   ├── temp-history-sync
│   ├── temp-logins-sync
│   ├── temp-rust-tabs-sync
│   ├── temp-sync
│   ├── temp-tabs-sync
│   ├── topsites-impression
│   ├── usage-deletion-request
│   └── usage-reporting
├── org-mozilla-ios-firefoxvpn
│   ├── baseline
│   ├── daemonsession
│   ├── deletion-request
│   ├── events
│   ├── extensionsession
│   ├── main
│   ├── metrics
│   └── vpnsession
├── org-mozilla-ios-firefoxvpn-network-extension
│   ├── baseline
│   ├── daemonsession
│   ├── deletion-request
│   ├── events
│   ├── extensionsession
│   ├── main
│   ├── metrics
│   └── vpnsession
├── org-mozilla-ios-focus
│   ├── baseline
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── metrics
│   ├── usage-deletion-request
│   └── usage-reporting
├── org-mozilla-ios-klar
│   ├── baseline
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── metrics
│   ├── usage-deletion-request
│   └── usage-reporting
├── org-mozilla-ios-lockbox
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── org-mozilla-ios-tiktok-reporter
│   ├── baseline
│   ├── deletion-request
│   ├── download-data
│   ├── email
│   ├── events
│   ├── metrics
│   ├── screen-recording
│   └── tiktok-report
├── org-mozilla-ios-tiktok-reporter-tiktok-reportershare
│   ├── baseline
│   ├── deletion-request
│   ├── download-data
│   ├── email
│   ├── events
│   ├── metrics
│   ├── screen-recording
│   └── tiktok-report
├── org-mozilla-klar
│   ├── activation
│   ├── baseline
│   ├── bounce-tracking-protection
│   ├── broken-site-report
│   ├── captcha-detection
│   ├── cookie-banner-report-site
│   ├── crash
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── fog-validation
│   ├── hang-report
│   ├── metrics
│   ├── pageload
│   ├── usage-deletion-request
│   ├── usage-reporting
│   ├── use-counters
│   └── user-characteristics
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
├── org-mozilla-social-nightly
│   ├── baseline
│   ├── deletion-request
│   ├── events
│   └── metrics
├── org-mozilla-tiktokreporter
│   ├── baseline
│   ├── deletion-request
│   ├── download-data
│   ├── email
│   ├── events
│   ├── metrics
│   ├── screen-recording
│   └── tiktok-report
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
│   ├── bounce-tracking-protection
│   ├── broken-site-report
│   ├── captcha-detection
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── fog-validation
│   ├── hang-report
│   ├── messaging-system
│   ├── metrics
│   ├── new-metric-capture-emulation
│   ├── newtab
│   ├── newtab-content
│   ├── onboarding-opt-out
│   ├── pageload
│   ├── pseudo-main
│   ├── spoc
│   ├── top-sites
│   ├── usage-deletion-request
│   ├── usage-reporting
│   ├── use-counters
│   └── user-characteristics
├── pocket
│   └── fire-tv-events
├── regrets-reporter
│   └── regrets-reporter-update
├── regrets-reporter-ucs
│   ├── deletion-request
│   ├── events
│   ├── main-events
│   ├── regret-details
│   ├── video-data
│   └── video-index
├── relay-backend
│   └── events
├── subscription-platform-backend
│   └── events
├── syncstorage
│   └── events
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
│   ├── first-shutdown-use-counter
│   ├── flash-shield-study
│   ├── focus-event
│   ├── frecency-update
│   ├── ftu
│   ├── health
│   ├── heartbeat
│   ├── installation
│   ├── main
│   ├── main-use-counter
│   ├── malware-addon-states
│   ├── mobile-event
│   ├── mobile-metrics
│   ├── modules
│   ├── new-profile
│   ├── normandy-login-study
│   ├── optout
│   ├── outofdate-notifications-system-addon
│   ├── pre-account
│   ├── prio
│   ├── regrets-reporter-update
│   ├── saved-session
│   ├── saved-session-use-counter
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
├── thunderbird-desktop
│   ├── baseline
│   ├── bounce-tracking-protection
│   ├── broken-site-report
│   ├── captcha-detection
│   ├── dau-reporting
│   ├── deletion-request
│   ├── events
│   ├── fog-validation
│   ├── hang-report
│   ├── metrics
│   ├── pageload
│   ├── use-counters
│   └── user-characteristics
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

882 directories
```

