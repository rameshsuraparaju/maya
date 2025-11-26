# MIT License

# Copyright (c) 2025 rameshsuraparaju

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

""" Provides class for random name generation."""

import logging

from faker import Faker


class Name:
    """Random name (persons and companies) generation. """

    def __init__(self) -> None:

        self.logger = logging.getLogger(__name__)
        self.locales = ["en_US"]

    def set_locales(self, locales: list):

        """Some tested locales
        Set in /config.json
        "en_IN",
        "en_AU",
        "en_NZ",
        "pt_BR",
        "sk_SK",
        "fr_FR",
        "jp_JP",
        "de_DE"
        """
        self.locales = locales

    def gen_first_name(self) -> str:

        fake = Faker(self.locales)
        return fake.first_name()

    def gen_last_name(self) -> str:

        fake = Faker(self.locales)
        return fake.last_name()

    def gen_name(self) -> str:

        fake = Faker(self.locales)
        return fake.name()

    def gen_company(self) -> dict:

        fake = Faker(self.locales)
        return fake.company()

    def gen_company_suffix(self) -> str:

        fake = Faker(self.locales)
        return fake.company_suffix()
