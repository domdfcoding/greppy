#!/usr/bin/env python3
#
#  __init__.py
"""
greppy: Recursively grep over Python files in the files in the given directory.
"""
#
#  Copyright © 2020-2021 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import re
from functools import partial
from typing import IO, Pattern, Set, Union

# 3rd party
import click
from domdf_python_tools.paths import PathPlus, unwanted_dirs
from domdf_python_tools.typing import PathLike
from domdf_python_tools.words import Plural
from rich.console import Console
from rich.syntax import Syntax

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.0.0"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["greppy"]

_match = Plural("match", "matches")


def greppy(
		pattern: Union[Pattern, str],
		search_dir: PathLike = '.',
		*,
		summary: bool = False,
		file: IO = None,
		) -> Set[PathPlus]:
	"""
	Recursively grep over Python files in the files in the given directory, and search for ``pattern``.

	:param pattern: The pattern to search for.
	:param search_dir: The directory to search in.
	:param summary: Show only a summary of the results.
	:param file: The output file descriptor. Defaults to ``sys.stdout``.
	:no-default file:
	"""

	if not isinstance(pattern, Pattern):
		pattern = re.compile(pattern)

	console = Console(file=file)
	echo = partial(click.echo, file=file)

	matching_files: Set[PathPlus] = set()
	match_count = 0
	searched_files = 0

	for filename in PathPlus(search_dir).iterchildren(exclude_dirs=(*unwanted_dirs, ".hg"), match="**/*.py"):

		if filename.suffix != ".py":  # pragma: no cover
			continue
		if "build" in filename.parts:
			continue

		searched_files += 1

		try:
			lines = filename.read_lines()
		except (UnicodeDecodeError, PermissionError, IsADirectoryError) as e:
			click.echo(f"Error reading {filename.as_posix()}: {e}", err=True)
			continue

		for lineno, content in enumerate(lines):
			lineno += 1
			for match in pattern.finditer(content):
				matching_files.add(filename)

				if summary:
					echo(f"{filename.as_posix()}:{lineno}:{match.span()[0]} Matches")
				else:
					echo(f"{filename.as_posix()}:{lineno}:{match.span()[0]}")

					context = lines[max(0, lineno - 3):lineno + 2]
					start_line = max(lineno - 2, 1)

					while not context[0]:
						context.pop(0)
						start_line += 1

					syntax = Syntax(
							'\n'.join(context),
							lexer_name="python",
							line_numbers=True,
							start_line=start_line,
							highlight_lines={lineno},
							)
					console.print(syntax)
					echo('-' * console.width)

				match_count += 1
				break

	if match_count:
		echo(
				f"{match_count} {_match(match_count)} in {len(matching_files)} "
				f"files (searched {searched_files} files)."
				)
	else:
		echo(f"No matches across {searched_files} files.")

	return matching_files
