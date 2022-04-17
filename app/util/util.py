import base64
import csv
import os
import re
import traceback
from random import randrange
from time import sleep
from typing import Optional, Any, List, Dict

from requests import Response

from app.core.build_config import BuildConfig
from app.models.schema.action_schema import ActionCreate
from app.models.schema.category_schema import Category
from app.models.schema.center_schema import Center
from app.models.schema.login_schema import LoginMerge, Login
from app.models.schema.post_schema import Post


def csv_to_logins(logins: List[List[str]]) -> List[LoginMerge]:
    LOGIN, PWD, TO, ROUTE = 0, 1, 2, 3
    return [LoginMerge(login=row[LOGIN],
                       pwd=row[PWD],
                       to=row[TO],
                       route=row[ROUTE]) for row in logins]


def read_encoded_csv(encoded_data: str) -> List[LoginMerge]:
    data = base64.b64decode(encoded_data).decode("UTF-8")
    lines = data.splitlines() if data else None

    csvreader = csv.reader(lines or [])
    rows = list(csvreader or [])

    if rows and rows[0][0] == "login":
        del rows[0]

    return csv_to_logins(rows or [])


def delete_file(filepath: str):
    if os.path.exists(filepath):
        os.remove(filepath)


def read_csv(path: str) -> List[LoginMerge]:
    if not os.path.exists(path):
        return []

    with open(path) as f:
        csvreader = csv.reader(f)
        # rows = [row for row in csvreader]
        rows = list(csvreader or [])

    if rows and rows[0][0] == "login":
        del rows[0]

    delete_file(path)

    return csv_to_logins(rows or [])


def call_stack() -> Optional[str]:
    log = ''
    for line in traceback.format_stack():
        log.join(re.sub(r'File ".*[\\/]([^\\/]+.py)"', r'File "\1"', line.strip()))
    return log


#
# center_name: str
# visa_type1:
#     date1 - slots
#     date2 - slots
# visa_type2:
#     date1 - slots
#     date2 - slots
#
# {'Poland Visa Application Center-Pinsk': {'National D-visa': {'03/03/2022': 3}, 'D-work': {'03/03/2022': 1}}}
def change_order_data(stored: Dict[str, Dict[str, Dict[str, int]]]) -> Dict[str, Dict[str, Dict[str, int]]]:
    data = {}
    for center, date_dict in stored.items():
        group = data.get(center)
        if not group:
            data[center] = group = {}

        for date, category_dict in date_dict.items():
            for category, slots in category_dict.items():
                visa_category = group.get(category)
                if not visa_category:
                    group[category] = visa_category = {}
                date_slot = visa_category.get(date)
                if not date_slot:
                    visa_category[date] = 0
                visa_category[date] += slots

    return data


#  center name
#    date1
#      visa1
#        count
#      visa2
#        count
#
# {'Poland Visa Application Center-Pinsk': {'03/03/2022': {'National D-visa': 3}}}
def parse_dates(data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Dict[str, int]]]:
    def safe_list(na: Optional[Any]) -> List[Dict[str, Any]]:
        return na if isinstance(na, List) else []

    def parse_category_slots(counters: List[Dict[str, Any]]) -> Any:
        categories = {}
        for counter in counters:
            for group in safe_list(counter.get("groups")):
                category_name = group.get("visaGroupName")
                slots = categories.get(category_name)
                if not slots:
                    categories[category_name] = 0
                categories[category_name] += len(safe_list(group.get("timeSlots")))
        return categories

    centers = {}
    for item in data:
        center_name, date = item.get("center"), item.get("date")
        if not center_name and not date:
            continue

        center = centers.get(center_name)
        if not center:
            centers[center_name] = center = {}
        center[date] = parse_category_slots(safe_list(item.get("counters")))

    return change_order_data(centers)


def parse_centers(data: List[Dict[str, Any]]) -> List[Center]:
    return [Center(name=r.get("centerName"), code=r.get("isoCode")) for r in data]


def parse_categories(data: List[Dict[str, Any]], parent: Optional[str] = None) -> List[Category]:
    rows = []
    for r in data:
        center, name, code, mission_code = r.get("centerCode"), r.get("name"), r.get("code"), r.get("missionCode")
        if name and code and mission_code and center:
            rows.append(Category(name=name, code=code, mission_code=mission_code, center=center, parent=parent))
    return rows


def dates_to_formatted_message(data: Dict[str, Dict[str, Dict[str, int]]]) -> str:
    message = ''
    for center_name, category in data.items():
        message += f"<b>{center_name}</b>\n"
        for visa_name, date_slot in category.items():
            message += f"{visa_name}\n"
            all_dates = sorted(date_slot.keys())
            for date in all_dates:
                message += f"<b>{date}</b> - <b>{date_slot[date]}</b> <i>time(s) slot(s)</i>\n\n"

    return message


def make_action(response: Response, login_id: Optional[int] = None) -> ActionCreate:
    return ActionCreate(login_id=login_id,
                        url=response.request.url,
                        client_headers=str(response.request.headers),
                        server_headers=str(response.headers),
                        response=response.text,
                        http_code=response.status_code)


def make_message_from_posts(posts: List[Post]) -> str:
    return ''.join([post.message for post in posts])


def make_client_headers(login: Login, use_auth: bool = False):
    headers = {
        # "Accept": "application/json, text/plain, */*",
        # "user-agent": login.agent,
        "route": login.route
    }
    if use_auth and login.token:
        headers["authorization"] = login.token
    return headers


def sleep_exec():
    if not BuildConfig.DEBUG:
        sleep(randrange(5, 15))
