"""
Common  Text processing utilities shared throughout dada-lake
"""

import re
import json
import string
from copy import copy
from typing import List
from io import StringIO
from html.parser import HTMLParser
from typing import Any, List, Set, Union

from bs4 import BeautifulSoup
from slugify import slugify
import jellyfish
from unidecode import unidecode

# sets for text cleaning.
PUNCTUATION = frozenset(string.punctuation)
DIGITS = frozenset(string.digits)
VOWELS = frozenset(["a", "e", "i", "o", "u"])

# doc strings
TEXT_PARAM = ":param text: the text to transform"
REPLACE_PARAM = ":param replace: the text to use as a replacement"

# from: https://stackoverflow.com/questions/5917082/regular-expression-to-match-numbers-with-or-without-commas-and-decimals-in-text
RE_NUMBERS = re.compile(
    r"(:?^|\s)(?=.)((?:0|(?:[1-9](?:\d*|\d{0,2}(?:,\d{3})*)))?(?:\.\d*[1-9])?)(?!\S)"
)
RE_CAMEL_1 = re.compile(r"(.)([A-Z][a-z]+)")
RE_CAMEL_2 = re.compile(r"([a-z0-9])([A-Z])")
RE_WHITESPACE = re.compile(r"\n|\t|\r|\s+")


def decode(text: Any) -> str:
    f"""
    Enforce unicode for a text value
    {TEXT_PARAM}
    :return str
    """
    if isinstance(text, str):
        return text
    elif isinstance(text, bytes):
        return unidecode(text.decode("utf-8", errors="ignore"))
    else:
        return str(text)


def rm_whitespace(text: str, replace: str = " ") -> str:
    f"""
    Standardize whitespace in a text (Eg ``foo  bar `` -> ``foo bar``)
    {TEXT_PARAM}
    :param replace: The string to replace whitespace with.
    :return str
    """
    return RE_WHITESPACE.sub(replace, decode(text)).strip()


def is_vowel(text: str, vowels: List[str] = VOWELS) -> bool:
    f"""
    Return true if this text is a vowel
    {TEXT_PARAM}
    :param punct: An optional list of punctuation characters check against
    :return bool
    """
    return text in vowels


def rm_vowels(text: str, vowels: List[str] = VOWELS) -> bool:
    """
    Remove vowels for a string
    {TEXT_PARAM}
    :param punct: An optional list of punctuation characters check against
    :return bool
    """
    return "".join(map(lambda x: x if not is_vowel(x, vowels) else replace, text))


def is_punct(text: str, punct: List[str] = PUNCTUATION) -> bool:
    f"""
    Return true if this text is a punctuation character
    {TEXT_PARAM}
    :param punct: An optional list of punctuation characters check against
    :return bool
    """
    return text in punct


def rm_punct(text: str, replace: str = " ", punct: List[str] = PUNCTUATION) -> str:
    f"""
    Remove punctuation from a text
    {TEXT_PARAM}
    {REPLACE_PARAM}
    :param punct: A list of punctuation characters to replace
    :return str
    """
    return "".join(map(lambda x: x if not is_punct(x, punct) else replace, text))


def is_digit(text: str, digits: Union[List[str], Set[str]] = DIGITS) -> bool:
    f"""
    Return true if this text is a digits character
    {TEXT_PARAM}
    :param digits: An optional list of digits characters check against
    :return bool
    """
    return text in digits


def is_int(text: str, digits: Union[List[str], Set[str]] = DIGITS) -> bool:
    f"""
    Return true if this text is an integer (all characters are numeric)
    {TEXT_PARAM}
    :param digits: An optional list of digits characters check against
    :return bool
    """
    return all([is_digit(c, digits) for c in text])


def is_not_int(text: str, digits: Union[List[str], Set[str]] = DIGITS) -> bool:
    f"""
    Return true if this text is definitely not integer (no characters are numeric)
    This is a faster check then `is_int` because it breaks once it finds a non-digit character
    We use this internally to distinguish between ids/slugs in api requests
    {TEXT_PARAM}
    :param digits: An optional list of digits characters check against
    :return bool
    """
    for c in text:
        if not is_digit(c, digits):
            return True
    return False


BOOL_TRUE_VALUES = frozenset(["true", "t", "yes", "1", "ok", "y"])
BOOL_FALSE_VALUES = frozenset(["false", "f", "no", "0", "n"])


def to_bool(text: str) -> Union[bool, None]:
    f"""
    Force a text charcter into a boolean object, or return none
    {TEXT_PARAM}
    :return bool
    """
    if text is not None:
        if str(text).lower().strip() in BOOL_TRUE_VALUES:
            return True
        elif str(text).lower().strip() in BOOL_FALSE_VALUES:
            return False
    return None


NA_VALUES = frozenset(
    ["", "none", "na", "nan", "<na>", "-", "nat", "-inf", "inf", "null"]
)


def is_null(text: Union[str, None]) -> bool:
    f"""
    Test whether a string represents a null value
    {TEXT_PARAM}
    :param digits: An optional list of digits characters check against
    :return bool
    """
    if text is None:
        return True
    if text.lower() in NA_VALUES:
        return True
    return False


def to_list(text: Union[str, list]) -> list:
    f"""
    Force a text character into a list or an empty list
    {TEXT_PARAM}
    :return bool
    """
    if isinstance(text, list):
        return text
    if text is not None and text != "":
        if text.startswith("["):
            return json.loads(text)
        if text.startswith("("):
            text = text[1:-1]
        if "," in text:
            return [s.strip() for s in text.split(",") if s.strip()]
        if "+" in text:
            return [s.strip() for s in text.split("+") if s.strip()]
        return [text.strip()]
    return []


def rm_digits(text: str, replace: str = " ", digits: List[Any] = DIGITS) -> str:
    f"""
    Remove digits from a text
    {TEXT_PARAM}
    {REPLACE_PARAM}
    :param digits: A list of punctuation characters to replace
    return str
    """
    return "".join(map(lambda x: x if is_digit(x, digits) else replace, text))


def to_tokens(text: str) -> List[str]:
    f"""
    Naive whitespace based-word splitter
    {TEXT_PARAM}
    :return list
    """
    return [t for t in text.split(" ") if t.strip() != "" and not is_punct(t.strip())]


def get_nwords(text: str) -> int:
    """
    Get the number of words in a text
    """
    return len(text.split(" "))


def to_ngrams(text: str, ngrams: int) -> list:
    """
    Naive n gram splitter
    :parm text: The input text
    """
    input_list = text.split(" ")
    return zip(*[input_list[i:] for i in range(n)])


def camel_to_slug(text: str) -> str:
    f"""
    Convert a camel-cased string into a slug-cased string (eg: ``RemoveFlag` -> ``remove-flag``)
    {TEXT_PARAM}
    """
    text = RE_CAMEL_1.sub(r"\1-\2", decode(text))
    return RE_CAMEL_2.sub(r"\1-\2", text).lower()


def camel_to_snake(text: str) -> str:
    f"""
    Convert a camel-cased string into a snake-cased string (eg: ``RemoveFlag` -> ``remove_flag``)
    {TEXT_PARAM}
    """
    return camel_to_slug(text).replace("-", "_")


def camel_to_title(text: str) -> str:
    f"""
    Convert a camel-cased string into a title-cased string (eg: ``RemoveFlag` -> ``Remove Flag``)
    {TEXT_PARAM}
    """
    return camel_to_slug(text).replace("-", " ").title()


def get_numbers(text: str, punct: List[str] = ["$", "%", "-"]) -> List[str]:
    f"""
    Extract numbers from a text via regular expression.
    {TEXT_PARAM}
    :param remove_punctuation: A list of puncutation characters to remove
    """
    # clean the text
    if text is None or text.strip() == "":
        return []

    text = rm_punctuation(text, punct)

    numbers = []
    for match in RE_NUMBERS.findall(text):
        m = match[1]
        if not m or m == "":
            continue
        numbers.append(m)
    return numbers


def get_slug(text: str) -> str:
    f"""
    Slugify a string
    {TEXT_PARAM}
    """
    text = rm_whitespace(text)
    text = camel_to_slug(text)
    return slugify(text).lower()


def get_snake(text: str) -> str:
    f"""
    Snakify a string
    {TEXT_PARAM}
    """
    s = get_slug(text)
    s = s.replace("-", "_")
    return s


def get_title(text: str) -> str:
    f"""
    get a filepath (or text's) title
    {TEXT_PARAM}
    """
    return " ".join([w.title() for w in get_slug(text).split("-") if w]).title()


def get_abbr(text: str) -> str:
    f"""
    get an abbreviation of a slugged text (eg ``file_type`` -> ``ft``)
    {TEXT_PARAM}
    """
    return "".join([w[0] for w in get_slug(text).split("-") if s.strip()]).lower()


def get_cli_name(text: str) -> str:
    f"""
    Generate a cli flag from a word. (eg ``remove flag`` -> ``--remove-flag``)
    {TEXT_PARAM}
    """
    return f"--{get_slug(text)}"


def get_cli_abbr(text: str) -> str:
    f"""
    Generate a cli abbr from a word. (eg ``remove flag`` -> ``-rf``)
    {TEXT_PARAM}
    """
    return f"-{get_abbr(text)}"


# /////////////
# Fuzzy string matching.
# /////////////


def get_jaro_distance(text: str, term: str) -> float:
    """
    Get the jaro distance between two srings
    {TEXT_PARM}
    :param term: The term to compare against the text
    :return float
    """
    return jellyfish.jaro_distance(text, term)


# /////////////
# HTML
# /////////////


def to_soup(text: str) -> BeautifulSoup:
    """
    Helper for bs4
    """
    return BeautifulSoup(html, "html.parser")


class __HTMLStripper__(HTMLParser):
    """
    An HTML Stripper
    From: https://stackoverflow.com/questions/753052/strip-html-from-strings-in-python
    """

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):
        """"""
        self.text.write(d)

    def get_data(self):
        """"""
        return self.text.getvalue()


def rm_html(text: str):
    """
    String tags and clean text from text.
    """
    s = __HTMLStripper__()
    s.feed(text)
    return decode(s.get_data())


# ////////////////
# Multi-featured Text Processing
# ////////////////

PROCESS_STEPS = {
    "decode": decode,
    "rm_whitespace": rm_whitespace,
    "rm_html": rm_html,
    "rm_digits": rm_digits,
    "rm_punct": rm_punct,
    "to_tokens": to_tokens,
    "to_ngrams": to_ngrams,
    "camel_to_slug": camel_to_slug,
    "camel_to_snake": camel_to_snake,
    "camel_to_title": camel_to_title,
    "get_slug": get_slug,
    "get_snake": get_snake,
    "get_title": get_title,
    "upper": lambda x: x.upper(),
    "lower": lambda x: x.lower(),
    "strip": lambda x: x.strip(),
    "split_lines": lambda x: x.splitlines(),
    "rm_vowels": rm_vowels,
    "get_numbers": get_numbers,
}
PROCESS_STEP_NAMES = list(PROCESS_STEPS.keys())
PROCESS_STEP_NAME_LIST = ", ".join(PROCESS_STEP_NAMES)

# TODO: support handling of lists
def process(text: str, steps=["decode"], **kwargs) -> Any:
    f"""
    Run a series of text processing steps
    {TEXT_PARAM}
    :param steps: A list of steps to run in the order to run them, choose from: {PROCESS_STEP_NAME_LIST}
    """
    for step in steps:
        fx = PROCESS_STEPS.get(step)
        if not fx:
            raise ValueError(
                f"Invalid text processing step: {step}. Choose from: {PROCESS_STEP_NAME_LIST}"
            )
        text = fx(text, **kwargs)
    return text
