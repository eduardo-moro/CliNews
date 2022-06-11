from rich import pretty, print as rprint
from rich.panel import Panel as panel
from rich.layout import Layout
from rich.console import Console
from rich.live import Live
from rich.console import group, Group
from rich.text import Text
from requests import get
from time import sleep

import json

API_URL = "https://www.tabnews.com.br/api/v1/"
POSTS_PER_PAGE = 4

if __name__ == "__main__":    
    
    post_page = 1
    console = Console()
    layout = Layout()

    def get_url(append):
        return API_URL + append

    def get_posts(page):
        response = get(get_url('contents'), params={'per_page': POSTS_PER_PAGE, 'page': page}).json()
        return response
    
    def post_layout(post, padding=0, limit=180): 
        body = post["body"][:limit]
        content = f'[bold]{post["title"]}  [/bold]\n[#0969da on #333333] {post["username"]} [/#0969da on #333333]\n\n{body}'
        
        return panel(content, padding=padding)

    def get_first_post():
        return get_posts(1)[0]

    post_shown = post_layout(get_first_post(), padding=1, limit=None)

    @group()
    def feed_layout(page):
        for post in get_posts(page):
            yield post_layout(post)

    layout.split(
        Layout(name="header", size=2),
        Layout(name="body", ratio=1)
    )

    layout["header"].split(
        Layout(Text('TabNews CLI', style="bold")),
        Layout(Text('Criado por Eduardo-moro [finn]', style="bold cyan", justify="right")),
        splitter="row"
    )

    layout["body"].split(
        Layout(post_shown,name="post", ratio=2),
        Layout(feed_layout(post_page),name="feed"),
        splitter="row"
    )

    with Live(layout, screen=True):
        while True:
            sleep(0)      
