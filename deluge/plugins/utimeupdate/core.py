#
# core.py
#
# Copyright (C) 2009 Pedro Algarvio <uf@ufsoft.org>
#
# Basic plugin template created by:
# Copyright (C) 2008 Martijn Voncken <mvoncken@gmail.com>
# Copyright (C) 2007-2009 Andrew Resch <andrewresch@gmail.com>
# Copyright (C) 2009 Damien Churchill <damoxc@gmail.com>
#
# Deluge is free software.
#
# You may redistribute it and/or modify it under the terms of the
# GNU General Public License, as published by the Free Software
# Foundation; either version 3 of the License, or (at your option)
# any later version.
#
# deluge is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with deluge.    If not, write to:
#     The Free Software Foundation, Inc.,
#     51 Franklin Street, Fifth Floor
#     Boston, MA  02110-1301, USA.
#
#    In addition, as a special exception, the copyright holders give
#    permission to link the code of portions of this program with the OpenSSL
#    library.
#    You must obey the GNU General Public License in all respects for all of
#    the code used other than OpenSSL. If you modify file(s) with this
#    exception, you may extend this exception to your version of the file(s),
#    but you are not obligated to do so. If you do not wish to do so, delete
#    this exception statement from your version. If you delete this exception
#    statement from all source files in the program, then also delete it here.
#

import os
import logging
from deluge.plugins.pluginbase import CorePluginBase
import deluge.component as component
import deluge.configmanager
from deluge.core.rpcserver import export
from deluge.ui.common import FileTree

DEFAULT_PREFS = {
    "enabled": False
}

log = logging.getLogger(__name__)

class Core(CorePluginBase):
    def enable(self):
        log.debug("Enabling %s UTimeUpdate Plugin", self.__class__.__name__)
        self.config = deluge.configmanager.ConfigManager("utimeupdate.conf", DEFAULT_PREFS)

        component.get("EventManager").register_event_handler(
            "TorrentFinishedEvent", self.on_torrent_finished
        )

    def disable(self):
        log.debug("Disabling %s UTimeUpdate Plugin", self.__class__.__name__)
        component.get("EventManager").deregister_event_handler(
            "TorrentFinishedEvent", self.on_torrent_finished
        )

    def update(self):
        pass

    @export
    def set_config(self, config):
        """Sets the config dictionary"""
        for key in config.keys():
            self.config[key] = config[key]
        self.config.save()

    @export
    def get_config(self):
        """Returns the config dictionary"""
        return self.config.config


    def on_torrent_finished(self, torrent_id):
        torrent = component.get("TorrentManager")[torrent_id]
        save_path = component.get("TorrentManager")[torrent_id]. \
                                        get_status(["save_path"])["save_path"]

        paths = []
        for entry in torrent.get_files():
            paths.append(entry['path'])

#        print paths

        torrent_tree = FileTree(paths)

#        print 2, torrent_tree
#        print 3, torrent_tree.tree
#        print 4, torrent_tree.tree.keys()

        for key in torrent_tree.tree.keys():
            utime_path = os.path.join(save_path, key)
            log.debug("Updating UTimes on %s", utime_path)
            os.utime(utime_path, None)
