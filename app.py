from textual.app import App, ComposeResult, on
from textual.widgets import Header, Footer, DirectoryTree, Log
from textual.containers import Horizontal


class AudiTUI(App):
    CSS = """
    #tree.hidden {
        display: none;
    }
    """

    BINDINGS = [
        ("d", "toggle_dark", "Toggle Dark Mode"),
        ("e", "toggle_tree", "Toggle Directory Tree"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal():
            yield DirectoryTree("testdir", id="tree")
            yield Log(id="log")

        yield Footer()

    @on(DirectoryTree.FileSelected)
    def file_selected(self, event: DirectoryTree.FileSelected) -> None:
        log = self.query_one("#log", Log)
        log.clear()

        try:
            log.write(event.path.read_text())
        except Exception as e:
            log.write(f"Error reading file: {e}")

    def action_toggle_dark(self) -> None:
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"

    def action_toggle_tree(self) -> None:
        tree = self.query_one("#tree", DirectoryTree)
        tree.toggle_class("hidden")


if __name__ == "__main__":
    AudiTUI().run()
