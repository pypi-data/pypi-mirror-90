from commanderbot_ext.faq.faq_guild_state import FaqGuildState
from commanderbot_ext.faq.faq_options import FaqOptions
from commanderbot_ext.faq.faq_store import FaqStore
from commanderbot_lib.state.abc.cog_state import CogState
from discord import Message
from discord.ext.commands import Context


class FaqState(CogState[FaqOptions, FaqStore, FaqGuildState]):
    store_class = FaqStore
    guild_state_class = FaqGuildState

    async def list_faqs(self, ctx: Context):
        if guild_state := await self.get_guild_state(ctx.guild):
            await guild_state.list_faqs(ctx)

    async def show_faq(self, ctx: Context, name: str):
        if guild_state := await self.get_guild_state(ctx.guild):
            await guild_state.show_faq(ctx, name)

    async def add_faq(self, ctx: Context, name: str, message: Message):
        if guild_state := await self.get_guild_state(ctx.guild):
            await guild_state.add_faq(ctx, name, message)

    async def remove_faq(self, ctx: Context, name: str):
        if guild_state := await self.get_guild_state(ctx.guild):
            await guild_state.remove_faq(ctx, name)
