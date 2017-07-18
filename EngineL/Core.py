"""
The Core module contains the very core classes required by every game.

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
from collections import deque
import os.path
from xml.etree import ElementTree
from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import QApplication, QErrorMessage

class StringResourceManager(QObject):
    """
    The StringResourceManager manages the strings used by the game. At startup, it loads them from
    the resources file and is able to look them up all the time in many different ways.
    """

    def __init__(self, parent=None):
        QObject.__init__(self, parent)

        try:
            self.tree = ElementTree.parse("./Resources/" + "strings.xml")
        except (FileNotFoundError, ElementTree.ParseError) as exception:
            parent.crash(str(exception))

    def get_tree(self):
        """
        This constant method returns the file tree.
        """
        return self.tree

    def get_element(self, key):
        """
        This constanct method returns the element with the given key, which has to be formatted
        like "key.to.string". If the requested element could not be found, it crashes the game since
        this is a fatal error.
        """
        split_path = key.split(".")
        index = 0
        current_element = self.tree.getroot()
        while index < len(split_path):
            new_element = current_element.find(split_path[index])
            if new_element is None:
                QApplication.instance().crash("Could not find a resource string with the key " +key)
            current_element = new_element
            index += 1
        return current_element

    def get_string(self, key, pure_text=True):
        """
        This constant method returns the string with the given key, which has to be formatted like
        "key.to.string". If pure_text is True, it will return the string as it is, otherwise, it
        will add <b>-tags if the string has the attribute "bold":"True".
        If the requested string could not be found, the game will crash.
        """
        try:
            element = self.get_element(key)
        except LookupError as err:
            raise err
        text = element.text
        if (not pure_text) and ("bold" in element.attrib):
            if bool(element.attrib["bold"]):
                text = "<b>" + text + "</b>"
        return text

    def decode_string(self, string, pure_text=False):
        """
        This constant method takes the given string, replaces every resource string key with it's
        representation and returns the result. If the given string contains a key that doesn't
        exist, the game will crash.
        """
        complete_text = string
        continue_searching = True
        while continue_searching:
            res_string_begin = complete_text.find("${")
            res_string_end = complete_text.find("}")

            if res_string_begin != -1 and res_string_end != -1:
                key = complete_text[res_string_begin+2:res_string_end]
                try:
                    middle_part = self.get_string(key, pure_text)
                except LookupError as err:
                    raise err

                if res_string_begin > 0:
                    first_part = complete_text[0:res_string_begin]
                else:
                    first_part = str()

                if res_string_end+1 < len(complete_text):
                    last_part = complete_text[res_string_end+1:len(complete_text)]
                else:
                    last_part = str()

                complete_text = first_part + middle_part + last_part
            else:
                continue_searching = False
        return complete_text

def get_res_man():
    """
    This constant method returns the current resources manager.
    """
    return QApplication.instance().get_res_man()

class Entity(QObject):
    """
    The Entity base class for all "things" inside the game.
    """

    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.description = str()
        self.is_place = False
        self.states = dict()
        self.hidden = False
        self.gender = "n"
        self.show_article = True
        self.use_definite_article = False
        self.activly_usable = False

    def transfer(self, targeted_parent):
        """
        This non-constant method tries to transfer us to the given parent. Also, it asks ourself,
        our parent and our targeted parent if the transfer is ok and fires a transfer event
        afterwards.
        """
        transfer_okay = True
        if self.parent() == targeted_parent:
            transfer_okay = False

        if not self.check_transfer_as_subject(targeted_parent):
            transfer_okay = False

        if self.parent() is not None:
            if not self.parent().check_transfer_as_parent(self, targeted_parent):
                transfer_okay = False

        if targeted_parent is not None:
            if not targeted_parent.check_transfer_as_target(self):
                transfer_okay = False

        if transfer_okay:
            old_parent = self.parent()
            self.setParent(targeted_parent)
            QApplication.instance().on_transfer(self, old_parent, targeted_parent)
        return transfer_okay

    def check_transfer_as_subject(self, targeted_parent):
        """
        This semi-abstract, constant method which checks a planned transfer from the point-of-view
        of the entity that should be transfered. At default, it returns True.
        """
        return True

    def check_transfer_as_parent(self, subject, target):
        """
        This constant method checks whether the planned transfer is ok. In detail, it checks whether
        the subject is one of our childs and whether the target is at the same place as we are.
        """
        if target is None:
            return True
        else:
            if not subject in self.children():
                return False
            parent = self
            while not parent.get_is_place():
                parent = parent.parent()
            return parent == target or parent.findChild(Entity, target.objectName()) is not None

    def check_transfer_as_target(self, subject):
        """
        A semi-abstract constant method which checks a planned transfer from the point of view of
        the targeted parent. At default, it returns True.
        """
        return True

    def on_transfer(self, subject, parent, target):
        """
        This semi-abstract method gets called when an entity in the game gets transfered from it's
        parent to a target. At default, it calles on_transfer to our children.
        """
        for child in self.children():
            if issubclass(child.__class__, Entity):
                child.on_transfer(subject, parent, target)

    def on_game_launched(self):
        """
        This semi-abstract method gets only called when the game has started. At default, it only
        passes the event to our children, but I can override it in any other way.
        """
        for child in self.children():
            if issubclass(child.__class__, Entity):
                child.on_game_launched()


    def talk_to(self, target_name):
        """
        This non-constant method starts a conversation with another entity by calling it's
        on_talk_to method. Returns True if the conversation was started and False if not and nothing
        will be changed.
        """
        place = self
        while not place.is_place:
            place = place.parent()
            if place is None:
                return False

        target = None
        if place.objectName() == target_name:
            target = place
        else:
            target = place.findChild(Entity, target_name)
        if target is None:
            return False

        return target.on_talk_to(self) is not self

    def on_talk_to(self, other_entity):
        """
        When an entity, usually the player, wants to talk to another entity, it calls this
        non-constant, semi-abstract method on it. The other_entity is the entity who started the
        conversation. At default, this returns other_entity to show that it is not implemented;
        Subclasses may override it to start a scene or do something else.
        """
        return other_entity

    def on_used(self, user, other_entity=None):
        """
        This non-constant, abstract method executes the tasks that the user abstractly does with
        ourselves and an optional other entity and returns whether this was successfull or not.

        At default, it has two modes: If self.activly_usable is True, it will try to pass the
        on_used to the other_entity and will return it's return value. If this did not work or
        self.activly_usable is False, it will return False.

        One example on how this may be overriden in a usefull way: The user wants to combine
        ourselves with another entity to create a new one. This method would check whether the other
        entity has the required type, would add the new one and disconnect us and the other entity
        from the world tree.
        """
        if other_entity is not None:
            if (not self.activly_usable) and other_entity.activly_usable:
                return other_entity.on_used(user, self)
        return False

    def get_raw_description(self):
        """
        This constant, semi-abstract method returns our current raw description which does not
        include automated descriptions like the exit or inventory listing. At default, this method
        always returns a single description, but it may be overriden at free will.
        """
        return self.description

    def generate_description(self):
        """
        This constant method returns our description including our raw description and additional
        automated listings.
        """
        inventory_list = self.generate_inventory_list()
        if len(inventory_list) > 0:
            return self.get_raw_description() + " " + inventory_list + "."
        else:
            return self.get_raw_description() + "."

    def generate_inventory_list(self, empty_note=False):
        """
        This constant method generates a list of our inventory (aka or children) for display
        purposes and returns it. If empty_note is True and we have no children, it will return a
        note telling so, but if empty_note is False, it will return an empty string. If an internal
        error occurs (e.g. a resource string could not be found), it will raise a LookupError.
        """
        children = []
        for child in self.children():
            if issubclass(child.__class__, Entity) and (not child.get_is_hidden()):
                children.append(child)

        string_key_root = "${core.entity.inventoryList."
        try:
            if len(children) == 0:
                if empty_note:
                    return ". " + self.get_pronoun(upper=True) + string_key_root + "emptyEntity}"
                else:
                    return str()

            if self.is_place:
                inventory_list = ". " + string_key_root + "placeBeginning} "
            else:
                inventory_list = ". " + self.get_pronoun(True) + " "
                inventory_list += string_key_root + "entityBeginning} "
            inventory_list += children[0].get_effective_article() + " "
            inventory_list += "<b>" + children[0].objectName() + "</b>"

            if len(children) > 2:
                for child in children[1:len(children)-1]:
                    inventory_list += string_key_root + "normalSeparator} "
                    inventory_list += child.get_effective_article() + " "
                    inventory_list += "<b>" + child.objectName() + "</b>"

            if len(children) >= 2:
                inventory_list += " " + string_key_root + "lastSeparator} "
                inventory_list += children[len(children)-1].get_effective_article() + " "
                inventory_list += "<b>" + children[len(children)-1].objectName() + "</b>"

            return inventory_list
        except LookupError as err:
            raise err

    def get_pronoun(self, upper=False):
        """
        This constant method returns a string containing the key to our pronoun. If upper is True
        (default), it will return the upper-case version, if not, the lower-case one.
        """
        if upper:
            case_key = "upper"
        else:
            case_key = "lower"
        return "${core.grammar.pronoun." + self.gender + "." + case_key + "}"

    def get_effective_article(self, upper=False):
        """
        This constant method returns a string containing the key to our article accounting our
        shown_article and use_definite_article flags. This might even lead to an empty string as a
        return value. If upper is True (default), it will return the upper-case version, if not,
        the lower-case one.
        """
        if self.get_show_article():
            if self.get_use_definite_article():
                return self.get_definite_article(upper)
            else:
                return self.get_indefinite_article(upper)
        else:
            return str()

    def get_definite_article(self, upper=False):
        """
        This constant method returns a string containing the key to our definite article. If upper
        is True (default), it will return the upper-case version, if not, the lower-case one.
        """
        if upper:
            case_key = "upper"
        else:
            case_key = "lower"
        return "${core.grammar.definiteArticle." + self.gender + "." + case_key + "}"

    def get_indefinite_article(self, upper=False):
        """
        This constant method returns a string containing the key to our indefinite article. If upper
        is True (default), it will return the upper-case version, if not, the lower-case one.
        """
        if upper:
            case_key = "upper"
        else:
            case_key = "lower"
        return "${core.grammar.indefiniteArticle." + self.gender + "." + case_key + "}"

    def get_preposition(self, upper=False):
        """
        This constant method returns a string containing the key to our indefinite article. If upper
        is True (default), it will return the upper-case version, if not, the lower-case one.
        """
        if upper:
            case_key = "upper"
        else:
            case_key = "lower"
        return "${core.grammar.preposition." + self.gender + "." + case_key + "}"

    def to_etree_element(self, parent_element):
        """
        This constant, semi-abstract method converts itself into a etree element, that will be saved
        as an XML file, and returns it. Overrides should always call the parent's method and
        modify the element they return. This way, all required information will be reserved.
        """
        element = ElementTree.Element(self.__class__.__name__)

        element.attrib["name"] = self.objectName()
        element.attrib["description"] = self.description
        element.attrib["gender"] = self.gender

        article_element = ElementTree.SubElement(element, "article")
        article_element.attrib["shown"] = str(self.show_article)
        article_element.attrib["used"] = str(self.use_definite_article)

        for state in self.states.items():
            children_element = ElementTree.SubElement(element, "state")
            children_element.attrib["key"] = state[0]
            children_element.attrib["value"] = str(state[1])

        children_element = ElementTree.SubElement(element, "children")
        for child in self.children():
            if issubclass(child.__class__, Entity):
                child.to_etree_element(children_element)

        parent_element.append(element)
        return element

    def from_etree_element(self, element):
        """
        This non-constant, semi-abstract method restores the object from the given etree element. In
        some cases, it might raise a LookupError. If so, the object and it's children are in a valid
        state, but might be changed.
        """
        try:
            o_name = get_res_man().decode_string(element.attrib["name"], True)
            self.setObjectName(o_name)
        except KeyError:
            pass

        try:
            o_description = element.attrib["description"]
            self.description = o_description
        except KeyError:
            pass

        try:
            o_gender = element.attrib["gender"]
            self.gender = o_gender
        except KeyError:
            pass

        article_element = element.find("article")
        if article_element is not None:
            try:
                o_show = article_element.attrib["shown"]
                o_show = bool(o_show)
                self.show_article = o_show
            except (TypeError, KeyError):
                pass

            try:
                o_definite = article_element.attrib["definite"]
                o_definite = bool(o_definite)
                self.use_definite_article = o_definite
            except (TypeError, KeyError):
                pass

        for state_element in element.findall("state"):
            key = state_element.get("key")
            value = state_element.get("value")

            if key is None or value is None:
                raise LookupError("Incomplete state tag!")

            try:
                value = int(value)
            except ValueError:
                raise LookupError("Invalid state value!")

            self.set_state(key, value)

        children_element = element.find("children")
        if children_element is not None:
            for child in list(children_element):
                entity_class = QApplication.instance().lookup_entity_class(child.tag)
                if entity_class is None:
                    raise LookupError("Could not find the entity class " + child.tag + "!")
                new_entity = entity_class(self)
                new_entity.from_etree_element(child)

    def set_state(self, key, value):
        """
        This non-constant method sets a state defined by it's key, which has to be a string, to the
        value, which has to be an integer. If the given state does not exist, it is going to be
        created and if the given type requirements weren't met, nothing will happen.
        """
        if isinstance(key, str) and isinstance(value, int):
            self.states[key] = value

    def remove_state(self, key):
        """
        This non-constant method removes a state from us. If the given state does not exist, nothing
        will happen.
        """
        try:
            del self.states[key]
        except KeyError:
            pass

    def get_states(self):
        """
        This constant method returns all of our states.
        """
        return self.states

    def get_state(self, key):
        """
        This constant method returns the state with the given key. If the demand state does not
        exist, it will raise a KeyError.
        """
        try:
            val = self.states[key]
            return val
        except KeyError as err:
            raise err

    def get_is_place(self):
        """
        This constant method returns True if it's a place
        """
        return self.is_place
    
    def get_is_hidden(self):
        """
        This constant method returns True if we are hidden and do not want to be listed in inventory
        or exit listings.
        """
        return self.hidden
    
    def set_is_hidden(self, is_hidden):
        """
        This non-constant method sets our `is_hidden` flag: If it is True, we won't be listed in
        inventory or exit listings.
        """

    def get_gender(self):
        """
        This constant method returns our grammatical gender, which is usually "m", "f" or "n".
        """
        return self.gender

    def set_gender(self, new_gender):
        """
        This non-constant method sets our grammatical gender to the given value, which should be
        "m", "f" or "n"
        """
        self.gender = new_gender

    def get_show_article(self):
        """
        This constant method returns True if we want our article to be shown and False if not.
        """
        return self.show_article

    def get_use_definite_article(self):
        """
        This constant method returns True if we want our definite article to be shown and False if
        we want the indefinite one.
        """
        return self.use_definite_article
    
    def get_activly_usable(self):
        """
        This constant method returns True if we are activly usable and False if not.
        """
        return self.activly_usable

class StaticEntity(Entity):
    """
    This so-called static entity won't move ever since it denies every transfer.
    """
    def __init__(self, parent=None):
        Entity.__init__(self, parent)

    def check_transfer_as_subject(self, targeted_parent):
        """
        This constant, overriden method always returns False, since this is a static entity which
        won't move.
        """
        if targeted_parent is None:
            return True
        else:
            return False

class Place(Entity):
    """
    The base class for all places in the game.
    """

    def __init__(self, parent=None):
        Entity.__init__(self, parent)
        self.is_place = True
        self.connected_places = []
        self.connected_places_names = []
        self.set_state("visited", 0)

    def check_transfer_as_parent(self, subject, target):
        """
        This overriden, constant, semi-abstract method checks whether the planned transfer is ok. If
        the new parent is a place, it tries to find a connection from us to it using a breadth-first
        search. If not, it uses the default behaviour. Returns True if the transfer is okay, False
        if not.
        """
        if target is None:
            return True
        elif target.is_place:
            if not subject in self.children():
                return False
            place_queue = deque()
            place_queue.append(self)
            checked_places = [self]
            while len(place_queue) > 0:
                for new_place in place_queue.popleft().get_connected_places():
                    if new_place == target:
                        return True
                    if new_place not in checked_places:
                        place_queue.append(new_place)
                        checked_places.append(new_place)
            return False
        else:
            return Entity.check_transfer_as_parent(self, subject, target)

    def get_connected_places(self, object_names=None):
        """
        This constant method works in two different ways: If object_names is None, what it will be
        when you leave it out, it will return all connected places, but if it is a list containing
        strings, it will return a list with all places that are mentioned in object_names.
        If not all entries could be found, it raises a LookupError.
        """
        if object_names is None:
            return self.connected_places
        else:
            found_places = []
            for place in self.connected_places:
                if place.objectName() in object_names:
                    found_places.append(place)
            if len(found_places) != object_names:
                raise LookupError("Could not find all requested elements!")
            return found_places

    def get_connected_place(self, object_name):
        """
        This constant method returns the connected place with the given object name or raises a
        LookupError if it doesn't exist.
        """
        for place in self.connected_places:
            if place.objectName() == object_name:
                return place
        raise LookupError()

    def connect_place(self, new_place):
        """
        This non-constant function connects us with the new_place. If new_place is not a subclass
        of Place, it throws a TypeError.
        """
        if issubclass(new_place.__class__, Place):
            if not new_place in self.connected_places:
                self.connected_places.append(new_place)
        else:
            raise TypeError(str(new_place) + " is not a Place!")

    def disconnect_place(self, object_name):
        """
        This non-constant method cuts the connection between us and the other place identified by
        it's object name. It might raise a LookupError if the given place does not exist or is not
        connected to us. If so, nothing will be changed.
        """
        places_index = -1
        for index in range(0, len(self.connected_places)):
            if self.connected_places[index].get_object_name() == object_name:
                places_index = index
                break
        if places_index == -1:
            raise LookupError("Could not find the place " + object_name + "!")
        del self.connected_places[places_index]

    def build_all_connections(self):
        """
        This non-constant method creates a connection the every place listed in
        connected_places_names. If a place could not be found, it raises a LookupError, but the
        object might be changed when this happens.
        """
        for name in self.connected_places_names:
            try:
                self.build_connection(name)
            except LookupError as err:
                raise err

    def build_connection(self, object_name):
        """
        This non-constant method tries to create a connection to the place with the given name. If
        the given place could not be found, it raises a LookupError, but nothing will be changed
        when this happens.
        """
        try:
            place = self.parent().findChild(Place, object_name)
        except LookupError as err:
            raise err
        self.connect_place(place)

    def generate_description(self):
        desc = self.description + self.generate_inventory_list()
        desc += self.generate_exit_list() + "."
        return desc

    def generate_exit_list(self):
        """
        This constant method generates a readable list of all places we are connected to. It may
        throw a LookupError if a resource string could not be found.
        """
        con_places = []
        for place in self.connected_places:
            if not place.get_is_hidden():
                con_places.append(place)

        if len(con_places) == 0:
            return "${core.place.exitList.noExits}"

        try:
            inventory_list = "${core.place.exitList.beginning} " + con_places[0].get_preposition()
            inventory_list += " <b>" + con_places[0].objectName() + "</b>"

            if len(con_places) > 2:
                separator = " ${core.place.exitList.normalSeparator} "
                for child in con_places[1:len(con_places)-1]:
                    inventory_list += separator + child.get_preposition()
                    inventory_list += " <b>" + child.objectName() + "</b>"

            if len(con_places) >= 2:
                inventory_list += " ${core.place.exitList.lastSeparator} "
                inventory_list += con_places[len(con_places)-1].get_preposition()
                inventory_list += " <b>" + con_places[len(con_places)-1].objectName() + "</b>"

            inventory_list += " ${core.place.exitList.ending}"
        except LookupError as err:
            raise err

        return inventory_list

    def to_etree_element(self, parent_element):
        element = Entity.to_etree_element(self, parent_element)
        for place in self.connected_places:
            ElementTree.SubElement(element, "connection", attrib={"name": place.objectName()})
        return element

    def from_etree_element(self, element):
        Entity.from_etree_element(self, element)
        for connection in element.findall("connection"):
            name = connection.attrib.get("name")
            if name is None:
                raise Exception("Illegal connection element!")
            name = get_res_man().decode_string(name, pure_text=True)
            self.connected_places_names.append(name)

class SinglePlayerApp(QApplication):
    """
    The SinglePlayerApp.
    """

    def __init__(self, argv):
        QApplication.__init__(self, argv)

        self.res_man = StringResourceManager(self)

        self.entity_classes_register = dict()
        self.register_entity_classes([Entity, StaticEntity, Place])

        if "-n" in argv:
            self.save_enabled = False
        else:
            self.save_enabled = True

    def crash(self, error_text, save_world=False):
        """
        This constant function opens an QErrorMessage with the given error_text and forces python to
        exit the program. Only call this if a fatal error has happened.
        """
        if save_world:
            self.save_world()
        error_message = QErrorMessage()
        error_message.setModal(True)
        error_message.showMessage(error_text)
        exit(error_message.exec_())

    def connect_places(self):
        """
        This non-constant method calls connect_places to every root child that is a place. It may
        throw a LookupError and the object may be changed when this happens.
        """
        try:
            for child in self.children():
                if issubclass(child.__class__, Place):
                    child.build_all_connections()
        except LookupError as err:
            raise err

    def on_transfer(self, subject, parent, target):
        """
        This non-constant method passes the on_transfer event to it's children.
        """
        for child in self.children():
            if issubclass(child.__class__, Entity):
                child.on_transfer(subject, parent, target)

    def get_res_man(self):
        """
        This constant method returns the game's resources manager
        """
        return self.res_man

    def register_entity_classes(self, entity_classes):
        """
        This non-constant method registers a new entity class that can be used in xml generation and
        save files. It only works if the given class is a subclass of Entity, of course.
        """
        for e_class in entity_classes:
            if issubclass(e_class, Entity):
                self.entity_classes_register[e_class.__name__] = e_class

    def lookup_entity_class(self, name):
        """
        This constant method returns the entity class with the given name or None if it could not be
        found.
        """
        return self.entity_classes_register.get(name)

    def save_world(self, save_path=None):
        """
        This constant method saves the complete state of the world into an XML file located in
        "Resources/save.xml" if saving wasn't disabled by the '-n' flag.
        """
        if self.save_enabled:
            tree = ElementTree.ElementTree(ElementTree.Element("save"))

            for child in self.children():
                if issubclass(child.__class__, Entity):
                    child.to_etree_element(tree.getroot())

            if save_path is None:
                save_path = "./Resources/" + "save.xml"

            tree.write(save_path, encoding="UTF-16", xml_declaration=True)

    def restore_world(self, save_path=None):
        """
        This non-constant method restores the complete world from an XML file located in
        "Resources/save.xml". If this file does not exist, it tries to read from
        "Resources/world.xml" and if this does not exist too, it will raise a FileNotFoundError.
        Also, it may raise any kind of exception if something in the process went wrong. If this is
        the case, the world will be in a valid but changed state.
        """
        if save_path is None:
            save_path = "./Resources/" + "save.xml"
            if not os.path.exists(save_path):
                save_path = "./Resources/" + "world.xml"
        
        tree = ElementTree.parse(save_path)

        for child in list(tree.getroot()):
            entity_class = self.lookup_entity_class(child.tag)
            if entity_class is None:
                raise LookupError("Could not find the entity class " + child.tag + "!")
            new_entity = entity_class(self)
            try:
                new_entity.from_etree_element(child)
            except Exception as err:
                raise err
