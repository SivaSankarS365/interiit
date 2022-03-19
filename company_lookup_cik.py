from distutils.log import debug
import json
from pprint import pprint
from sys import argv
from re import sub
from typing import Final
from urllib import request

permid_api_key: Final = "Tn0sHMWzlK3kqFlbUqdGNMvnVwsexgOZ"


def get_data_via_cik(cik):
    url = json.loads(
        (
            request.urlopen(
                f"https://api-eit.refinitiv.com/permid/search?q=cik:{cik:0>10}&access-token={permid_api_key}&entityType=organization"
            )
            .read()
            .decode()
        )
    )["result"]["organizations"]["entities"][0].get("hasURL", "")
    return url


def search_company_via_cik(cik):
    result = json.loads(
        request.urlopen(
            "https://efts.sec.gov/LATEST/search-index",
            data=json.dumps({"keysTyped": cik, "narrow": True}).encode(),
        )
        .read()
        .decode()
    )["hits"]["hits"][0]

    if not result:
        return {}

    url = get_data_via_cik(result["_id"])
    return {
        "cik": result["_id"],
        "ticker": result.get("_source", {}).get("tickers", ""),
        "name": sub(r" \([A-Z]+\)", "", result["_source"]["entity_words"]),
        "url": url,
        "logo": f"https://logo.clearbit.com/{url}",
    }


results = search_company_via_cik(argv[1])
pprint(results)
