import requests
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Optional, Type

BASE_URL = "https://hacker-news.firebaseio.com/v0"


def fetch_stories_from_hn(limit: int = None):
    url = f"{BASE_URL}/topstories.json"
    story_ids = requests.get(url).json()

    if limit:
        story_ids = story_ids[:limit]

    return story_ids

def fetch_story_info(story_id: int):
    url = f"{BASE_URL}/item/{story_id}.json"
    return requests.get(url).content
    

def get_hnn_stories(limit: int = 5):
    story_ids = fetch_stories_from_hn(limit)
    stories = []
    
    for story_id in story_ids:
        stories.append(fetch_story_info(story_id))
    return stories

#print(fetch_stories_from_hn(limit=5))
#print(get_hnn_stories())

class Stories(BaseModel):
    limit: int = Field(
        default=5,
        description="The limit number of stories to be fetched from Hacker News."
    )

class StoriesTool(BaseTool):
    name = "get_hnn_stories"
    description = "This is acool tool for interacting with HN"

    def _run(self, limit: int = 5):
        stories = get_hnn_stories(limit)
        return stories
    
    args_schema: Optional[Type[BaseModel]] = Stories