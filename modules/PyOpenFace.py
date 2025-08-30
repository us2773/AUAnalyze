import subprocess
import glob
import os

inputdir = "input"
donedir = "done"
def get_movie_file():
    # inputディレクトリの動画ファイルのリストを返す
    inputs = glob.glob(inputdir+"/*")
    movie_list = []
    for movie_path in inputs :
        movie_name = os.path.splitext(os.path.basename(movie_path))[0]
        movie_list.append(movie_name)
    print(movie_list)
    return movie_list

def get_OpenFace_result() :
    # PowerShell スクリプト実行
    ps_cmd = ["powershell", "-ExecutionPolicy", "ByPass", "-File", "Exec_FeatureExtraction.ps1"]
    result = subprocess.run(ps_cmd, text=True)
    print("PowerShell stdout:", result.stdout)
    print("PowerShell stderr:", result.stderr)
    
if __name__ == "__main__":
    get_movie_file()
    #get_OpenFace_result()