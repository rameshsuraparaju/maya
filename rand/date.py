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

"""Provides class for random date generation.

In SAP, the data element DATS is used for a Date.
DATS representation of a date is 'YYYYMMDD'.

In BigQuery, date is represented as 'YYYY-MM-DD'
The `DATE 'YYYY-MM-DD'` function is used to convert
the date formatted string to DATE type.
"""

import logging

from datetime import date, datetime, timedelta
from random import randint, choices
import calendar
from faker import Faker


class Date:
    """Date is a class for random date generation."""

    Faker.seed(4711)
    faker = Faker()
    logger = logging.getLogger(__name__)

    def gen_date_between(self, start: str, end: str) -> date:
        """Generates a date in between two input dates

        Args:
            start (str): Earliest date in ISO format.
            end (str): Latest date in ISO format.

        Raises:
            ValueError: One of the input dates are not in ISO format.

        Returns:
            date (datetime.date): A date object in between lower and upper.
        """

        try:
            delta = date.fromisoformat(end) - date.fromisoformat(start)
            return date.fromisoformat(start) + timedelta(randint(1, delta.days))
        except ValueError as err:
            raise ValueError(err) from None

    def gen_skewed_date_between(self, months: list, weights: list) -> date:
        """Generates a date in between two input dates with a skew.

        Args:
            start (str): start date in ISO format.
            end (str): end date in ISO format.
            choices (list): choices (in months) to choose from.
            weights (list): weights for the choices.

        Returns:
            date: a date object in between lower and upper with a skew.
        """

        if len(months) != len(weights):
            raise ValueError("Months and weights must have the same length.")
        if sum(weights) != 100:
            raise ValueError("Weights must sum to 100.")
        if len(months) == 1:
            month_year = months[0].split("-")
            start = month_year[0] + "-" + month_year[1] + "-01"
        else:
            month_year = choices(months, weights=weights, k=1)[0].split("-")
            start = month_year[0] + "-" + month_year[1] + "-01"
            end = (
                month_year[0]
                + "-"
                + month_year[1]
                +"-"
                + str(calendar.monthrange(int(month_year[0]), int(month_year[1]))[1])
            )

        return self.gen_date_between(start, end)

    def gen_timestamp_between(self, start: str, end: str) -> datetime:

        return self.faker.date_time_between(start, end)

    def gen_date_around(self, key_date: str, range_days: int) -> date:
        """Generates a date around a specified key date.

        Args:
            key_date (str): Key date around which output date is generated.
            range_days (int): Max. days earlier or later to the key date.

        Raises:
            ValueError: Input key_date is not in ISO format.

        Returns:
            date(datetime.date): A date as date object around a key date.
        """

        try:
            delta = randint(1, range_days) * (randint(0, 1) * 2 - 1)
            return date.fromisoformat(key_date) + timedelta(days=delta)
        except ValueError as err:
            raise ValueError(err) from None

    def gen_date_after_days(self, start_date: date, days: int) -> date:
        return start_date + timedelta(days=days)

    def gen_date(self) -> date:
        """Generates today as date.

        Returns:
            datetime.date: Today as date object (~BigQuery DATE).
        """

        return date.today()

    def gen_date_ultimo(self) -> date:
        """Generates date ultimate upper (for SAP tables).

        Returns:
            datetime.date: '9999-12-31' as date object (~BigQuery DATE).
        """
        return date.fromisoformat("9999-12-31")

    def gen_date_begin(self) -> date:
        """Generates date begin oldest (for SAP tables).

        Returns:
            datetime.date: '1970-01-01' as date object (~BigQuery DATE).
        """
        return date.fromisoformat("1970-01-01")

    def gen_timestamp(self) -> datetime:
        """Generates now as datetime.

        Returns:
            datetime.datetime: Now as a datetime object (~BigQuery TIMESTAMP)
        """

        return datetime.today()

    def gen_micros_from_epoch(self) -> int:
        """Generates the number of microseconds since epoch.

        Returns:
            int: number of microseconds since epoch.
        """
        now = datetime.now()
        epoch = datetime(1970, 1, 1)
        return int((now - epoch).total_seconds() * 1000000)

    def get_micros_from_epoch(self, timestamp: datetime) -> int:
        """Generates the number of microseconds since epoch.

        Args:
            timestamp (datetime.datetime): A datetime object.

        Returns:
            int: number of microseconds since epoch.
        """

        epoch = datetime(1970, 1, 1)
        return int((timestamp - epoch).total_seconds() * 1000000)

    def gen_time(self) -> datetime:
        return datetime.today().time()

    def date_to_timestamp(self, date_obj: date) -> datetime:
        """Converts a python date object to a python timestamp object.

        Args:
            date_obj (date): A python date object.

        Returns:
            datetime: A python timestamp object
                      with the time part taken from the current time.
        """

        now = datetime.now()
        return datetime(
            date_obj.year,
            date_obj.month,
            date_obj.day,
            now.hour,
            now.minute,
            now.second,
            now.microsecond,
        )
