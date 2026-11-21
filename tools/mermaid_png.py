#!/usr/bin/env python3
"""
Diagramas Mermaid no jogo.

O GitHub desenha os blocos ```mermaid sozinho. O painel de texto do Project
Zomboid nao entende Mermaid, entao este modulo le o mesmo bloco e gera uma
imagem PNG (tema escuro, combinando com o jogo) que vai junto com o mod.

Suporta o tipo mais usado em guias, o fluxograma:

    flowchart TD            (ou graph; direcoes TD, TB, BT, LR, RL)
        A[Retangulo] --> B(Arredondado)
        B --> C{Decisao?}
        C -->|Sim| D([Inicio/fim])
        C -- Nao --> E((Circulo))
        E -.-> F[[Sub-rotina]]
        F ==> G{{Hexagono}}
        A & B --- H[(Banco)]

Linhas: --> seta, --- sem seta, -.-> pontilhada, ==> grossa, <--> dupla.
Textos com "aspas", <br> para quebrar linha. classDef, style, class, click e
linkStyle sao aceitos (o GitHub usa, o jogo ignora). subgraph aparece sem a
caixa no jogo. Outros tipos de diagrama (sequence, pie...) sao recusados.

Uso direto, para ver a imagem:
    python tools/mermaid_png.py arquivo.mmd saida.png
"""
import hashlib
import pathlib
import re
import sys

FONT_FILE = pathlib.Path(__file__).resolve().parent / "fonts" / "DejaVuSans.ttf"
THEME_VERSION = "1"        # mude para forcar novas imagens quando o visual mudar
MAX_NODES = 40
MAX_WIDTH = 1400           # pixels; mais largo que isso fica ilegivel no jogo
SS = 3                     # desenha 3x maior e reduz (bordas suaves)
FONT_SIZE = 14

BG = (28, 30, 34)
BG_BORDER = (70, 74, 82)
TEXT = (238, 238, 238)
EDGE = (175, 180, 190)
EDGE_TEXT = (205, 210, 220)
STYLE = {
    "rect":       ((48, 54, 66), (232, 180, 80)),
    "round":      ((48, 54, 66), (232, 180, 80)),
    "subroutine": ((48, 54, 66), (232, 180, 80)),
    "cylinder":   ((48, 54, 66), (140, 180, 230)),
    "hexagon":    ((48, 54, 66), (140, 180, 230)),
    "diamond":    ((62, 54, 36), (240, 205, 95)),
    "stadium":    ((38, 60, 50), (110, 200, 140)),
    "circle":     ((38, 60, 50), (110, 200, 140)),
}


class DiagramError(Exception):
    pass


# ---------------------------------------------------------------------------
# Leitura
# ---------------------------------------------------------------------------

HEADER = re.compile(r"^(flowchart|graph)(?:\s+(TD|TB|BT|LR|RL))?\s*;?\s*$", re.I)
IGNORE = re.compile(r"^(classDef|class|style|linkStyle|click|direction|accTitle|accDescr)\b")
SHAPES = [  # (abre, fecha, forma) - os mais longos primeiro
    ("([", "])", "stadium"), ("[[", "]]", "subroutine"), ("[(", ")]", "cylinder"),
    ("((", "))", "circle"), ("{{", "}}", "hexagon"), ("[/", "/]", "rect"),
    ("[\\", "\\]", "rect"), ("[/", "\\]", "rect"), ("[\\", "/]", "rect"),
    ("[", "]", "rect"), ("(", ")", "round"), ("{", "}", "diamond"), (">", "]", "rect"),
]
NODE_ID = re.compile(r"\s*([\w]+)", re.U)
LINK = re.compile(r"\s*(<?)(-{2,}>|={2,}>|-\.+->|-{2,}[ox]|={2,}[ox]|-{3,}|={3,}|-\.+-)\s*(?:\|([^|]*)\|)?")


def clean_label(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] == '"':
        s = s[1:-1]
    if len(s) >= 2 and s[0] == s[-1] == "`":
        s = s[1:-1]
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = s.replace("**", "").replace("#quot;", '"').replace("#35;", "#")
    s = re.sub(r"fa:fa-[\w-]+\s*", "", s)
    return "\n".join(line.strip() for line in s.split("\n")).strip()


def split_statements(text):
    """Separa por linha e por ';' fora de aspas e colchetes."""
    out = []
    for line in text.replace("\r\n", "\n").split("\n"):
        depth, quote, cur = 0, False, []
        for ch in line:
            if ch == '"':
                quote = not quote
            elif not quote and ch in "[({":
                depth += 1
            elif not quote and ch in "])}":
                depth = max(0, depth - 1)
            if ch == ";" and not quote and depth == 0:
                out.append("".join(cur)); cur = []
            else:
                cur.append(ch)
        out.append("".join(cur))
    return [s.strip() for s in out]


def normalize_link_text(s):
    """'A -- texto --> B' vira 'A -->|texto| B' (e os equivalentes)."""
    s = re.sub(r"(?<![-.=<])--\s+([^\s>|\-][^>|]*?)\s+-->", r"-->|\1|", s)
    s = re.sub(r"(?<![-.=<])--\s+([^\s>|\-][^>|]*?)\s+---", r"---|\1|", s)
    s = re.sub(r"-\.\s+([^>|]+?)\s+\.->", r"-.->|\1|", s)
    s = re.sub(r"==\s+([^>|=]+?)\s+==>", r"==>|\1|", s)
    return s


class Graph:
    def __init__(self, direction):
        self.direction = direction
        self.nodes = {}      # id -> {"label", "shape"}
        self.order = []
        self.edges = []      # {"a", "b", "label", "style", "head", "tail"}

    def node(self, nid, label=None, shape=None):
        if nid not in self.nodes:
            self.nodes[nid] = {"label": nid, "shape": "rect"}
            self.order.append(nid)
        if label is not None:
            self.nodes[nid]["label"] = label
        if shape is not None:
            self.nodes[nid]["shape"] = shape

    def labels(self):
        out = [n["label"] for n in self.nodes.values()]
        out += [e["label"] for e in self.edges if e["label"]]
        return " ".join(out).replace("\n", " ")


def parse_node(s, pos, g, where):
    m = NODE_ID.match(s, pos)
    if not m:
        raise DiagramError(f"{where}: esperava o nome de um no em '{s[pos:pos + 20].strip()}'")
    nid, pos = m.group(1), m.end()
    if nid in ("end", "subgraph"):
        raise DiagramError(f"{where}: '{nid}' nao pode ser nome de no")
    for op, cl, shape in SHAPES:
        if s.startswith(op, pos):
            start = pos + len(op)
            if s[start:start + 1] == '"':
                q = s.find('"', start + 1)
                if q < 0:
                    raise DiagramError(f"{where}: aspas sem fechar no no '{nid}'")
                end = s.find(cl, q + 1)
            else:
                end = s.find(cl, start)
            if end < 0:
                raise DiagramError(f"{where}: faltou fechar '{op}' no no '{nid}'")
            g.node(nid, clean_label(s[start:end]), shape)
            pos = end + len(cl)
            break
    else:
        g.node(nid)
    if s.startswith(":::", pos):
        m = re.match(r":::[\w-]+", s[pos:])
        pos += m.end() if m else 3
    return nid, pos


def parse_group(s, pos, g, where):
    ids = []
    while True:
        nid, pos = parse_node(s, pos, g, where)
        ids.append(nid)
        m = re.match(r"\s*&\s*", s[pos:])
        if not m:
            return ids, pos
        pos += m.end()


def parse(source, where="diagrama"):
    lines = [l for l in split_statements(source) if l and not l.startswith("%%")]
    if not lines:
        raise DiagramError(f"{where}: diagrama vazio")
    m = HEADER.match(lines[0])
    if not m:
        kind = lines[0].split()[0]
        raise DiagramError(f"{where}: o jogo so desenha 'flowchart' ou 'graph' (recebeu '{kind}'). "
                           "Use um fluxograma ou deixe o diagrama fora do manual.")
    g = Graph((m.group(2) or "TD").upper().replace("TB", "TD"))
    for st in lines[1:]:
        if IGNORE.match(st) or st == "end" or st.startswith("subgraph"):
            continue
        st = normalize_link_text(st)
        left, pos = parse_group(st, 0, g, where)
        while pos < len(st) and st[pos:].strip():
            lm = LINK.match(st, pos)
            if not lm:
                raise DiagramError(f"{where}: nao entendi '{st[pos:].strip()}' em '{st}'")
            both, kind, label = lm.group(1) == "<", lm.group(2), lm.group(3)
            right, pos = parse_group(st, lm.end(), g, where)
            style = "dotted" if "." in kind else "thick" if kind.startswith("=") else "solid"
            head = kind[-1] in ">ox"
            for a in left:
                for b in right:
                    g.edges.append({"a": a, "b": b, "label": clean_label(label or ""),
                                    "style": style, "head": head, "tail": both})
            left = right
    if not g.nodes:
        raise DiagramError(f"{where}: nenhum no no diagrama")
    if len(g.nodes) > MAX_NODES:
        raise DiagramError(f"{where}: {len(g.nodes)} nos; o maximo no jogo e {MAX_NODES}. Divida em dois diagramas.")
    return g


# ---------------------------------------------------------------------------
# Posicoes (camadas, estilo Sugiyama simplificado)
# ---------------------------------------------------------------------------

def _font(size):
    from PIL import ImageFont
    return ImageFont.truetype(str(FONT_FILE), size)


def _text_size(font, text):
    lines = text.split("\n") or [""]
    lh = int(font.size * 1.3)
    w = max((font.getlength(l) for l in lines), default=0)
    return int(w), lh * len(lines), lh


def _node_size(font, label, shape):
    tw, th, _ = _text_size(font, label)
    px, py = 14 * SS, 9 * SS
    if shape == "diamond":
        return int(tw * 1.67 + 24 * SS), int(th * 2.5 + 8 * SS)
    if shape == "circle":
        d = int(max(tw, th) + 2 * px)
        return d, d
    if shape == "hexagon":
        return int(tw + th + 3 * px), int(th + 2 * py)
    if shape == "stadium":
        return int(tw + th + 2 * px), int(th + 2 * py)
    return max(int(tw + 2 * px), 60 * SS), int(th + 2 * py)


def layout(g):
    font = _font(FONT_SIZE * SS)
    small = _font(int(FONT_SIZE * 0.86) * SS)
    vertical = g.direction in ("TD", "BT")
    ids = list(g.order)
    size = {n: _node_size(font, g.nodes[n]["label"], g.nodes[n]["shape"]) for n in ids}

    # 1) tira os ciclos (inverte as arestas de volta)
    adj = {n: [] for n in ids}
    for i, e in enumerate(g.edges):
        if e["a"] != e["b"]:
            adj[e["a"]].append(i)
    state, rev = {}, set()

    def dfs(n):
        state[n] = 1
        for i in adj[n]:
            b = g.edges[i]["b"]
            if state.get(b) == 1:
                rev.add(i)
            elif b not in state:
                dfs(b)
        state[n] = 2
    sys.setrecursionlimit(10000)
    for n in ids:
        if n not in state:
            dfs(n)
    dag = []
    for i, e in enumerate(g.edges):
        if e["a"] == e["b"]:
            continue
        a, b = (e["b"], e["a"]) if i in rev else (e["a"], e["b"])
        dag.append((a, b, i))

    # 2) camadas pelo caminho mais longo
    layer = {n: 0 for n in ids}
    indeg = {n: 0 for n in ids}
    for a, b, _ in dag:
        indeg[b] += 1
    queue = [n for n in ids if indeg[n] == 0]
    while queue:
        n = queue.pop(0)
        for a, b, _ in dag:
            if a == n:
                layer[b] = max(layer[b], layer[a] + 1)
                indeg[b] -= 1
                if indeg[b] == 0:
                    queue.append(b)

    # 3) nos invisiveis para arestas que pulam camadas
    chains, dsize = {}, (10 * SS, 10 * SS)
    for a, b, i in dag:
        chain = [a]
        for k in range(layer[a] + 1, layer[b]):
            d = f"__d{i}_{k}"
            layer[d] = k
            size[d] = dsize
            chain.append(d)
        chain.append(b)
        chains[i] = chain
    nlayers = max(layer.values()) + 1
    rows = [[] for _ in range(nlayers)]
    for n in ids:
        rows[layer[n]].append(n)
    for i in sorted(chains):
        for d in chains[i][1:-1]:
            rows[layer[d]].append(d)
    up, down = {}, {}
    for chain in chains.values():
        for x, y in zip(chain, chain[1:]):
            down.setdefault(x, []).append(y)
            up.setdefault(y, []).append(x)

    # 4) ordem dentro da camada (baricentro)
    def sweep(rng, nb):
        for li in rng:
            pos = {n: k for k, n in enumerate(rows[li - 1 if nb is up else li + 1])}
            def key(n, k):
                ns = [pos[m] for m in nb.get(n, []) if m in pos]
                return sum(ns) / len(ns) if ns else k
            rows[li] = [n for _, n in sorted(((key(n, k), n) for k, n in enumerate(rows[li])),
                                             key=lambda t: t[0])]
    for _ in range(6):
        sweep(range(1, nlayers), up)
        sweep(range(nlayers - 2, -1, -1), down)

    # 5) coordenadas: u = ao longo da camada, v = entre camadas
    def usz(n): return size[n][0] if vertical else size[n][1]
    def vsz(n): return size[n][1] if vertical else size[n][0]
    gap_u = 28 * SS
    label_room = 0
    for e in g.edges:
        if e["label"]:
            w, h, _ = _text_size(small, e["label"])
            label_room = max(label_room, (h if vertical else w) + 12 * SS)
    gap_v = max(46 * SS, label_room + 24 * SS)

    u = {}
    for row in rows:
        x = 0
        for n in row:
            u[n] = x + usz(n) / 2
            x += usz(n) + gap_u
    width_of = lambda row: (u[row[-1]] + usz(row[-1]) / 2) if row else 0
    widest = max(width_of(r) for r in rows)
    for row in rows:
        off = (widest - width_of(row)) / 2
        for n in row:
            u[n] += off

    def sep(a, b):
        return usz(a) / 2 + usz(b) / 2 + (gap_u if not (a.startswith("__d") and b.startswith("__d")) else gap_u / 2)

    for _ in range(4):
        for li_range, nb in ((range(1, nlayers), up), (range(nlayers - 2, -1, -1), down)):
            for li in li_range:
                row = rows[li]
                want = []
                for n in row:
                    ns = [u[m] for m in nb.get(n, [])]
                    want.append(sum(ns) / len(ns) if ns else u[n])
                left = list(want)
                for k in range(1, len(row)):
                    left[k] = max(left[k], left[k - 1] + sep(row[k - 1], row[k]))
                right = list(want)
                for k in range(len(row) - 2, -1, -1):
                    right[k] = min(right[k], right[k + 1] - sep(row[k], row[k + 1]))
                mid = [(l + r) / 2 for l, r in zip(left, right)]
                for k in range(1, len(row)):
                    mid[k] = max(mid[k], mid[k - 1] + sep(row[k - 1], row[k]))
                for n, x in zip(row, mid):
                    u[n] = x
    minu = min(u[n] - usz(n) / 2 for n in u)
    for n in u:
        u[n] -= minu

    v, y = {}, 0
    for row in rows:
        thick = max(vsz(n) for n in row)
        for n in row:
            v[n] = y + thick / 2
        y += thick + gap_v
    total_v = y - gap_v
    total_u = max(u[n] + usz(n) / 2 for n in u)
    if g.direction in ("BT", "RL"):
        for n in v:
            v[n] = total_v - v[n]

    pos = {n: ((u[n], v[n]) if vertical else (v[n], u[n])) for n in u}
    W, H = (total_u, total_v) if vertical else (total_v, total_u)
    return {"font": font, "small": small, "pos": pos, "size": size, "chains": chains,
            "rev": rev, "W": W, "H": H, "vertical": vertical}


# ---------------------------------------------------------------------------
# Desenho
# ---------------------------------------------------------------------------

def _border_point(cx, cy, w, h, shape, tx, ty):
    """Ponto na borda do no na direcao de (tx, ty)."""
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    if shape == "diamond":
        t = 1 / (abs(dx) / (w / 2) + abs(dy) / (h / 2))
    elif shape == "circle":
        t = (w / 2) / (dx * dx + dy * dy) ** 0.5
    else:
        tx_ = (w / 2) / abs(dx) if dx else float("inf")
        ty_ = (h / 2) / abs(dy) if dy else float("inf")
        t = min(tx_, ty_)
    return cx + dx * t, cy + dy * t


def _dashed(draw, p, q, width, color, dash=6 * SS, gap=5 * SS):
    (x1, y1), (x2, y2) = p, q
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    if length == 0:
        return
    k = 0.0
    while k < length:
        e = min(k + dash, length)
        draw.line([(x1 + (x2 - x1) * k / length, y1 + (y2 - y1) * k / length),
                   (x1 + (x2 - x1) * e / length, y1 + (y2 - y1) * e / length)], fill=color, width=width)
        k = e + gap


def _arrow(draw, p, q, color):
    (x1, y1), (x2, y2) = p, q
    length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 or 1
    ux, uy = (x2 - x1) / length, (y2 - y1) / length
    L, Wd = 10 * SS, 5 * SS
    bx, by = x2 - ux * L, y2 - uy * L
    draw.polygon([(x2, y2), (bx - uy * Wd, by + ux * Wd), (bx + uy * Wd, by - ux * Wd)], fill=color)
    return bx, by


def _draw_text(draw, font, cx, cy, text, color):
    lines = text.split("\n")
    lh = int(font.size * 1.3)
    y = cy - lh * len(lines) / 2
    for line in lines:
        w = font.getlength(line)
        draw.text((cx - w / 2, y + (lh - font.size) / 2 - font.size * 0.1), line, font=font, fill=color)
        y += lh


def render(g):
    from PIL import Image, ImageDraw
    L = layout(g)
    m = 18 * SS
    W, H = int(L["W"] + 2 * m), int(L["H"] + 2 * m)
    if W / SS > MAX_WIDTH:
        raise DiagramError(f"diagrama com {int(W / SS)} px de largura (maximo {MAX_WIDTH}). "
                           "Use 'flowchart TD' ou divida em partes.")
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, W - 1, H - 1], radius=10 * SS, fill=BG, outline=BG_BORDER, width=2 * SS)
    pos = {n: (x + m, y + m) for n, (x, y) in L["pos"].items()}
    size = L["size"]

    # arestas
    labels = []
    for i, e in enumerate(g.edges):
        if i not in L["chains"]:
            continue
        chain = L["chains"][i]
        pts = [pos[n] for n in chain]
        if i in L["rev"]:
            chain, pts = chain[::-1], pts[::-1]
        a, b = chain[0], chain[-1]
        sa, sb = g.nodes[a]["shape"], g.nodes[b]["shape"]
        pts[0] = _border_point(*pos[a], *size[a], sa, *pts[1])
        pts[-1] = _border_point(*pos[b], *size[b], sb, *pts[-2])
        width = (4 if e["style"] == "thick" else 2) * SS
        if e["head"]:
            pts[-1] = _arrow(d, pts[-2], pts[-1], EDGE)
        if e["tail"]:
            pts[0] = _arrow(d, pts[1], pts[0], EDGE)
        for p, q in zip(pts, pts[1:]):
            if e["style"] == "dotted":
                _dashed(d, p, q, width, EDGE)
            else:
                d.line([p, q], fill=EDGE, width=width)
        if e["label"]:
            k = (len(pts) - 1) // 2
            (x1, y1), (x2, y2) = pts[k], pts[k + 1]
            labels.append(((x1 + x2) / 2, (y1 + y2) / 2, e["label"]))

    # nos
    for n in g.order:
        cx, cy = pos[n]
        w, h = size[n]
        shape = g.nodes[n]["shape"]
        fill, line = STYLE.get(shape, STYLE["rect"])
        box = [cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2]
        lw = 2 * SS
        if shape == "diamond":
            d.polygon([(cx, box[1]), (box[2], cy), (cx, box[3]), (box[0], cy)], fill=fill, outline=line, width=lw)
        elif shape == "circle":
            d.ellipse(box, fill=fill, outline=line, width=lw)
        elif shape == "hexagon":
            k = h / 2
            d.polygon([(box[0] + k, box[1]), (box[2] - k, box[1]), (box[2], cy), (box[2] - k, box[3]),
                       (box[0] + k, box[3]), (box[0], cy)], fill=fill, outline=line, width=lw)
        elif shape == "stadium":
            d.rounded_rectangle(box, radius=h / 2, fill=fill, outline=line, width=lw)
        elif shape in ("round", "cylinder"):
            d.rounded_rectangle(box, radius=10 * SS, fill=fill, outline=line, width=lw)
        else:
            d.rectangle(box, fill=fill, outline=line, width=lw)
            if shape == "subroutine":
                d.line([(box[0] + 7 * SS, box[1]), (box[0] + 7 * SS, box[3])], fill=line, width=lw)
                d.line([(box[2] - 7 * SS, box[1]), (box[2] - 7 * SS, box[3])], fill=line, width=lw)
        _draw_text(d, L["font"], cx, cy, g.nodes[n]["label"], TEXT)

    # textos das setas por cima de tudo
    for x, y, text in labels:
        tw, th, _ = _text_size(L["small"], text)
        pad = 5 * SS
        d.rounded_rectangle([x - tw / 2 - pad, y - th / 2 - pad / 2, x + tw / 2 + pad, y + th / 2 + pad / 2],
                            radius=4 * SS, fill=BG)
        _draw_text(d, L["small"], x, y, text, EDGE_TEXT)

    return img.resize((max(1, W // SS), max(1, H // SS)), Image.LANCZOS)


def image_name(source):
    norm = "\n".join(l.rstrip() for l in source.strip().replace("\r\n", "\n").split("\n"))
    return "d_" + hashlib.sha1((THEME_VERSION + "\n" + norm).encode("utf-8")).hexdigest()[:12] + ".png"


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    try:
        img = render(parse(src, sys.argv[1]))
    except DiagramError as e:
        print("erro:", e, file=sys.stderr)
        return 1
    img.save(sys.argv[2], optimize=True)
    print(f"gravado: {sys.argv[2]} ({img.width}x{img.height})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
