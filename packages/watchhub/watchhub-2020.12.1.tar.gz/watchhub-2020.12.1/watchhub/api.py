# -*- coding: utf-8 -*-
""" API client for WatchHub """

import asyncio

import aiohttp

_BASE_URL = "https://watchhub.strem.io/stream"

_MOVIE_URL = _BASE_URL + "/movie/{imdb_id}.json"

_TV_SERIES_URL = _BASE_URL + "/series/{imdb_id}%3A{season}%3A{episode}.json"


async def lookup(imdb_id: str):
    """Looks up a tv series and movie streams for an imdb_id"""
    results = await asyncio.gather(*[lookup_movie(imdb_id), lookup_tv_series(imdb_id)])
    return {**results[0], **results[1]}


async def lookup_movie(imdb_id: str):
    """Looks up movie streams for an imdb id"""
    return await _fetch(_MOVIE_URL.format(imdb_id=imdb_id))


async def lookup_tv_series(imdb_id: str, episode: int = 1, season: int = 1):
    """Looks up tv series streams for an imdb id"""
    return await _fetch(
        _TV_SERIES_URL.format(imdb_id=imdb_id, episode=episode, season=season)
    )


async def _fetch(url):
    """Fetches the provided URL"""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await _response_formatter(response)


async def _response_formatter(response):
    """Formats the watchhub response as a dict"""
    response_json = await response.json()
    formatted_response = {}
    streams = response_json.get("streams")
    if streams:
        for stream in streams:
            formatted_response[
                stream.get("name").lower().replace(" ", "_")
            ] = stream.get("externalUrl")
    return formatted_response
