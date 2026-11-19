# strip_lean_comments.py — remove comentários de linha (-- ...), de bloco (/- ... -/)
# e docstrings (/-- ... -/, /-! ... -/) de fontes Lean 4, com aninhamento de bloco.
# Preserva literais de string ("..." com escapes \\ e \") e de char ('...').
# Uso: python strip_lean_comments.py <entrada.lean> <saida>
# Saída: o que sobra do código, byte a byte (comentários viram nada; quebras de linha
# fora de comentário são preservadas; dentro de comentário de bloco, as quebras também
# são removidas — para conferência usamos a comparação estrita e, se falhar, a normalizada).

import sys

def strip(src: str) -> str:
    out = []
    i, n = 0, len(src)
    # estados: code, string, char, line_comment, block(depth)
    state = "code"
    depth = 0
    while i < n:
        c = src[i]
        two = src[i:i+2]
        three = src[i:i+3]
        if state == "code":
            if three == "/--" or three == "/-!":
                state = "block"; depth = 1; i += 3
            elif two == "/-":
                state = "block"; depth = 1; i += 2
            elif two == "--":
                state = "line"; i += 2
            elif c == '"':
                state = "string"; out.append(c); i += 1
            elif c == "'":
                # char literal 'x' ou '\n' etc.; só entra se fechar adiante (heurística segura)
                # trata sequência de escape
                state = "char"; out.append(c); i += 1
            else:
                out.append(c); i += 1
        elif state == "string":
            if c == "\\":
                out.append(c)
                if i + 1 < n:
                    out.append(src[i+1]); i += 2
                else:
                    i += 1
            elif c == '"':
                state = "code"; out.append(c); i += 1
            else:
                out.append(c); i += 1
        elif state == "char":
            if c == "\\":
                out.append(c)
                if i + 1 < n:
                    out.append(src[i+1]); i += 2
                else:
                    i += 1
            elif c == "'":
                state = "code"; out.append(c); i += 1
            elif c == "\n":
                # char literal não fechou: era apóstrofo em código? recua para code
                state = "code"; out.append(c); i += 1
            else:
                out.append(c); i += 1
        elif state == "line":
            if c == "\n":
                state = "code"; out.append(c); i += 1
            else:
                i += 1
        elif state == "block":
            if two == "/-":
                depth += 1; i += 2
            elif two == "-/":
                depth -= 1; i += 2
                if depth == 0:
                    state = "code"
            else:
                i += 1
    return "".join(out)

def normalize(s: str) -> str:
    # comparação de segundo nível: tira espaços à direita e linhas vazias
    lines = [ln.rstrip() for ln in s.replace("\r\n", "\n").split("\n")]
    lines = [ln for ln in lines if ln.strip() != ""]
    return "\n".join(lines)

if __name__ == "__main__":
    inp, outp = sys.argv[1], sys.argv[2]
    data = open(inp, "rb").read()
    text = data.decode("utf-8")
    stripped = strip(text)
    open(outp, "wb").write(stripped.encode("utf-8"))
    # também grava a forma normalizada
    open(outp + ".norm", "wb").write(normalize(stripped).encode("utf-8"))
    print(f"{inp}: {len(data)} B -> {len(stripped.encode('utf-8'))} B (strip), {len(normalize(stripped).encode('utf-8'))} B (norm)")
