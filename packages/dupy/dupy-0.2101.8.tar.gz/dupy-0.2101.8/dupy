#!/usr/bin/env python

"""
Based on https://www.pythoncentral.io/finding-duplicate-files-with-python/
"""
#  Copyright (c) 2020. Davi Pereira dos Santos
#  This file is part of the dupy project.
#  Please respect the license - more about this in the section (*) below.
#
#  dupy is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  dupy is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with dupy.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is a crime and is unethical regarding the effort and
#  time spent here.
#  Relevant employers or funding agencies will be notified accordingly.


import os, sys
import hashlib
import json
from operator import itemgetter, attrgetter

globaldups = {}
sizes = {}
s = 0
f = 0


def findDup(parentFolder):
    global s
    global f
    # Dups in format {hash:[names]}
    dups = {}
    print(f"{parentFolder}\t")
    t = 0
    for filename in os.listdir(parentFolder):
        f += 1
        path = os.path.join(parentFolder, filename)
        a = 0
        if not os.path.islink(path):
            a = os.path.getsize(path)
            if os.path.isfile(path):
                try:
                    file_hash = hashfile(path)

                    if file_hash in globaldups:
                        globaldups[file_hash].append(path)
                    else:
                        globaldups[file_hash] = [path]

                    if file_hash in dups:
                        dups[file_hash].append(path)
                    else:
                        dups[file_hash] = [path]

                    if file_hash not in sizes:
                        sizes[file_hash] = a

                except FileNotFoundError:
                    pass
            elif os.path.isdir(path):
                dirdups = findDup(path)
                dir_hash = hashlib.md5("".join(dirdups.keys()).encode()).hexdigest()
                entries = {"path": path, "content": dirdups}

                if dir_hash in globaldups:
                    globaldups[dir_hash].append(path)
                else:
                    globaldups[dir_hash] = [path]

                if dir_hash in dups:
                    dups[dir_hash].append(entries)
                else:
                    dups[dir_hash] = [entries]

                if dir_hash not in sizes:
                    sizes[dir_hash] = a

        t += a
    s += t
    print(f"{f} {len(sizes)} {round(s / 100000) / 10}MB ...\n")
    return dups


# Joins two dictionaries
def joinDicts(dict1, dict2):
    """
        Usage:
        >>> a = {'a': 1}
        >>> joinDicts(a, {'b': 2})
        >>> a
        {'a': 1, 'b': 2}

    Parameters
    ----------
    dict1
    dict2

    Returns
    -------

    """
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]


def hashfile(path, blocksize=65536):  # pragma: no cover
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


if __name__ == '__main__':  # pragma: no cover
    if len(sys.argv) > 1:
        dups = {}
        folders = sys.argv[1:]
        for i in folders:
            # Iterate the folders given
            if os.path.exists(i):
                print(i, "...")
                joinDicts(dups, findDup(i))
            else:
                print('%s is not a valid path, please verify' % i)
                sys.exit()
        print()
        print("========================")
        for k, v in sorted(sizes.items(), key=itemgetter(1)):
            if len(globaldups[k]) > 1:
                print(k, f"{round(v / 100000) / 10}MB", end=":")
                print(json.dumps(globaldups[k], indent=2))
    else:
        print('Usage:\n dupy folder')
        print('Usage:\n dupy folder1 folder2 folder3 ...')
