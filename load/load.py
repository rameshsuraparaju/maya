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

"""Provides class JSON file loading and validation."""

import json
import jsonschema
from jsonschema import validate
from pathlib import Path


class Load:
    """Config is a class for JSON file loading and validation."""

    def __load_file(self, file: str) -> dict:
        """load a JSON file in to a dict.

        Args:
            file (str): file name with full path.

        Raises:
            FileNotFoundError: File not found.
            Exception: Incorrect or malformed JSON format in file.

        Returns:
            dict: JSON object in the file as a dict.
        """

        if not Path(file).is_file():
            raise FileNotFoundError(f"File: '{file}' does not exist.")

        with open(file, mode='r', encoding='utf-8') as f:
            try:
                content = json.load(f)
            except json.JSONDecodeError:
                e_msg = f'File {file} is malformed or empty.'
                raise Exception(e_msg) from None
        return content

    def __validate(self, config: dict, schema: dict) -> bool:
        """validates configuration against JSON schema

        Args:
            config (dict): configuration object.
            schema(dict): schema to validate the file content.

        Raises:
            Exception: Invalid configuration

        Returns:
            bool: configuration is valid or not.
        """

        try:
            validate(instance=config, schema=schema)
        except jsonschema.exceptions.ValidationError as err:
            raise Exception(err) from None
        return True

    def load(self, file: str, schema_file: str = None) -> dict:
        """loads JSON file and validates against its JSON schema definition

        Args:
            file (str): JSON file to load
            schema_file (str): JSON schema file to validate the file content with.

        Returns:
            dict: JSON object as dict
        """
        config = self.__load_file(file)
        if schema_file:
            schema = self.__load_file(schema_file)
            if self.__validate(config, schema):
                return config
        else:
            return config
