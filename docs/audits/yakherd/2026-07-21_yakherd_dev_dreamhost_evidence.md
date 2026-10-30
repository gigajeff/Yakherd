# Yakherd.dev DreamHost Capability Evidence

- Retrieved/observed: 2026-07-21
- Purpose: Section 10 pre-Implementation capability gate
- Scope: official DreamHost documentation plus signed-in, non-secret panel
  inventory; no probe file, OpenAI key, live model call, concierge deployment,
  Git mutation, or production activation
- Authority: evidence for Architecture and Red Team only

## Signed-In Panel Inventory

The following non-secret facts were observed without recording personal account
identifiers, existing unrelated sites/users, passwords, or credential-bearing
panel links:

- `yakherd.dev` was changed from DNS-only to Shared Unlimited hosting on the
  existing shared server with a new dedicated website user, PHP 8.3, and web
  directory `$HOME/yakherd.dev/public`.
- `staging.yakherd.dev` was created under the same dedicated user with PHP 8.3
  and web directory `$HOME/yakherd.dev/staging-public`.
- DreamHost reported both hosting setups successful.
- Free Let's Encrypt issuance for the newly hosted names was pending/automatic;
  valid staging HTTPS had not yet been proven.
- No website/probe bytes, `.htaccess`, `.htpasswd`, SSH key, API key, application
  secret, or cron job were uploaded or created.

## Official DreamHost Facts

1. Shared hosting runs Apache and supports `.htaccess`; the account's Shared
   Unlimited target is therefore not an Nginx vhost with a user-editable external
   `nginx/<domain>` configuration directory.
2. The panel Htaccess/WebDAV password-protection tool creates server-owned
   `.htaccess` and `.htpasswd` files inside the website directory, prevents the
   user from editing them, and overwrites an existing `.htaccess` file.
3. DreamHost also documents manual Apache Basic Auth using a user-managed
   `.htaccess` plus an `AuthUserFile`; HTTPS must be valid before credentials are
   tested.
4. DreamHost's access-log panel records timestamp, status, IP address, path,
   referrer, and user agent. Current documentation says HTTP/access logs are
   retained for up to/default seven days, within v3's 30-day maximum.
5. Panel-created cron jobs can run as the website user, support locking, and can
   invoke PHP 8.3 at `/usr/local/php83/bin/php`. Panel schedule times use the
   server's Pacific timezone, so a desired UTC execution time must be converted
   and daylight-saving behavior recorded rather than assumed.
6. A website user can be changed from SFTP-only to a Shell user in the panel;
   only a Shell user can run SSH commands required by the reviewed atomic deploy
   and capability checks.
7. Each `.dev` subdomain needs its own certificate. DreamHost provides free
   Let's Encrypt certificates with automatic renewal; `.dev` browsers force
   HTTPS.

## Official Sources

- Shared hosting uses Apache:
  `https://help.dreamhost.com/hc/en-us/articles/214878798-Hosting-plan-FAQs`
- Panel password protection behavior:
  `https://help.dreamhost.com/hc/en-us/articles/217239847-Password-protecting-your-site-in-the-DreamHost-panel`
- Manual Apache Basic Auth:
  `https://help.dreamhost.com/hc/en-us/articles/216363187-Password-protecting-your-site-with-an-htaccess-file`
- Access-log fields and seven-day retention:
  `https://help.dreamhost.com/hc/en-us/articles/36522940441492-Viewing-your-access-logs-in-the-panel`
- Website log retention:
  `https://help.dreamhost.com/hc/en-us/articles/35845703281556-The-Website-Logs-page`
- Panel cron jobs and PHP paths:
  `https://help.dreamhost.com/hc/en-us/articles/215088668-Create-a-cron-job`
- Enabling Shell/SSH access:
  `https://help.dreamhost.com/hc/en-us/articles/216385837-Creating-a-user-with-Shell-SSH-access`
- SSL and `.dev` behavior:
  `https://help.dreamhost.com/hc/en-us/articles/216041537-SSL-certificates-overview`
- Let's Encrypt behavior:
  `https://help.dreamhost.com/hc/en-us/articles/216539558-Let-s-Encrypt-SSL-certificate-overview`

## Capability Result

PASS so far: same dedicated user, exact production/staging roots, shared server,
PHP 8.3 selection, documented Apache `.htaccess`, documented Shell conversion,
documented panel cron/PHP 8.3 path, and documented seven-day hosting-log
retention.

NOT YET PROVEN: valid staging HTTPS; Shell conversion and SSH authentication;
PHP extensions/functions; filesystem permissions; `flock`; symlink/atomic
rename; `.htaccess` headers/404; manual Basic Auth; outbound TLS; runtime limits;
actual logs; cron execution; probe deletion.

FAILED ASSUMPTION: v3 requires vhost-level staging Basic Auth whose configuration
bytes remain outside the symlinked release. On this Shared Apache target, the
panel protection tool instead overwrites a server-owned `.htaccess` inside that
web root. Using it would destroy the reviewed production-style `.htaccess` and
would be lost or mutate immutable bytes during a staging symlink swap.

The failure occurred before any probe upload or access-control secret. V3
requires a revised, independently reviewed staging overlay topology before the
capability probe can continue. Implementation remains parked.
