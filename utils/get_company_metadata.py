import json
from sys import argv
from typing import Final
from urllib import request


clearbit_api_key: Final = "sk_d2fa9136230150546c4159c43f749a66"


def get_company_meta(domain):
    req = request.Request(
        url=f"https://company-stream.clearbit.com/v2/companies/find?domain={domain}"
    )
    req.add_header("Authorization", f"Bearer {clearbit_api_key}")
    print(req.headers)
    res = request.urlopen(req).read().decode()

    return json.loads(res)
