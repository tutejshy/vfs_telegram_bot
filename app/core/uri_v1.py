import datetime
from typing import Optional

from app.core.build_config import BuildConfig


class URIv1:
    __dev_domain: str = "http://localhost:4848/"
    __prod_domain: str = "https://lift-api.vfsglobal.com/"

    @staticmethod
    def domain() -> str:
        if BuildConfig.DEBUG:
            return f"{URIv1.__dev_domain}api/v1/demo/"
        return URIv1.__prod_domain

    @staticmethod
    def centers(to: str) -> str:
        # "https://lift-api.vfsglobal.com/master/center/ltu/blr"
        return f"{URIv1.domain()}master/center/{to}/blr"

    @staticmethod
    def categories(to: str, center: str, parent_category: Optional[str] = None) -> str:
        if parent_category:
            # "https://lift-api.vfsglobal.com/master/subvisacategory/ltu/blr/Mins/2"
            return f"{URIv1.domain()}master/subvisacategory/{to}/blr/{center}/{parent_category}"
        # "https://lift-api.vfsglobal.com/master/visacategory/ltu/blr/Mins"
        return f"{URIv1.domain()}master/visacategory/{to}/blr/{center}"

    @staticmethod
    def login() -> str:
        return f"{URIv1.domain()}user/login"

    @staticmethod
    def slots(login_email: str, mission_code: str, center_code: str, visa_code: str) -> str:
        days = 180
        date_from = datetime.datetime.now() + datetime.timedelta(days=1)
        date_to = date_from + datetime.timedelta(days=days)
        # https://lift-api.vfsglobal.com/appointment/slots
        return f"{URIv1.domain()}appointment/slots?" \
               f"countryCode=blr&missionCode={mission_code}&" \
               f"centerCode={center_code}&" \
               f"loginUser={login_email}&" \
               f"visaCategoryCode={visa_code}&" \
               f"languageCode=en-US&" \
               f"applicantsCount=1&" \
               f"days={days}&" \
               f"fromDate={date_from.strftime('%d/%m/%Y')}&" \
               f"slotType=2&" \
               f"toDate={date_to.strftime('%d/%m/%Y')}"
