"""JSON input interface."""
import gzip
import json
from pathlib import Path
from typing import Optional, TextIO, Union

from ..music import Music


def load_json(
    path: Union[str, Path, TextIO], compressed: Optional[bool] = None
) -> Music:
    """Load a JSON file into a Music object.

    Parameters
    ----------
    path : str, Path or TextIO
        Path to the file or the file to load.
    compressed : bool, optional
        Whether the file is a compressed JSON file (`.json.gz`). Has no
        effect when `path` is a file object. Defaults to infer from the
        extension (`.gz`).

    Returns
    -------
    :class:`muspy.Music`
        Loaded Music object.

    Notes
    -----
    When a path is given, assume UTF-8 encoding and gzip compression if
    `compressed=True`.

    """
    if isinstance(path, (str, Path)):
        if compressed is None:
            if str(path).lower().endswith(".gz"):
                compressed = True
            else:
                compressed = False
        if compressed:
            with gzip.open(path, "rt", encoding="utf-8") as f:
                return Music.from_dict(json.load(f))
        with open(path, encoding="utf-8") as f:
            return Music.from_dict(json.load(f))

    return Music.from_dict(json.load(path))
