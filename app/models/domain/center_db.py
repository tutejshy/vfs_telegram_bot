from sqlalchemy import Column, Integer, String

from app.models.domain.base_db import BaseDB


class CenterDB(BaseDB):
    center_id = Column(Integer, primary_key=True, unique=True, index=True)
    route = Column(String(56), index=True)
    code = Column(String(12), index=True)  # isoCode
    name = Column(String(128))             # centerName


# {
# 	"id": 5590,
# 	"masterId": 0,
# 	"centerName": "Lithuania Visa Application Center- Minsk",
# 	"missionCode": "ltu",
# 	"missionName": "Lithuania",
# 	"countryCode": "blr",
# 	"countryName": "Belarus",
# 	"cultureCode": "en-US",
# 	"isoCode": "Mins",
# 	"city": "Minsk",
# 	"contactNumber": null,
# 	"callCenterNumber": "+375 17 388 02 82",
# 	"address": "Bobruiskaya 6, Galileo Shopping mall, 6 th floor (entrance from the bus station)",
# 	"state": null,
# 	"country": "Belarus",
# 	"pincode": "220089",
# 	"email": "info.lithminsk@vfshelpline.com",
# 	"website": "http://www.vfsglobal.com/lithuania/belarus/English/index.html",
# 	"timeZone": "Kaliningrad Standard Time",
# 	"vacType": "VAC",
# 	"operationHours": "9:00 TO 17:00",
# 	"upvFees": 0,
# 	"upvCurrency": "BYN",
# 	"error": null
# }