import json
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from avri.endpoints import BASE_URL, CALENDAR, FETCH_ADDRESS

import requests
from functional import seq
from requests.exceptions import SSLError

CACHE_LIMIT_DAYS = 6
AVRI_COMPANY_CODE = "78cd4156-394b-413d-8936-d407e334559a"


@dataclass(frozen=True)
class Garbage:
    name: str
    day: datetime


@dataclass(frozen=True)
class Cache:
    data: List[Garbage]
    date: datetime


class AvriException(Exception):
    pass


class Avri:
    def __init__(
        self,
        postal_code: str,
        house_nr: int,
    ):
        self.postal_code = self.clean_postal_code(postal_code)
        self.house_nr = house_nr

        self._cache: Optional[Cache] = None

    @staticmethod
    def clean_postal_code(pc: str):
        return pc.replace(" ", "")

    def __should_recache(self):
        return not self._cache or (datetime.now() - self._cache.date).days > CACHE_LIMIT_DAYS

    def get_address_id(self) -> str:
        payload = {
            "postCode": self.postal_code,
            "houseNumber": self.house_nr,
            "companyCode": AVRI_COMPANY_CODE,
        }
        data = self._perform_request(FETCH_ADDRESS, payload)
        self._validate_response(data)
        return data["dataList"][0]["UniqueId"]

    def _validate_response(self, response):
        if not response["dataList"]:
            raise AvriException(f"No data found for {self.postal_code} {self.house_nr}")

    def get_pickup_dates(self):
        if self.__should_recache():
            address_id = self.get_address_id()
            payload = {
                "companyCode": AVRI_COMPANY_CODE,
                "startDate": str(datetime.now().date()),
                "endDate": "2100-01-01",
                "community": "Zaltbommel",
                "uniqueAddressID": address_id,
            }
            data = self._perform_request(CALENDAR, payload)
            self._validate_response(data)
            parsed_content = self._parse_content(data)
            self._cache = Cache(parsed_content, datetime.now())
        return self._cache.data

    def _perform_request(self, service: str, payload: dict, verify=True) -> dict:
        try:
            content = requests.post(f"{BASE_URL}{service}", data=payload, verify=verify).content
        except SSLError as e:
            if verify:
                return self._perform_request(service, payload, verify=False)
            raise AvriException("Something went wrong contacting the Avri API") from e
        except Exception as e:
            raise AvriException("Something went wrong contacting the Avri API") from e
        else:
            return json.loads(content)

    @staticmethod
    def _parse_content(content: dict) -> List[Garbage]:
        def parse_date(date: str) -> datetime:
            return datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")

        parsed = (
            seq(content["dataList"]).flat_map(
                lambda t: [Garbage(t["_pickupTypeText"], parse_date(d)) for d in t["pickupDates"]]
            )
        ).to_list()

        return parsed

    @staticmethod
    def _today_midnight():
        return datetime.combine(datetime.now(), datetime.min.time())

    def upcoming(self, dt: datetime = None):
        if not dt:
            dt = self._today_midnight()
        data = self.get_pickup_dates()
        return seq(data).filter(lambda g: g.day >= dt).sorted(lambda g: g.day).first()

    def upcoming_of_each(self, dt: datetime = None):
        if not dt:
            dt = self._today_midnight()
        data = self.get_pickup_dates()
        return (
            seq(data)
            .filter(lambda g: g.day >= dt)
            .sorted(lambda g: g.day)
            .map(lambda g: (g.name, g.day))
            .reduce_by_key(lambda x, y: min(x, y))
            .map(lambda arg: Garbage(*arg))
            .list()
        )

    def all_upcoming(self):
        data = self.get_pickup_dates()
        return seq(data).filter(lambda g: g.day >= datetime.now()).sorted(lambda g: g.day).list()
