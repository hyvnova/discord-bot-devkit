from os import link
import random
from typing import List
from googleapiclient.discovery import build


api_key = "AIzaSyDLEnbj_EZvfsB0vDJSFsMyIyl-_YYzA3E"
cse_id = "479d1ec0c40f1453f"


def search_image(query: str, num=1, file_type=".jpg") -> List[str]:
    """Returns a list of images links"""

    service = build("customsearch", "v1", developerKey=api_key)
    res = (
        service.cse()
        .list(q=query, cx=cse_id, num=10, searchType="image", fileType=file_type)
        .execute()
    )

    links = []
    for item in res.get("items", []):
        link = item.get("link")

        if link and (file_type == ".any" or link.endswith(file_type)) and len(links) < num:
            links.append(link)

    return links

