#!/usr/bin/env python3

import os
from itertools import zip_longest

def split_line(line, size):
    if len(line) <= size and '\n' not in line:
        return [line]
    lines = line.split('\n')
    out = []
    for piece in lines:
        out += [piece[i:i+size] for i in range(0, len(piece), size)]
    return out

class Table:
    STYLE_ASCII = '-|/+\+++\+/'
    STYLE_THIN = '\u2500\u2502\u250c\u252c\u2510\u251c\u253c\u2524\u2514\u2534\u2518'
    STYLE_THICK = '\u2501\u2503\u250f\u2533\u2513\u2523\u254b\u252b\u2517\u253b\u251b'
    STYLE_DOUBLE = '\u2550\u2551\u2554\u2566\u2557\u2560\u256c\u2563\u255a\u2569\u255d'

    def __init__(self, *, style=None):
        self._chars = None
        self._width = None
        self._sizes = None
        self._columns = []
        self._rows = []
        self.set_style(style or self.STYLE_ASCII)

    def __str__(self):
        return self._render()

    def _calc_sizes(self):
        full_width = self._width or os.get_terminal_size().columns
        full_width -= (1 + (len(self._columns) - 1) + 1)
        rem_width = full_width
        flexible_cells = []
        sizes = []
        for i, col_size in enumerate(c[1] for c in self._columns):
            sizes.append(None)
            if type(col_size) == float: col_size = int(col_size * full_width)
            if col_size < 0:
                flexible_cells.append((i, col_size))
                continue
            sizes[i] = col_size
            rem_width -= col_size
        tot = sum(s for _, s in flexible_cells)
        for i, s in flexible_cells:
            sizes[i] = int(s/tot * rem_width)
        self._sizes = sizes
        return sizes

    def _get_border(self, kind):
        sizes = self._sizes
        separators = (self._chars['h']*s for s in sizes)
        begin, middle, end = self._chars[kind]
        return f'{begin}{middle.join(separators)}{end}\n'

    def _format_frag(self, line):
        buf = (t.ljust(w) for t, w in zip(line, self._sizes))
        return self._chars['v'].join(('', *buf, ''))

    def _format_row(self, row):
        sizes = self._sizes
        rowsplit = []
        for cell, size in zip(row, sizes):
            rowsplit.append(split_line(cell, size))
        fragments = []
        for frag in zip_longest(*rowsplit, fillvalue=''):
            fragments.append(self._format_frag(frag))
        return '\n'.join(fragments)+'\n'

    def _render(self):
        self._calc_sizes()
        top = self._get_border('top')
        middle = self._get_border('middle')
        bottom = self._get_border('bottom')
        head = self._format_row(c[0] for c in self._columns)
        lines = [self._format_row(row) for row in self._rows]
        return f'{top}{middle.join((head, *lines))}{bottom}'

    def set_width(self, width):
        self._width = width
        self._sizes = None

    def set_style(self, chars):
        h, v = chars[:2]
        t, m, b = chars[2:5], chars[5:8], chars[8:11]
        self._chars = dict(h=h, v=v, top=t, middle=m, bottom=b)

    def add_column(self, text, *, size=-1, align=None):
        self._columns.append((text, size))
        self._rows = []
        self._sizes = None

    def add_row(self, *row):
        self._rows.append(row)
