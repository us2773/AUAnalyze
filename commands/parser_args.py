import shlex

def perse_args(line: str) -> dict :
    args_dict = {}
    tokens = shlex.split(line)
    for token in tokens:
        if token.startswith("-") :
            if "=" in token :
                key, value = token[1:].split("=", 1)
                args_dict[key] = value
            else :
                args_dict[token[1:]] = True
        else:
            raise ValueError(f"無効な引数: {token}")
    
    return args_dict