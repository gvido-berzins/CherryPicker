from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer


def pigmentize(code: str) -> str:
    lexer = guess_lexer(code)
    formatter = HtmlFormatter(style="lovelace")
    result = highlight(code, lexer, formatter)
    return result
