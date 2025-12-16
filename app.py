from textual.app import App, ComposeResult, on
from textual.widgets import Header, Footer, DirectoryTree, Log
from textual.containers import Horizontal
from typing import Iterable
from pathlib import Path

class FilteredDirectoryTree(DirectoryTree):
    def __init__(self, *args, allowed_extensions: set[str] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_extensions = ({ext.lower() for ext in allowed_extensions} if allowed_extensions is not None else None)

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        for path in paths:
            if path.is_dir():
                yield path
            elif self.allowed_extensions is None:
                yield path
            elif path.suffix.lower() in self.allowed_extensions:
                yield path

class AudiTUI(App):
    CSS = """
    #tree.hidden {
        display: none;
    }

    #tree {
        width: 30;
        max-width: 40;
    }
    """

    BINDINGS = [
        ("d", "toggle_dark", "Toggle Dark Mode"),
        ("e", "toggle_tree", "Toggle Directory Tree"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()

        with Horizontal():
            yield FilteredDirectoryTree("testdir", id="tree", allowed_extensions={".txt"})
            yield Log(id="log")

        yield Footer()

    @on(FilteredDirectoryTree.FileSelected)
    def file_selected(self, event: FilteredDirectoryTree.FileSelected) -> None:
        log = self.query_one("#log", Log)
        log.clear()

        try:
            log.write(event.path.read_text())
        except Exception as e:
            log.write(f"Error reading file: {e}")

    def action_toggle_dark(self) -> None:
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"

    def action_toggle_tree(self) -> None:
        tree = self.query_one("#tree", FilteredDirectoryTree)
        tree.toggle_class("hidden")


if __name__ == "__main__":
    AudiTUI().run()
