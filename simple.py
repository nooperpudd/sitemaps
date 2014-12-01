# -*- coding: utf-8 -*-

from sitemap import SiteMapRoot, SiteMap
from datetime import datetime


def generate_sitemap():
    """
    """
    sitemap = SiteMap()
    sitemap.append("http://www.xxx.com", datetime.now(), "weekly", 0.9)
    sitemap.append("http://www.xxx.com/a1", datetime.now(), "monthly", 0.7)
    sitemap.save_xml("sitemap.xml")


def generate_sitemap_gz():
    """

    :return:
    """
    sitemap = SiteMap()
    sitemap.append("http://www.xxx.com", datetime.now(), "weekly", 0.9)
    sitemap.append("http://www.xxx.com/a1", datetime.now(), "monthly", 0.7)

    xml_string = sitemap.to_string

    sitemap_root = SiteMapRoot("http://www.new.com", "root_sitemap.xml", False)
    sitemap_root.append("sitemap1.xml.gz", xml_string)
    sitemap_root.save_xml()


if __name__ == "__main__":
    generate_sitemap()
    generate_sitemap_gz()