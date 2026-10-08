/**
 * Tyros Group: contact endpoint (Google Apps Script web app).
 * Receives the site contact form, checks it on the server, and e-mails it to Tyros.
 * Nothing else: no spreadsheet, no file storage, no automatic e-mail to the visitor.
 * The visitor sees a confirmation on the site only after the e-mail has actually been sent.
 *
 * Optional Script Property:
 *   NOTIFY_TO   address that receives the requests (default: contact@tyros-group.com)
 */
var MIN_FILL_MS = 4000;                 // faster than this: not a human
var MAX_FILL_MS = 24 * 3600 * 1000;     // older than a day: stale form
var MAX_PER_EMAIL_PER_HOUR = 3;
var MAX_PER_HOUR = 120;

function doGet() { return json_({ ok: true, service: 'tyros-contact' }); }

function doPost(e) {
  try {
    var p = (e && e.parameter) || {};
    if (clean_(p.website, 200)) return json_({ ok: true });                       // honeypot: silent success, nothing sent
    var t0 = parseInt(p.t0, 10), now = Date.now();
    if (!t0 || now - t0 < MIN_FILL_MS || now - t0 > MAX_FILL_MS) return json_({ ok: false, error: 'timing' });
    var v = {
      name: clean_(p.name, 120), email: clean_(p.email, 200).toLowerCase(), company: clean_(p.company, 160),
      subject: clean_(p.subject, 200), message: clean_(p.message, 5000, true),
      lang: p.lang === 'en' ? 'en' : 'fr', page: clean_(p.page, 160), offer: clean_(p.offer, 40), intent: clean_(p.intent, 12),
      source_url: clean_(p.source_url, 300)
    };
    if (!v.name || !v.email || !v.subject || !v.message) return json_({ ok: false, error: 'required' });
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.email)) return json_({ ok: false, error: 'email' });
    if (!rateOk_(v.email)) return json_({ ok: false, error: 'rate' });
    MailApp.sendEmail({
      to: notifyTo_(),
      replyTo: v.email,                                    // "Reply" answers the visitor directly
      name: 'Tyros Group (site)',
      subject: '[Site] ' + v.subject + ' (' + v.lang.toUpperCase() + ')',
      body: ['Nom : ' + v.name, 'Email : ' + v.email, 'Entreprise : ' + (v.company || '-'), 'Langue : ' + v.lang.toUpperCase(),
        'Page d\'origine : ' + (v.page || '-'), 'Offre : ' + (v.offer || '-') + (v.intent ? ' (' + v.intent + ')' : ''),
        'URL : ' + (v.source_url || '-'), 'Reçu (UTC) : ' + Utilities.formatDate(new Date(), 'UTC', 'yyyy-MM-dd HH:mm'),
        '', 'Objet : ' + v.subject, '', v.message].join('\n')
    });
    return json_({ ok: true });                            // only reached if the e-mail was sent
  } catch (err) {
    console.error(err && err.stack || err);
    return json_({ ok: false, error: 'server' });
  }
}

function notifyTo_() { return PropertiesService.getScriptProperties().getProperty('NOTIFY_TO') || 'contact@tyros-group.com'; }
function clean_(s, max, keepNewlines) {
  s = String(s == null ? '' : s);
  s = s.replace(keepNewlines ? /[\u0000-\u0009\u000B\u000C\u000E-\u001F\u007F]/g : /[\u0000-\u001F\u007F]/g, ' ');
  return s.trim().slice(0, max);
}
function rateOk_(email) {
  var cache = CacheService.getScriptCache(), hour = Math.floor(Date.now() / 3600000);
  var k1 = 'e:' + hour + ':' + Utilities.base64EncodeWebSafe(Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, email)).slice(0, 20);
  var k2 = 'all:' + hour;
  var n1 = parseInt(cache.get(k1) || '0', 10), n2 = parseInt(cache.get(k2) || '0', 10);
  if (n1 >= MAX_PER_EMAIL_PER_HOUR || n2 >= MAX_PER_HOUR) return false;
  cache.put(k1, String(n1 + 1), 3700); cache.put(k2, String(n2 + 1), 3700);
  return true;
}
function json_(o) { return ContentService.createTextOutput(JSON.stringify(o)).setMimeType(ContentService.MimeType.JSON); }

/** Run once from the editor to grant the Mail permission. */
function authorizeOnce() { console.log('OK, mail quota left: ' + MailApp.getRemainingDailyQuota()); }

/** Real test from the editor: runs the contact handler directly and sends 2 real mails (FR then EN). */
function selfTest() {
  var base = { name: 'Test Tyros', email: 'test@example.com', company: '[TEST]', page: '/selftest', t0: String(Date.now() - 10000) };
  var cases = [
    { lang: 'fr', subject: 'Test : échange confidentiel', message: 'Test 1' },
    { lang: 'en', subject: 'Test : Programme request : Manager as Recruiter', message: 'Test 2', offer: 'manager-recruiter', intent: 'programme' },
    { lang: 'fr', subject: 'x', message: 'x', website: 'spam' }
  ];
  var out = cases.map(function (c, i) {
    var pl = {}; Object.keys(base).forEach(function (k) { pl[k] = base[k]; }); Object.keys(c).forEach(function (k) { pl[k] = c[k]; });
    var r = doPost({ parameter: pl }).getContent();
    return (i + 1) + '. ' + r + (i === 2 ? '  (honeypot: ok:true but NO mail)' : '');
  });
  console.log(out.join('\n') + '\nExpected: 2 mails in ' + notifyTo_() + ' ([Site] Test ...).');
}
