"""

"""

from __future__ import annotations
import royalnet.royaltyping as t

import royalnet.engineer as engi
import logging
import discord
import datetime

from .royaltyping import MsgChannel

log = logging.getLogger(__name__)


class DiscordUser(engi.User):
    def __init__(self, _user: discord.User):
        self._user: discord.User = _user

    def __hash__(self) -> int:
        return self._user.id

    async def name(self) -> str:
        return f"{self._user.name}#{self._user.discriminator}"

    async def send_message(self, text: str) -> t.Optional[DiscordMessage]:
        _msg = await self._user.send(content=text)
        # TODO: use message class instead of static class
        return DiscordMessage(_msg=_msg)


class DiscordChannel(engi.Channel):
    def __init__(self, _ch: MsgChannel):
        self._ch: MsgChannel = _ch

    def __hash__(self) -> int:
        return self._ch.id

    async def name(self) -> str:
        return self._ch.name

    async def topic(self) -> str:
        return self._ch.topic

    async def users(self, user_class: t.Type[DiscordUser] = DiscordUser) -> t.List[DiscordUser]:
        return [user_class(_user=member) for member in self._ch.members]

    async def send_message(self, text: str) -> t.Optional[DiscordMessage]:
        _msg = await self._ch.send(content=text)
        # TODO: use message class instead of static class
        return DiscordMessage(_msg=_msg)


class DiscordMessage(engi.Message):
    def __init__(self, _msg: discord.Message):
        self._msg: discord.Message = _msg

    def __hash__(self) -> int:
        return self._msg.id

    async def text(self) -> str:
        return self._msg.content

    async def timestamp(self) -> datetime.datetime:
        return self._msg.created_at

    async def reply_to(self) -> engi.Message:
        return self.__class__(_msg=self._msg.reference)

    async def channel(self, channel_class: t.Type[DiscordChannel] = DiscordChannel) -> DiscordChannel:
        return channel_class(_ch=self._msg.channel)

    async def send_reply(self, text: str) -> t.Optional[DiscordMessage]:
        # TODO: when discord.py 1.6 comes out, uncomment this
        # _msg = await self._msg.reply(content=text)
        _msg = await self._msg.channel.send(content=text)
        # TODO: use message class instead of static class
        return DiscordMessage(_msg=_msg)


__all__ = (
    "DiscordUser",
    "DiscordChannel",
    "DiscordMessage",
)
