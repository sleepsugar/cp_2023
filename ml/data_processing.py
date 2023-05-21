import numpy as np


def clear_answers(source_string):
    source_string.strip()

    unwanted_prefixes = [
        "в ",
        "В ",
        "на ",
        "На ",
        ", ",
        "; "
    ]


def remove_duplications(source_strings):
    return list(np.unique(source_strings))
