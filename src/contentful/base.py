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

from . import asset
from . import entry
from . import space
from . import content_type

BASE_URL = "https://cdn.contentful.com/"
""" The default base url to be used when no other
base url value is provided to the constructor """

LOGIN_URL = "https://be.contentful.com/"
""" The base url that is going to be used for the login
associated end points (interactive) """

SCOPE = (
    "content_management_manage",
)
""" The list of permissions to be used to create the
scope string for the oauth value """

class API(
    appier.OAuth2API,
    asset.AssetAPI,
    entry.EntryAPI,
    space.SpaceAPI,
    content_type.ContentTypeAPI
):

    def __init__(self, *args, **kwargs):
        appier.OAuth2API.__init__(self, *args, **kwargs)
        self.client_id = appier.conf("CONTENTFUL_ID", None)
        self.client_secret = appier.conf("CONTENTFUL_SECRET", None)
        self.access_token = appier.conf("CONTENTFUL_TOKEN", None)
        self.redirect_url = appier.conf("CONTENTFUL_REDIRECT_URL", None)
        self.space = appier.conf("CONTENTFUL_SPACE", "default")
        self.base_url = kwargs.get("base_url", BASE_URL)
        self.login_url = kwargs.get("login_url", LOGIN_URL)
        self.client_id = kwargs.get("client_id", self.client_id)
        self.client_secret = kwargs.get("client_secret", self.client_secret)
        self.redirect_url = kwargs.get("redirect_url", self.redirect_url)
        self.access_token = kwargs.get("access_token", self.access_token)
        self.scope = kwargs.get("scope", SCOPE)
        self.space = kwargs.get("space", self.space)

    def oauth_authorize(self, state = None):
        url = self.login_url + "oauth/authorize"
        values = dict(
            client_id = self.client_id,
            redirect_uri = self.redirect_url,
            response_type = "code",
            scope = " ".join(self.scope)
        )
        if state: values["state"] = state
        data = appier.legacy.urlencode(values)
        url = url + "?" + data
        return url

    def oauth_access(self, code):
        url = self.base_url + "oauth/access_token"
        contents = self.post(
            url,
            token = False,
            client_id = self.client_id,
            client_secret = self.client_secret,
            grant_type = "authorization_code",
            redirect_uri = self.redirect_url,
            code = code
        )
        contents = contents.decode("utf-8")
        contents = appier.legacy.parse_qs(contents)
        self.access_token = contents["access_token"][0]
        self.trigger("access_token", self.access_token)
        return self.access_token
