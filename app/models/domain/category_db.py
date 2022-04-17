from sqlalchemy import Column, Integer, String

from app.models.domain.base_db import BaseDB


class CategoryDB(BaseDB):
    category_id = Column(Integer, primary_key=True, unique=True, index=True)
    parent = Column(String(12))
    route = Column(String(56), index=True)
    name = Column(String(128))                      # name
    code = Column(String(12), index=True)           # code
    mission_code = Column(String(12))               # missionCode
    center = Column(String(12), index=True)         # centerCode


# {
# 	"id": 3070,
# 	"parentId": 0,
# 	"masterId": 0,
# 	"name": "Short-Term VISA Type C",
# 	"missionCode": "ltu",
# 	"centerCode": "Mins",
# 	"code": "3",
# 	"culturecode": "en-US",
# 	"iswaitlist": false,
# 	"isTMIEnabled": false,
# 	"isVLNNumberEnable": false,
# 	"vlnNumberRegex": null,
# 	"vlnNumberLabelFormat": null,
# 	"error": null
# }