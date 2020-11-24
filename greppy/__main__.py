#!/usr/bin/env python3
#
#  __main__.py
"""
greppy: Recursively grep over Python files in the files in the given directory.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import sys

# 3rd party
import click
from consolekit import click_command

# this package
from greppy import greppy

__all__ = ["main"]


@click.argument("pattern", type=click.STRING)
@click.option(
		"-d",
		"--dir",
		type=click.STRING,
		help="The directory to search in.",
		default='.',
		metavar="DIRECTORY",
		)
@click.option("-s", "--summary", is_flag=True, default=False, help="Show a summary of the results.")
@click.option("-i", "--ignore-case", is_flag=True, default=False, help="Ignore case.")
@click_command()
def main(pattern, dir: str = '.', summary: bool = False, ignore_case: bool = False):
	"""
	Recursively grep over Python files in the files in the given directory, and search for PATTERN.
	"""

	# stdlib
	import re

	flags = 0

	if ignore_case:
		flags |= re.IGNORECASE

	greppy(re.compile(pattern, flags), dir, summary)


if __name__ == "__main__":
	sys.exit(main())
