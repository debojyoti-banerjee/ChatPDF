from core.pdf_loader import PDFLoaderManager
from core.exceptions import PDFLoadError

loader=PDFLoaderManager()

try:
    docs=loader.load_pdf(["Btechproj.pdf"])
    print(docs)
except PDFLoadError as e:
    print(e.message)
