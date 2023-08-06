import asyncio
import logging
from base64 import b64decode
from functools import partial
from json import dumps, loads
from typing import Optional, Tuple, Type

from aiohttp import ClientResponse, ClientSession

from .error import (
    BadRequestException,
    ForbiddenException,
    InternalServerErrorException,
    NotFoundException,
    TooManyRequestsException,
    UnauthorizedException,
)
from .guild import Guild, Leaderboard, Sort
from .json_encoder import Encoder as JSONEncoder
from .number import Number
from .perms import Permissions
from .user import User

log = logging.getLogger(__name__)

__all__ = ("Client",)


def no_none(d: dict) -> dict:
    return {i: j for i, j in d.items() if j is not None}


def serialize_values(
    d: dict, serialize=dumps, classes: Tuple[Type, ...] = (str, int, float)
) -> dict:
    return {
        i: j if isinstance(j, classes) else serialize(j) for i, j in d.items()
    }


class Client:
    """An UnbelievaBoat API client. The heart of the Pybelieva."""

    _json_serializer = partial(dumps, cls=JSONEncoder)
    _url: str
    _session: ClientSession
    id: int
    wait_on_ratelimits: bool

    def __init__(
        self,
        token: str,
        *,
        base_url: str = "https://unbelievable.pizza/api",
        version: int = 1,
        wait_on_ratelimits: bool = True,
    ):
        self._url = f"{base_url}/v{version}"
        self._session = ClientSession(
            headers={"Authorization": token},
            json_serialize=self._json_serializer,
        )
        self.id = int(loads(b64decode(token.split(".")[1]).decode())["app_id"])
        self.wait_on_ratelimits = wait_on_ratelimits

    async def close(self):
        await self._session.close()

    def oauth_url(self, guild_id: Optional[int] = None) -> str:
        return (
            "https://unbelievaboat.com/applications/authorize"
            f"?app_id={self.id}"
            + (f"&guild_id={guild_id}" if guild_id else "")
        )

    async def __request(
        self, method: str, path: str, *, data: dict = None, query: dict = None
    ):
        resp: ClientResponse = await self._session.request(
            method,
            f"{self._url}{path}",
            json=data,
            params=serialize_values(query, serialize=self._json_serializer)
            if query is not None
            else None,
        )
        log.debug(f"{resp.request_info.method} {resp.url} {data}")
        if resp.status == 400:
            raise BadRequestException()
        if resp.status == 401:
            raise UnauthorizedException()
        if resp.status == 403:
            raise ForbiddenException()
        if resp.status == 404:
            raise NotFoundException()
        if resp.status == 500:
            raise InternalServerErrorException()
        json: dict = await resp.json()
        log.debug(f"{json=}")
        if resp.status == 429:
            retry_after = json.get("retry_after", 1000)
            log.info(f"Ratelimited for {retry_after}ms")
            if not self.wait_on_ratelimits:
                raise TooManyRequestsException(**json)
            await asyncio.sleep(retry_after / 1000)
            return await self.__request(method, path, data=data, query=query)
        return json

    async def get_user_balance(self, guild_id: int, user_id: int) -> User:
        return User.parse_obj(
            await self.__request("GET", f"/guilds/{guild_id}/users/{user_id}")
        )

    async def set_user_balance(
        self,
        guild_id: int,
        user_id: int,
        *,
        cash: Optional[Number] = None,
        bank: Optional[Number] = None,
        reason: Optional[str] = None,
    ) -> User:
        return User.parse_obj(
            await self.__request(
                "PUT",
                f"/guilds/{guild_id}/users/{user_id}",
                data=no_none({"cash": cash, "bank": bank, "reason": reason}),
            )
        )

    async def patch_user_balance(
        self,
        guild_id: int,
        user_id: int,
        cash: Optional[Number] = None,
        bank: Optional[Number] = None,
        reason: Optional[str] = None,
    ) -> User:
        return User.parse_obj(
            await self.__request(
                "PATCH",
                f"/guilds/{guild_id}/users/{user_id}",
                data=no_none({"cash": cash, "bank": bank, "reason": reason}),
            )
        )

    async def get_guild_leaderboard(
        self,
        guild_id: int,
        *,
        sort: Optional[Sort] = None,
        offset: Optional[int] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Leaderboard:
        return Leaderboard.parse_obj(
            await self.__request(
                "GET",
                f"/guilds/{guild_id}/users",
                query=no_none(
                    {
                        "offset": offset,
                        "page": page,
                        "limit": limit,
                        "sort": sort,
                    }
                ),
            )
        )

    async def get_guild(self, guild_id: int) -> Guild:
        return Guild(**await self.__request("GET", f"/guilds/{guild_id}"))

    async def get_permissions(self, guild_id: int) -> Permissions:
        return Permissions(
            (
                await self.__request(
                    "GET", f"/applications/@me/guilds/{guild_id}"
                )
            )["permissions"]
        )
