#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
import re

import grequests
import requests
from bs4 import BeautifulSoup

url = "https://core.telegram.org/schema"
source = requests.get(url).text

soup = BeautifulSoup(source, features="html.parser")
links = soup.code.find_all("a", href=True)

combinators = {
    "type": [],
    "constructor": [],
    "method": []
}

ignore = ["Bool", "True", "Vector%20t", "int", "string", "Error", "Null", "%23", "long", "bytes", "double",
          "boolFalse",
          "boolTrue", "true", "vector", "error", "null", ]

for link in links:
    kind, name = re.match(r"/(.+)/(.+)", link["href"]).groups()

    if name in ignore:
        continue

    if name not in combinators[kind]:
        combinators[kind].append(name)

combinators["type"] = sorted(combinators["type"])
combinators["constructor"] = sorted(combinators["constructor"])
combinators["method"] = sorted(combinators["method"])

base = "https://core.telegram.org/{kind}/{name}"

docs = {
    "type": {},
    "constructor": {},
    "method": {}
}

unwanted = [
    "for more info see the passport docs »",
    "More about Telegram Login »",
    "see here for more info on decompression »",
    "as described in decrypting data »",
    "it must be verified, first ».",
    "as computed in top peer rating »",
    "for more info click here »",
    "as described in files »",
]


def beautify(s):
    for x in unwanted:
        s = s.replace(x, "")

    s = s.strip(" ,.:»") + "."
    s.replace("\n", "\n    ")

    return s


for kind in docs:
    req = [grequests.get(base.format(kind=kind, name=name)) for name in combinators[kind]]
    res = grequests.map(req)

    for r in res:
        soup = BeautifulSoup(r.text, features="html.parser")

        title = soup.title.get_text()

        if "." in title:
            namespace, name = title.split(".")
            namespace = namespace.lower()
            name = name[0].upper() + name[1:]
            title = ".".join([namespace, name])
        else:
            title = title[0].upper() + title[1:]

        details = {"desc": beautify(soup.p.get_text())}

        if kind != "type":
            details["params"] = {}

            if soup.tbody:
                params_raw = soup.tbody.find_all("tr")
            else:
                params_raw = []

            for param in params_raw:
                name = param.contents[1].get_text()
                has_flags = param.contents[3].get_text() == "#"
                description = beautify(param.contents[-2].get_text())

                if has_flags:
                    continue

                details["params"][name] = description

        docs[kind][title] = details

import json

with open("docs.json", "w") as f:
    json.dump(docs, f, indent=2)
