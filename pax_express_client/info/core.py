import os
from rich import print
from rich.markdown import Markdown

source_code_path = os.path.dirname(os.path.abspath(__file__))


def show_readme():
    with open(os.path.join(source_code_path, "../../README.md")) as f:
        markdown_string = f.read()
        print(Markdown(markdown_string))


def show_releasing():
    with open(os.path.join(source_code_path, "../../docs/releasing.md")) as f:
        markdown_string = f.read()
        print(Markdown(markdown_string))
