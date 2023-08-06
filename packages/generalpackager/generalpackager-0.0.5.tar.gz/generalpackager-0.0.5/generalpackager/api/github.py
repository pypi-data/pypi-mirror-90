
import requests
import os
import json


class GitHub:
    """ Tools to interface a GitHub Repository. """
    def __init__(self, name, owner="ManderaGeneral", token=None):
        self.name = name
        self.owner = owner
        self.token = os.environ['packager_github_api'] if token is None else token

        self.assert_url_up()  # Checks name, owner and token all in one

    def assert_url_up(self, url=None):
        """ Assert that url is working. """
        response = self._request(url=url)
        if response.status_code != 200:
            raise AssertionError(f"Request for url '{url}' status code {response.status_code} != 200.")

    def url(self):
        """ Get static URL from owner and name. """
        return f"https://github.com/{self.owner}/{self.name}"

    def api_url(self, endpoint=None):
        """ Get URL from owner, name and enpoint. """
        return "/".join(("https://api.github.com", "repos", self.owner, self.name) + ((endpoint, ) if endpoint else ()))

    def get_website(self):
        """ Get website specified in repository details.

            :rtype: list[str] """
        return self._request(method="get").json()["homepage"]

    def set_website(self, website):
        """ Set a website for the GitHub repository. """
        return self._request(method="patch", name=self.name, homepage=website)


    def get_topics(self):
        """ Get a list of topics in the GitHub repository.

            :rtype: list[str] """
        return self._request(method="get", endpoint="topics").json()["names"]

    def set_topics(self, *topics):
        """ Set topics for the GitHub repository.

            :param str topics: """
        return self._request(method="put", endpoint="topics", names=topics)


    def get_description(self):
        """ Get a string of description in the GitHub repository.

            :rtype: list[str] """
        return self._request(method="get").json()["description"]

    def set_description(self, description):
        """ Set a description for the GitHub repository. """
        return self._request(method="patch", name=self.name, description=description)

    def _request(self, method="get", url=None, endpoint=None, **data):
        """ :rtype: requests.Response """
        method = getattr(requests, method.lower())

        kwargs = {
            "headers": {"Accept": "application/vnd.github.mercy-preview+json"},
            "auth": (self.owner, self.token),
        }
        if data:
            kwargs["data"] = json.dumps(data)

        if url is None:
            url = self.api_url(endpoint=endpoint)
        return method(url=url, **kwargs)
