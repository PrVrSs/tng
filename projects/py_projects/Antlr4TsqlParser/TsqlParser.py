from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker, InputStream
from tsql.tsqlLexer import tsqlLexer
from tsql.tsqlListener import tsqlListener
from tsql.tsqlParser import tsqlParser
import time


class KeyPrinter(tsqlListener):

    def __init__(self, ):
        self.key_table = []
        self.key_db = []
        self.key_column = []

    def enterTable_name(self, ctx):
        self.key_table.append(ctx.getText())

    def enterUse_statement(self, ctx):
        self.key_db.append(ctx.getText()[3:])

    def enterFull_column_name(self, ctx):
        self.key_column.append(ctx.getText())


class Parser:

    def __init__(self, input_data, type):
        start_time = time.time()
        if type == 1:
            input = FileStream(input_data)
        if type == 2:
            input = InputStream(input_data)
        lexer = tsqlLexer(input)
        self.stream = CommonTokenStream(lexer)
        self.parser = tsqlParser(self.stream)
        self.tree = self.parser.tsql_file()
        self.time = "time {:.2f} sec".format(time.time() - start_time)
        if self.parser._syntaxErrors:
            self.status = False
        else:
            self.status = True

    def to_string(self):
        return self.tree.toStringTree(recog=self.parser)

    def to_lisp_string(self):
        return self.lisp_string(self.to_string())

    def tokens(self):
        token = {}
        for tok in self.stream.tokens:
            if tok.type == -1:
                break
            token[tok.text] = self.parser.symbolicNames[tok.type]
        return token

    # вывод запроса в 1 строку(для файлов)
    def as_line(self):
        paterns_lexeme = ['DECLARE', 'CURSOR', 'SET', 'SELECT', 'USE', 'FROM', 'OPEN', 'FETCH', 'WHILE',
                          'BEGIN', 'END', 'CLOSE', 'DEALLOCATE', 'GO', 'GLOBAL', 'SCROLL', 'FOR', 'WHERE',
                          'LIKE', 'ORDER', 'BY']
        ret = ''
        for index, a in enumerate(self.tree.getChildren()):
            out_string = ''
            in_string = a.getText()
            word = ''
            for symbol in in_string:
                word += symbol
                for pat_lexeme in paterns_lexeme:
                    if word.find(pat_lexeme) != -1:
                        out_string += in_string[:in_string.index(word)] + \
                                      in_string[in_string.index(word):in_string.index(word) + len(word) - len(
                                          pat_lexeme)] + ' ' + in_string[in_string.index(word) + len(word) - len(
                                           pat_lexeme):in_string.index(word) + len(word)] + ' '
                        in_string = in_string[in_string.index(word) + len(word):]
                        word = ''
                        break
            else:
                out_string += word
            ret += ' '.join(out_string.split()) + '\n'
        return ret

    def get_time(self):
        return self.time

    def to_json(self):
        printer = KeyPrinter()
        walker = ParseTreeWalker()
        walker.walk(printer, self.tree)
        json_dict = {'DB': list(set(printer.key_db)), 'Table': list(set(printer.key_table)),
                     'Column': list(set(printer.key_column))}
        return json_dict

    @staticmethod
    def lisp_string(in_string):
        indent_size = 4
        add_indent = ' ' * indent_size
        if in_string[0] == '(':
            out_string = '{'
        else:
            out_string = in_string[0]
        indent = ''
        for i in range(1, len(in_string) - 1):
            if in_string[i] == '(' and in_string[i + 1] != ' ':
                indent += add_indent
                out_string += "\n" + indent + '{'
            elif in_string[i] == ')':
                out_string += "\n" + indent + '}'
                if len(indent) > 0:
                    indent = indent.replace(add_indent, '', 1)
            else:
                out_string += in_string[i]
        return out_string
