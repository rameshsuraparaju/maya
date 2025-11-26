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
""" Provides class for random address generation. """
import logging

from random import choice
from geonamescache import GeonamesCache
from geopy import geocoders
import pgeocode
from babel.numbers import get_territory_currencies

from faker import Faker
from faker.providers import internet

class Address:
    """Address is a class for random address generation."""

    def __init__(self, min_len: int = 10, max_len: int = 100):
        """Initialize self.

        Args:
            min_len (int, optional): min. length of street name. Defaults to 5.
            max_len (int, optional): max. length of street name. Defaults to 10.
        """

        self.logger = logging.getLogger(__name__)

        self.min_len = min_len
        self.max_len = max_len
        self.gc = GeonamesCache()
        self.locales = []

    def __get_country(self, country_code: str) -> dict:
        """Generates a random country dict."""
        try:
            return self.gc.get_countries()[country_code]["name"]
        except TypeError:
            return ""

    def __get_city(self, country_code: str) -> str:
        """Randomly picks a city in a country.
        Args:
            country_code (str): ISO Country Code (alpha 2).

        Returns:
            str: City name.
        """
        return choice(
            [
                c.get("name")
                for c in list(map(list, zip(*self.gc.get_cities().items())))[1]
                if c.get("countrycode") == country_code
            ]
        )

    def __get_location(self, country_code: str, city_name: str) -> dict:
        """Generates a location with PO Code, state infos.

        Args:
            country_code (str): ISO Country code (alpha 2).
            city_name (str): City name.

        Returns:
            dict: location dict with keys:
                pocode (str): Postal Code.
                statename (str): State name.
                statecode (str): State Code.
        """
        try:
            location = [
                "" if str(x) == "nan" else x
                for x in choice(
                    pgeocode.Nominatim(country_code)
                    .query_location(city_name)
                    .values.tolist()
                )
            ]
            return {
                "pocode": location[1],
                "statename": location[3],
                "statecode": location[4],
            }
        except IndexError:
            return {"pocode": "", "statename": "", "statecode": ""}

    def set_locales(self, locales: list) -> None:

        self.locales = locales

    def gen_address(self) -> dict:
        """Generates a address dict.

        Returns:
            dict: Address dict with keys:
                country_code(str): ISO Country code (alpha 2),
                country_name(str): Country name (alpha),
                state_code(str): State code (alphanumeric),
                state_name(str): State name (alpha),
                postal_code(str): Postal Code (alphanumeric)
                city_name(str): City name (alpha),
                street(str): Street name (alphanumeric)
        """
        try:
            country_code = self.gen_country_code()
            country_name = self.__get_country(country_code)
            city = self.__get_city(country_code)
            location = self.__get_location(country_code, city)
            street = self.gen_street_address()
            geoloc = self.get_geolocation(city, str(location["statename"]), country_name)
            currency_code = get_territory_currencies(country_code)[0]

            return {
                "country_code": country_code,
                "country_name": country_name,
                "state_code": str(location["statecode"]),
                "state_name": str(location["statename"]),
                "postal_code": str(location["pocode"]),
                "city_name": city,
                "street": street,
                "latitude": geoloc.get("latitude",0.0),
                "longitude": geoloc.get("longitude",0.0),
                "currency_code": currency_code
            }
        except TypeError:
            return None

    def get_geolocation(
        self,
        city: str,
        state: str,
        country: str
    ) -> dict:
        """Get geolocation (lat, long) for a given address"""

        address = (city + ", " + state + ", " + country)
        try:
            geolocator = geocoders.Nominatim(user_agent="datagenApp")
            geolocation = geolocator.geocode(address)
            if geolocation is not None:
                return {"latitude": geolocation.latitude, "longitude": geolocation.longitude}
            else:
                return {"latitude": 0.0, "longitude": 0.0}
        except Exception as e:
            self.logger.error(e)
            return {"latitude": 0.0, "longitude": 0.0}

    def gen_address2(self) -> str:

        fake = Faker(self.locales)
        return fake.address()

    def gen_street_address(self) -> str:

        fake = Faker(self.locales)
        return fake.street_address()

    def gen_street_name(self) -> str:

        fake = Faker(self.locales)
        return fake.street_name()

    def gen_street_suffix(self) -> str:

        fake = Faker(self.locales)
        return fake.street_suffix()

    def gen_city(self) -> str:

        fake = Faker(self.locales)
        return fake.city()

    def gen_country(self) -> str:

        fake = Faker(self.locales)
        return fake.country()

    def gen_country_code(self) -> str:

        fake = Faker(self.locales)
        return fake.current_country_code()

    def gen_state(self) -> str:

        return self.gen_address().get("state_name")

    def gen_state_code(self) -> str:

        return self.gen_address().get("state_code")

    def gen_postcode(self) -> str:

        fake = Faker(self.locales)
        return fake.postcode()

    def gen_building_number(self) -> str:

        fake = Faker(self.locales)
        return fake.building_number()

    def gen_country_calling_code(self) -> str:

        fake = Faker(self.locales)
        return fake.country_calling_code()

    def gen_msisdn(self) -> str:

        fake = Faker(self.locales)
        return fake.msisdn()

    def gen_phone_number(self) -> str:

        fake = Faker(self.locales)
        return fake.phone_number()

    def gen_email(self):

        fake = Faker(self.locales)
        return fake.email()

    def gen_company_email(self):

        fake = Faker(self.locales)
        return fake.company_email()

    def gen_free_email(self):

        fake = Faker(self.locales)
        return fake.free_email()

    def gen_uri(self, deep:int):

        # add_provider is not implemented in multiple locale mode
        fake = Faker()
        fake.add_provider(internet)
        _ = deep
        return fake.uri()

    def get_currency_code(
        self,
        locale: str = "en_US",
        country_code: str = None
    ):

        if country_code:
            return get_territory_currencies(country_code)[0]
        elif locale:
            return get_territory_currencies(
                locale.split("_")[1].upper()
            )[0]

