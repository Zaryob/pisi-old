#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#
#
#  Copyright 2016 Metehan Özbek <mthnzbk@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#

from pisi.db.filesdb import FilesDB
import re
import sys

dep_tag = "<Dependency>%s</Dependency>"

cmake_file = sys.argv[1]

package_list = []

with open(cmake_file) as file_cmake:
    for line in file_cmake.readlines():
        compile = re.compile(r"^find_package\((.*) +[0-9][A-Z]\)")
        obj = compile.search(line)

        if obj:
            package_list.append(obje.groups()[0].split(" ")[0])

        compile = re.compile(r"^find_package\((.*)\)\n")
        obj = compile.search(line)

        if obj:
            package_list.append(obje.groups()[0].split(" ")[0])

files_db = FilesDB()

print(package_list)

counter = 0
packages = []

for package in package_list:
    list = files_db.search_file(package)
    if list:
        for li in list:
            for l in li[-1]:
                if (l.startswith("usr/share/%s/" % package) or l.startswith("usr/lib/cmake/%s/" % package)) and l.endswith("cmake"):
                    print package, "-", li[0], "-", l
                    counter += 1
                    packages.append(li[0])

                if not counter:
                    pass #print(package, "-", u"Bulunamadı")

                else:
                    counter = 0

    else:
        pass #print(package, "-", u"Bulunamadı")

for package in set(packages):
    print dep_tag % package