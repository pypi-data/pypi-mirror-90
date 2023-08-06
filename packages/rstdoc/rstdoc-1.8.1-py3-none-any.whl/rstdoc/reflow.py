#!/usr/bin/env python
# encoding: utf-8

# def gen_head(lns,**kw):
#    b,e = list(rindices('^"""',lns))[:2]
#    return lns[b+1:e]
# def gen_head(lns,**kw)
# def gen_api(lns,**kw):
#    yield from doc_parts(lns,signature='py',prefix='reflow.')
# def gen_api

from .retable import retable, titlerex, re_title
from .listtable import gridtable, row_to_listtable
from textwrap import wrap
import re
from rstdoc import __version__

"""
.. _`rstreflow`:

rstreflow
=========

| rstreflow: shell command
| reflow: rstdoc module

Reflow tables and paragraphs in a rst document produced from a docx.

Post-process a docx in this order::

    rstfromdocx doc.docx
    rstlisttable doc/doc.rst > doc/tmp.rst
    rstuntable doc/tmp.rst > doc/tmp1.rst
    rstreflow doc/tmp1.rst > doc/tmp2.rst
    rstreimg doc/tmp2.rst > doc/tmp3.rst
    rm doc/doc.rst
    mv doc/tmp3.rst doc/doc.rst
    rm doc/tmp*

Check the intermediate results.

Else one can also do inplace::

    rstfromdocx doc.docx
    rstlisttable -i doc/doc.rst
    rstuntable -i doc/doc.rst
    rstreflow -i doc/doc.rst
    rstreimg -i doc/doc.rst

.. note:: DOCX to RST using Pandoc

   ``rstfromdocx -lurg doc.rst`` converts a docx to RST and
   does all the post-processing in one step.

   It is adviced, though, to compare the output with the original and do some manual
   corrections here and there.

"""


'''
API
---

.. code-block:: py

   import rstdoc.reflow as reflow

'''

_pgrphrex = [
    re.compile(r'\s+'),
    re.compile(r'\s*-(\s|$)'),
    re.compile(r'\s*\*(\s|$)'),
    re.compile(r'\s*\* -(\s|$)'),
    re.compile(r'\s*\w\.(\s|$)'),
    re.compile(r'\s*#\.(\s|$)'),
    re.compile(r'\s*:?\w\+:(\s|$)'),
]


def reflowparagraph(p, sentence=False):
    '''
    Reflow a paragaph using ``textwarp.wrap``. Possibly split sentences.

    :param p: paragraph
    :param sentence: if True lines are split at the end of the sentence

    '''

    if p:
        if len(p) == 3 and titlerex.match(p[0]) and titlerex.match(
                p[2]) or len(p) == 2 and titlerex.match(p[1]):
            re_title(p, 0, 0)
            yield from p
        elif p[0][0] == '=':  # simple table
            yield from p
        elif len(p[0]) > 3 and p[0][0:3] == '.. ':  # directive, comment
            yield from p
        else:
            #p = ['This e.g. is a sentence. And here a new one.','A new one.']
            st = 0
            mo = ''
            for rp in _pgrphrex:
                m = rp.match(p[0])
                if m:
                    if m.span()[1] > st:
                        st = m.span()[1]
                        mo = m.group(0)
            if p[0] and st < len(p[0]) and p[0][st] in '|+':
                yield from p
            else:
                if sentence:
                    txt = ' '.join([p[0][st:]] + [pp.strip() for pp in p[1:]])
                    wraptxt = []
                    ss = re.split('(?<!e\.g)\.\s+', txt)
                    for ph in ss:
                        wraptxt.extend(wrap(ph, width=150))
                        if wraptxt:
                            wraptxt[-1] += '.'
                    else:
                        try:
                            wraptxt[-1] = wraptxt[-1][:-1]
                        except:
                            pass
                else:
                    txt = '\n'.join([p[0][st:]] + [pp.strip() for pp in p[1:]])
                    wraptxt = wrap(txt)
                lmo = 0
                if not wraptxt:
                    yield mo
                else:
                    for tl in wraptxt:
                        if not lmo:
                            yield mo + tl
                            lmo = len(mo)
                        else:
                            yield ' ' * lmo + tl
        del p[:]


def reflowparagraphs(lns, sentence=False):
    '''
    Reflow paragraphs using |reflow.reflowparagraph|.

    :param lns: lines from rst file
    :param sentence: if True lines are split at the end of the sentence

    '''

    # yield from lns
    p = []
    literal = False

    def reflowp(p):
        return reflowparagraph(p, sentence)

    re_literal = re.compile('^(?!\.\. ).*::\s*$')
    for dd in lns:
        if dd.strip() == '':
            dds = ['']
        else:
            dds = dd.splitlines()
        for d in dds:
            if literal and d and d[0] != ' ':
                p.append(d)
                literal = False
            elif literal:
                yield d
            elif re_literal.search(d):
                p.append(d)
                yield from reflowp(p)
                literal = True
            else:
                dstrip = d.strip()
                if not dstrip:
                    yield from reflowp(p)
                    yield d
                elif any([rp.match(dstrip) for rp in _pgrphrex]):
                    yield from reflowp(p)
                    p.append(d)
                else:
                    p.append(d)
    yield from reflowp(p)


def nostrikeout(lns):
    '''
    Removes ``[strikeout:xxx]``

    :param lns: lines from rst file

    '''

    nso = re.compile(r'\[STRIKEOUT:[^\]]*\]', re.M | re.I)
    # lns='''hello [STRIKEOUT:Firmware may deactivate the high-voltage circuits in
    #   ***STOP*** state.] there [STRIKEOUT:guy]'''.splitlines(True)
    all = ''.join([x + '\n' if not x.endswith('\n') else x for x in lns])
    res = nso.sub('', all)
    yield from res.splitlines()


def rmextrablankline(lns):
    '''
    Remove excessive blank lines.

    :param lns: lines from rst file

    '''

    bc = 0
    for d in lns:
        if not d.strip():
            bc = bc + 1
        else:
            bc = 0
        if bc < 3:
            yield d


def no3star(lns):
    '''
    Removes three stars, as they are not supported by docutils.

    :param lns: lines from rst file

    '''

    for d in lns:
        # d='****'
        res = re.sub('\*\*\*\*+', '', d)
        # res='***Hello***'
        res = res.replace('***', '**')
        #res='**space before **'
        res = re.sub('(\w)\s+\*\*\s*$', r'\1**', res)
        # res='**'
        res = re.sub('^\s*\*\*\s*(\*\*)*$', r'', res)
        res = res.replace('.. _``:', '')
        res = re.sub('^:$', r'', res)
        yield res


def noblankend(lns):
    '''
    Removes blanks at the end of the line.

    :param lns: lines from rst file

    '''

    nbe = re.compile('\s+$')
    for d in lns:
        yield nbe.sub('', d)


class reflowrow():
    '''
    This replaces |listtable.row_to_listtable| in |listtable.gridtable| to reflow a grid table.

    '''

    def __init__(self):
        self.tbl = []

    def __call__(self, row, colwidths, withheader, join, indent, tableend):
        for lne in row_to_listtable(row, colwidths, withheader, join, indent,
                                    tableend):
            if not tableend or lne.strip():
                self.tbl.append(lne)
        if tableend:
            yield from retable(self.tbl)
            del self.tbl[:]


def reflow(lns, join='1', sentence=False):
    '''
    Combines all rst corrections of this file.

    :param lns: lines from rst file
    :param join: 0 no space, 1 with space, 2 keep as-is
    :param sentence: if True lines are split at the end of the sentence

    '''

    r = reflowrow()
    for ln in noblankend(
            rmextrablankline(
                no3star(
                    reflowparagraphs(
                        nostrikeout(gridtable(lns, join, r)), sentence)))):
        yield ln + '\n'


def main(**args):
    '''
    This corresponds to the |rstreflow| shell command.

    :param args: Keyword arguments. If empty the arguments are taken from ``sys.argv``.

    ``rstfile`` is the file name

    ``in_place`` defaults to False

    '''

    import codecs
    import sys
    import argparse

    if not args:
        parser = argparse.ArgumentParser(
            description=
            '''Reflow paragraphs and tables, for the latter using join as for listtable'''
        )
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
            '-s',
            '--sentence',
            action='store_true',
            default=False,
            help='''Break lines at the end of sentences.''')
        parser.add_argument(
            '-i',
            '--in-place',
            action='store_true',
            default=False,
            help='''change the file itself''')
        args = parser.parse_args().__dict__

    if not 'in_place' in args:
        args['in_place'] = False
    if not 'sentence' in args:
        args['sentence'] = False
    if 'join' not in args:
        args['join'] = '012'

    if isinstance(args['rstfile'], str):
        args['rstfile'] = [
            argparse.FileType('r', encoding='utf-8')(args['rstfile'])
        ]

    for infile in args['rstfile']:
        lns = infile.readlines()
        infile.close()
        if args['in_place']:
            f = open(infile.name, 'w', encoding='utf-8', newline='\n')
        else:
            # '≥'.encode('cp1252') # UnicodeEncodeError on Windows, therefore...  makes problems with pdb, though
            sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
            sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())
            f = sys.stdout
        try:
            f.writelines(reflow(lns, args['join'], sentence=args['sentence']))
        finally:
            if args['in_place']:
                f.close()


if __name__ == '__main__':
    main()

# vim: ts=4 sw=4 sts=4 et noai nocin nosi
