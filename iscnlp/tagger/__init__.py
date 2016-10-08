# -*- coding: utf-8 -*-

"""POS-Tagger for Indian Languages.

This module provides a POS-tagger for major Indian languages
including Urdu, Kashmiri and English.

Copyright (c) 2015-2016 Riyaz Ahmad Bhat, Irshad Ahmad Bhat
<riyaz.bhat@research.iiit.ac.in>
<irshad.bhat@research.iiit.ac.in>
"""

import io
import sys
import codecs
import argparse

from .tagger import Tagger

__all__ = ['Tagger']
__version__ = '1.0'


def parse_args(args):
    prog = 'isc-tagger'
    description = 'POS-Tagger for Indian Languages'
    languages = 'hin urd'.split()
    lang_help = 'select language (3 letter ISO-639 code) {%s}' % (
                ', '.join(languages))
    # parse command line arguments
    parser = argparse.ArgumentParser(prog=prog,
                                     description=description)
    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version='%s %s' % (prog, __version__))
    parser.add_argument('-i',
                        '--input',
                        metavar='',
                        dest='infile',
                        type=str,
                        help='<input-file>')
    parser.add_argument('-o',
                        '--output',
                        metavar='',
                        dest='outfile',
                        type=str,
                        help='<output-file>')
    parser.add_argument('-l',
                        '--language',
                        metavar='',
                        dest='lang',
                        choices=languages,
                        default='hin',
                        help=lang_help)
    args = parser.parse_args(args)
    return args


def get_file_pointers(args):
    if args.infile:
        ifp = io.open(args.infile, encoding='utf-8')
    else:
        if sys.version_info[0] >= 3:
            ifp = codecs.getreader('utf8')(sys.stdin.buffer)
        else:
            ifp = codecs.getreader('utf8')(sys.stdin)

    if args.outfile:
        ofp = io.open(args.outfile, mode='w', encoding='utf-8')
    else:
        if sys.version_info[0] >= 3:
            ofp = codecs.getwriter('utf8')(sys.stdout.buffer)
        else:
            ofp = codecs.getwriter('utf8')(sys.stdout)
    return ifp, ofp


def process_args(args):
    ifp, ofp = get_file_pointers(args)

    # initialize tagger
    tagger = Tagger(lang=args.lang)

    # tag
    for line in ifp:
        line = line.split()
        if not line:
            continue
        wtags = tagger.tag(line)
        ofp.write('%s\n\n' % '\n'.join(['\t'.join(wt) for wt in wtags]))

    # close files
    ifp.close()
    ofp.close()


def main():
    # parse arguments
    args = parse_args(sys.argv[1:])
    process_args(args)
