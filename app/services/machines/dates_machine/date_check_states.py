from enum import Enum


class DateCheck(Enum):
    FIND_LOGIN = "find_login"
    LOGIN = "login"
    CENTERS = "centers"
    CATEGORIES = "categories"
    DATES = "dates"
    RELEASE_RESOURCES = "release_resources"
    TERMINATE = "terminate"
