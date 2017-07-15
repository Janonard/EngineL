"""
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
import EngineL

class GameApp(EngineL.Core.SinglePlayerApp):
    """
    Game App class.
    """
    def __init__(self, argv):
        EngineL.Core.SinglePlayerApp.__init__(self, argv)

        try:
            EngineL.Gameplay.register_entity_classes(self)

            # Place your class registrations here!

            self.restore_world()

            self.connect_places()
        except Exception as err:
            self.crash(str(err))

        for child in self.children():
            if issubclass(child.__class__, EngineL.Core.Entity):
                child.on_game_launched()
