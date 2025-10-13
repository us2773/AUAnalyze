import sys
import os

# ルートディレクトリ（AUAnalyze）をsys.pathに追加
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from cmd import Cmd
from modules import stats, get_AUdata, exec, PyOpenFace
from commands import parser_args

class analyze_tools(Cmd) :
    intro = "'help'でコマンド一覧を表示"
    prompt = ">"
    
    def __init__(self, completekey = "tab", stdin = None, stdout = None):
        super().__init__(completekey, stdin, stdout)
        
    def do_help(self, arg):
        return super().do_help(arg)
    
    def do_AUAnalyze(self, arg) :
        try :
            exec.exec()
        except Exception as e:
            print("Error:", e)
    
    def do_stats(self, arg) :
        try:
            arg_dict = parser_args.perse_args(arg)
            print("DEBUG arg_dict:", arg_dict)
            stats.get_stats(arg_dict["person"], arg_dict["date"], int(arg_dict["num"]), int(arg_dict["au"]))
        except Exception as e:
            print("ERROR:", e)
            
    def do_trend(self, arg) :
        try: 
            arg_dict = parser_args.perse_args(arg)
            data = stats.get_data_from_property(arg_dict["person"], arg_dict["date"])
            is_all = "all" in arg_dict
            print(is_all)
            for i in data:
                df = get_AUdata.csv_to_dataframe(f"output/{i.movie_name}.csv")
                get_AUdata.show_trend_noise_graph(df, int(arg_dict["au"]), is_all)
                
        except Exception as e:
            print("ERROR:", e)
            
    def do_peaks(self, arg) :
        try: 
            arg_dict = parser_args.perse_args(arg)
            is_all = "all" in arg_dict
            data = stats.get_data_from_property(arg_dict["person"], arg_dict["date"])
            for i in data:
                df = get_AUdata.csv_to_dataframe(f"output/{i.movie_name}.csv")
                get_AUdata.show_AU_peak_graph(df, int(arg_dict["au"]), is_all)
                
        except Exception as e:
            print("ERROR:", e)
            
    def do_move(self, arg) :
        try :
            PyOpenFace.transfer_input_movies()
        except Exception as e:
            print("ERROR:", e)
            
    def do_EOF(self, arg):
        return True
    
    def emptyline(self):
        return super().emptyline()

if __name__ == "__main__": 
    analyze_tools().cmdloop()