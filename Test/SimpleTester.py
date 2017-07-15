"""
Resources for the simple tests.

Copyright (C) 2017 Jan-Oliver "Janonard" Opdenhövel

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import EngineL.Core
import EngineL.Gameplay
from PyQt5.QtCore import QTimer

class StartTestApp(EngineL.Core.SinglePlayerApp):
    """
    This test starts up the game and closes it after a second.
    """
    def __init__(self, argv):
        EngineL.Core.SinglePlayerApp.__init__(self, argv)

        EngineL.Gameplay.register_entity_classes(self)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.quit)
        self.timer.start()
