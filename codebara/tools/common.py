import math
def seededRandom(
    seed1: int, seed2: int, min: int = 1, max: int = 100000, renderProb=0.5
):
    c = 2147483647  # Un grand nombre premier

    seed = (1664525 * (seed1 ^ seed2) + 1013904223) % c
    seed = (
        seed * 48271
    ) % c  # Applique un multiplicateur supplémentaire pour plus d'aléatoire

    # Génère un nombre pseudo-aléatoire entre 0 et 1 basé sur la graine
    probabilityFactor = (seed % 10000) / 10000

    # Génération d'un ajustement probabiliste reproductible
    biasSeed = (seed * 16807) % c  # Applique un autre calcul basé sur le seed
    biasFactor = (
        (biasSeed % 10000) / 10000 < probabilityFactor
        if renderProb > 0.5
        else (1 - probabilityFactor)
    )

    return math.floor(
        min + biasFactor * (max - min)
    )  # Assure que la valeur est entre min et max
