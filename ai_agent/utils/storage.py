
import json, os, time
def save_json(obj, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return path
def ts():
    return time.strftime("%Y-%m-%d %H:%M:%S")
