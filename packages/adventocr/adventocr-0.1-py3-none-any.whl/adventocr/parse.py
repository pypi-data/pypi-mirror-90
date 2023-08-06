"""
Parsing functions to identify characters from visual outputs.

"""
from typing import Generator, Iterable, Any, List

from adventocr.mappings import mappings


def _chunks(lst, n) -> Generator[List, None, None]:
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield list(lst[i:i + n])


def _format_row(row: Iterable[int]) -> str:
    row = ''.join('#' if str(char) == '1' else ' ' for char in row)
    return row


def letter(text: Iterable[Iterable[int]]) -> str:
    """
    Parse a visual letter into a character. 6 Rows should be given as
    a 5 item list with a 1 to indicate a filled cell.

    Parameters
    ----------
    text: List of rows.

    Returns
    -------
    solution: str

    """
    rows = [_format_row(row) for row in text]
    text = '\n'.join(rows)
    solution = mappings[text]
    return solution


def word(characters: Iterable[Any]) -> str:
    """
    Parse a visual word into a character.

    Parameters
    ----------
    characters: Iterable of the image, from left to right, top to
        bottom with 1 indicating a filled cell.

    Returns
    -------
    str

    """
    characters = [item for item in characters if item != '\n']
    rows = _chunks(characters, len(characters)//6)
    blocks = (_chunks(row, 5) for row in rows)
    answer = (letter(char) for char in zip(*blocks))
    return ''.join(answer)
