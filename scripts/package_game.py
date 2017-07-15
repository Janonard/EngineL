#!/usr/bin/python3
"""
This script packages the engine into a .zip and a .tar.gz archive.

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
import shutil

required_folders = ["EngineL", "Game", "Resources"]
required_files = ["LICENSE", "README.md", "Start Game.pyw"]

for folder_path in required_folders:
    shutil.copytree("../" + folder_path, "../package/" + folder_path)

for file_path in required_files:
    shutil.copy2("../" + file_path, "../package/" + file_path)

shutil.make_archive("Game", "zip", "../package")
shutil.make_archive("Game", "gztar", "../package")

shutil.rmtree("../package")
