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

"""Provides class for JSON validation and dump to file."""

import json
import jsonschema
from jsonschema import validate
from pathlib import Path


class Dump:
    """Config is a class for JSON file loading and validation."""

    def __load_file(self, file: str) -> dict:
        """load contents of a file (JSON) into a dict object

        Args:
            file (str): file to be loaded

        Raises:
            FileNotFoundError: File not Found
            Exception: File is malformed or empty

        Returns:
            dict: dict representation of the file's JSON content
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

    def __dump_file(self, file: str, data:dict) -> bool:
        """writes the data (dict) as a JSON object into the file

        Args:
            file (str): file to be written to.
            data (dict): dict object containing data

        Raises:
            FileNotFoundError: File not found.
            Exception: _description_

        Returns:
            bool: file written or not.
        """

        if not Path(file).is_file():
            raise FileNotFoundError(f"File: '{file}' does not exist.")
        try:
            with open(file, mode='w', encoding='utf-8') as f:
                f.write(json.dumps(data, indent=2))
            return True
        except (PermissionError, OSError) as err:
            raise Exception from err


    def __validate(self, config: dict, schema: dict) -> bool:
        """validates configuration against JSON schema

        Args:
            config (dict): configuration object.
            schema(dict): schema to validate the file content.

        Raises:
            Exception: jsonschema.exceptions.ValidationError

        Returns:
            bool: configuration is valid or not.
        """

        try:
            validate(instance=config, schema=schema)
        except jsonschema.exceptions.ValidationError as err:
            raise Exception from err
        return True

    def dump(self, file: str, data: dict, schema_file: str) -> bool:
        """writes data (JSON object as dict) to file after validation

        Args:
            file (str): filename
            data (dict): dict representation of a JSON object
            schema_file (str): JSON schema file to validate data against

        Raises:
            Exception: jsonschema.exceptions.ValidationError
            Exception: PermissionError
            Exception: OSError

        Returns:
            bool: file written or not
        """
        schema = self.__load_file(schema_file)
        try:
            if self.__validate(data, schema):
                return self.__dump_file(file, data)
        except jsonschema.exceptions.ValidationError as schema_err:
            raise Exception(schema_err) from schema_err
        except (PermissionError, OSError) as err:
            raise Exception from err
