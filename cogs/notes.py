from discord.ext import commands
import discord

class Notes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_notes = {}        # {user_id: [note1, note2, ...]}
        self.user_done_flags = {}   # {user_id: [False, True, ...]}

    @commands.command(name='addnote')
    async def add_note(self, ctx, *, note: str):
        user_id = str(ctx.author.id)
        self.user_notes.setdefault(user_id, []).append(note)
        self.user_done_flags.setdefault(user_id, []).append(False)

        embed = discord.Embed(
            title="📝 Note Added",
            description=f"`{note}`",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name='notes')
    async def view_notes(self, ctx):
        user_id = str(ctx.author.id)
        notes = self.user_notes.get(user_id, [])
        done_flags = self.user_done_flags.get(user_id, [])

        if not notes:
            await ctx.send("You don’t have any notes yet.")
            return

        # Create formatted list with done status
        desc = ""
        for i, note in enumerate(notes):
            if i < len(done_flags) and done_flags[i]:
                desc += f"{i+1}. ~~{note}~~\n"
            else:
                desc += f"{i+1}. {note}\n"

        embed = discord.Embed(
            title="📒 Your Notes",
            description=desc,
            color=discord.Color.blurple()
        )

        view = CombinedDropdownView(self.user_notes, self.user_done_flags, user_id)
        await ctx.send(embed=embed, view=view)

# COMBINED DROPDOWN VIEW
class CombinedDropdownView(discord.ui.View):
    def __init__(self, notes_dict, done_flags, user_id):
        super().__init__(timeout=None)
        self.notes_dict = notes_dict
        self.done_flags = done_flags
        self.user_id = user_id
        self.add_item(MarkDoneDropdown(notes_dict, done_flags, user_id))
        self.add_item(DeleteNoteDropdown(notes_dict, done_flags, user_id))

# ✅ MARK DONE DROPDOWN
class MarkDoneDropdown(discord.ui.Select):
    def __init__(self, notes_dict, done_flags, user_id):
        self.notes_dict = notes_dict
        self.done_flags = done_flags
        self.user_id = user_id
        options = []

        notes = self.notes_dict.get(user_id, [])
        for i in range(len(notes)):
            options.append(discord.SelectOption(label=f"Note {i+1}", value=str(i)))

        super().__init__(
            placeholder="✅ Mark note as done...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("This isn’t your note!", ephemeral=True)
            return

        index = int(self.values[0])
        try:
            self.done_flags[self.user_id][index] = True
            await interaction.response.send_message(f"✅ Marked Note {index+1} as done!", ephemeral=True)
            await interaction.message.delete()  # Delete old message
        except IndexError:
            await interaction.response.send_message("Invalid note selected.", ephemeral=True)

# 🗑️ DELETE DROPDOWN
class DeleteNoteDropdown(discord.ui.Select):
    def __init__(self, notes_dict, done_flags, user_id):
        self.notes_dict = notes_dict
        self.done_flags = done_flags
        self.user_id = user_id
        options = []

        notes = self.notes_dict.get(user_id, [])
        for i in range(len(notes)):
            options.append(discord.SelectOption(label=f"Note {i+1}", value=str(i)))

        super().__init__(
            placeholder="🗑️ Delete a note...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("This isn’t your note!", ephemeral=True)
            return

        index = int(self.values[0])
        try:
            note = self.notes_dict[self.user_id].pop(index)
            self.done_flags[self.user_id].pop(index)
            await interaction.response.send_message(f"🗑️ Deleted: `{note}`", ephemeral=True)
            await interaction.message.delete()
        except IndexError:
            await interaction.response.send_message("Note already deleted.", ephemeral=True)

# Setup function to load cog
async def setup(bot):
    await bot.add_cog(Notes(bot))
