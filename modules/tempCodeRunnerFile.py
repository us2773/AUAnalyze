import glob
import pandas as pd
outputdir = "output"

outputs = glob.glob(outputdir+"/*")
print(outputs)

# 取得した
for i in range(5) :
    try:
        df = pd.read_csv(outputs[-i])
        print(df)
    except Exception as e:
        raise RuntimeError(f"fail to load csv: {e}")
    