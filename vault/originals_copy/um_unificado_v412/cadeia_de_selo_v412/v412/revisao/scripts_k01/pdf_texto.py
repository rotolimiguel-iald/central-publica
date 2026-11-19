import sys, io
src, dst = sys.argv[1], sys.argv[2]
txt = None
try:
    import fitz
    doc = fitz.open(src)
    txt = "\n".join(f"\n=====PAGE {i+1}=====\n" + pg.get_text() for i, pg in enumerate(doc))
    print("fitz ok", len(doc))
except Exception as e:
    print("fitz falhou:", e)
    try:
        import pypdf
        r = pypdf.PdfReader(src)
        txt = "\n".join(f"\n=====PAGE {i+1}=====\n" + (p.extract_text() or "") for i, p in enumerate(r.pages))
        print("pypdf ok", len(r.pages))
    except Exception as e2:
        print("pypdf falhou:", e2)
if txt:
    io.open(dst, "w", encoding="utf-8").write(txt)
    print("escrito", len(txt))
