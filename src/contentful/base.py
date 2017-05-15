#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Contentful API
# Copyright (c) 2008-2017 Hive Solutions Lda.
#
# This file is part of Hive Contentful API.
#
# Hive Contentful API is free software: you can redistribute it and/or modify
# it under the terms of the Apache License as published by the Apache
# Foundation, either version 2.0 of the License, or (at your option) any
# later version.
#
# Hive Contentful API is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# Apache License for more details.
#
# You should have received a copy of the Apache License along with
# Hive Contentful API. If not, see <http://www.apache.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2017 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "Apache License, Version 2.0"
""" The license for the module """

import appier

from . import entry
from . import space

BASE_URL = "https://cdn.contentful.com/"
""" The default base url to be used when no other
base url value is provided to the constructor """

class Api(
    appier.OAuth2Api,
    entry.EntryApi,
    space.SpaceApi
):

    def __init__(self, *args, **kwargs):
        appier.Api.__init__(self, *args, **kwargs)
        self.client_id = appier.conf("CONTENTFUL_ID", None)
        self.client_secret = appier.conf("CONTENTFUL_SECRET", None)
        self.access_token = appier.conf("CONTENTFUL_TOKEN", None)
        self.base_url = kwargs.get("base_url", BASE_URL)
        self.client_id = kwargs.get("client_id", self.client_id)
        self.client_secret = kwargs.get("client_secret", self.client_secret)
        self.access_token = kwargs.get("access_token", self.access_token)
