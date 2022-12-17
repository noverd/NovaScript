from lexer import NovaLexer
from parser import NovaParser
if __name__ == '__main__':
    lexer = NovaLexer()
    parser = NovaParser()
    input_str = """
# ПЛанируем ситаксис
@sprite Sprite { # New Sprite
    @event on_key_pressed("X") { # On key pressed "X"
        x = 10+5*10 # Set var x to 1
    }
}"""
    tokens = lexer.tokenize(input_str)
    parsed = parser.parse(tokens)
    print(parsed)

