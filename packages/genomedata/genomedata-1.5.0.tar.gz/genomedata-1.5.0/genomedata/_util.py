#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

# Copyright 2008-2014 Michael M. Hoffman <michael.hoffman@utoronto.ca>

from argparse import ArgumentParser, FileType
from contextlib import closing
from gzip import open as _gzip_open
from os import extsep
import sys

from numpy import append, array, empty, nan
from tables import Filters, Float32Atom, NoSuchNodeError



FILTERS_GZIP = Filters(complevel=1)

EXT_GZ = "gz"
SUFFIX_GZ = extsep + EXT_GZ

GENOMEDATA_ENCODING="ascii"

DEFAULT_CHROMOSOME_NAME_STYLE = "UCSC-style-name"

chromosome_name_map_parser = ArgumentParser(add_help=False)
chromsome_names = chromosome_name_map_parser.add_argument_group("Chromosome naming")
chromsome_names.add_argument(
    "-r", "--assembly-report",
    dest="assembly_report", type=FileType('r'),
    metavar="ASSEMBLY-REPORT",
    help="Tab-delimited file with columnar mappings"
    " between chromosome naming styles.")
chromsome_names.add_argument(
    "-n", "--name-style",
    default=DEFAULT_CHROMOSOME_NAME_STYLE, dest="name_style",
    help="Chromsome naming style to use based on"
    " ASSEMBLY-REPORT. Default: {}"
    .format(DEFAULT_CHROMOSOME_NAME_STYLE))


def die(msg="Unexpected error."):
    print(msg, file=sys.stderr)
    sys.exit(1)

class LightIterator(object):
    def __init__(self, handle):
        self._handle = handle
        self._defline = None

    def __iter__(self):
        return self

    def __next__(self):
        lines = []
        defline_old = self._defline

        for line in self._handle:
            if not line:
                if not defline_old and not lines:
                    raise StopIteration
                if defline_old:
                    self._defline = None
                    break
            elif line.startswith(">"):
                self._defline = line[1:].rstrip()
                if defline_old or lines:
                    break
                else:
                    defline_old = self._defline
            else:
                lines.append(line.rstrip())

        if not lines:
            raise StopIteration

        if defline_old is None:
            raise ValueError("no definition line found at next position in %r" % self._handle)

        return defline_old, ''.join(lines)

    def next(self):
        return self.__next__()

# XXX: suggest as default
def fill_array(scalar, shape, dtype=None, *args, **kwargs):
    if dtype is None:
        dtype = array(scalar).dtype

    res = empty(shape, dtype, *args, **kwargs)
    res.fill(scalar)

    return res

# XXX: suggest as default
def gzip_open(*args, **kwargs):
    return closing(_gzip_open(*args, **kwargs))

def maybe_gzip_open(filename, mode="rt", *args, **kwargs):
    if filename.endswith(SUFFIX_GZ): 
        return gzip_open(filename, mode=mode, *args, **kwargs)
    else:
        return open(filename, mode=mode, *args, **kwargs)

def init_num_obs(num_obs, continuous):
    curr_num_obs = continuous.shape[1]
    assert num_obs is None or num_obs == curr_num_obs

    return curr_num_obs

def new_extrema(func, data, extrema):
    curr_extrema = func(data, 0)

    return func([extrema, curr_extrema], 0)


def ignore_comments(iterable):
    return (item for item in iterable if not item.startswith("#"))

def decode_tracknames(gdfile):
    return [trackname.decode(GENOMEDATA_ENCODING) for trackname in gdfile._file_attrs.tracknames]

def add_trackname(gdfile, trackname):
    # gdfile can refer to either a file for the whole genome or a single chromosome 
    assert gdfile.isopen
    if gdfile._isfile:
        # Update tracknames attribute with new trackname
        file_attrs = gdfile._file_attrs
        if "tracknames" in file_attrs:
            tracknames = file_attrs.tracknames
            if trackname in tracknames:
                raise ValueError("%s already has a track of name: %s"
                                 % (gdfile.filename, trackname))
        else:
            tracknames = array([])

        file_attrs.tracknames = append(tracknames,
                                       trackname.encode(GENOMEDATA_ENCODING))

class GenomedataDirtyWarning(UserWarning):
    pass

class OverlapWarning(UserWarning):
    pass

def main(args=sys.argv[1:]):
    pass

if __name__ == "__main__":
    sys.exit(main())
