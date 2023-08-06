import traceback
from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexer import RegexLexer
from pygments.lexer import bygroups
from pygments.lexer import using
from pygments.lexers import PythonLexer
from pygments.style import Style
from pygments.token import Text
from pygments.token import Name
from pygments.token import Number
from pygments.token import Generic
from ..parser import ast
from .utils import CompileError
from .imports_visitor import ImportsVisitor
from .definitions import find_definitions
from .header_visitor import HeaderVisitor
from .source_visitor import SourceVisitor

class TracebackLexer(RegexLexer):

    tokens = {
        'root': [
            (r'^(  File )("[^"]+")(, line )(\d+)(\n)',
             bygroups(Generic.Error, Name.Builtin, Generic.Error, Number, Text)),
            (r'^(\s+?)(\^)(\n)',
             bygroups(Text, Generic.Error, Text)),
            (r'^(    )(.+)(\n)',
             bygroups(Text, using(PythonLexer), Text)),
            (r'^([^:]+)(: )(.+)(\n)',
             bygroups(Generic.Escape, Text, Name, Text), '#pop')
        ]
    }

def style_traceback(traceback):
    return highlight(traceback,
                     TracebackLexer(),
                     Terminal256Formatter(style='monokai'))

def transpile_file(tree,
                   source,
                   filename,
                   module_hpp,
                   module,
                   definitions,
                   skip_tests=False,
                   has_main=False):
    namespace = 'mys::' + module_hpp[:-8].replace('/', '::')
    module_levels = module_hpp[:-8].split('/')
    source_lines = source.split('\n')
    header = HeaderVisitor(namespace,
                           module_levels,
                           source_lines,
                           definitions,
                           definitions[module],
                           has_main).visit(tree)
    source = SourceVisitor(module_levels,
                           module_hpp,
                           filename,
                           skip_tests,
                           namespace,
                           source_lines,
                           definitions,
                           definitions[module]).visit(tree)

    return header, source

class Source:

    def __init__(self,
                 contents,
                 filename='',
                 module='',
                 mys_path='',
                 module_hpp='',
                 skip_tests=False,
                 hpp_path='',
                 cpp_path='',
                 has_main=False):
        self.contents = contents
        self.filename = filename
        self.module = module
        self.mys_path = mys_path
        self.module_hpp = module_hpp
        self.skip_tests = skip_tests
        self.hpp_path = hpp_path
        self.cpp_path = cpp_path
        self.has_main = has_main

def transpile(sources):
    generated = []
    trees = []
    definitions = {}

    try:
        for source in sources:
            trees.append(ast.parse(source.contents, source.mys_path))
    except SyntaxError:
        lines = traceback.format_exc(0).splitlines()

        if 'Traceback (most recent call last):' in lines[0]:
            lines = lines[1:]

        raise Exception(style_traceback('\n'.join(lines)))

    try:
        for source, tree in zip(sources, trees):
            ImportsVisitor().visit(tree)
            
        for source, tree in zip(sources, trees):
            definitions[source.module] = find_definitions(tree,
                                                          source.contents.split('\n'))

        for source, tree in zip(sources, trees):
            generated.append(transpile_file(tree,
                                            source.contents,
                                            source.mys_path,
                                            source.module_hpp,
                                            source.module,
                                            definitions,
                                            source.skip_tests,
                                            source.has_main))

        return generated
    except CompileError as e:
        line = source.contents.splitlines()[e.lineno - 1]
        marker_line = ' ' * e.offset + '^'

        raise Exception(
            style_traceback(f'  File "{source.mys_path}", line {e.lineno}\n'
                            f'    {line}\n'
                            f'    {marker_line}\n'
                            f'CompileError: {e.message}'))
