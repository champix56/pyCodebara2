import math
import hashlib
#from io import StringIO
from typing import Final
import string
import random
import base64
def str_random(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
def getSha256OfStr(strToHash:str)->str:
    hasher=hashlib.new('sha256')
    #bufferedvalue=StringIO( strToHash)
    hasher.update(strToHash.encode())
    return hasher.hexdigest()
def getSha256FromFile(path:str, bufSize:int=1024)->str:
    hasher=hashlib.new('sha256')
    with open(path, 'rb') as f:
        while True:
            data = f.read(bufSize)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()
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


MASK64: Final[int] = 0xFFFFFFFFFFFFFFFF


def splitmix64(x: int) -> int:
    """PRNG déterministe SplitMix64."""
    x = (x + 0x9E3779B97F4A7C15) & MASK64
    z = x
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9 & MASK64
    z = (z ^ (z >> 27)) * 0x94D049BB133111EB & MASK64
    return z ^ (z >> 31)


def build_seed(seed_user: int, season_seed: int, cb_field_input: int) -> int:
    """Combine les seeds de manière déterministe."""
    x = seed_user
    x ^= season_seed << 21
    x ^= cb_field_input << 42
    return splitmix64(x)



def getBase64OfFile(fileLoc:str, encoding:str='utf-8')->str|None:
    base64_output=''
    with open(fileLoc, 'rb') as binary_file:
        binary_file_data = binary_file.read()
        base64_encoded_data = base64.b64encode(binary_file_data)
        base64_output = base64_encoded_data.decode(encoding)
    return base64_output if len(base64_output)>10 else None