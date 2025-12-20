from textual.app import App, ComposeResult, on
from textual.widgets import Header, Footer, DirectoryTree, Log
from textual.containers import Horizontal, Vertical
from typing import Iterable
from pathlib import Path
import json


from detect.ssn import find_ssns


class FilteredDirectoryTree(DirectoryTree):
    def __init__(self, *args, allowed_extensions: set[str] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_extensions = ({ext.lower() for ext in allowed_extensions} if allowed_extensions is not None else None)
        self.ssns = {}
        self.match_id = 0

    def filter_paths(self, paths: Iterable[Path]) -> Iterable[Path]:
        for path in paths:
            # Return all dirs
            # TODO: Stop returning dir if no files/subdirs have violations
            if path.is_dir():
                yield path
                continue

            # Filter out files with bad extensions
            if self.allowed_extensions is not None and path.suffix.lower() not in self.allowed_extensions:
                continue

            # Try to read text from the file
            try:
                text = path.read_text(errors="ignore")
            except Exception:
                continue
 
            # Find files with violations
            new_ssns, self.match_id = find_ssns(text, self.match_id, path)
            if new_ssns:
                self.ssns.update(new_ssns)
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
            with Vertical():
                yield Log(id="log")
                yield Log(id="match_info_log")
            

        yield Footer()

    @on(FilteredDirectoryTree.FileSelected)
    def file_selected(self, event: FilteredDirectoryTree.FileSelected) -> None:
        log = self.query_one("#log", Log)
        log.clear()
        match_info_log = self.query_one("#match_info_log", Log)
        match_info_log.clear()
        
        tree = self.query_one("#tree", FilteredDirectoryTree)
        try:
            log.write(event.path.read_text())
            matches_for_file = {
                k: v
                for k, v in tree.ssns.items()
                if v["path"] == str(event.path)
            }
                
            match_info_log.write(json.dumps(matches_for_file, indent=2))
        except Exception as e:
            log.write(f"Error reading file: {e}")
            match_info_log.write(f"Error getting match information: {e}")

    def action_toggle_dark(self) -> None:
        self.theme = "textual-dark" if self.theme == "textual-light" else "textual-light"

    def action_toggle_tree(self) -> None:
        tree = self.query_one("#tree", FilteredDirectoryTree)
        tree.toggle_class("hidden")


if __name__ == "__main__":
    AudiTUI().run()
