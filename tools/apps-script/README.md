# Contact endpoint (Google Apps Script)

One contact form for the whole site. The request is e-mailed to Tyros (default contact@tyros-group.com), with the visitor as reply-to, so "Reply" answers them directly. No spreadsheet, no file storage, no automatic e-mail to the visitor. The site shows its confirmation only after the e-mail has actually been sent.

## Deploy (about 5 minutes, from the Google account of the mailbox that should receive requests)
1. script.google.com > New project. Replace the default code with the content of `Code.gs`.
2. Optional: Project settings > Script properties > `NOTIFY_TO` = the address that receives requests. Without it, requests go to contact@tyros-group.com.
3. Choose `authorizeOnce` > Run > accept the Mail permission.
4. Deploy > New deployment > Web app > Execute as: Me > Who has access: Anyone > Deploy. Copy the URL ending in `/exec`.
5. Choose `selfTest` > Run: 2 test mails must arrive (subjects "[Site] Test ..."), the third request (honeypot) must send nothing.
6. Put the `/exec` URL in `assets/request.js` (replace `__DEPLOY_ID__`), publish, then send one request from the real site in FR and one in EN.

## Checks done on the server
Honeypot (silent success, nothing sent), minimum fill time 4 s, maximum age 24 h, required fields, e-mail format, length caps, line breaks removed from the subject, 3 requests per e-mail per hour and 120 per hour overall.

## Limits
Free Google account: about 100 mails a day. Google Workspace: about 1,500.

## Alternative
A form service such as Formspree gives the same result without code, but adds a third-party processor and its own limits. Apps Script keeps everything in your own mailbox.
