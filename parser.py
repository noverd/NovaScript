from lexer import NovaLexer
from sly import Parser


class NovaParser(Parser):
    tokens = NovaLexer.tokens
    literals = NovaLexer.literals
    precedence = (
        ('left', "+", "-"),
        ('left', "*", "/"),
    )

    @_("ID")
    def expr(self, p):
        return ["ID", p.ID]

    @_("STRING")
    def expr(self, p):
        return p.STRING

    @_("NUMBER")
    def expr(self, p):
        return p.NUMBER

    @_(
        "expr EQUALITY expr",
        "expr INEQUALITY expr",
        "expr SOEQ expr",
        "expr BOEQ expr",
        "expr '+' expr",
        "expr '-' expr",
        "expr '*' expr",
        "expr '/' expr",
        "expr SMALLER expr",
        "expr BIGGER expr",
        "expr AND expr",
        "expr OR expr"
    )
    def expr(self, p):
        return [p[1], p.expr0, p.expr1]

    @_("ID ASSING expr")
    def expr(self, p):
        return ["vardec", p.ID, p.expr]

    @_('ID "(" expr ")"', 'ID "(" ")"')
    def expr(self, p):
        try:
            return ["call", p.ID, p.expr]
        except Exception:
            return ["call", p.ID, []]

    @_('SPRITE ID "{" expr "}"')
    def expr(self, p):
        return ["sprite", p.ID, p.expr]

    @_(
        'IF "(" expr ")" "{" expr "}" ELSE "{" expr "}" ',
        'IF "(" expr ")" "{" expr "}"',
    )
    def expr(self, p):
        return ["if", p.expr0, p.expr1, p.expr2 or []]

    @_('FOR "(" ID ";" expr ";" expr ")" "{" expr "}"')
    def expr(self, p):
        return ["for", p.ID, p.expr0, p.expr1, p.expr2]

    @_('EVENT ID "(" args ")" "{" expr "}"',
       'EVENT ID "(" ")" "{" expr "}"')
    def expr(self, p):
        try:
            return ["event_func", p.ID, p.args, p.expr]
        except Exception:
            return ["event_func", p.ID, [], p.expr]

    @_('DEFINE ID "(" args ")" "{" expr "}"',
       'DEFINE ID "(" ")" "{" expr "}"')
    def expr(self, p):
        try:
            return ["func", p.ID, p.args or [], p.expr]
        except Exception:
            return ["func", p.ID, [], p.expr]

    @_("args COMMA expr")
    def args(self, p):
        return p.args.append(p.expr)

    @_("expr COMMA expr")
    def args(self, p):
        return [p.expr0, p.expr1]

    @_("expr")
    def args(self, p):
        return [p.expr]
