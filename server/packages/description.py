#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the Apache License v. 2 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2025-2025 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        description.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-29     xqyjlj       initial version
#

import json

from public.csp.i18n import I18n


class PackageDescription:
    class Author:
        class Website:
            def __init__(self, data: dict):
                self.__data = data

            def __str__(self) -> str:
                return json.dumps(self.__data, indent=2, ensure_ascii=False)

            @property
            def origin(self) -> dict:
                return self.__data

            @property
            def blog(self) -> str:
                return self.__data.get("blog", "")

            @property
            def github(self) -> str:
                return self.__data.get("github", "")

        # ----------------------------------------------------------------------
        def __init__(self, data: dict):
            self.__data = data
            self.__website = None

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def name(self) -> str:
            return self.__data.get("name", "")

        @property
        def email(self) -> str:
            return self.__data.get("email", "")

        @property
        def website(self) -> Website:
            if self.__website is None:
                self.__website = PackageDescription.Author.Website(
                    self.__data.get("website", {})
                )
            return self.__website

    # --------------------------------------------------------------------------
    def __init__(self, data: dict):
        self.__data = data

        self.__author = None
        self.__vendorUrl = None
        self.__description = None
        self.__url = None

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def author(self) -> Author:
        if self.__author is None:
            self.__author = PackageDescription.Author(self.__data.get("author", {}))
        return self.__author

    @property
    def name(self) -> str:
        return self.__data.get("name", "")

    @property
    def version(self) -> str:
        return self.__data.get("version", "")

    @property
    def license(self) -> str:
        return self.__data.get("license", "")

    @property
    def type(self) -> str:
        return self.__data.get("type", "")

    @property
    def vendor(self) -> str:
        return self.__data.get("vendor", "")

    @property
    def vendorUrl(self) -> I18n:
        if self.__vendorUrl is None:
            self.__vendorUrl = I18n(self.__data.get("vendorUrl", {}))
        return self.__vendorUrl

    @property
    def description(self) -> I18n:
        if self.__description is None:
            self.__description = I18n(self.__data.get("description", {}))
        return self.__description

    @property
    def url(self) -> I18n:
        if self.__url is None:
            self.__url = I18n(self.__data.get("url", {}))
        return self.__url

    @property
    def support(self) -> str:
        return self.__data.get("support", "")
