import os
from typing import Literal

from dotenv import load_dotenv
from perplexity import Perplexity
from pydantic import BaseModel
import requests

load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
perplexity = Perplexity(api_key=PERPLEXITY_API_KEY)


class SearchResponseFormat(BaseModel):
    web_url: str
    image_url: str


class SearchContentResponseFormat(SearchResponseFormat):
    title: str


def search_perplexity(
    query: str,
    model: str = "sonar",
    return_images: bool = True,
    response_format: BaseModel | None = None,
) -> dict:
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": model,
        "media_response": {"enable_media_classifier": return_images},
        "messages": [{"role": "user", "content": query}],
    }
    if response_format:
        data["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "schema": response_format.model_json_schema(),
            },
        }

    try:
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    except Exception as e:
        print(f"Error occurred: {e}")
        return {}


def search_person(name: str) -> SearchResponseFormat:
    query = f"""
    Return a profile image url and a wikipedia url for the person '{name}'.
    If a wikipedia url is not found, return another relevant biographical url or personal website.
    
    Respond in using the format {str(SearchResponseFormat.model_json_schema())}
    """
    completion = search_perplexity(query, response_format=SearchResponseFormat)
    result = SearchResponseFormat.model_validate_json(
        completion["choices"][0]["message"]["content"]
    )
    return result


def search_organisation(name: str) -> SearchResponseFormat:
    query = f"""
    Return a logo image url and a wikipedia url for the organisation '{name}'.
    If a wikipedia url is not found, return another relevant url.
    
    Respond in using the format {str(SearchResponseFormat.model_json_schema())}
    """
    completion = search_perplexity(query, response_format=SearchResponseFormat)
    result = SearchResponseFormat.model_validate_json(
        completion["choices"][0]["message"]["content"]
    )
    return result


def search_twitter(
    text: str,
    author: str | None = None,
    date: str | None = None,
) -> str:
    """Returns a tweet url matching the text and author"""
    return ""


def search_content(
    description: str,
    author: str | None = None,
    content_type: Literal["article", "video", "book", "tweet"] | None = "article",
    content_source: str | None = None,  # e.g., "New York Times", "YouTube", "Twitter" etc.
    date: str | None = None,
) -> SearchContentResponseFormat:
    # TODO: Maybe add search filters based on date
    query = f"""
    Return a source url and for the {content_type or "content"} referencing '{description}'.
    The author is '{author or "unknown"}' and the content date is '{date or "unknown"}'.

    If content_type is 'video', return source url from YouTube.
    If content_type is 'book', return a Goodreads or Amazon url.
    If content_type is 'article', return url from {content_source or "a reputable news site"}.
    If otherwise, return a relevant url.

    Respond in using the format {str(SearchContentResponseFormat.model_json_schema())}
    where title is a headline summary of the content.
    """
    # TODO: https://twitterapi.io/ much cheaper
    # if content_type == "tweet":
    #     return search_twitter(text, author)

    completion = search_perplexity(query, response_format=SearchContentResponseFormat)
    result = SearchContentResponseFormat.model_validate_json(
        completion["choices"][0]["message"]["content"]
    )
    return result


def search_event(
    description: str,
    date: str | None = None,
) -> SearchResponseFormat:
    # TODO: Maybe add search filters based on date
    query = f"""
    Return a source url and for the event referencing '{description}'.
    The content date is '{date or "unknown"}'.

    Respond in using the format {str(SearchResponseFormat.model_json_schema())}
    """
    completion = search_perplexity(query, response_format=SearchResponseFormat)
    result = SearchResponseFormat.model_validate_json(
        completion["choices"][0]["message"]["content"]
    )
    return result
