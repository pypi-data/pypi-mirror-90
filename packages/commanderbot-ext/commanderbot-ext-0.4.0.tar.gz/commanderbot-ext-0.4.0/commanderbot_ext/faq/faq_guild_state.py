from commanderbot_ext.faq.faq_cache import FaqEntry
from commanderbot_ext.faq.faq_options import FaqOptions
from commanderbot_ext.faq.faq_store import FaqStore
from commanderbot_lib.guild_state.abc.cog_guild_state import CogGuildState
from discord import Message
from discord.ext.commands import Context


class FaqGuildState(CogGuildState[FaqOptions, FaqStore]):
    async def list_faqs(self, ctx: Context):
        if entries := await self.store.iter_guild_faqs(self.guild):
            sorted_entries = sorted(entries, key=lambda entry: entry.name)
            faq_names = (entry.name for entry in sorted_entries)
            text = "`" + "` `".join(faq_names) + "`"
            await ctx.send(text)
        else:
            await ctx.send(f"No FAQs available")

    async def show_faq(self, ctx: Context, name: str):
        if entry := await self.store.get_guild_faq(self.guild, name):
            await ctx.send(entry.content)
        else:
            await ctx.send(f"No such FAQ `{name}`")

    async def add_faq(self, ctx: Context, name: str, message: Message):
        if await self.store.get_guild_faq(self.guild, name):
            await ctx.send(f"FAQ `{name}` already exists")
        else:
            faq_entry = FaqEntry(name=name, content=message.content, message_link=message.jump_url)
            await self.store.add_guild_faq(self.guild, faq_entry)
            await ctx.send(f"Added FAQ `{name}`")

    async def remove_faq(self, ctx: Context, name: str):
        if removed_entry := await self.store.remove_guild_faq(self.guild, name):
            await ctx.send(f"Removed FAQ `{removed_entry.name}`")
        else:
            await ctx.send(f"No such FAQ `{name}`")

    # @overrides CogGuildState
    async def on_message(self, message: Message):
        prefix = self.options.prefix
        if prefix:
            content = message.content
            if isinstance(content, str):
                if content.startswith(prefix) and len(content) > len(prefix):
                    ctx = Context(message=message, prefix=prefix)
                    name = content[len(prefix) :]
                    await self.show_faq(ctx, name)
