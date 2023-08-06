"""
Functions for parsing, formatting, and generating emojis.
TODO:
    - [ ] Implement text-based emoji things
    - [ ] Move to text module?
"""
# ///////////////////
# Imports
# ///////////////////

import random
import logging

from emoji import emojize
from emoji_data_python import emoji_data

# ///////////////////
# Logger
# ///////////////////

EMOJI_LOGGER = logging.getLogger()

# ///////////////////
# Constants
# ///////////////////

EMOJI_BASE = {e.short_name: e for e in emoji_data if e and hasattr(e, "short_name")}
# EMOJI_SKIN_VARIATIONS = {ee.short_name: ee for name, e in EMOJI_BASE.items() for key, ee in e.__dict__.get('skin_variations', {}).items() if ee}
EMOJI = dict(EMOJI_BASE.items())
VALID_EMOJIS = list(EMOJI.keys())

# ///////////////////
# Custom Types
# ///////////////////

# ///////////////////
# Doc strings
# ///////////////////
EMOJI_PARAM = ":param emoji: An emoji name as a string"
STRING_PARAM = ":param string: A string to emojize"

# ///////////////////
# Functions
# ///////////////////


def emoji_is_valid(emoji: str) -> bool:
    f"""
    Check if an emoji name is valid.
    {EMOJI_PARAM}
    """
    return emoji in VALID_EMOJIS


def emoji_from_string(string) -> str:
    f"""
    Given a string with emoji names in it, "emojize" the string.
    {STRING_PARAM}
    """
    return emojize(string)


def emoji_gen_random() -> str:
    """
    Choose a random emoji.
    """
    return random.choice(VALID_EMOJIS)
