"""
.. todo:: Document :mod:`royalnet_discordpy.royaltyping`.
"""

from __future__ import annotations
import royalnet.royaltyping as t

import discord

MsgChannel = t.Union[discord.TextChannel, discord.DMChannel, discord.GroupChannel]

__all__ = (
    "MsgChannel",
)
