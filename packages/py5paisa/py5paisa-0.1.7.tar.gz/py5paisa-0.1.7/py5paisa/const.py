"""
Contains reusable payloads across requests
"""
from .conf import APP_NAME, USER_ID, PASSWORD, USER_KEY
import datetime

HEADERS = {'Content-Type': 'application/json'}

GENERIC_PAYLOAD = {
    "head": {
        "appName": APP_NAME,
        "appVer": "1.0",
        "key": USER_KEY,
        "osName": "WEB",
        "requestCode": "",
        "userId": USER_ID,
        "password": PASSWORD
    },
    "body": {
        "ClientCode": ""
    }
}

LOGIN_PAYLOAD = {"head": {
    "appName": APP_NAME,
    "appVer": "1.0",
    "key": USER_KEY,
    "osName": "WEB",
    "requestCode": "5PLoginV2",
    "userId": USER_ID,
    "password": PASSWORD
},
    "body":
    {
    "Email_id": "",
    "Password": "",
    "LocalIP": "",
    "PublicIP": "",
    "HDSerailNumber": "",
    "MACAddress": "",
    "MachineID": "039377",
    "VersionNo": "1.7",
    "RequestNo": "1",
    "My2PIN": "",
    "ConnectionType": "1"
}
}

TODAY_TIMESTAMP = int(datetime.datetime.today().timestamp())
NEXT_DAY_TIMESTAMP = int(
    (datetime.datetime.today()+datetime.timedelta(days=1)).timestamp())
