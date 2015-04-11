#!/usr/bin/env python
from __future__ import print_function

DESCRIP = 'clear outputs from notebook and resave'
EPILOG = \
"""
Opens notebook(s) and clears code outputs and prompts, saving to new
filename.
"""
import io

from os.path import basename, splitext

from argparse import ArgumentParser, RawDescriptionHelpFormatter

from IPython.nbformat import current

def cellgen(nb, type=None):
    for ws in nb.worksheets:
        for cell in ws.cells:
            if type is None:
                yield cell
            elif cell.cell_type == type:
                yield cell


def strip_after_comments(code_input):
    if code_input.startswith('# - '):
        return code_input
    out_lines = []
    for line in code_input.splitlines():
        if not line.startswith('#'):
            break
        if line.startswith('#: '):
            break
        out_lines.append(line)
    return '\n'.join(out_lines)


def main():
    parser = ArgumentParser(description=DESCRIP,
                            epilog=EPILOG,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('in_fname', type=str,
                        help='input notebook filename')
    parser.add_argument('out_fname', type=str,
                        help='output notebook filename')
    args = parser.parse_args()
    out_name = splitext(basename(args.out_fname))[0]
    with io.open(args.in_fname, 'r') as f:
        nb = current.read(f, 'json')
    nb.name = out_name
    for cell in cellgen(nb, 'code'):
        if hasattr(cell, 'prompt_number'):
            del cell['prompt_number']
        cell.outputs = []
        if hasattr(cell, 'input'):
            cell['input'] = strip_after_comments(cell['input'])
    with io.open(args.out_fname, 'w') as f:
        current.write(nb, f, 'ipynb')


if __name__ == '__main__':
    main()
