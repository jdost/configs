// Personal settings
user_pref("browser.startup.page", 3);  // Open previous windows and tabs startup
user_pref("media.autoplay.default", 5);  // Block all autoplay

// Fixes
//user_pref("ui.context_menus.after_mouseup", true);  // Fix for weird right click behavior
user_pref("browser.aboutConfig.showWarning", false);  // Don't warn when wanting to change config values

// Hardware Acceleration
user_pref("media.ffmpeg.vaapi.enabled", true);
user_pref("media.rdd-ffmpeg.vaapi.enabled", true);
user_pref("layers.acceleration.disabled", false);

// A lot of these settings are from github.com/pyllyukko/user.js
/**** Security ****/
// Disable Service Workers
user_pref("dom.serviceWorkers.enabled", false);
// Disable Notifications
user_pref("dom.webnotifications.enabled", false);
// Limit timing API
user_pref("dom.enable_performance", false);
user_pref("dom.enable_user_timing", false);
// Disable Web Audio API
//user_pref("dom.webaudio.enabled", false);  // Disabled, discord webapp fails to load
// Limit geo API
user_pref("geo.enabled", false);
user_pref("geo.wifi.uri", "https://location.services.mozilla.com/v1/geolocate?key=%MOZILLA_API_KEY%");
user_pref("geo.wifi.network.uri", "https://location.services.mozilla.com/v1/geolocate?key=%MOZILLA_API_KEY%");
user_pref("geo.wifi.logging.enabled", false);
// Disable OS specific geo services
user_pref("geo.provider.ms-windows-location", false);  // Windows
user_pref("geo.provider.use_corelocation", false);  // Mac
user_pref("geo.provider.use_gpsd", false);  // Linux
// Disable Region updates
user_pref("browser.region.network.url", "");
user_pref("browser.region.update.enabled", false);
// Disable mozTCPSocket
user_pref("dom.mozTCPSocket.enabled", false);
// WebRTC limitations
user_pref("media.peerconnection.enabled", false);
user_pref("media.peerconnection.ice.default_address_only", true);
user_pref("media.peerconnection.ice.no_host", true);
// These are probably necessary for video conferencing
user_pref("media.navigator.enabled", false);
user_pref("media.navigator.video.enabled", false);
user_pref("media.getusermedia.screensharing.enabled", false);
user_pref("media.getusermedia.audiocapture.enabled", false);
// WebGL
user_pref("webgl.disabled", true);
user_pref("webgl.min_capability_mode", true);
user_pref("webgl.disable-extensions", true);
user_pref("webgl.disable-fail-if-major-performance-caveat", true);
user_pref("webgl.enable-debug-renderer-info", true);
user_pref("webgl.dxgl.enabled", false);
user_pref("webgl.enable-webgl2", false);
// WASM
user_pref("javascript.options.wasm", false);
// Misc unnecessary APIs
user_pref("dom.netinfo.enabled", false);  // connection info API
user_pref("dom.network.enabled", false);  // network API
user_pref("dom.battery.enabled", false);  // battery API
user_pref("dom.telephony.enabled", false);  // web telephony
user_pref("beacon.enabled", false);  // beacon- async telemetry transfers
//user_pref("dom.event.clipboardevents.enabled", false);  // limit clipboard events in JS -- Disabled, basically blocks copy+pasting in some pages
user_pref("dom.allow_cut_copy", false);  // disable adding to clipboard via JS
user_pref("media.webspeech.recognition.enabled", false);  // speech recognition
user_pref("media.webspeech.synth.enabled", false);  // speech synthesis
user_pref("device.sensors.enabled", false);
user_pref("browser.send_pings", false);
user_pref("browser.send_pings.require_same_host", true);
user_pref("dom.gamepad.enabled", false);  // JS gamepad API
user_pref("dom.vr.enabled", false);  // JS VR API
user_pref("dom.vibrator.enabled", false);  // JS vibration API
user_pref("dom.enable_resource_timing", false);
user_pref("dom.archivereader.enabled", false);
user_pref("camera.control.face_detection.enabled", false);  // Face detection?
/**** Sane Settings ****/
// Search Locales, avoid GeoIP tricks
user_pref("browser.search.countryCode", "US");
user_pref("browser.search.region", "US");
user_pref("browser.search.geoip.url", "");
// Hard code Accept-Language header
user_pref("intl.accept_languages", "en-US, en");
// Force defined locale rather than OS lookup
user_pref("intl.local.matchOS", false);
// Don't let mozilla override search engines based on location
user_pref("browser.search.geoSpecificDefaults", false);
// Disable linux autocopy functionality
user_pref("clipboard.autocopy", false);
// Strip special characters in clipboard actions
user_pref("clipboard.plainTextOnly", true);
// Tell JS to always use en_us for locale formatting
user_pref("javascript.use_us_english_locale", true);
// Don't fallback to searching for invalid URL entries?
user_pref("keyword.enabled", false);
// Don't trim the protocol in the URL bar
user_pref("browser.urlbar.trimURLs", false);
// Don't try and guess correct domain on invalid URL bar entries
user_pref("browser.fixup.alternate.enabled", false);
// Strip password in URL suggestions?
user_pref("browser.fixup.hide_user_pass", true);
// If SOCKS is enabled, route DNS through SOCKS
user_pref("network.proxy.socks_remote_dns", true);
// Don't detect online/offline status
user_pref("network.manage-offline-status", false);
// Mixed Content Blocked: HTTPS websites that load HTTP content
user_pref("security.mixed_content.block_active_content", true);
user_pref("security.mixed_content.block_display_content", true);
// Anonymize browser details
user_pref("general.buildID.override", "20100101");
user_pref("general.startup.homepage_override.buildID", "20100101");
// Disable bad settings
user_pref("network.jar.open-unsafe-types", false);  // JARs w/ usnafe types
user_pref("security.xpconnect.plugin.unrestricted", false);  // JS can't script plugins
user_pref("security.fileuri.strict_origin_policy", true);  // strict file:/// origins usage
user_pref("browser.urlbar.filter.javascript", true);  // filter javascript from URLBar history
user_pref("gfx.font_rendering.opentype_svg.enabled", false);  // SVG in opentype fonts
//user_pref("svg.disabled", true);  // disable SVG rendering
user_pref("media.video_stats.enabled", false);  // Disable video stats
//user_pref("browser.display.use_document_fonts", 0);  // Hide system fonts to avoid fingerprinting -- Disabled, some pages require icon fonts
// External protocol handler settings
user_pref("network.protocol-handler.warn-external-default", true);
user_pref("network.protocol-handler.external.http", false);
user_pref("network.protocol-handler.external.https", false);
user_pref("network.protocol-handler.external.javascript", false);
user_pref("network.protocol-handler.external.moz-extension", false);
user_pref("network.protocol-handler.external.ftp", false);
user_pref("network.protocol-handler.external.file", false);
user_pref("network.protocol-handler.external.about", false);
user_pref("network.protocol-handler.external.chrome", false);
user_pref("network.protocol-handler.external.blob", false);
user_pref("network.protocol-handler.external.data", false);
user_pref("network.protocol-handler.expose-all", false);
user_pref("network.protocol-handler.expose.http", true);
user_pref("network.protocol-handler.expose.https", true);
user_pref("network.protocol-handler.expose.javascript", true);
user_pref("network.protocol-handler.expose.moz-extension", true);
user_pref("network.protocol-handler.expose.ftp", true);
user_pref("network.protocol-handler.expose.file", true);
user_pref("network.protocol-handler.expose.about", true);
user_pref("network.protocol-handler.expose.chrome", true);
user_pref("network.protocol-handler.expose.blob", true);
user_pref("network.protocol-handler.expose.data", true);
/**** Extensions/Plugins ****/
// Delay add on installation
user_pref("security.dialog_enable_delay", 1000);  // milliseconds
// Require extension signatures
//user_pref("xpinstall.signatures.required", true);
// Sane updating settings
user_pref("extensions.update.enabled", true);
// Disable misc built-ins
user_pref("extensions.getAddons.cache.enabled", false);  // add-on metadata updates
user_pref("lightweightThemes.update.enabled", false);  // Themes/persona updates
user_pref("plugin.state.flash", 0);  // Flash Player NPAPI plugin
user_pref("plugin.state.java", 0);  // Java NPAPI plugin
user_pref("dom.ipc.plugins.flash.subprocess.crashreporter.enabled", false);  // Flash crash reporter
user_pref("dom.ipc.plugins.reportCrashURL", false);  // Don't include URL in crash reports
user_pref("browser.safebrowsing.blockedURIs.enabled", true);  // Use a blocklist for flash
user_pref("plugin.state.libgnome-shell-browser-plugin", 0);  // Gnome shell integration plugin
//user_pref("media.gmp-provider.enabled", false);  // Bundled OpenH264 codec
user_pref("plugins.click_to_play", true);  // Click-to-play plugin
user_pref("extensions.blocklist.enabled", true);  // Use mozilla's blocklists for extensions
user_pref("services.blocklist.update_enabled", true);  // Update mozilla's blocklist
user_pref("extensions.blocklist.url", "https://blocklist.addons.mozilla.org/blocklist/3/%APP_ID%/%APP_VERSION%/");
    // Simplify the blocklist URL to anonymize as much as possible
user_pref("extensions.systemAddon.update.enabled", false);  // Disable system add-on updates
/**** Fix firefox features ****/
user_pref("browser.newtabpage.activity-stream.asrouter.userprefs.cfr", false);  // Extension recommendations
// WebIDE
user_pref("devtools.webide.enabled", false);
user_pref("devtools.webide.autoinstallADBHelper", false);
user_pref("devtools.webide.autoinstallFxdtAdapters", false);
// Remote Debugging
user_pref("devtools.debugger.remote-enabled", false);
user_pref("devtools.chrome.enabled", false);
user_pref("devtools.debugger.force-local", true);
// Mozilla Telemetry/Experiments
user_pref("toolkit.telemetry.enabled", false);
user_pref("toolkit.telemetry.unified", false);
user_pref("toolkit.telemetry.archive.enabled", false);
user_pref("toolkit.telemetry.server", "data:,");
user_pref("toolkit.telemetry.newProfilePing.enabled", false);
user_pref("toolkit.telemetry.shutdownPingSender.enabled", false);
user_pref("toolkit.telemetry.updatePing.enabled", false);
user_pref("toolkit.telemetry.bhrPing.enabled", false);
user_pref("toolkit.telemetry.firstShutdownPing.enabled", false);
user_pref("toolkit.telemetry.coverage.opt-out", true);
user_pref("toolkit.telemetry.pioneer-new-studies-available", false);
user_pref("toolkit.coverage.opt-out", true);
user_pref("toolkit.coverage.endpoing.base", "");
user_pref("browser.ping-centre.telemetry", false);
user_pref("experiments.supported", false);
user_pref("experiments.enabled", false);
user_pref("experiments.manifest.uri", "");
user_pref("extensions.getAddons.showPane", false);  // Uses Google Analytics
user_pref("extensions.htmlaboutaddons.recommendations.enabled", false);
// Pocket
user_pref("browser.pocket.enabled", false);
user_pref("extensions.pocket.enabled", false);
user_pref("browser.newtabpage.activity-stream.feeds.section.topstories", false);
// Misc
user_pref("breakpad.reportURL", "");  // Firefox crash reports
user_pref("browser.tabs.crashReporting.sendReport", false);
user_pref("browser.crashReports.unsubmittedCheck.enabled", false);
user_pref("browser.crashReports.unsubmittedCheck.autoSubmit2", false);
user_pref("dom.flyweb.enabled", false);  // FlyWeb (IoT discovery)
user_pref("browser.uitour.enabled", false);  // UITour backend
user_pref("browser.startup.blankWindow", false);  // disable fast window display on launch
user_pref("pdfjs.disabled", true);  // Built-in PDF viewer
user_pref("app.update.enabled", true);  // Update checks
// Privacy Settings
user_pref("privacy.trackingprotection.enabled", true);
user_pref("privacy.trackingprotection.pbmode.enabled", true);
user_pref("privacy.userContext.enabled", true);
user_pref("privacy.resistFingerprinting", true);
user_pref("privacy.resistFingerprinting.block_mozAddonManager", true);
//user_pref("privacy.resistFingerprinting.letterboxing", true);
//user_pref("privacy.resistFingerprinting.letterboxing.dimensions", "800x600, 1000x1000, 1600x900");
user_pref("extensions.webextensions.restrictedDomains", "");
user_pref("datareporting.healthreport.uploadEnabled", false);
user_pref("datareporting.healthreport.service.enabled", false);
user_pref("datareporting.policy.dataSubmissionEnabled", false);
user_pref("browser.discovery.enabled", false);
user_pref("app.normandy.enabled", false);
user_pref("app.normandy.api_url", "");
user_pref("extensions.shield-recipe-client.enabled", false);
user_pref("app.shield.optoutstudies.enabled", false);
user_pref("loop.logDomains", false);
user_pref("browser.safebrowsing.enabled", true); // Firefox < 50
user_pref("browser.safebrowsing.phishing.enabled", true); // firefox >= 50
user_pref("browser.safebrowsing.malware.enabled", true);
user_pref("browser.safebrowsing.downloads.remote.enabled", false);
/**** Connectivity Optimizations ****/
// Disable prefetching of <link rel="next"> URLs
user_pref("network.prefetch-next", false);
// Disable DNS prefetching
user_pref("network.dns.disablePrefetch", true);
user_pref("network.dns.disablePrefetchFromHTTPS", true);
// Disable the predictive service (Necko)
user_pref("network.predictor.enabled", false);
// Reject .onion hostnames before passing the to DNS
user_pref("network.dns.blockDotOnion", true);
// Disable search suggestions in the search bar
user_pref("browser.search.suggest.enabled", false);
// Disable "Show search suggestions in location bar results"
user_pref("browser.urlbar.suggest.searches", false);
// When using the location bar, don't suggest URLs from browsing history
//user_pref("browser.urlbar.suggest.history", false);
// Disable SSDP
user_pref("browser.casting.enabled", false);
// Disable automatic downloading of OpenH264 codec
user_pref("media.gmp-gmpopenh264.enabled", false);
user_pref("media.gmp-manager.url", "");
// Disable speculative pre-connections
user_pref("network.http.speculative-parallel-limit", 0);
// Disable downloading homepage snippets/messages from Mozilla
user_pref("browser.aboutHomeSnippets.updateUrl", "");
// Never check updates for search engines
user_pref("browser.search.update", false);
// Disable automatic captive portal detection (Firefox >= 52.0)
user_pref("network.captive-portal-service.enabled", false);
user_pref("captivedetect.canonicalURL", "");
user_pref("network.connectivity-service.enabled", false);

// CSP (Content Security Policy)
user_pref("security.csp.experimentalEnabled", true);
user_pref("security.csp.enable", true);
// Auto Login/Forms
user_pref("signon.rememberSignons", false);  // Password manager
user_pref("browser.formfill.enable", false);  // Autofill forms
user_pref("signon.autofillForms", false);
user_pref("signon.formlessCapture.enabled", false);
user_pref("signon.autofillForms.http", false);
user_pref("security.insecure_field_warning.contextual.enabled", true);  // Display insecure warning for logins
user_pref("browser.formfill.expire_days", 0);
//user_pref("signon.storeWhenAutocompleteOff", false);  // Password Manager respects `autocomplete` attribute
user_pref("security.ask_for_password", 2);  // Lock password storage regularly
user_pref("security.password_lifetime", 1);  // Lock password storage after 1m

user_pref("network.negotiate-auth.allow-insecure-ntlm-v1", false);  // NTLM - windows login manager
user_pref("security.sri.enable", true);  // Subresource Integrity
user_pref("privacy.donottrackheader.enabled", true);
//user_pref("network.http.referer.spoofSource", true);
user_pref("network.http.referer.XOriginPolicy", 2);  // No referrer header across domains
user_pref("network.cookie.cookieBehavior", 1);  // 1st party cookies
user_pref("privacy.firstparty.isolate", true);  // https://wiki.mozilla.org/Security/FirstPartyIsolation
user_pref("network.cookie.thirdparty.sessionOnly", true);  // 3rd party cookies don't persist
//user_pref("browser.privatebrowsing.autostart", true);  // Incognito/Private browsing only
user_pref("browser.cache.offline.enable", false);  // Disable offline cache
user_pref("browser.cache.disk.enable", false);  // Disk Cache
user_pref("browser.cache.disk_cache_ssl", false);  // Disk cache for SSL
//user_pref("browser.cache.memory.enable", false);  // Memory Cache
//user_pref("browser.download.manager.retention", 0);  // Download history
//user_pref("network.cookie.lifetimePolicy", 2);  // All cookies are session cookies
user_pref("network.stricttransportsecurity.preloadlist", true);  // HSTS preload
user_pref("dom.security.https_only_mode", true);  // HTTPS only
user_pref("security.ssl.disable_session_identifiers", true);  // TLS session tickets
user_pref("security.cert_pinning.enforcement_level", 2);  // HTTP public key pinning
user_pref("security.pki.sha1_enforcement_level", 1);
user_pref("security.ssl.treat_unsafe_negotiation_as_broken", true); // Warn of unsafe SSL negotiation
//user_pref("security.ssl.require_safe_negotiation", true);  // Enforce SSL safe negotiation
user_pref("security.ssl.errorReporting.automatic", false);  // Auto SSL error reporting
user_pref("browser.ssl_override_behavior", 1);  // Don't pre-fetch SSL certificates
user_pref("network.security.esni.enabled", true);  // Encrypted SNI
user_pref("browser.sessionstore.privacy_level", 2);  // Clear SSL form data
user_pref("browser.helperApps.deleteTempFileOnExit", true);  // Clear temp files on close
user_pref("browser.shell.shortcutFavicons", false);  // Don't store favicons for .url files
user_pref("browser.bookmarks.max_backups", 0);  // Disable bookmark backups
//user_pref("browser.chrome.site_icons", false);  // Disable favicons
user_pref("security.insecure_password.ui.enabled", true);  // Warn on passwords on non HTTPS pages
//user_pref("browser.download.folderList", 2);  // Disable downloading to desktop
//user_pref("dom.event.contextmenu.enabled", false);  // Disable JS overriding context menu
//user_pref("dom.disable_beforeunload", true);  // disable "unload" JS events
//user_pref("browser.download.useDownloadDir", false);  // Always ask download location
user_pref("plugins.update.notifyUser", true);  // Notify on outdated plugins
user_pref("network.IDN_show_punycode", true);  // Force DNS punycode
user_pref("layout.css.visited_links_enabled", false);  // Strip :visited CSS selector
user_pref("browser.shell.checkDefaultBrowser", false);  // Don't check if default browser
user_pref("browser.offline-apps.notify", true);  // Notify when using offline app
// Clear Recent History Settings
//user_pref("privacy.sanitize.timeSpan", 0);  // Always clear everything when clearing history
user_pref("privacy.cpd.offlineApps", true);
user_pref("privacy.cpd.downloads", true);
user_pref("privacy.cpd.formdata", true);
// User-agent spoofing
//user_pref("general.useragent.override", "Mozilla/5.0 (Windows NT 6.1; rv:45.0) Gecko/20100101 Firefox/45.0");
//user_pref("general.appname.override", "Netscape");
//user_pref("general.appversion.override", "5.0 (Windows)");
//user_pref("general.platform.override", "Win32");
//user_pref("general.oscpu.override", "Windows NT 6.1");
// Online Certificate Status Protocol
user_pref("security.OCSP.enabled", 1);
user_pref("security.ssl.enable_ocsp_stapling", true);
user_pref("security.ssl.enable_ocsp_must_staple", true);
user_pref("security.OCSP.require", true);
// TLS version enforcement
user_pref("security.tls.version.min", 1);
user_pref("security.tls.version.max", 4);
user_pref("security.tls.version.fallback-limit", 3);
// New tabpage behavior
user_pref("browser.pagethumbnails.capturing_disabled", true);  // Don't keep page thumbnails
user_pref("browser.newtabpage.enabled", false);
user_pref("browser.newtab.url", "about:blank");
user_pref("browser.newtabpage.activity-stream.feeds.snippets", false);
user_pref("browser.newtabpage.activity-stream.enabled", false);
user_pref("browser.newtabpage.enhanced", false);
user_pref("browser.newtab.preload", false);
user_pref("browser.newtabpage.directory.ping", "");
user_pref("browser.newtabpage.directory.source", "data:text/plain,{}");
// Bookmark exporting
//user_pref("browser.bookmarks.autoExportHTML",  true);
//user_pref("browser.bookmarks.file", '/path/to/bookmarks-export.html');
// Mozilla VPN
user_pref("browser.privatebrowsing.vpnpromourl", "");
user_pref("browser.contentblocking.report.hide_vpn_banner", true);
user_pref("browser.contentblocking.report.vpn.enabled", false);
// URL bar
//user_pref("browser.urlbar.autoFill", false);
//user_pref("browser.urlbar.autoFill.typed", false);
//user_pref("browser.urlbar.autocomplete.enabled", false);  // Disable super bar suggestions
// SSL Cipher cleanup
user_pref("security.ssl3.rsa_null_sha", false);
user_pref("security.ssl3.rsa_null_md5", false);
user_pref("security.ssl3.ecdhe_rsa_null_sha", false);
user_pref("security.ssl3.ecdhe_ecdsa_null_sha", false);
user_pref("security.ssl3.ecdh_rsa_null_sha", false);
user_pref("security.ssl3.ecdh_ecdsa_null_sha", false);
user_pref("security.ssl3.rsa_seed_sha", false);
user_pref("security.ssl3.rsa_rc4_40_md5", false);
user_pref("security.ssl3.rsa_rc2_40_md5", false);
user_pref("security.ssl3.rsa_1024_rc4_56_sha", false);
user_pref("security.ssl3.rsa_camellia_128_sha", false);
user_pref("security.ssl3.ecdhe_rsa_aes_128_sha", false);
user_pref("security.ssl3.ecdhe_ecdsa_aes_128_sha", false);
user_pref("security.ssl3.ecdh_rsa_aes_128_sha", false);
user_pref("security.ssl3.ecdh_ecdsa_aes_128_sha", false);
user_pref("security.ssl3.dhe_rsa_camellia_128_sha", false);
user_pref("security.ssl3.dhe_rsa_aes_128_sha", false);
user_pref("security.ssl3.ecdh_ecdsa_rc4_128_sha", false);
user_pref("security.ssl3.ecdh_rsa_rc4_128_sha", false);
user_pref("security.ssl3.ecdhe_ecdsa_rc4_128_sha", false);
user_pref("security.ssl3.ecdhe_rsa_rc4_128_sha", false);
user_pref("security.ssl3.rsa_rc4_128_md5", false);
user_pref("security.ssl3.rsa_rc4_128_sha", false);
user_pref("security.tls.unrestricted_rc4_fallback", false);
user_pref("security.ssl3.dhe_dss_des_ede3_sha", false);
user_pref("security.ssl3.dhe_rsa_des_ede3_sha", false);
user_pref("security.ssl3.ecdh_ecdsa_des_ede3_sha", false);
user_pref("security.ssl3.ecdh_rsa_des_ede3_sha", false);
user_pref("security.ssl3.ecdhe_ecdsa_des_ede3_sha", false);
user_pref("security.ssl3.ecdhe_rsa_des_ede3_sha", false);
user_pref("security.ssl3.rsa_des_ede3_sha", false);
user_pref("security.ssl3.rsa_fips_des_ede3_sha", false);
user_pref("security.ssl3.ecdh_rsa_aes_256_sha", false);
user_pref("security.ssl3.ecdh_ecdsa_aes_256_sha", false);
user_pref("security.ssl3.rsa_camellia_256_sha", false);
user_pref("security.ssl3.ecdhe_ecdsa_aes_128_gcm_sha256", true); // 0xc02b
user_pref("security.ssl3.ecdhe_rsa_aes_128_gcm_sha256", true); // 0xc02f
user_pref("security.ssl3.ecdhe_ecdsa_chacha20_poly1305_sha256", true);
user_pref("security.ssl3.ecdhe_rsa_chacha20_poly1305_sha256", true);
user_pref("security.ssl3.dhe_rsa_camellia_256_sha", false);
user_pref("security.ssl3.dhe_rsa_aes_256_sha", false);
user_pref("security.ssl3.dhe_dss_aes_128_sha", false);
user_pref("security.ssl3.dhe_dss_aes_256_sha", false);
user_pref("security.ssl3.dhe_dss_camellia_128_sha", false);
user_pref("security.ssl3.dhe_dss_camellia_256_sha", false);
//user_pref("security.ssl3.rsa_aes_256_sha", false);
//user_pref("security.ssl3.rsa_aes_128_sha", false);
//user_pref("security.ssl3.ecdhe_rsa_aes_256_sha", false);
//user_pref("security.ssl3.ecdhe_ecdsa_aes_256_sha", false);
