import subprocess

def get_OpenFace_result() :
    # PowerShell スクリプト実行
    ps_cmd = ["powershell", "-ExecutionPolicy", "ByPass", "-File", "Exec_FeatureExtraction.ps1"]
    result = subprocess.run(ps_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    print("PowerShell stdout:", result.stdout)
    print("PowerShell stderr:", result.stderr)
    
if __name__ == "__main__":
    get_OpenFace_result()