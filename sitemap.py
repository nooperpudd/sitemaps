# -*- coding: utf-8 -*-

from xml.dom import minidom
from datetime import datetime
import gzip


class SiteMap(object):
    """
    http://www.sitemaps.org/protocol.html
    """
    def __init__(self, domain=None):
        """
        :param domain: the website domain
        """
        self._doc = minidom.Document()
        self._url_set = None
        self._build_xml()

        if domain:
            self.append(loc=domain, priority=1)

    def _build_xml(self):

        self._url_set = self._doc.createElement("urlset")
        self._url_set.setAttribute("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
        self._doc.appendChild(self._url_set)

    def append(self, loc, last_mod=None, change_freq=None, priority=None):
        """
        append the xml url element
        :param loc: str,URL of the page.  This value must be less than 2,048 characters.
        :param last_mod: datetime or string, The date of last modification of the file. use YYYY-MM-DD.
        :param change_freq: always
                            hourly
                            daily
                            weekly
                            monthly
                            yearly
                            never
        :param priority: float or int, The priority of this URL relative to other URLs on your site.
                         Valid values range from 0.0 to 1.0

        """
        assert len(loc) <= 2048, 'exceeded the maximum number of characters'

        # url
        url_element = self._doc.createElement("url")
        self._url_set.appendChild(url_element)

        # loc
        loc_element = self._doc.createElement("loc")
        loc_element.appendChild(self._doc.createTextNode(loc))
        url_element.appendChild(loc_element)

        # lastmod

        if last_mod:
            last_mod = last_mod.strftime("%Y-%m-%d") if isinstance(last_mod, datetime) else last_mod
            lastmod_element = self._doc.createElement("lastmod")
            lastmod_element.appendChild(self._doc.createTextNode(last_mod))
            url_element.appendChild(lastmod_element)

        # change freq
        if change_freq:
            assert change_freq in ['always', 'hourly', 'daily', 'weekly', 'monthly',
                                   'yearly', 'never'], 'changefreq not correct'
            change_freq_element = self._doc.createElement("changefreq")
            change_freq_element.appendChild(self._doc.createTextNode(str(change_freq)))
            url_element.appendChild(change_freq_element)

        # priority
        if priority:
            try:
                priority = float(priority)
            except ValueError:
                assert ValueError("Priority value must be a float type")
            assert 0.0 <= priority <= 1.0, 'priority out of range'

            priority_element = self._doc.createElement("priority")
            priority_element.appendChild(self._doc.createTextNode(str(priority)))
            url_element.appendChild(priority_element)

    def save_xml(self, path):
        """
        :param path: the xml file path,
        """
        with open(path, "w+") as xml_file:
            self._doc.writexml(xml_file, indent="\t", addindent="\t", newl="\n", encoding="utf-8")

    @property
    def to_string(self):
        """
        get the xml string
        """
        return self._doc.toprettyxml(encoding="utf-8")


class SiteMapRoot(object):

    def __init__(self, domain, file_path, exist):
        """
        :param domain: the website domain
        :param file_path: the sitemap xml file path
        :param exist: bool, check the sitemap exist or not
        """
        self.domain = domain
        self.index = None
        self.exist = exist
        self.file_path = file_path
        if not exist:
            self.doc = minidom.Document()
            self._build_xml()
        else:
            self.doc = minidom.parse(file_path)
            self.index = self.doc.getElementsByTagName("sitemapindex")[0]

    def _build_xml(self):

        self.index = self.doc.createElement("sitemapindex")
        self.index.setAttribute("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
        self.doc.appendChild(self.index)

    def append(self, filename, data):
        """
        :param filename: to save the xml file name
        :param data: the xml string
        """
        sitemap_element = self.doc.createElement("sitemap")
        self.index.appendChild(sitemap_element)

        # loc
        gzip_file = gzip.GzipFile(filename, mode="wb")
        gzip_file.write(data)
        gzip_file.close()

        loc_element = self.doc.createElement("loc")
        loc_element.appendChild(self.doc.createTextNode(self.domain + "/" + gzip_file.name))
        sitemap_element.appendChild(loc_element)

        # lastmod
        lastmod_element = self.doc.createElement("lastmod")
        lastmod_element.appendChild(self.doc.createTextNode(datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")))
        sitemap_element.appendChild(lastmod_element)

    def save_xml(self):
        with open(self.file_path, mode="w+") as xml_file:
            self.doc.writexml(xml_file, indent="\t", addindent="\t", newl="\n", encoding="utf-8")
