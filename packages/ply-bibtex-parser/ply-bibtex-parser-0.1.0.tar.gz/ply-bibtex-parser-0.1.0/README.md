# ply-bibtex-parser

A simple ply-based parser for BibTeX

[ply](https://www.dabeaz.com/ply/) is an easy-to-use, pure-Python parser generator. However
it's not the most modern or performant tool.

This is mostly an academic exercise into writing a simple parser, but I used it in my personal website in order to parse
a `.bib` file to identify the different citations and write them back after reformatting
them.

## Install

```
pip install ply-bibtex-parser
```

## Usage

### Parsing

The main entry point is through `parser`:

```python
from ply_bibtex_parser import parser
input = '@article{citekey, author={Smith, Micah J.}, title={Foo bar}}'
parser.parse(input)
# [BibtexEntry(type='article', key='citekey', fields={'author': '{Smith, Micah J.}', 'title': '{Foo bar}'})]
```

The parser produces a possibly-empty list of `BibtexEntry` objects. Note that values in
the entry which are usually delimited with braces contain the braces: this makes it easy to
write back the bibtex entry without trying to escape its contents. The caller is responsible
for further parsing the values if they intend to use the string after escaping is performed.

### Lexing

You can also use the `lexer` directly:

```python
from ply_bibtex_parser import lexer
input = '@article{citekey, author={Smith, Micah J.}, title={Foo bar}}'
lexer.input(input)
for tok in lexer:
    print(tok)
# LexToken(AT,'@',1,0)
# LexToken(ID,'article',1,1)
# LexToken(ENTRYBEGIN,'{',1,8)
# LexToken(ID,'citekey',1,9)
# LexToken(COMMA,',',1,16)
# LexToken(ID,'author',1,18)
# LexToken(EQUALS,'=',1,24)
# LexToken(VALUE,'{Smith, Micah J.}',1,41)
# LexToken(COMMA,',',1,42)
# LexToken(ID,'title',1,44)
# LexToken(EQUALS,'=',1,49)
# LexToken(VALUE,'{Foo bar}',1,58)
# LexToken(ENTRYEND,'}',1,59)
```

## Development

Install
```
pip install poetry
poetry install
```

Check
```
inv test lint
```

## Limitations

See the TODO notes in [./ply_bibtex_parser/lexer.py](./ply_bibtex_parser/lexer.py) and [./ply_bibtex_parser/parser.py](./ply_bibtex_parser/parser.py).
