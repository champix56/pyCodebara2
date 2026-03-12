from itertools import product

def generer_combinaisons(data: dict) -> list[str]:
    """
    Génère toutes les combinaisons possibles de prompts
    avec un préfixe composé des id concaténés.
    """

    prompt_base = data.get("promptBase", "").strip()
    sections = data["barcodeData"]["prompt"]

    # récupérer (id, value)
    listes_valeurs = [
        [(v["id"], v["value"].strip()) for v in section["values"]]
        for section in sections
    ]

    combinaisons = product(*listes_valeurs)

    resultat = []

    for combo in combinaisons:

        # concaténation des id sans séparateur
        prefix = "".join(str(c[0]) for c in combo)

        values = [c[1] for c in combo]

        #prompt = "; ".join([prompt_base, *values]) if prompt_base else "; ".join(values)
        prompt = " ".join([prompt_base, *values]) if prompt_base else " ".join(values)

        resultat.append(f"{prefix}/{prompt}")

    return resultat