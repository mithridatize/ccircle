from pathlib import Path


def hash_combine(seed, hashed):
    """ 'Adds' a hash to a seed, returning the new hash. """
    seed ^= hashed + 0x9e3779b9 + (seed << 6) + (seed >> 2)
    return seed


def get_cc_image_path(relative_path: str):
    """ Get the pathlib.Path obj for the path relative to the cc directory."""
    cc_dir = Path(__file__).resolve().parent
    return cc_dir.joinpath(relative_path)
