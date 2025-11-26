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

"""Provides class for random identifier generation."""

import logging

from os.path import abspath, dirname, join
from uuid import uuid4
from random import choice, choices
from string import ascii_letters, ascii_lowercase, digits

from load import load

class ID:
    """ ID is a class for random identifier generation."""

    logger = logging.getLogger(__name__)

    def gen_string_uuid(self) -> str:
        """Generates UUID as a string.  Will contain hyphens ('-')

        Returns:
            str: UUID as string.
        """

        return str(uuid4())

    def gen_alphanumeric_uuid(self) -> str:
        """Generates UUID as a string.  Will not contain hyphens ('-')

        Returns:
            str: UUID as a string with alphanumeric characters only.
        """

        return str(uuid4().hex)

    def gen_upper_alphanumeric_uuid(self) -> str:
        """Generates UUID as alphanumeric string in UPPERCASE.
            Will not contain hyphens ('-')

        Returns:
            str: UUID as a string in UPPERCASE
                 with alphanumeric characters only.
        """

        return self.gen_alphanumeric_uuid().upper()

    def gen_numeric_id(self, length: int) -> str:
        """Generates a numeric identifier.

        Args:
            length (int): max. length of the identifier.

        Returns:
            str: A generated numeric identifier.
        """
        return ''.join(choice(digits) for _ in range(length))


    def gen_alphanumeric_id(self, length: int) -> str:
        """Generates an alphanumeric identifier.

        Args:
            length (int): max. length of the identifier.

        Returns:
            str: A generated alphanumeric identifier.
        """
        chars = ascii_lowercase + digits
        return ''.join(choice(chars) for _ in range(length))

    def gen_hyphenated_alphanumeric_id(self, length: int) -> str:

        chars = ascii_letters + digits + '-' + '_'
        return ''.join(choices(chars, k= length))

    def gen_upper_alphanumeric_id(self, length: int) -> str:
        """Generates an alphanumeric identifier in UPPERCASE.

        Args:
            length (int): max. length of the identifier.

        Returns:
            str: A generated alphanumeric identifier in UPPERCASE.
        """
        return self.gen_alphanumeric_id(length).upper()


    def __get_prefixes(self) -> list:

        d = dirname(abspath(__file__))
        prefix_file = join(d, 'salesforce-identifier-prefixes.json')
        prefix_schema_file = join(d, 'salesforce-identifier-prefixes.schema.json')
        return load.Load().load(prefix_file, prefix_schema_file)

    def gen_salesforce_id(self, entity:str) -> str:
        """generates a 18 character Salesforce ID.
        Args:
            entity(str): Salesforce entity type
        Returns:
            str: Salesforce ID
        """
        prefixes = self.__get_prefixes()
        try:
            prefix = [
                p for p in prefixes
                if p.get('entity') == entity
            ][0].get('keyPrefix','XXX')
        except IndexError as err:
            print(err)

        instance = self.gen_alphanumeric_id(2)
        reserve = '0'
        id = self.gen_alphanumeric_id(12)

        return prefix + instance + reserve + id

