# -*- coding: utf-8 -*-
#
# Copyright (C) 2016, Aquila Nipalensis
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

import gettext
__trans = gettext.translation('pisi', fallback=True)
_ = __trans.gettext

import pisi
import pisi.db.repodb
import pisi.db.itembyrepo
import pisi.group
import pisi.db.lazydb as lazydb

class GroupNotFound(Exception):
    pass

class GroupDB(lazydb.LazyDB):

    def __init__(self):
        lazydb.LazyDB.__init__(self, cacheable=True)

    def init(self):
        group_nodes = {}
        group_components = {}

        repodb = pisi.db.repodb.RepoDB()

        for repo in repodb.list_repos():
            doc = repodb.get_repo_doc(repo)
            group_nodes[repo] = self.__generate_groups(doc)
            group_components[repo] = self.__generate_components(doc)

        self.gdb = pisi.db.itembyrepo.ItemByRepo(group_nodes)
        self.gcdb = pisi.db.itembyrepo.ItemByRepo(group_components)

    def __generate_components(self, doc):
        groups = {}
        components = doc.getElementsByTagName("Component")
        for c in components:
            groupobj = c.getElementsByTagName("Group")[0]
            for group in groupobj:
                nodes = group.childNodes
                for node in nodes:
                   if node.nodeType == node.TEXT_NODE:
                       group = node.data
                       if not group:
                           group = "unknown"
                       groups.setdefault(group, []).append(c.getElementsByTagName("Name").childNodes.data())
        return groups

    def __generate_groups(self, doc):
        #return dict([(x.getTagData("Name"), x.toString()) for x in doc.tags("Group")])
        for x in doc.tags("Group"):
             return dict([x.getElementsByTagName("Name").childNodes[].data, x.tostring()])

    def has_group(self, name, repo = None):
        return self.gdb.has_item(name, repo)

    def list_groups(self, repo=None):
        return self.gdb.get_item_keys(repo)

    def get_group(self, name, repo = None):

        if not self.has_group(name, repo):
            raise GroupNotFound(_('Group %s not found') % name)

        group = pisi.group.Group()
        group.parse(self.gdb.get_item(name, repo))

        return group

    def get_group_components(self, name, repo=None):
        if not self.has_group(name, repo):
            raise GroupNotFound(_('Group %s not found') % name)

        if self.gcdb.has_item(name):
            return self.gcdb.get_item(name, repo)

        return []
