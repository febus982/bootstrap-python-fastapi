from pathlib import Path

from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory=Path(__file__).parent.joinpath("templates"))
