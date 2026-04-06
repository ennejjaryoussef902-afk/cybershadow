import hashlib

def genera_hash(testo, algoritmo="sha256"):
    """Genera l'hash di una stringa usando l'algoritmo scelto."""
    hash_obj = hashlib.new(algoritmo)
    hash_obj.update(testo.encode('utf-8'))
    return hash_obj.hexdigest()

def verifica_hash(testo_chiaro, hash_da_controllare, algoritmo="sha256"):
    """Controlla se il testo corrisponde all'hash."""
    return genera_hash(testo_chiaro, algoritmo) == hash_da_controllare