import discord
import asyncio


class EPages(Exception):
    pass


class Pages:
    def __init__(
            self,
            ctx,
            bot,
            member: discord.Member,
            embeds: list = None,
            mode: str = "default",
            reaction_backward: str = "◀",
            reaction_forward: str = "▶"
        ):
        self.ctx = ctx
        self.bot = bot
        self.member = member
        self.embeds = embeds
        self.mode = mode
        self.bReacrion = reaction_backward
        self.fReaction = reaction_forward

        self.message = discord.Message

        self.reactions = [self.bReacrion, self.fReaction]
        self.index = 0

        if embeds is None:
            raise EPages("not found embeds")

    async def runPages(self):
        if self.mode == "default":
            await self.edit_embeds()
            self.message = await self.ctx.send(embed=self.embeds[0])
            await self.addReactions()

            while True:
                print(4)
                reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == self.member and reaction.message.id == self.message.id and reaction.emoji in self.reactions)
                print(5)
                print(str(reaction.emoji))
                if str(reaction.emoji) == "◀":
                    print(7)
                    await self.previousPage()
                    print(8)
                    await self.message.remove_reaction("◀", self.member)
                    print(9)
                elif str(reaction.emoji) == "▶":
                    print(10)
                    await self.nextPage()
                    print(11)
                    await self.message.remove_reaction("▶", self.member)
                    print(12)

    async def previousPage(self):
        if self.index != 0:
            self.index -= 1
            await self.message.edit(embed=self.embeds[self.index])
        elif self.index == 0:
            self.index = len(self.embeds) - 1
            await self.message.edit(embed=self.embeds[self.index])

    async def nextPage(self):
        if self.index != len(self.embeds) - 1:
            self.index += 1
            await self.message.edit(embed=self.embeds[self.index])
        else:
            self.index = 0
            await self.message.edit(embed=self.embeds[self.index])

    async def addReactions(self):
        if self.mode == "default":
            for reaction in self.reactions:
                await self.message.add_reaction(reaction)

    async def edit_embeds(self):
        new_embeds = []
        for embed in self.embeds:
            embed.set_footer(text=f'Страница {self.index + 1} из {len(self.embeds)}')
            new_embeds.append(embed)
            self.index += 1
        self.embeds = new_embeds
        self.index = 0
