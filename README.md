# renaissance-site

Pages publiques de l'application Android **Renaissance** (fr.renaissance.app) :
politique de confidentialité FR/EN, page d'accueil légale, contact.

Code source de l'application : dépôt privé séparé.

## Générer / mettre à jour

Les pages sont générées depuis les modèles de `src/` :

    python3 build.py --nom "..." --statut "..." --adresse "..." \
        --email "..." --url "https://<owner>.github.io/renaissance-site/politique-confidentialite.html"

Puis `git add -A && git commit -m "..." && git push`.

Ne pas éditer les `.html` à la main : ils sont écrasés à chaque build.
