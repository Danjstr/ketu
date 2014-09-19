#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function

import cPickle
from IPython.parallel import Client, require


@require(cPickle)
def search(pkl_fn):
    with open(pkl_fn, "rb") as f:
        q, pipe = cPickle.load(f)

    print("Starting {0}".format(q["kicid"]))
    pipe.query(**q)
    print("Finished {0}".format(q["kicid"]))


if __name__ == "__main__":
    import os
    import sys
    import glob
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("file_pattern", help="the file pattern")
    parser.add_argument("-p", "--profile-dir", default=None,
                        help="the IPython profile dir")

    args = parser.parse_args()
    print("Running with the following arguments:")
    print("sys.argv:")
    print(sys.argv)
    print("args:")
    print(args)

    c = Client(profile_dir=args.profile_dir)
    pool = c.load_balanced_view()
    list(pool.map(search, map(os.path.abspath, glob.glob(args.file_pattern))))