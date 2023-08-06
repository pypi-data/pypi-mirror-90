# Copyright (C) 2000-2001 The OpenRPG Project
#
#   openrpg-dev@lists.sourceforge.net
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# --
#
# File: orpg_log.py
# Author: Dj Gilcrease
# Maintainer:
# Version:
#   $Id: orpg_log.py,v 1.9 2007/05/06 16:43:02 digitalxero Exp $
#
# Description: classes for orpg log messages
#

import os.path

from orpg.config import Settings
from orpg.orpgCore import *

class orpgLog:

    debug_loglevel = Settings.define("debug.loglevel", 0x07)

    def __init__(self, home_dir):
        self.logName = os.path.join(home_dir, time.strftime('runlog-%Y-%m-%d.txt',
                                                            time.localtime(time.time())))

    def log(self, msg, type, to_console=False):
        if to_console or type == ORPG_CRITICAL:
            print(msg)

        if type & self.debug_loglevel.value:
            logMsg = time.strftime( '[%Y-%m-%d %H:%M:%S] ', time.localtime(time.time())) + msg + "\n"
            logFile = open(self.logName, "a")
            logFile.write(logMsg)
            logFile.close()
