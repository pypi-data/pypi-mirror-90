#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Administration Scripts
# Copyright (c) 2008-2020 Hive Solutions Lda.
#
# This file is part of Hive Administration Scripts.
#
# Hive Administration Scripts is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Administration Scripts is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Administration Scripts. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2020 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

configurations = (
    {
        "recursive" : True,
        "tab_to_spaces" : True,
        "trailing_newlines" : True,
        "windows_newline" : True,
        "file_extensions" : (
            "py",
            "js",
            "rb",
            "php",
            "cs",
            "java",
            "css",
            "cpp",
            "c",
            "m",
            "mm",
            "hpp",
            "h",
            "cl",
            "pch",
            "lua",
            "cs",
            "sol",
            "st",
            "ctp",
            "xml",
            "xsd",
            "html",
            "xhtml",
            "wiki",
            "wik",
            "prl",
            "json",
            "yml",
            "txt",
            "hxml",
            "hx",
            "as",
            "am",
            "m4",
            "mxml",
            "bat",
            "tpl",
            "vcproj",
            "csproj",
            "sln",
            "strings",
            "conf",
            "rst",
            "liquid",
            "go",
            "gitignore",
            "swift",
            "Dockerfile",
            "vue",
            "gradle"
        ),
        "file_exclusion" : ("android-sdk",)
    },
    {
        "recursive" : True,
        "tab_to_spaces" : True,
        "trailing_newlines" : True,
        "windows_newline" : False,
        "file_extensions" : (
            "sh",
            "drg",
            "am",
            "m4",
            "md",
            "csv",
            "kt",
            "asm"
        ),
        "file_exclusion" : ("android-sdk",)
    }
)
