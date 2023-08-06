"""Git diff parsing."""
import re
import typing

import more_itertools

RE_HUNK_HEADER = re.compile(
    r"^@@ -(?P<minus_offset>\d+)(?:,(\d+))? \+(?P<plus_offset>\d+)(?:,(\d+))?\ @@[ ]?(.*)"  # noqa:E501,SC100
)


def changed_lines_in_multiple_hunks(
    lines: typing.Sequence[str],
) -> typing.Iterator[int]:
    """Yields the changed lines given an iterable of multiple unidiff hunks."""
    hunk_line_numbers = [
        line_number
        for line_number, line in enumerate(lines)
        if RE_HUNK_HEADER.match(line)
    ]
    for hunk_start, hunk_end in more_itertools.pairwise(hunk_line_numbers):
        yield from _changed_lines_in_hunk(lines, hunk_start, hunk_end)
    if hunk_line_numbers:
        yield from _changed_lines_in_hunk(lines, hunk_line_numbers[-1], None)


def _changed_lines_in_hunk(
    lines: typing.Sequence[str], start: int, end: typing.Optional[int]
) -> typing.Iterator[int]:
    hunk_line = lines[start]
    match = RE_HUNK_HEADER.match(hunk_line)
    if not match:
        raise ValueError("bad match in hunk.")
    hunk_offset = int(match["plus_offset"]) - 1
    yield from (
        line_number + hunk_offset
        for line_number in _changed_lines_relative_to_hunk(lines[start:end])
    )


def _changed_lines_relative_to_hunk(hunk: typing.Iterable[str]) -> typing.Iterator[int]:
    """Yields the line numbers of changed lines relative to the given hunk."""
    for line_number, line in enumerate(
        line for line in hunk if not line.startswith("-")
    ):
        if line.startswith("+"):
            yield line_number
