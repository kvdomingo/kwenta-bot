import string

from discord.ext import commands
from google.oauth2 import service_account
from googleapiclient import discovery
from tabulate import tabulate

from ..config import BASE_DIR, SHEET_ID, TEST_SHEET_ID


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

    @sheet_group.command(aliases=["addgroup"])
    async def add_group(self, ctx: commands.Context, *name: str):
        name = " ".join(name)
        data = [[], [name.upper(), "", "", ""]]
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
        updated_range = updates.get("updatedRange")
        usheet, urange = updated_range.split("!")
        start_range, end_range = urange.split(":")
        requests = [
            {
                "updateCells": {
                    "fields": "userEnteredFormat",
                    "rows": [
                        {
                            "values": [
                                {
                                    "userEnteredFormat": {
                                        "backgroundColor": {"red": 0.5, "green": 0.5, "blue": 0.5},
                                        "textFormat": {"bold": True},
                                    },
                                }
                            ]
                        }
                    ],
                    "range": {
                        "sheetId": TEST_SHEET_ID,
                        "startColumnIndex": string.ascii_uppercase.index(start_range[0]),
                        "startRowIndex": int(start_range[1:]),
                        "endColumnIndex": string.ascii_uppercase.index("D"),
                        "endRowIndex": int(end_range[1:]),
                    },
                },
            },
        ]
        self.sheet.batchUpdate(spreadsheetId=SHEET_ID, body={"requests": requests}).execute()
        await ctx.send(f"Added new group **{name.upper()}**")

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

    @sheet_group.command()
    async def batch(self, ctx: commands.Context, *args: str):
        pass
