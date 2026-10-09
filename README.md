# Tyros Group, site tyros-group.com

Site statique FR/EN hébergé sur GitHub Pages (branche `gh-pages`, domaine via `CNAME`). Une URL par langue : le français à la racine, l'anglais sous `/en/`. Le sélecteur FR/EN est un lien vers la page jumelle.

## Branches
- `claude/tyros-group-offline-k1jbyl` : développement (source).
- `gh-pages` : publication. Elle ne contient ni `tools/` ni `design-system/` ni ce fichier.

## Générer et vérifier
- `python3 tools/sync.py` : remplit l'en-tête, le pied de page, les hreflang et les feuilles de style de chaque page depuis un gabarit par langue.
- `python3 tools/make_private.py`, `make_legal.py`, `make_request.py` : pages Tyros Private, légales et formulaire. `python3 tools/make_sitemap.py` : sitemap.
- `python3 tools/audit_static.py` : liens, ancres, canonical, hreflang. `node tools/audit_render.js` : rendu mobile et bureau. `node tools/test_forms.js`, `node tools/test_consent.js` : formulaires et consentement (formulaire simulé).

## Formulaire et consentement
Un seul formulaire (`/demande/`, `/en/request/`) envoie un e-mail à contact@tyros-group.com via Google Apps Script (`tools/apps-script/`). Google Tag Manager ne se charge qu'après consentement (bandeau FR/EN, lien « Gérer les cookies »).

## Publication
Uniquement sur demande explicite : copie de la source (sans `tools/`, `design-system/`, `README.md`) sur `gh-pages`, en conservant `CNAME`.
