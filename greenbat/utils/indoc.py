import typing as t
import re


def get_first_line_with_content(lines: list[str]) -> t.Optional[int]:
    for index, line in enumerate(lines):
        if line and not line.isspace():
            return index
    else:
        return None


INDENTATION_PATTERN = re.compile(r"^(?P<indentation>[ \t]*)")


def get_indentation(line: str) -> str:
    if match := INDENTATION_PATTERN.match(line):
        return match.group("indentation")
    raise ValueError("INDENTATION_PATTERN failed to match. This is a bug.")


def get_indentation_pattern(indentation: str) -> t.Pattern:
    return re.compile(f"^{indentation}")


def indoc(string: str) -> str:
    """
    Strip indentation from `string`.
    """

    lines = string.split("\n")
    fl_index = get_first_line_with_content(lines)
    indentation = get_indentation(lines[fl_index])
    pattern = get_indentation_pattern(indentation)

    def remove_indentation(line: str) -> str:
        return pattern.sub("", line)

    clean_lines = map(remove_indentation, lines)
    return "\n".join(clean_lines)
