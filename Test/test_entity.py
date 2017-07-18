"""
This module tests the capabilites of the entity class.

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

def build_playground():
    """
    This function creates a playground with a place ("Place0") and an entity ("Entity0") and returns
    them.
    """
    game = Test.EngineL.Core.SinglePlayerApp(Test.sys.argv)
    place0 = Test.EngineL.Core.Place(game)
    place0.setObjectName("Place0")
    entity0 = Test.EngineL.Core.Entity(place0)
    entity0.setObjectName("Entity0")
    return [game, place0, entity0]

def test_transfer_to_itself():
    """
    This function tests whether a transfer to our current parent gets blocked.
    """
    [game, place0, entity0] = build_playground()

    assert not entity0.transfer(place0) # An entity may not be transfered to it's current parent.
    assert entity0.parent() == place0

def test_transfer_to_n_from_none():
    """
    This function tests whether transfers from and to None work.
    """
    [game, place0, entity0] = build_playground()
    entity0.setParent(None)

    assert entity0.parent() is None
    assert entity0.transfer(place0) # An entity may transfer from None to somewhere
    assert entity0.parent() == place0
    assert entity0.transfer(None) # and from somewhere to None.
    assert entity0.parent() is None

def test_transfers_inside_place():
    """
    This function tests all transfer possibilities inside a place.
    """
    [game, place0, entity0] = build_playground()
    entity1 = Test.EngineL.Core.Entity(place0)
    entity1.setObjectName("Entity1")
    entity2 = Test.EngineL.Core.Entity(place0)
    entity2.setObjectName("Entity2")

    assert entity0.transfer(entity1)
    assert entity0.parent() == entity1

    assert entity0.transfer(entity2)
    assert entity0.parent() == entity2

    assert entity0.transfer(place0)
    assert entity0.parent() == place0

def test_transfer_to_place():
    """
    This function tests a transfer to another place.
    """
    [game, place0, entity0] = build_playground()
    place1 = Test.EngineL.Core.Place(game)
    place1.setObjectName("Place1")
    place0.connected_places = [place1]
    place1.connected_places = [place0]

    assert entity0.transfer(place1)
    assert entity0.parent() == place1
