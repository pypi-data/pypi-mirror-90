# SPDX-License-Identifier: GPL-3.0-only
# This file is part of renspell.

import logging
import re
from pathlib import Path
from typing import Final, List, Set, Tuple

RESERVED_TOKENS: Final[List[str]] = [
    "#.*",
    "\$",
    "as",
    "at",
    "behind",
    "call",
    "default",
    "define",
    "else",
    "expression",
    "hide",
    "if",
    "in",
    "jump",
    "label",
    "menu",
    "onlayer",
    "pause",
    "play",
    "return",
    "stop",
    "voice",
    "while",
    "window",
    "with",
    "zorder",
]

BLOCK_STARTERS: Final[List[str]] = [
    "init",
    "image",
    "python",
    "scene",
    "screen",
    "show",
    "style",
    "transform",
]
BLOCK_REGEX: Final[str] = "(" + "|".join([f"{x}[ \:]" for x in BLOCK_STARTERS]) + ")"

RESERVED_REGEX: Final[str] = "(" + "|".join(RESERVED_TOKENS) + ")"


def find_files(search_file: str) -> Tuple[Set[Path], bool]:
    files: Set[Path] = set()
    root = Path(search_file)
    if root.is_dir():
        # Assume this is a ren'py game directory. Note, because we are unable to
        # perform the Ren'Py search as described in
        # https://www.renpy.org/doc/html/language_basics.html#game-directory, we
        # have to assume we've either been given the right game directory or the
        # user wants us to check all subdirs.
        files.update(root.rglob("*.rpy"))
        was_dir = True
    else:
        files.add(root)
        was_dir = False
    return (files, was_dir)


class ParsedLine:
    content: Final[str]
    filename: Final[str]
    line_number: Final[int]

    def __init__(self, filename: str, content: str, line_number: int) -> None:
        self.content = content
        self.filename = filename
        self.line_number = line_number


# Portions of this command are taken from renpy's parser.py, which is Copyright
# 2004-2020 Tom Rothamel <pytom@bishoujo.us> under the Expat license
def parse_file(script: Path) -> List[ParsedLine]:
    filename: str = str(script)
    lines: List[ParsedLine] = []
    lnum: int = 0
    in_block: int = -1

    with script.open() as f:
        for line in f:
            lnum += 1

            # Before other processing, check if we're skipping until whitespace
            # changes to strip blocks
            if in_block > -1:
                line_indent: int = get_line_indent(line)
                if line_indent > in_block:
                    continue
                else:
                    in_block = -1

            # Strip UTF byte-order-mark
            if lnum == 1 and line.startswith("\ufeff"):
                line = line[1:]

            if re.match("^\s*" + RESERVED_REGEX + "(?:\s|$|\:)", line):
                # Some form of non-dialogue; bail
                continue

            if not line or line.isspace() or line.strip() == '""':
                continue

            # Strip block commands
            if re.match("^\s*" + BLOCK_REGEX, line):
                in_block = get_line_indent(line)
                continue

            # We have some dialogue, hopefully
            ended: bool = False
            addl_num: int = 0
            while not ended:
                # If we're more than five lines deep, something has probably
                # gone horribly wrong.
                if addl_num > 5:
                    logging.error(
                        f"Parse error in file {filename}; too many continuation lines"
                    )
                    ended = True

                # Need re.DOTALL here because the failure case preserves
                # line-breaks and we need to match across the entire content of
                # the logical line, even if there are newlines in it.
                text = re.match(
                    r"^[^'\"]*(['\"])((?:(?!\1|\\).|\\.)*)\1", line, re.DOTALL
                )
                if text:
                    dialogue = text[2]
                    ended = True
                else:
                    logging.debug(
                        f"Found a line extension in {filename}, line {lnum}, extension #{addl_num}"
                    )
                    addl_num += 1
                    line += " " + f.readline().strip()

            # Substitute variable interpolations for placeholders
            dialogue = re.sub(r"(\[[^\]]+\])", "PLACEHOLDER", dialogue)

            # Strip out formatting
            dialogue = re.sub(r"(\{[^\}]*\})", "", dialogue)

            # Strip quotes, leading and trailing whitespace
            dialogue = dialogue.replace("\\", "")
            dialogue = dialogue.strip()
            parsed_line = ParsedLine(filename, dialogue, lnum)
            lines.append(parsed_line)

            # Now that the line numbers are written out, update the counter with
            # any extra lines that were added during the loop.
            lnum += addl_num
    return lines


def get_line_indent(line: str) -> int:
    before: int = len(line)
    after: int = len(line.lstrip())
    return before - after
