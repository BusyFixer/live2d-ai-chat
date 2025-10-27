import json
from pathlib import Path
# ----------
with open("config.json", "r", encoding="utf-8") as cfg:
    config = json.load(cfg)
path = config["model3.json_path"]
# ----------
path = Path(path)
path2 = path.parent
print(path2)
with open(path,"r",encoding="utf-8") as f:
    target = json.load(f)
print(target)
target['FileReferences']['Expressions'] = []
all_exp = list(path2.glob("*.exp3.json"))
# all_motion = list(path2.glob("*.motion3.json"))
for exp1 in all_exp:
    exp = str(exp1).split("\\")[-1]
    print(f"Inject:{exp1}", end="     ")
    form = {"Name": exp,"File": exp}
    target['FileReferences']['Expressions'].append(form)
    print("done.")
with open(path, "w", encoding="utf-8") as f:
    json.dump(target, f, ensure_ascii=False, indent=2)
