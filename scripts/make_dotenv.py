from pathlib import Path

from loguru import logger
from mako.template import Template

from .get_secret_string import get_secret_string

BASE_DIR = Path(__file__).parent.parent


def make_dotenv():
    template = Template(filename=str(BASE_DIR / "scripts" / "templates" / ".env.mako"))
    env = template.render(
        DISCORD_TOKEN=get_secret_string("DISCORD_TOKEN"),
        SHEET_ID=get_secret_string("SHEET_ID"),
        ENTITY_IDS=get_secret_string("ENTITY_IDS"),
    )
    with open(BASE_DIR / ".env", "w+") as f:
        f.write(env)
    logger.info(".env ok")

    credentials = get_secret_string("CREDENTIALS_JSON")
    with open(BASE_DIR / "credentials.json", "w+") as f:
        f.write(credentials)
    logger.info("credentials.json ok")


if __name__ == "__main__":
    make_dotenv()
