import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import lxml.html


__all__ = ["HTTPResponse"]


links_attributes = [
    "href",
    "codebase",
    "cite",
    "action",
    "background",
    "longdesc",
    "profile",
    "src",
    "formaction",
    "icon",
    "manifest",
    "poster",
    "archive"
]

class SoupError(Exception):
    pass

class HTTPResponse:
    """The class is a wrapper for requests.models.Response class.
    It implements helpful methods to analyse http(s) response.
    """
    def __init__(self, response):
        parsed = urlparse(response.url)
        #: Requests lib response
        self._response = response
        #: Response hostname
        self._host = "://".join([parsed.scheme, parsed.netloc])
        #: Response page path (without hostname)
        self._path = parsed.path
        #: Response status code
        self._code = response.status_code
        #: Response text as XML object
        self._xml = self._xml()
        #: Response text as BeautifulSoup object
        self._soup = self._makesoup()

    def __getattr__(self, attr):
        orig_attr = getattr(self._response, attr)
        if callable(orig_attr):
            def hooked(*args, **kwargs):
                result = orig_attr(*args, **kwargs)
                ## prevent wrapped object from becoming unwrapped
                # if result == self._response:
                #    return self
                return result
            return hooked
        else:
            return orig_attr

    def __repr__(self):
        return f"<[{self.code}] {self.url}>"

    @property
    def host(self):
        """
        """
        return self._host

    @property
    def path(self):
        """
        """
        return self._path

    @property
    def code(self) -> int:
        """Shortest way to call status_code
        """
        return self._code

    @property
    def isok(self) -> bool:
        """Indicates if status code is 200
        """
        return self.code == 200

    @property
    def isforbid(self) -> bool:
        """Indicates if status code is 403
        """
        return self.code == 403

    @property
    def exists(self) -> bool:
        """Return True if the requested url exists but not necessarily 
        accessible, False otherwise.

        Returns:
            bool: True if url exists, false otherwise
        """
        url = self.url
        location = ""
        if self.is_redirect:
            location = self._response.headers.get("Location", None)
            if location:
                location = urlparse(location).path
                url = urlparse(url).path
        return self.code in (200, 403) or location == "".join((url, "/"))

    @property
    def delay(self):
        """Reteurn response time in seconds.
        """
        return self._response.elapsed.total_seconds()

    def _xml(self):
        """Converts response into an XML object

        Returns:
            : parsed content
        """
        if self._response.text:
            return lxml.html.fromstring(self._response.text)
        return lxml.html.fromstring("<>")

    def _makesoup(self):
        """Parse HTTP response body as BeautifulSoup objcect

        Returns:
            bs4.BeautifulSoup: parsed content
        """
        return BeautifulSoup(self._response.text, "lxml")

    def xpath(self, query):
        """Excute xpath on xmltree
        """
        return self._xml.xpath(query)

    def hrefs(self):
        """Return all href values links in content page.
        """
        return self.xpath("//@href")

    def scripts(self):
        """Return all src values of scripts in content page

        Returns:
            list: list of content scripts
        """
        soup = BeautifulSoup(self._response.text, "lxml")
        return [script.prettify() for script in soup.findAll("script")]

    def srcs(self):
        """Return all src values in content page

        Returns:
            list: findings list
        """
        return self.xpath("//@src")

    def links(self) -> list:
        """
        Returns:
            list: findings list
        """
        links = set()
        for attr in links_attributes:
            for link in self.xpath(f"//@{attr}"):
                links.add(link)
        return list(links)

    
    def paths(self) -> list:
        """Find paths internal to the website in response body

        Returns:
            list: findings list
        """
        paths = []
        host = urlparse(self.host).netloc

        for link in self.links():
            parsed = urlparse(link)
            if (parsed.path and (parsed.netloc == host or not parsed.netloc)):
                paths.append(parsed.path)
        return paths

    def form(self, **attrs):
        """Get form input tag values from http.HTTPResonse

        Args:
            response (http.HTTPResonse): HTTP Response object
            **attrs: BeautifulSoup attrs

        Returns:
            str, dict: form action and inputs dictionary ready to 
                be send as POST HTTP request
        """
        form_dict = {}
        form = self.tag("form", attrs=attrs)

        # Exctracting inputs
        for input_tag in form.findAll("input"):
            if "name" in input_tag.attrs:
                value = ""
                if "value" in input_tag.attrs:
                    value = input_tag["value"]
                form_dict[input_tag["name"]] = value

        # Exctracting textareas        
        for textarea in form.findAll("textarea"):
            if "name" in textarea.attrs:
                form_dict[textarea["name"]] = textarea.text

        return form["action"], form_dict
    
    def search(self, *regex):
        """Use regular expression to search expression in the response content.
        
        Args:
            regex: regular(s) expression to use.

        Returns:
            re.match: regular expression match
        """
        for r in regex:
            match = re.search(r, self._response.text)
            if match:               
                return match


    def findall(self, regex):
        """Use regular expression to find all match of an expression in the 
        response content.
        
        Args:
            regex: regular expression to use.

        Return:
            list: regular expression results
        """
        return re.findall(regex, self._response.text)


    def tag(self, *args, **kwargs):
        """Return http response searched tags.
        
        Args:
            tag: tag name to find.
        
        Returns:
            bs4.element.Tag: Tag matching
        """
        return self._soup.find(*args, **kwargs)


    def tags(self, *args, **kwargs):
        """Return http response searched tags
        Args:
            BeautifulSoup.findall args

        Returns:
            list: tags matching
        """
        return self._soup.findAll(*args, **kwargs)
