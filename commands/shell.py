import sys
import os

# ルートディレクトリ（AUAnalyze）をsys.pathに追加
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from cmd import Cmd
from modules import stats
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
        try:
            arg_dict = parser_args.perse_args(arg)
            print("DEBUG arg_dict:", arg_dict)
            stats.get_stats(arg_dict["person"], arg_dict["date"], int(arg_dict["num"]), int(arg_dict["au"]))
        except Exception as e:
            print("ERROR:", e)
if __name__ == "__main__": 
    analyze_tools().cmdloop()