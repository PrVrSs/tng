from TsqlParser import Parser
import json
import sys
from cmd2 import Cmd, make_option, options


class CmdLineApp(Cmd):

    @options([make_option('-t', '--time', action="store_true", help="show time"),
              make_option('-f', '--file', action="store_true", help="indicate file"),
              make_option('-j', '--json', action="store_true", help="show json"),
              make_option('-l', '--lisp_string', action="store_true", help="show lisp_string"),
              make_option('-s', '--string', action="store_true", help="show string"),
              make_option('-k', '--tokens', action="store_true", help="show tokens"),
              make_option('-a', '--as_line', action="store_true", help="show as_line")
              ])
    def do_parse(self, arg, opts=None):

        if len(arg) < 1:
            self.stdout.write("Требуется ввести запрос или с помощью флага -f указать файл c запросом\n")
            sys.exit()
        if opts.file:
            p = Parser(input_data=arg, type=1)
        else:
            p = Parser(input_data=arg, type=2)
        if p.status is False:
            print("Некорректный запрос\n")
            sys.exit()
        if opts.time:
            self.stdout.write(p.get_time())
            self.stdout.write('\n')
        if opts.json:
            self.stdout.write(json.dumps(p.to_json(), sort_keys=False, indent=4, separators=(',', ': ')))
            self.stdout.write('\n')
        if opts.lisp_string:
            self.stdout.write(p.to_lisp_string())
            self.stdout.write('\n')
        if opts.string:
            self.stdout.write(p.to_string())
            self.stdout.write('\n')
        if opts.tokens:
            self.stdout.write(json.dumps(p.tokens(), sort_keys=False, indent=4, separators=(',', ': ')))
            self.stdout.write('\n')
        if opts.as_line:
            self.stdout.write(p.as_line())
            self.stdout.write('\n')
        if opts.json is None and opts.time is None and opts.lisp_string is None\
                and opts.string is None and opts.tokens is None and opts.as_line is None:
            self.stdout.write("Не выбран параметр вывода\n")


if __name__ == '__main__':
    c = CmdLineApp()
    c.cmdloop()
