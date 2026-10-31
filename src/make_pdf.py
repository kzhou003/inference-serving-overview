"""Build the book PDF: cover + contents (with real page numbers) + reading map + chapters with map-crop openers.
Two passes: the first finds which page each chapter/subsection lands on, the second writes those numbers
into the contents. Then a footer (title, author, page number) is stamped on every page except the cover."""
import json, re, subprocess, sys, io, os, html
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '..', 'index.html')
OUT = os.path.join(HERE, '..', 'inference-serving-guide.pdf')
AUTHOR = 'kzhoulatte'
page = open(SRC).read()
front = open(os.path.join(HERE, 'print_front.html')).read()
inject = open(os.path.join(HERE, 'print_inject.html')).read()

def build(pages, out):
    pre = f'<script>window.__TOC_PAGES = {json.dumps(pages)};</script>\n'
    i = page.rindex('</body>')
    path = os.path.join(HERE, 'print_book.html')
    open(path, 'w').write(page[:i] + pre + front + inject + page[i:])
    subprocess.run(['google-chrome', '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
                    f'--print-to-pdf={out}', '--virtual-time-budget=20000', 'file://' + path],
                   check=True, stderr=subprocess.DEVNULL)

def norm(s): return re.sub(r'\s+', '', html.unescape(re.sub(r'<[^>]+>', '', s)))
# targets: reading map, every chapter h2, and the h3 subsections of chapter 04
targets = [('mapPane', '阅读地图')]
for sid, body in re.findall(r'<section id="(\w+)">(.*?)</section>', page, re.S):
    h2 = re.search(r'<h2><span class="no">\d+</span>(.*?)</h2>', body)
    if h2: targets.append((sid, norm(h2.group(1))[:12]))
    if sid == 'llm':
        for hid, h3 in re.findall(r'<h3 id="(\w+)">(.*?)</h3>', body):
            targets.append((hid, norm(h3)[:10]))

def locate(pdf):
    # Chrome emits a named destination for every in-document link target, so page numbers come straight from the PDF
    r = PdfReader(pdf)
    dests = r.named_destinations
    found = {}
    for key, _ in targets:
        d = dests.get('/' + key)
        if d is None: sys.exit(f'no destination for {key}')
        found[key] = r.get_destination_page_number(d) + 1
    return found, len(r.pages)

raw = os.path.join(HERE, 'book_raw.pdf')
build({}, raw); pages, _ = locate(raw)
for _ in range(2):
    build(pages, raw); again, n = locate(raw)
    if again == pages: break
    pages = again
print('pages', n, json.dumps(pages, ensure_ascii=False))

reader = PdfReader(raw); writer = PdfWriter()
W, H = A4
for i, pg in enumerate(reader.pages):
    if i > 0:
        buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(float(pg.mediabox.width), float(pg.mediabox.height)))
        c.setFont('Helvetica', 7.5); c.setFillGray(0.45)
        c.drawString(34, 18, f'Inference Serving  ·  {AUTHOR}')
        c.drawRightString(float(pg.mediabox.width) - 34, 18, str(i + 1))
        c.setStrokeGray(0.8); c.setLineWidth(0.4); c.line(34, 28, float(pg.mediabox.width) - 34, 28)
        c.save(); buf.seek(0)
        pg.merge_page(PdfReader(buf).pages[0])
    writer.add_page(pg)
writer.add_metadata({'/Title': 'Inference Serving 全景：从指标、瓶颈到框架与生态', '/Author': AUTHOR, '/Subject': 'Inference serving interview notes', '/Creator': AUTHOR})
with open(OUT, 'wb') as f: writer.write(f)
print('wrote', OUT)
