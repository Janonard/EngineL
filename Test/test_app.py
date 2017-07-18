"""
This module tests the capabilites of the core app and the string resource manager.

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
import Test

def test_startup():
    """
    This test starts the game and looks if it works.
    """
    game_instance = Test.EngineL.Core.SinglePlayerApp(Test.sys.argv)
    game_thread = Test.threading.Thread(target=game_instance.exec_)
    game_thread.start()
    game_instance.quit()
    game_thread.join()
    assert True

def test_class_lookup():
    """
    This test checks whether the class lookup system works or not.
    """
    import EngineL.Gameplay

    game_instance = Test.EngineL.Core.SinglePlayerApp(Test.sys.argv)
    EngineL.Gameplay.register_entity_classes(game_instance)
    assert game_instance.lookup_entity_class("Player") == EngineL.Gameplay.Player

def test_rsm():
    """
    This test checks the functionalities of the string resource manager.
    """
    game_instance = Test.EngineL.Core.SinglePlayerApp(Test.sys.argv)
    rsm = Test.EngineL.Core.get_res_man()
    assert rsm is not None

    key_text = "${core.windowTitle}${core.entity.inventoryList.normalSeparator} "
    key_text += "${core.gameplayParser.genericError}"
    result = "EngineL, Das geht nicht!"

    assert result == rsm.decode_string(key_text)
