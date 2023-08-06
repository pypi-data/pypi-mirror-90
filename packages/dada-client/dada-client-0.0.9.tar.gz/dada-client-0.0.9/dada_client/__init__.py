import os
import json

import requests
from requests import Session, Request
from requests.exceptions import ConnectionError

# python 2 -> 3
try:
    from urlparse import urljoin
except ImportError:
    from urllib.parse import urljoin

RET_CODES = [200, 201, 202]
GOOD_CODES = RET_CODES + [204]


class ClientError(Exception):
    pass


class BaseClient(object):

    """
    A base client for each endpoint to inherit from.
    """

    def __init__(self, **kw):

        # defaults / helpers
        self.api_key = kw.get("api_key", os.getenv("DADA_API_KEY"))
        self.url = kw.pop("url", os.getenv("DADA_API_URL", "http://localhost:3031"))
        self.raise_errors = kw.get("raise_errors", False)
        if not self.api_key:
            raise ClientError("You haven't set your api_key!")

        # standardize url
        if self.url.endswith("/"):
            self.url = self.url[:-1]

        # establish session
        self.session = Session()
        self.session.headers.update({"X-DADA-API-KEY": self.api_key})

    def format_url(self, *args):
        """
        Add segments to endpoint to form a URL.
        """

        return urljoin(self.url, "/".join([str(a) for a in args]))

    def request(self, method, url, **kwargs):
        """
        A wrapper for all request executions.
        """

        # issue request.
        err = None
        resp = None
        try:
            r = Request(method, url, **kwargs)
            resp = self.session.send(r.prepare())

        except ConnectionError as e:
            err = ClientError(
                "Could not connect to {0} beacuse: {1}".format(self.url, e)
            )

        # handle errors
        return self._handle_response(resp, err)

    def prepare_request_kwargs(self, raw, params=[], json=True):
        """
        Allow POST/PUT methods to accept an undifferentiated list of kwargs.
        This function will separate them into query parameters, data, and files
        so we can initalize the Request object properly.
        """

        # pop api key
        if "api_key" in raw:
            api_key = raw.pop("api_key")
            self.api_key = api_key

        # defaults
        prepared_kwargs = {"params": {}, "headers": {"X-DADA-API-KEY": self.api_key}}

        # include in params
        for p in params:
            if p in raw:
                prepared_kwargs["params"][p] = raw.pop(p)

        # separate out file from data
        if "file" in raw:
            prepared_kwargs["files"] = {"file": raw.pop("file")}

        # if we have anything else...
        if len(raw.keys()):
            # if everything should be parameters...
            if not json:
                prepared_kwargs["params"].update(raw)

            # otherwise it's POST/PUT data
            else:
                prepared_kwargs["json"] = raw

        return prepared_kwargs

    def _handle_response(self, resp, err):
        """
        Handle all errors + format response.
        """
        # check for connection errors
        if not resp and err:
            raise err

        if resp.status_code not in GOOD_CODES:
            if self.raise_errors:
                d = resp.json()
                raise ClientError(d["message"])

        # just return the response and let the client handle
        # json parsing etc
        return resp


class CollectionClient(BaseClient):
    """
    An abstract client for simple collections
    """

    def __init__(self, *args, **kwargs):
        _name = kwargs.pop("name")
        BaseClient.__init__(self, *args, **kwargs)
        self.name = _name

    def search(self, **kw):
        """
        Search a collection
        """
        kwargs = self.prepare_request_kwargs(kw, json=False)
        url = self.format_url("/{0}/".format(self.name))
        return self.request("GET", url, **kwargs)

    def upsert(self, **kw):
        """
        Upsert an instance of a collection
        """
        kwargs = self.prepare_request_kwargs(kw)
        url = self.format_url("/{0}/".format(self.name))
        return self.request("POST", url, **kwargs)

    def get(self, id, **kw):
        """
        Fetch an instance of a collection
        """
        kwargs = self.prepare_request_kwargs(kw, json=False)
        url = self.format_url("/{0}/{1}".format(self.name, id))
        return self.request("GET", url, **kwargs)

    def delete(self, id, **kw):
        """
        Delete an instance of a collection
        """
        kwargs = self.prepare_request_kwargs(kw, json=False)
        url = self.format_url("/{0}/{1}".format(self.name, id))
        return self.request("DELETE", url, **kwargs)


class TagCollectionClient(CollectionClient):
    def add_tag(self, id, tag_id, **kw):
        """
        Add a tag to an item in a collection.
        """
        kwargs = self.prepare_request_kwargs(kw, json=False)
        url = self.format_url("/{0}/{1}/tags/{2}".format(self.name, id, tag_id))
        return self.request("POST", url, **kwargs)

    def remove_tag(self, id, tag_id, **kw):
        """
        Remove a tag to an item in a collection.
        """
        kwargs = self.prepare_request_kwargs(kw, json=False)
        url = self.format_url("/{0}/{1}/tags/{2}".format(self.name, id, tag_id))
        return self.request("DELETE", url, **kwargs)


class Users(TagCollectionClient):
    """
    Users have some special cases.
    """

    def login(self, **kw):
        """
        Login via email + password.
        """
        kwargs = self.prepare_request_kwargs(kw)
        url = self.format_url("/{0}/login".format(self.name))
        return self.request("POST", url, **kwargs)


class Me(BaseClient):
    """
    Users have some special cases.
    """

    def get(self, **kw):
        """
        Upsert an instance of a collection
        """
        kwargs = self.prepare_request_kwargs(kw)
        url = self.format_url(f"/{self.name}")
        return self.request("GET", url, **kwargs)

    def update(self, **kw):
        """
        Fetch an instance of a collection
        """
        kwargs = self.prepare_request_kwargs(kw, json=False)
        url = self.format_url(f"/{self.name}")
        return self.request("PUT", url, **kwargs)


class Files(TagCollectionClient):

    """
    The Files API includes additional endpoints
    for managing related collections (folder + fields)
    """

    def prepare_file_upsert_request_kwargs(self, kw, **kwargs):
        """
        We include a method for file creation since requests
        gets confused when you include `files` and `json`
        arguments (it defaults to setting to content-type to multipart upload,
        thereby suppressing the `json`).
        We handle this by passing `json` to the `data` argument
        and serializing the fields as a json string under
        the key 'fields'. We do serialize field_data as json
        because Flask gets confused with nested data POSTs.
        """
        kwargs = self.prepare_request_kwargs(kw, json=True)
        fields = kwargs["json"].pop("fields", {})
        folders = kwargs["json"].pop("folders", [])
        desktops = kwargs["json"].pop("desktops", [])
        tags = kwargs["json"].pop("tags", [])
        kwargs["json"].update(
            {
                "fields": json.dumps(fields),
                "folders": json.dumps(folders),
                "tags": json.dumps(tags),
                "desktops": json.dumps(desktops),
            }
        )
        kwargs["data"] = kwargs.pop("json")
        return kwargs

    def upsert(self, **kw):
        """"""
        kwargs = self.prepare_file_upsert_request_kwargs(kw)
        url = self.format_url("/{0}/".format(self.name))
        return self.request("POST", url, **kwargs)

    def add_to_folder(self, id, folder_id, **kw):
        """
        Add a file to a folder.
        """
        kwargs = self.prepare_request_kwargs(kw, json=True)
        url = self.format_url("/{0}/{1}/folders/{2}".format(self.name, id, folder_id))
        return self.request("POST", url, **kwargs)

    def remove_from_folder(self, id, folder_id, **kw):
        """
        Remove a file from a folder.
        """
        kwargs = self.prepare_request_kwargs(kw, json=False)
        url = self.format_url("/{0}/{1}/folders/{2}".format(self.name, id, folder_id))
        return self.request("DELETE", url, **kwargs)

    def stream(self, id, **kw):
        """
        Get the streaming file contents. Reutrns just Request for now
        """
        kwargs = self.prepare_request_kwargs(kw, json=False)
        url = self.format_url("/{0}/{1}/stream".format(self.name, id))
        return self.session.get(url, **kwargs)

    def download(self, id, **kw):
        """
        Download a file as an attachment.
        """
        kwargs = self.prepare_request_kwargs(kw, json=False)
        url = self.format_url("/{0}/{1}/download".format(self.name, id))
        return self.session.get(url, **kwargs)


class Folders(TagCollectionClient):
    def prepare_folder_upsert_request_kwargs(self, kw, **kwargs):
        """
        We include a method for file creation since requests
        gets confused when you include `files` and `json`
        arguments (it defaults to setting to content-type to multipart upload,
        thereby suppressing the `json`).
        We handle this by passing `json` to the `data` argument
        and serializing the fields as a json string under
        the key 'fields'. We do serialize field_data as json
        because Flask gets confused with nested data POSTs.
        """
        kwargs = self.prepare_request_kwargs(kw, json=True)
        desktops = kwargs["json"].pop("desktops", [])
        tags = kwargs["json"].pop("tags", [])
        kwargs["json"].update(
            {"tags": json.dumps(tags), "desktops": json.dumps(desktops),}
        )
        kwargs["data"] = kwargs.pop("json")
        return kwargs

    def upsert(self, **kw):
        """"""
        kwargs = self.prepare_folder_upsert_request_kwargs(kw)
        url = self.format_url("/{0}/".format(self.name))
        return self.request("POST", url, **kwargs)

    def add_to_desktop(self, id, desktop_id, **kw):
        """
        Add a Folder to a desktop, optionally setting its position.
        """
        kwargs = self.prepare_request_kwargs(kw, json=True)
        url = self.format_url("/{0}/{1}/desktops/{2}".format(self.name, id, desktop_id))
        return self.request("POST", url, **kwargs)

    def remove_from_desktop(self, id, desktop_id, **kw):
        """
        Remove a Folder from a desktop, resetting the position of all other folders in this desktop.
        """
        kwargs = self.prepare_request_kwargs(kw, json=False)
        url = self.format_url("/{0}/{1}/desktops/{2}".format(self.name, id, desktop_id))
        return self.request("DELETE", url, **kwargs)


class DadaClient(BaseClient):

    """
    A class for interacting with the DADA Lake API.
    """

    def __init__(self, *args, **kwargs):
        BaseClient.__init__(self, *args, **kwargs)
        self.me = Me(name="me", **kwargs)
        self.users = Users(name="users", **kwargs)
        self.files = Files(name="files", **kwargs)
        self.folders = Folders(name="folders", **kwargs)
        self.desktops = TagCollectionClient(name="desktops", **kwargs)
        self.fields = TagCollectionClient(name="fields", **kwargs)
        self.tags = TagCollectionClient(name="tags", **kwargs)
