# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ply_bibtex_parser']

package_data = \
{'': ['*']}

install_requires = \
['ply>=3.11,<4.0']

setup_kwargs = {
    'name': 'ply-bibtex-parser',
    'version': '0.1.0',
    'description': 'A simple ply-based parser for BibTeX',
    'long_description': "# ply-bibtex-parser\n\nA simple ply-based parser for BibTeX\n\n[ply](https://www.dabeaz.com/ply/) is an easy-to-use, pure-Python parser generator. However\nit's not the most modern or performant tool.\n\nThis is mostly an academic exercise into writing a simple parser, but I used it in my personal website in order to parse\na `.bib` file to identify the different citations and write them back after reformatting\nthem.\n\n## Install\n\n```\npip install ply-bibtex-parser\n```\n\n## Usage\n\n### Parsing\n\nThe main entry point is through `parser`:\n\n```python\nfrom ply_bibtex_parser import parser\ninput = '@article{citekey, author={Smith, Micah J.}, title={Foo bar}}'\nparser.parse(input)\n# [BibtexEntry(type='article', key='citekey', fields={'author': '{Smith, Micah J.}', 'title': '{Foo bar}'})]\n```\n\nThe parser produces a possibly-empty list of `BibtexEntry` objects. Note that values in\nthe entry which are usually delimited with braces contain the braces: this makes it easy to\nwrite back the bibtex entry without trying to escape its contents. The caller is responsible\nfor further parsing the values if they intend to use the string after escaping is performed.\n\n### Lexing\n\nYou can also use the `lexer` directly:\n\n```python\nfrom ply_bibtex_parser import lexer\ninput = '@article{citekey, author={Smith, Micah J.}, title={Foo bar}}'\nlexer.input(input)\nfor tok in lexer:\n    print(tok)\n# LexToken(AT,'@',1,0)\n# LexToken(ID,'article',1,1)\n# LexToken(ENTRYBEGIN,'{',1,8)\n# LexToken(ID,'citekey',1,9)\n# LexToken(COMMA,',',1,16)\n# LexToken(ID,'author',1,18)\n# LexToken(EQUALS,'=',1,24)\n# LexToken(VALUE,'{Smith, Micah J.}',1,41)\n# LexToken(COMMA,',',1,42)\n# LexToken(ID,'title',1,44)\n# LexToken(EQUALS,'=',1,49)\n# LexToken(VALUE,'{Foo bar}',1,58)\n# LexToken(ENTRYEND,'}',1,59)\n```\n\n## Development\n\nInstall\n```\npip install poetry\npoetry install\n```\n\nCheck\n```\ninv test lint\n```\n\n## Limitations\n\nSee the TODO notes in [./ply_bibtex_parser/lexer.py](./ply_bibtex_parser/lexer.py) and [./ply_bibtex_parser/parser.py](./ply_bibtex_parser/parser.py).\n",
    'author': 'Micah Smith',
    'author_email': 'micahjsmith@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/micahjsmith/ply-bibtex-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
