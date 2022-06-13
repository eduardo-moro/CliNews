from rich.panel import Panel as panel
from rich.table import Table
from rich.layout import Layout
from rich.console import Console, RenderableType
from rich.console import group
from rich.markdown import Markdown
from requests import get
from textual.app import App
from textual.widgets import ScrollView
from textual.widget import Widget
from textual.reactive import Reactive

API_URL = "https://www.tabnews.com.br/api/v1/"
POSTS_PER_PAGE = 30

post_page = 1
console = Console()
layout = Layout()


def get_url(append):
    return API_URL + append


def get_posts(page):
    response = get(
        get_url('contents'),
        params={'per_page': POSTS_PER_PAGE, 'page': page}
    ).json()
    return response


def post_layout(post, padding=1):
    content = f'[bold]{post["title"]}  [/bold]\n\
[#0969da on #333333] {post["username"]} [/#0969da on #333333]'

    return panel(content, padding=padding, expand=True)


def get_first_post():
    return get_posts(1)[0]


post_shown = post_layout(get_first_post(), padding=1)


@group()
def feed_layout(page):
    for post in get_posts(page):
        yield post_layout(post)


class Header(Widget, Table):
    def render(self) -> None:
        table = Table.grid(padding=(0, 1), expand=True)
        table.add_column("app", justify="left", ratio=0, width=10)
        table.add_column("creator", justify="right", width=20)
        table.add_row("CliNews", "Criado por Eduardo-moro [finn]")

        header: RenderableType
        header = panel(table)


        return table


class Feed(Widget):
    mouse_over = Reactive(False)

    def render(self) -> panel:
        return panel(feed_layout(post_page), border_style=("white" if self.mouse_over else "black"))

    def on_enter(self) -> None:
        self.mouse_over = True

    def on_leave(self) -> None:
        self.mouse_over = False


class CliNews(App):
    async def on_load(self) -> None:
        await self.bind('q', 'quit', 'sair')

    async def on_mount(self) -> None:
        await self.view.dock(Header(), edge="top", size=3)
        grid = await self.view.dock_grid(edge="left")

        grid.add_column(fraction=3, name="post", min_size=60)
        grid.add_column(fraction=1, name="feed")

        grid.add_row(fraction=1, name="main")
        grid.add_row(fraction=2, name="content")

        grid.add_areas(
            post="post, main",
            feed="feed, main"
        )

        grid.place(
            post=ScrollView(post_shown),
            feed=ScrollView(Feed())
        )


CliNews.run(log="textual.log")
