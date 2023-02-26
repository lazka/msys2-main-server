#!/usr/bin/env python3

import os
import re
import unittest
import ssl
from urllib.request import urlopen


def get_mirrors():
    """Returns a list of URLs for all our mirrors"""

    DIR = os.path.dirname(os.path.realpath(__file__))
    mirrors = set()
    script = os.path.join(DIR, "..", "services", "mirrorbits", "add_mirrors.sh")
    with open(script, "r", encoding="utf-8") as h:
        for line in h.readlines():
            if line.startswith("#"):
                continue
            mirrors.update(
                re.findall('((?:http|https)://[a-zA-Z0-9./?=_%:-]*)', line))
    return sorted(mirrors)


class TestMirrors(unittest.TestCase):

    TIMEOUT = 75 if "CI" in os.environ else 25

    def test_mirrors_support_tls12(self):
        # https://github.com/msys2/msys2.github.io/issues/204
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.maximum_version = ssl.TLSVersion.TLSv1_2
        for url in get_mirrors():
            somefile = url.rstrip("/") + "/lastsync"
            try:
                with urlopen(somefile, context=context, timeout=self.TIMEOUT):
                    pass
            except Exception as exc:
                raise Exception(somefile) from exc


if __name__ == '__main__':
    unittest.main()
