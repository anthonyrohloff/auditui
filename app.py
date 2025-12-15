from engine.walk import list_files
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, DirectoryTree, Log
from textual.containers import Horizontal


class AudiTUI(App):
    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]

    def compose(self) -> ComposeResult:
        with Horizontal():
            yield DirectoryTree("testdir")
            yield Log()

        yield Header()
        yield Footer()


    def on_ready(self) -> None:
        with open("testdir/subdir/file3.txt", "r") as f:
            lines = f.readlines()            

        log = self.query_one(Log)
        log.write_lines(lines)


    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode"""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )


if __name__ == "__main__":
    app = AudiTUI()
    app.run()