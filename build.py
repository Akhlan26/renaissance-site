#!/usr/bin/env python3
"""Génère les pages publiques de Renaissance à partir des modèles de src/.

Usage :
  python3 build.py --nom "Prénom Nom" --statut "particulier" \
      --adresse "12 rue X, 42000 Saint-Étienne, France" \
      --email "contact@..." \
      --url "https://akhlan26.github.io/renaissance-site/politique-confidentialite.html" \
      --retention "12 mois" --date "18 novembre 2026"

Le script refuse de produire une page s'il reste un marqueur [À COMPLÉTER].
"""
import argparse
import datetime
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
MARKER = re.compile(r"\[À COMPLÉTER[^\]]*\]")

# Règles : (mots-clés recherchés dans le marqueur, nom du champ)
RULES = [
    ("identité", "identite"),
    ("identity", "identite"),
    ("adresse", "adresse"),
    ("address", "adresse"),
    ("e-mail", "email"),
    ("duration", "retention"),
    ("durée", "retention"),
    ("url", "url"),
    ("date", "date"),
]


def resolve(marker: str, values: dict) -> str:
    low = marker.lower()
    for keyword, field in RULES:
        if keyword in low:
            return values[field]
    raise ValueError(f"Marqueur inconnu, à traiter à la main : {marker}")


def render(text: str, values: dict) -> str:
    def sub(m):
        return resolve(m.group(0), values)

    out = MARKER.sub(sub, text)
    if MARKER.search(out):
        raise RuntimeError("Il reste un marqueur non résolu.")
    # les valeurs remplies ne doivent plus être surlignées en jaune (classe .todo)
    return out.replace('<span class="todo">', "<span>")


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--nom", required=True)
    p.add_argument("--statut", required=True, help="particulier / micro-entreprise / ...")
    p.add_argument("--adresse", required=True)
    p.add_argument("--adresse-en", default=None, help="version anglaise de l'adresse (défaut : identique)")
    p.add_argument("--email", required=True)
    p.add_argument("--url", required=True, help="URL publique de la page FR")
    p.add_argument("--retention", default="12 mois")
    p.add_argument("--date", default=None)
    args = p.parse_args()

    date = args.date or datetime.date.today().strftime("%-d %B %Y")
    url_en = args.url.replace("politique-confidentialite", "privacy-policy")

    values = {
        "identite": f"{args.nom} ({args.statut})",
        "adresse": args.adresse,
        "email": args.email,
        "retention": args.retention,
        "url": args.url,
        "date": date,
    }
    values_en = dict(values, retention=args.retention, url=url_en,
                     adresse=args.adresse_en or args.adresse)

    outputs = {
        "politique-confidentialite.src.html": ("politique-confidentialite.html", values),
        "privacy-policy.src.html": ("privacy-policy.html", values_en),
        "index.src.html": ("index.html", values),
    }

    for src_name, (out_name, vals) in outputs.items():
        src = (SRC / src_name).read_text(encoding="utf-8")
        (ROOT / out_name).write_text(render(src, vals), encoding="utf-8")
        print(f"écrit : {out_name}")

    print(f"\nFR : {args.url}")
    print(f"EN : {url_en}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
