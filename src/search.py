import os
from typing import Literal

from dotenv import load_dotenv
from perplexity import Perplexity
from pydantic import BaseModel, Field
import requests

from src.utils import is_valid_url

load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
perplexity = Perplexity(api_key=PERPLEXITY_API_KEY)


class SearchResponseFormat(BaseModel):
    web_url: str
    image_url: str


class SearchContentResponseFormat(SearchResponseFormat):
    headline: str = Field(default="Brief headline summary of the content")


class SearchBookResponseFormat(SearchResponseFormat):
    title: str


class SearchItemResponseFormat(SearchResponseFormat):
    name: str


class SearchVideoResponseFormat(SearchResponseFormat):
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
        print(response.json())
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
    result.image_url = result.image_url if is_valid_url(result.image_url) else ""
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
    result.web_url = result.web_url if is_valid_url(result.web_url) else ""
    result.image_url = result.image_url if is_valid_url(result.image_url) else ""
    return result


def search_twitter(
    text: str,
    author: str | None = None,
    date: str | None = None,
) -> str:
    """Returns a tweet url matching the text and author"""
    return ""


def search_book(title: str, author: str | None = None) -> SearchBookResponseFormat:
    query = f"""
    Return a source url and image url for the book '{title}'.
    The author is '{author or "unknown"}'.
    Return a Goodreads or Amazon url if available, otherwise return another relevant url.

    Respond in using the format {str(SearchBookResponseFormat.model_json_schema())}
    """
    completion = search_perplexity(query, response_format=SearchBookResponseFormat)
    result = SearchBookResponseFormat.model_validate_json(
        completion["choices"][0]["message"]["content"]
    )
    result.web_url = result.web_url if is_valid_url(result.web_url) else ""
    result.image_url = result.image_url if is_valid_url(result.image_url) else ""
    return result


def search_item(
    name: str,
    content_source: str | None = None,
) -> SearchItemResponseFormat:
    query = f"""
    Return a source url and image url for the item '{name}'.
    If content_type is 'item', return url from {content_source or "a reputable e-commerce site"}.
    The content source is '{content_source or "unknown"}'.

    Respond in using the format {str(SearchItemResponseFormat.model_json_schema())}
    """
    completion = search_perplexity(query, response_format=SearchItemResponseFormat)
    result = SearchItemResponseFormat.model_validate_json(
        completion["choices"][0]["message"]["content"]
    )
    result.web_url = result.web_url if is_valid_url(result.web_url) else ""
    result.image_url = result.image_url if is_valid_url(result.image_url) else ""
    return result


def search_video(
    description: str,
) -> SearchVideoResponseFormat:
    query = f"""
    Return a source url and image url for the video referencing '{description}'.
    Return a YouTube url if available, otherwise return another relevant url.
    For the image url, return a thumbnail or relevant image if available.
    Return title of the video as well.

    Respond in using the format {str(SearchVideoResponseFormat.model_json_schema())}
    """
    completion = search_perplexity(query, response_format=SearchVideoResponseFormat)
    result = SearchVideoResponseFormat.model_validate_json(
        completion["choices"][0]["message"]["content"]
    )
    result.web_url = result.web_url if is_valid_url(result.web_url) else ""
    result.image_url = result.image_url if is_valid_url(result.image_url) else ""
    return result


def search_content(
    description: str,
    content_source: (
        str | None
    ) = None,  # e.g., "New York Times", "YouTube", "Twitter", "Amazon" etc.
    date: str | None = None,
) -> SearchContentResponseFormat:
    # TODO: Maybe add search filters based on date
    query = f"""
    Return a source url and image url for the "content" referencing '{description}'.
    
    If content is 'article', return url from {content_source or "a reputable news site"}.
    If otherwise, return a relevant url.

    Respond in using the format {str(SearchContentResponseFormat.model_json_schema())}
    where title is a headline summary of the content.
    """
    completion = search_perplexity(query, response_format=SearchContentResponseFormat)
    result = SearchContentResponseFormat.model_validate_json(
        completion["choices"][0]["message"]["content"]
    )
    result.image_url = result.image_url if is_valid_url(result.image_url) else ""
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
    result.image_url = result.image_url if is_valid_url(result.image_url) else ""
    return result
