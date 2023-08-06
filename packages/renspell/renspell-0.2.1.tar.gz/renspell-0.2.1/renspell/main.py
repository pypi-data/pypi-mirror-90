# SPDX-License-Identifier: GPL-3.0-only
# This file is part of renspell.

import csv
import logging
import string
import sys
from pathlib import Path
from typing import Any, Final, List, Optional, TextIO, Tuple

import click
import colorama  # type: ignore
import language_tool_python  # type: ignore

import renspell.parse as parse
from renspell.parse import ParsedLine

VERSION: Final[str] = "0.2.1"

log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

csv_initialized: bool = False


@click.command()
@click.version_option(version=VERSION)
@click.option(
    "--color/--no-color",
    default=True,
    help="Whether to use color in the output.  Has no effect when format is not text.",
)
@click.option(
    "--dictionary",
    "-d",
    multiple=True,
    type=click.File("r"),
    help="Dictionary of custom words to accept.",
)
@click.option(
    "--output-format",
    "-f",
    default="text",
    help="Output format for suggestions.",
    type=click.Choice(["csv", "text"], case_sensitive=False),
)
@click.option("--output-file", "-o", type=click.File("w"), default="-")
@click.option(
    "--language", "-l", default="en-US", help="Language to use for checking (BCP 47)."
)
@click.option(
    "--mother-tongue",
    "-m",
    type=str,
    help="The native language of the author. This activates checks for false-friends (bilingual homophones).",
)
@click.option(
    "--spelling-only", "-s", is_flag=True, help="Check for spelling errors only."
)
@click.option("--style/--no-style", default=False, help="Activate style checks.")
@click.argument("scripts", type=click.Path(exists=True, readable=True))
def main(
    scripts: str,
    dictionary: Tuple[TextIO],
    language: str,
    mother_tongue: str,
    spelling_only: bool,
    style: bool,
    color: bool,
    output_format: str,
    output_file: TextIO,
) -> None:
    """renspell, a spell checker for Ren'Py scripts

    SCRIPTS should be the file or directory that you want spellchecked. If you
    specify a directory, renspell assumes that it is a Ren'Py game directory and
    will check all .rpy scripts recursively.

    """
    # Don't need to check for existance or readability, as click validates that
    # already for us.
    (files, was_dir) = parse.find_files(scripts)

    # Disable the EN_QUOTES check as it doesn't make sense in Ren'Py scripts
    tool = language_tool_python.LanguageTool(language)
    tool.disabled_rules.add("EN_QUOTES")

    # Arg handling
    if mother_tongue:
        tool.mother_tongue = mother_tongue
    if spelling_only:
        tool.enabled_rules_only = True
        tool.enabled_categories |= set(["COMPOUNDING", "TYPOS"])
        # Can't mix disabled rules and enabled_rules_only.
        tool.disabled_rules.remove("EN_QUOTES")
    if not style and not spelling_only:
        tool.disabled_categories.add("STYLE")

    # For Windows, we must initialize the terminal for colorization
    if output_format == "text" and color:
        colorama.init()

    ignore_words: List[str] = []
    for d in dictionary:
        words: List[str] = d.read().split()
        ignore_words += words
    # Unfortunately, there's no good way to add exceptions to LanguageTool
    # through the API. Instead, hack it in even though it's going to be
    # ugly.
    root_language: str = language.split("-", maxsplit=1)[0]
    lt_cache_dir: str = language_tool_python.utils.get_language_tool_directory()
    dirtype = "hunspell" if not root_language == "nl" else "spelling"
    ignore_file: Path = Path(
        f"{lt_cache_dir}/org/languagetool/resource/{root_language}/{dirtype}/ignore.txt"
    )
    ignores: str = ignore_file.read_text()
    orig_ignores: str = ignores.split("###renspell ignores###")[0]
    ignore_file.write_text(
        orig_ignores + "\n###renspell ignores###\n" + "\n".join(ignore_words)
    )

    # Prepare csvwriter
    cwriter: Any = None
    if output_format == "csv":
        cwriter = csv.writer(output_file, quoting=csv.QUOTE_MINIMAL)

    for f in files:
        parsed_lines = parse.parse_file(f)
        log.info(f"Processing file {str(f)}")

        # Iterate over each logical line
        for parsed_line in parsed_lines:
            matches = tool.check(parsed_line.content)
            present_matches(
                color,
                cwriter,
                matches,
                output_file,
                output_format,
                parsed_line,
                was_dir,
            )


def present_matches(
    color: bool,
    cwriter: Any,
    matches: List[ParsedLine],
    output_file: TextIO,
    output_format: str,
    parsed_line: ParsedLine,
    was_dir: bool,
) -> None:
    if not matches:
        pass
    for i in matches:
        if output_format == "text":
            filename = parsed_line.filename if was_dir else None
            print(
                present_spelling_error_txt(i, filename, parsed_line.line_number, color),
                file=output_file,
            )
        elif output_format == "csv":
            # Because csvwriter wants a file object, pass it through
            # instead of handling I/O here
            present_spelling_error_csv(
                i, parsed_line.filename, parsed_line.line_number, cwriter
            )


def present_spelling_error_txt(
    match: language_tool_python.match.Match,
    filename: Optional[str],
    lnum: int,
    color: bool,
) -> str:
    offset: int = match.offsetInContext
    length: int = match.errorLength
    context: str = match.context
    message: str = match.message[0].lower() + match.message[1:].rstrip(
        string.punctuation
    )

    if filename:
        intro = f"In file {filename} on line {lnum},"
    else:
        intro = f"On line {lnum},"

    if color:
        context = (
            context[:offset]
            + click.style(context[offset : offset + length], fg="red", underline=True)
            + context[offset + length :]
        )

    if not match.replacements:
        correction = ""
    elif len(match.replacements) == 1:
        correction = f" Did you mean “{match.replacements[0]}”?"
    else:
        correction = f" Did you mean one of {match.replacements[:4]}?"

    return f"{intro} {message}: “{context}”{correction}"


def present_spelling_error_csv(
    match: language_tool_python.match.Match, fname: str, lnum: int, cwriter: Any
) -> None:
    global csv_initialized
    if not csv_initialized:
        cwriter.writerow(["File", "Line Number", "Message", "Error Phrase", "Rule ID"])
        csv_initialized = True
    cwriter.writerow([fname, lnum, match.message, match.matchedText, match.ruleId])


if __name__ == "__main__":
    main()
