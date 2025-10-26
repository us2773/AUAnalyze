import subprocess
import glob
import os
import shutil

inputdir = "input"
donedir = "done"
done_json_dir = f"{donedir}/json"
done_movie_dir = f"{donedir}/movie"
jsondir = "json"

def get_movie_file():
    # inputディレクトリの動画ファイルのリストを返す
    inputs = glob.glob(inputdir+"/*")
    movie_list = []
    for movie_path in inputs :
        movie_name = os.path.splitext(os.path.basename(movie_path))[0]
        movie_list.append(movie_name)
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
    os.makedirs(done_json_dir, exist_ok=True)
    os.makedirs(done_movie_dir, exist_ok=True)

    for filename in os.listdir(inputdir):
        if filename.endswith(".mp4"): 
            shutil.move(os.path.join(inputdir, filename),
                        os.path.join(done_movie_dir, filename))
    
    for filename in os.listdir(jsondir) :
        if filename.endswith(".json") :
            shutil.move(os.path.join(jsondir, filename), 
                        os.path.join(done_json_dir, filename))
    
if __name__ == "__main__":
    get_movie_file()
    get_OpenFace_result()
    transfer_input_movies()