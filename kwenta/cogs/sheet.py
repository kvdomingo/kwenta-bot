from discord.ext import commands
from google.oauth2 import service_account
from googleapiclient import discovery
from tabulate import tabulate

from ..config import BASE_DIR, SHEET_ID


class GSheet(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        credentials = service_account.Credentials.from_service_account_file(
            str(BASE_DIR / "credentials.json"), scopes=scopes
        )
        service = discovery.build("sheets", "v4", credentials=credentials)
        self.sheet = service.spreadsheets()

    @commands.group("sheet")
    async def sheet_group(self, ctx: commands.Context):
        pass

    @sheet_group.command()
    async def get(self, ctx: commands.Context):
        result = self.sheet.values().get(spreadsheetId=SHEET_ID, range="Net!A1:D4").execute()
        values = result.get("values", [])
        headers = values.pop(0)
        await ctx.send(
            f"```{tabulate(values, headers=headers)}```\n**Google Sheets link:** <https://docs.google.com/spreadsheets/d/{SHEET_ID}>"
        )

    @sheet_group.command()
    async def add(
        self,
        ctx: commands.Context,
        item: str,
        entity_a_amount: str,
        entity_b_amount: str = None,
        entity_c_amount: str = None,
    ):
        if entity_b_amount is None and entity_c_amount is None:
            entity_c_amount = entity_b_amount = entity_a_amount = f"={entity_a_amount}/3"
        data = [[item, entity_a_amount, entity_b_amount, entity_c_amount]]
        result = (
            self.sheet.values()
            .append(
                spreadsheetId=SHEET_ID,
                valueInputOption="USER_ENTERED",
                body={"values": data},
                range="BOT_TEST!A:D",
            )
            .execute()
        )
        updates = result.get("updates")
        await ctx.send(f"Appended {(updates.get('updatedCells'))} cells across {updates.get('updatedRows')} rows.")
