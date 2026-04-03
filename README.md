# Vietmetric News Collector - Thu thap va phan tich thong tin quoc te

He thong thu thap va phan tich thong tin quoc te phuc vu an ninh doi ngoai Viet Nam.

## Tinh nang

- Thu thap tu 30+ nguon quoc te da ngon ngu (Anh, Phap, Nga, Trung, Han, Nhat, Tay Ban Nha)
- Tich hop GDELT, Reddit, nguon tinh bao mo (OSINT)
- Phan tich tu dong: danh gia muc do de doa, trich xuat thuc the, chu de noi bat
- Upload file .docx, .pdf de trich xuat tu khoa
- Xuat bao cao .docx va .pdf
- Giao dien tieng Viet

## Cai dat va chay

```bash
chmod +x start.sh
./start.sh
```

Hoac chay thu cong:

```bash
pip install -r backend/requirements.txt
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Truy cap: http://localhost:8000

## Cau truc

```
osint-app/
  backend/
    main.py          # FastAPI server
    collector.py     # Module thu thap tin
    analyzer.py      # Module phan tich
    exporter.py      # Xuat bao cao .docx, .pdf
    sources.py       # Danh sach 30+ nguon tin
    requirements.txt
  frontend/
    index.html       # Giao dien web (single-page)
  start.sh           # Script khoi chay
```

## API Endpoints

- GET  /api/sources          - Danh sach nguon tin
- POST /api/collect          - Thu thap va phan tich
- POST /api/upload           - Upload file dau vao
- POST /api/export/docx      - Xuat bao cao Word
- POST /api/export/pdf       - Xuat bao cao PDF
- POST /api/export/cached/*  - Xuat tu du lieu da cache

## Tac gia

Vietmetric
