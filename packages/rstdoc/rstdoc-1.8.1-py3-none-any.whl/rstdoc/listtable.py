#!/usr/bin/env python
# encoding: utf-8

# def gen_head(lns,**kw):
#    b,e = list(rindices('^"""',lns))[:2]
#    return lns[b+1:e]
# def gen_head(lns,**kw)
# def gen_api(lns,**kw):
#    yield from doc_parts(lns,signature='py',prefix='listtable.')
# def gen_api

import re
from rstdoc import __version__

"""

.. _`rstlisttable`:

rstlisttable
============

| rstlisttable: shell command
| listable: rstdoc module

Convert RST grid tables to list-tables.

#. Convert grid tables in a file to list-tables. The result is output to stdout::

    $ listtable.py input.rst

#. Convert several files::

    $ listtable.py input1.rst input2.rst
    $ listtable.py *.rst

#. Use pipe (but ``cat`` might not keep the encoding)::

    $ cat in.rst | listtable.py -  | untable.py - > out.rst

Options
-------
-j, --join       e.g.002. Join method per column: 0="".join; 1=" ".join; 2="\\n".join

"""


'''
API
---


.. code-block:: py

   import rstdoc.listtable as listtable


'''


def combine2(e):
    res = [ee[len(re.split('[^ ]', e[0])[0]):].rstrip() for ee in e]
    while res and not res[-1].strip():
        del res[-1]
    if not res:
        res = ['']
    return res


combine = {
    0: lambda e: [''.join([ee.strip() for ee in e]).strip()],
    1: lambda e: [' '.join([ee.strip() for ee in e]).strip()],
    2: combine2
}


def _header(line):
    return line.startswith('+==')


def _isgridline(line):
    return line.startswith('+--') or _header(line)


def row_to_listtable(
        row ,colwidths ,withheader ,join ,indent ,tableend
    ):
    '''
    This is the default ``process_row`` parameter of |listtable.gridtable|.

    :param row: list of cells for the row
    :param colwidths: The widths of the columns
    :param withheader: produce :header-:param rows: 1
    :param join: 0,1,2 telling how to combine the lines of a cell

    - 0 = without space
    - 1 = with space
    - 2 = keep multi-line

    :param indent: indentation of the table
    :param tableend: True, if end of table


    '''

    nColumns = len(colwidths)

    def splitline(lne):
        st = indent + 1
        sl = []
        for s in colwidths:
            nst = s + st
            sl.append(lne[st:nst])
            st = nst + 1
        return sl

    output = []
    output = [
        combine[int(join[c] if c < len(join) else join[-1])](e)
        for c, e in enumerate(
            zip(*[
                splitline(lne) for lne in row if not _isgridline(lne[indent:])
            ]))
    ]
    clms = [(('       ' if j else ('     - ' if i else '   * - ')) + xx)
            for i, x in enumerate(output) for j, xx in enumerate(x)]
    indentstr = ' ' * indent
    if len(row) == 1:
        colwidth = str(int(100 / nColumns))
        colwidth = (' ' + colwidth) * nColumns
        yield indentstr + ".. list-table::\n"
        yield indentstr + "   :widths:{0}\n".format(colwidth)
        yield indentstr + "   :header-rows: {0}\n".format(withheader)
        clms += ['']
    for clm in clms:
        yield indentstr + clm + '\n'
    yield indentstr + '\n'


def gridtable(
        data ,join='012' ,process_row=row_to_listtable
    ):
    '''
    Convert grid table to list table with same column number throughout.
    See |listtable.row_to_listtable|.

    :param data: from file.readlines() or str.splitlines(True)
    :param join: join column 0 without space, column 1 with space and leave the rest as-is
    :param process_row: creates a list-table entry for the row
    '''

    grid = False
    insert = False
    row = []
    withheader = 0
    lendata = len(data)
    indent = 0
    for iL, line in enumerate(data):
        if _isgridline(line.strip()):
            indent = re.search('\s*', line).span()[1]
            grid = True
            insert = True
            row.append(line)
        elif grid and line.strip().startswith('|'):
            row.append(line)
        else:
            grid = False
        if grid:
            if insert:
                insert = False
                if len(row) == 1:
                    colwidths = [len(x) for x in line.split('+')[1:-1]]
                    withheader = 0
                    for t in range(iL, len(data)):
                        tL = data[t].strip()
                        if tL[0] == '+':
                            withheader = int(len(tL) > 1 and tL[1] == '=')
                            break
                tableend = 1
                try:
                    tableend = int(data[iL + 1].strip()[0] not in '+|')
                except:
                    pass
                yield from process_row(row, colwidths, withheader, join,
                                       indent, tableend)
                row = []
                indent = 0
        else:
            yield line


def main(**args):
    '''
    This corresponds to the |rstlisttable| shell command.

    :param args: Keyword arguments. If empty the arguments are taken from ``sys.argv``.

    ``rstfile`` is the file name

    ``in_place`` defaults to False

    ``join`` defaults to "012"


    '''

    import argparse
    import codecs
    import sys

    if not args:
        parser = argparse.ArgumentParser(
            description='''Convert RST grid tables to list-tables.''')
        parser.add_argument('--version', action='version', version = __version__)
        parser.add_argument(
            'rstfile',
            type=argparse.FileType('r', encoding='utf-8'),
            nargs='+',
            help='RST file(s)')
        parser.add_argument(
            '-j',
            '--join',
            action='store',
            default='012',
            help=
            '''e.g.002. Join method per column: 0="".join; 1=" ".join; 2="\\n".join'''
        )
        parser.add_argument(
            '-i',
            '--in-place',
            action='store_true',
            default=False,
            help='''change the file itself''')
        args = parser.parse_args().__dict__

    if not 'in_place' in args:
        args['in_place'] = False
    if not 'join' in args:
        args['join'] = '012'

    if isinstance(args['rstfile'], str):
        args['rstfile'] = [
            argparse.FileType('r', encoding='utf-8')(args['rstfile'])
        ]

    for infile in args['rstfile']:
        data = infile.readlines()
        infile.close()
        if args['in_place']:
            f = open(infile.name, 'w', encoding='utf-8', newline='\n')
        else:
            # '≥'.encode('cp1252') # UnicodeEncodeError on Windows, therefore...  makes problems with pdb, though
            sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
            sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())
            f = sys.stdout
        try:
            f.writelines(gridtable(data, args['join']))
        finally:
            if args['in_place']:
                f.close()


if __name__ == '__main__':
    main()

# vim: ts=4 sw=4 sts=4 et noai nocin nosi
