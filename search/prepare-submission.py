#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import zipfile
import projectParams

try:
    raw_input
except NameError:
    raw_input = input

here = os.path.abspath(os.path.dirname(__file__))


def zipit(zipname, files):
    with zipfile.ZipFile(zipname, 'w') as zp:
        for fn in files:
            zp.write(os.path.join(here, fn), fn)


def main():
    uid = None
    if len(sys.argv) > 1:
        # We are only interested in the last argument
        try:
            int(sys.argv[-1])
            uid = sys.argv[-1]
        except TypeError:
            pass

    if uid is None:
        uid = raw_input('Seu número de matricula: ')

    zipname = os.path.join(here, uid + '.zip')

    try:
        os.unlink(zipname)
    except:
        pass

    zipit(zipname, projectParams.STUDENT_CODE_DEFAULT.split(','))

if __name__ == '__main__':
    main()
