from cmd import Cmd
from modules import *
from commands import parser_args

class analyze_tools(Cmd) :
    intro = "'help'でコマンド一覧を表示"
    prompt = ">"
    
    def __init__(self, completekey = "tab", stdin = None, stdout = None):
        super().__init__(completekey, stdin, stdout)
        
    def do_help(self, arg):
        return super().do_help(arg)
    
    def do_AUAnalyze(self) :
        exec()
    
    def do_stats(self, arg) :
        arg_dict = parser_args.perse_args(arg)
        