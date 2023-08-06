from __future__ import annotations
from pathlib import Path
from typing import List, Union
import regex as re
from inspect import signature


FILE_NAME_PATTERN = r'(?P<file_name>[^=]*?)'
INDENT_PATTERN = r'(?P<indent>[ \t]*?)'
TEMPLATE_REGEX: re = re.compile(
    INDENT_PATTERN + r'(?P<comment># *)?{{(?P<wrap_code>%.*?%)?\s*' + FILE_NAME_PATTERN + r'\s*}}')

KEY_PATTERN = r'(?P<key>.*?)'
TEMPLATE_REPLACE_REGEX: re = re.compile(
    INDENT_PATTERN + r'(?P<comment># *)?{{(?P<wrap_code>%.*?%)?=\s*' + KEY_PATTERN + r'\s*}}')


REGEX_MATCH_GROUPS = {
    'indent': 0,
    'comment': 1,
    'wrap_code': 2,
    'file_name': 3,
    'key': 3
}

LEFT_TRAILING_SPACES: re = re.compile(r'(^\s*)')
TABULATOR = '    '


MAX_LINE_LENGTH = 82


def replace_filename_regex(file_name: str) -> re:
    replacer = TEMPLATE_REGEX.pattern.replace(FILE_NAME_PATTERN, file_name).replace(INDENT_PATTERN, '')
    return re.compile(replacer)


def replace_key_regex(key: str) -> re:
    replacer = TEMPLATE_REPLACE_REGEX.pattern.replace(KEY_PATTERN, key).replace(INDENT_PATTERN, '')
    return re.compile(replacer)


def side_by_side_code(left: str, right: str, titles=['', ''], max_line_length: int = MAX_LINE_LENGTH, use_full_space: bool = False) -> str:
    if len(titles[0]) > 0 or len(titles[1]) > 0:
        left_lines = [titles[0], '', *left_align_code(left).splitlines()]
        right_lines = [titles[1], '', *left_align_code(right).splitlines()]
        has_title = True
    else:
        left_lines = left_align_code(left).splitlines()
        right_lines = left_align_code(right).splitlines()
        has_title = False

    max_left = max(list(map(lambda line: len(line), left_lines)))
    max_right = max(list(map(lambda line: len(line), right_lines)))
    if use_full_space:
        left_over = max_line_length - max_left - max_right - 3
        if left_over > 0:
            left_over2 = left_over // 2
            max_left += left_over2
            max_right += left_over2

    if has_title:
        left_lines[1] = '-' * max_left
        right_lines[1] = '-' * max_right

    if max_left + max_right > max_line_length - 3:
        m = max(max_left, max_right)
        if has_title:
            t1 = f"- {titles[0]} {'-' * (m - len(titles[0]) - 3)}"
            t2 = f"- {titles[1]} {'-' * (m - 3 - len(titles[1]))}"
            return f'{t1}\n{left}\n{t2}\n{right}'
        else:
            return f'{left}\n{"-" * m}\n{right}'

    left_lines = list(map(lambda line: line.ljust(max_left), left_lines))

    side_by_side = []
    for i in range(max(len(left_lines), len(right_lines))):
        left = left_lines[i] if i < len(left_lines) else ' ' * max_left
        right = right_lines[i] if i < len(right_lines) else ''
        side_by_side.append(f'{left} | {right}')
    if has_title:
        side_by_side[1] = '-' * (max_left + max_right + 3)
    return '\n'.join(side_by_side)


def left_align_code(code: str) -> str:
    lines = code.splitlines()
    if len(lines) == 0:
        return code

    # replace tabulators with spaces
    for idx in range(len(lines)):
        lines[idx] = lines[idx].replace('\t', TABULATOR)
        if lines[idx].strip() == '':
            lines[idx] = ''
    idx = 0

    while lines[idx] == '':
        idx = idx + 1
        if idx == len(lines):
            return code
    left_spaces = LEFT_TRAILING_SPACES.match(lines[idx]).span()[1]
    for idx, line in enumerate(lines):
        if line.startswith(' ' * left_spaces):
            lines[idx] = line[left_spaces:]
    return '\n'.join(lines)


def wrap_code(code: str, language: str = '', indent: str = ''):
    language = language.replace('.', '')
    return f'```{language}\n{code}\n{indent}```'


def indent_lines(lines: List[str], indent: str, skip_first_indent: bool = False):
    lines = list(map(lambda line: f'{indent}{line.rstrip()}', lines))
    if skip_first_indent and len(lines) > 0:
        lines[0] = lines[0][len(indent):]
    return '\n'.join(lines)


def get_file_path(file_dir: Path, file_name: str) -> Union[Path, None]:
    file_dir = Path(file_dir)
    if file_dir.joinpath(file_name).exists():
        return file_dir.joinpath(file_name)
    files = list(file_dir.rglob(file_name))
    if len(files) == 0:
        # try parent
        files = list(file_dir.parent.rglob(file_name))
        if len(files) == 0:
            print('no script file found: ', file_dir.joinpath(file_name))
            return None
        print(f'using parent folder location: {file_dir.parent}')

    if len(files) == 1:
        return files[0]
    else:
        print(f'multiple files "{file_name}" found. Using the first {files[0]}')
        return files[0]


def lookup_key(values: dict, raw_key: str):
    if raw_key is None:
        return
    keys = re.split(r'\.', raw_key)
    value = values
    for k in keys:
        if k in value:
            value = value[k]
        else:
            return
    return value


def process_template(template: str, values: dict = {}, lookup_dir: Path = Path(__file__).parent):
    place_holders = TEMPLATE_REGEX.findall(template)
    for match in place_holders:
        file_name = match[REGEX_MATCH_GROUPS['file_name']]
        script_file = get_file_path(lookup_dir, file_name)
        if script_file is None:
            break

        with open(script_file, 'r', encoding="utf8") as f:
            processed_script = process_template(
                f.read(),
                values=values,
                lookup_dir=lookup_dir
            )
            script_lines = processed_script.splitlines()
        indent: str = match[REGEX_MATCH_GROUPS['indent']]
        raw_script = indent_lines(script_lines, indent)
        is_wrapping = len(match[REGEX_MATCH_GROUPS['wrap_code']]) > 2
        if is_wrapping:
            language = match[REGEX_MATCH_GROUPS['wrap_code']][1:-1].strip()
            script = wrap_code(raw_script, language=language, indent=indent)
        else:
            script = raw_script
        to_replace = replace_filename_regex(file_name)
        template = re.sub(to_replace, script, template)

    replacers = TEMPLATE_REPLACE_REGEX.findall(template)
    for match in replacers:
        key = match[REGEX_MATCH_GROUPS['key']]
        indent: str = match[REGEX_MATCH_GROUPS['indent']]
        raw_val = lookup_key(values, key)
        if raw_val is not None:
            if type(raw_val).__name__ == 'function':
                arg_count = len(signature(raw_val).parameters)
                if arg_count > 0:
                    arg = match[REGEX_MATCH_GROUPS['wrap_code']]
                    if len(arg) > 2:
                        arg = arg[1:-1].strip()  # strip off surrounding %
                    val = str(raw_val(arg))
                else:
                    val = str(raw_val())
            else:
                val = str(raw_val)
                is_wrapping = len(match[REGEX_MATCH_GROUPS['wrap_code']]) > 0
                if is_wrapping:
                    language = match[REGEX_MATCH_GROUPS['wrap_code']][1:-1].strip()
                    val = wrap_code(val, language=language)

            val = val.splitlines()
            if len(val) == 1:
                indent = ''

            script = indent_lines(val, indent, skip_first_indent=True)
            to_replace = replace_key_regex(key)
            template = re.sub(to_replace, script, template)
        else:
            print('No value found: ', key)
    return template


def process_file(file: Path, values: dict = {}, lookup_dir: Path = None):
    with open(file, 'r', encoding="utf8") as f:
        content = f.read()
    if lookup_dir is None:
        lookup_dir = file.parent
    return process_template(content, values, lookup_dir)


def process(root: Path, values: dict = {}):
    for file in root.rglob("*.py.*"):
        print(f"Process file: {file}")
        content = process_file(file, values)
        final_file = str(file).replace('.py.', '.')
        with open(final_file, 'w', encoding="utf8") as f:
            f.write(content)


if __name__ == '__main__':
    process(Path(__file__).parent)
