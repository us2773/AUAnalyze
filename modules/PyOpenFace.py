import subprocess
import glob
import os
import shutil

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
    
def transfer_input_movies():
    # input ディレクトリ内の動画ファイルを done に移動
    os.makedirs(donedir, exist_ok=True)

    for filename in os.listdir(inputdir):
        if filename.endswith(".mp4"): 
            shutil.move(os.path.join(inputdir, filename),
                        os.path.join(donedir, filename))
    
if __name__ == "__main__":
    get_movie_file()
    get_OpenFace_result()
    transfer_input_movies()