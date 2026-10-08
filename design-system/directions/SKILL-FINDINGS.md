# Ce que recommandent les trois skills pour le site Tyros actuel

Rédigé avant tout code. Chaque point vient d'une exécution réelle (scripts, recherches, références lues) ou est marqué comme observation personnelle.

## 0. Vérifications préalables

- Skills chargés dans cette session : `brand`, `design-system`, `ui-ux-pro-max` (plus `ui-styling` et `banner-design` présents sur disque, non utilisés ; `ui-styling` n'installe rien, Tyros reste en HTML/CSS statique).
- Branches : `gh-pages` = `0ad1b94`, construction GitHub Pages réussie (exécution n°48). `64a68b7` (images de partage) est l'avant-dernier commit de `gh-pages` : `0ad1b94` a été publié 10 minutes plus tard (« Reach = International ») et contient `64a68b7`. Les deux affirmations étaient vraies à leur heure.
- Branche de développement = `acde6be` (brouillons commités, jamais publiés). `gh-pages` n'a pas été modifié.
- Charte Tyros utilisée par `brand` : dérivée du site. 15 couleurs, toutes présentes dans le CSS réel. Deux écarts corrigés : « Succès » et « Erreur » (n'existent pas sur le site, retirés) et une phrase d'exemple qui ne figurait que sur des pages retirées (remplacée).

## 1. BRAND (skill `brand`)

**ADN visuel Tyros.** Un mot-marque TYR + anneau + S avec un arc doré (l'anneau est le seul dispositif graphique propre à la maison) ; Fraunces 600 en très grand et très serré pour les affirmations, Plex Sans pour la lecture ; un papier chaud, de l'encre, l'or comme structure, le bleu marine réservé à l'action ; un langage de filets et d'étiquettes numérotées (01 à 08) ; une voix institutionnelle, directe, discrète, précise (« Leadership Shapes Markets. »).

**Ce qui doit rester.** Les deux familles de polices, la palette et ses rôles (or = structure, marine = action), le mot-marque, l'anneau, l'absence de gradient et d'ombre, la voix, les étiquettes en capitales espacées, FR/EN, le thème sombre.

**Ce qui est trop sage ou générique aujourd'hui** (application de la liste de cohérence de `brand` au site réel, plus observations personnelles) :
1. Chaque section répète le même gabarit (étiquette, titre, grille de cartes blanches) : monotonie, aucune respiration ni tension.
2. Le hero est le seul grand geste ; les titres de section ont tous la même taille.
3. L'anneau, signature de la marque, est presque invisible (crème sur crème).
4. L'or n'apparaît qu'en petit texte, jamais en grand élément (trait, numéro, anneau).
5. La bande de confiance (icônes fines, « Tier-1 European Bank ») ressemble à un modèle SaaS.
6. Les cartes blanches à coins légèrement arrondis et ombre douce sont le motif le plus « template ».
7. Les chiffres clés sont un bloc isolé sous le hero, pas un argument.

**Opportunités de différenciation.** L'anneau comme dispositif de composition ; les chapitres numérotés comme navigation ; la grille éditoriale à filets ; des déclarations typographiques de très grande taille ; l'or en grandes surfaces graphiques (anneau, trait, numéro) plutôt qu'en texte ; l'alternance papier / encre / marine comme rythme ; un hero asymétrique.

**Écarté de `brand`.** Le validateur d'actifs (`validate-asset`) renvoie « FAIL » sur les images de partage uniquement à cause de sa convention de nommage de bibliothèque marketing (`type_campagne_description_date`). Sans objet pour des fichiers web déjà référencés par URL : les renommer casserait les balises. Taille (42 à 65 Ko) et format : conformes.

## 2. DESIGN SYSTEM (skill `design-system`)

**Recommandations structurelles réellement utiles.**
1. **Jetons à trois couches** (primitif, sémantique, composant). Le site n'a aujourd'hui qu'une couche plate (`--gold`, `--ink`) mêlée à des valeurs en dur. Le fichier `tokens/tyros-tokens.json` pose les rôles (`action`, `accent`, `accent-text`, `rule`, `surface`). **Intérêt direct ici : les trois directions ne diffèrent qu'au niveau « composant »**, la couche sémantique reste commune.
2. **Spécification par états** (défaut, survol, focus, actif, désactivé) pour le bouton, la rangée d'offre, le lien de menu. Le site n'a pas d'état « actif » ni de bouton désactivé défini.
3. **Dette structurelle repérée par `validate-tokens`** : le validateur n'a analysé que `assets/tyros-ds.css` (20 occurrences, ce sont les définitions de jetons). Le vrai CSS du site est **intégré dans chacune des 40 pages (environ 23 Ko dupliqués)** et échappe à toute validation. Recommandation : le centraliser progressivement dans une feuille jetonisée (pas dans ce chantier).
4. **Thème sombre par couche sémantique** : le site le fait déjà (`data-theme`). Le générateur du skill émet `.dark`, qui ne correspond pas : à adapter vers `:root[data-theme="dark"]`.
5. **Échelle d'espacement** : le site utilise des rem ad hoc ; l'échelle 4/8/16/24/32/48/96 plus un jeton fluide de section existent maintenant.

**Jetons et composants qui méritent d'évoluer.** Espacement de section (fluide), épaisseur de filet (1 px / 2 px), rayon (0), numéro de chapitre, étiquette, rangée de sommaire, cellule d'offre, cellule de chiffre, bandeau (papier / encre / marine).

**À ne pas changer.** Valeurs de la palette, polices, mot-marque, anneau de focus (2 px, décalage 3 px, or lisible : conforme à la spécification du skill), mouvement réduit, couleur des filets, mécanisme FR/EN (`data-en`), cibles de 44 px, contrastes AA du design system v1.

**Non applicable.** Intégration Tailwind, générateur de diapositives, Chart.js, jetons d'ombre (la maison n'en veut pas).

## 3. UI/UX PRO MAX (skill `ui-ux-pro-max`)

**Recommandations pertinentes de composition et de hiérarchie** (résultats réels des recherches) :
- *Editorial Grid / Magazine* : grille asymétrique, filets de section, typographie inspirée de l'imprimé, équilibre des blancs, zones de grille nommées. Base de B et de C.
- *Swiss Modernism 2.0* : 12 colonnes, hiérarchie nette, un seul accent, espacement mathématique. Base du hero de B (8/4).
- *Minimalism & Swiss* : « éviter ombres et dégradés », bordures fines. Base de A.
- *Brutalism*, **partiellement** : grille visible, angles à 0 px, grands blocs, typographie forte. Base de C.
- UX « Heading Line Balance » : borner la mesure, tester le retour à la ligne naturel, **ne pas** insérer d'espaces insécables systématiques ni de `<br>` forcés. Appliqué : largeurs en `ch`, aucun `<br>` ajouté.
- UX « Viewport Units » : ne pas utiliser `100vh` en plein écran mobile. Appliqué : hero dimensionné par marges, pas par hauteur d'écran.
- UX « Progress Indicators » : un repère de progression. Appliqué dans C sous forme de rail de chapitres.
- UX « Smooth Scroll » (gravité haute) et « Reduced Motion » (gravité haute) : défilement doux, désactivé si mouvement réduit.
- UX « Excessive Motion » : animer 1 à 2 éléments par vue au maximum. Appliqué : aucune chorégraphie, seulement survols et rail.
- UX « Contrast » ≥ 4,5:1 : règle conservée pour l'or en petit texte ; les grands numéros d'ornement sont décoratifs (pas d'information).

**Rejeté car trop générique ou contraire à vos contraintes.** Les sorties du générateur de design system : accents vert, rose, cyan ; polices Outfit, Libre Bodoni, Inter, Playfair ; patron de page « Hero + Features + CTA » ; « Scroll-Triggered Storytelling » comme structure de page ; Brutalism en ce qu'il impose polices système, rouge/bleu/jaune primaires et transitions instantanées ; SplitText et parallaxe.

**À exploiter réellement.** Editorial Grid, Swiss 12 colonnes, la grille visible du Brutalism, l'indicateur de progression, le défilement doux, la gestion du mouvement réduit, la mesure bornée des titres.
