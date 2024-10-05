_id_counter = 0


def get_unique_id():
    """
    Generates a unique ID. Using this method reduces the token size for LLMs.
    """
    global _id_counter
    _id_counter += 1
    return _id_counter
