from sly import Lexer, Parser


class MathAction:
    def __init__(self, action: str, expr, term):
        self.term = term
        self.expr = expr
        self.action = action


class NovaLexer(Lexer):
    # This is the set of tokens we are exporting to the Parser
    tokens = {NUMBER, ASSING, SOEQ, BOEQ, OR, AND, EQUALITY, COMMA, INEQUALITY, BIGGER, SMALLER,
              IF, ELSE, FOR, WHILE, DEFINE, EVENT, SPRITE,
              STRING, ID}
    # Any literals we want to ignore
    ignore_comment = r'\#.*'
    ignore = " \t"
    ignore_newline = r'\n+'
    literals = {"{", "}", "+", "-", "*", "/", "(", ")"}

    EQUALITY = r'=='
    ASSING = r'='
    INEQUALITY = r'!='
    SOEQ = r"<="
    BOEQ = r">="
    BIGGER = r'>'
    SMALLER = r'<'
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    COMMA = r','
    IF = r"if"
    FOR = r"for"
    WHILE = r"while"
    ELSE = r"ELSE"
    DEFINE = r"@define"
    EVENT = r"@event"
    SPRITE = r"@sprite"

    @_(r"[0-9]+\.[0-9]+", r"0x[0-9a-fA-F]+", r'[0-9]+')
    def NUMBER(self, t):
        t.value = int(t.value[2:], 16) if t.value.startswith('0x') else float(t.value)
        return t

    @_(r'''("[^"\\]*(\\.[^"\\]*)*"|'[^'\\]*(\\.[^'\\]*)*')''')
    def STRING(self, t):
        t.value = self.remove_quotes(t.value)
        return t

    def remove_quotes(self, text: str):
        return text[1:-1] if text.startswith('\"') or text.startswith('\'') else text


