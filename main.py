from rich.panel import Panel as panel
from rich.table import Table
from rich.layout import Layout
from rich.console import Console, RenderableType
from rich.console import group
from rich.markdown import Markdown
from requests import get
from textual.app import App
from textual.widgets import ScrollView, Button, ButtonPressed
from textual.widget import Widget
from textual.reactive import Reactive


API_URL = "https://www.tabnews.com.br/api/v1/"
POSTS_PER_PAGE = 30

post_page = Reactive(1)
post_page = 1
open_post = Reactive(1)
open_post = 1

console = Console()
layout = Layout()


def watch_post_page(self, val):
    return False 


def watch_open_post(self, val):
    return False


def get_url(append):
    return API_URL + append


def get_posts(page):
    response = get(
        get_url('contents'),
        params={'per_page': POSTS_PER_PAGE, 'page': page}
    ).json()
    return response


def post_header_layout(post, padding=None):
    if not padding:
        padding = 1

    content = f'[bold]{post["title"]}  [/bold]\n\n\
[#0969da on #333333] {post["username"]} [/#0969da on #333333]\n\n'

    return content


def post_body(post):
    content = Markdown(post["body"])
    return panel(content, border_style="#333344", padding=1)


def shown_post():
    print(post_page)
    return get_posts(post_page)[open_post]


post_shown_header = panel(post_header_layout(shown_post()), padding=(0, 1), border_style="#333344")
post_shown_body = post_body(shown_post())


def set_post(number):
    global open_post
    open_post = number


@group()
def feed_layout(page):
    for post in get_posts(page):
        yield post_header_layout(post)


class Header(Widget, Table):
    def render(self) -> None:
        table = Table.grid(padding=(0, 1), expand=True)
        table.add_column("app", justify="left", ratio=0, width=10)
        table.add_column("creator", justify="right", width=20)
        table.add_row("📁[bold cyan]CliNews", "Criado por Eduardo-moro [finn]")

        header: RenderableType
        header = panel(table, border_style="bold cyan")

        return header


class Feed(Widget):
    def render(self) -> panel:
        return feed_layout(post_page)


class MainLayout(Widget):
    def render(self) -> RenderableType:
        grid = Layout()

        grid.split_row(
            Layout(name="post"),
            Layout(panel(Feed(), border_style="#333344"))
        )

        grid["post"].split_column(
            Layout(post_shown_header, size=6, ratio=1),
            Layout(post_shown_body),
        )

        return(grid)


class CliNews(App):
    async def on_load(self) -> None:
        await self.bind('q', 'quit', 'sair')

    async def on_mount(self) -> None:
        self.body = ScrollView(gutter=1)
        await self.view.dock(Header(), edge="top", size=3)
        await self.view.dock(ScrollView(MainLayout()), edge="left")

CliNews.run(log="textual.log")
