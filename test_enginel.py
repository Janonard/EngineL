#!/usr/bin/python3
"""
EngineL test script

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
import sys
import Test

def test_startup():
    """
    This test starts the game and looks if it works.
    """
    print("HI!")
    game_instance = Test.SimpleTester.StartTestApp(sys.argv)
    #assert not bool(game_instance.exec_())
