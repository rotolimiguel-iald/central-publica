import json, hashlib
P = r"C:\IALD\Central de Patentes\work\conjunto_D_20261029\parametrizacao_03nov\PODER_RAMO_B_ANTES_DE_ABRIR.json"
b = open(P, "rb").read()
print("sha256", hashlib.sha256(b).hexdigest(), len(b))
d = json.loads(b.decode("utf-8"))
def walk(o, path="", depth=0):
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, (dict, list)) and depth < 3:
                print("  "*depth + str(k) + ":", type(v).__name__, len(v))
                walk(v, path + "/" + k, depth+1)
            else:
                s = str(v)
                print("  "*depth + str(k) + " =", s[:240])
    elif isinstance(o, list):
        for i, v in enumerate(o[:6]):
            if isinstance(v, (dict, list)):
                print("  "*depth + "[%d]" % i, type(v).__name__)
                walk(v, path, depth+1)
            else:
                print("  "*depth + "[%d] = " % i + str(v)[:200])
walk(d)
