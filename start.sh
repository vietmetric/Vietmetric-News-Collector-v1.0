#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# Vietmetric News Collector - Khởi chạy ứng dụng
# ═══════════════════════════════════════════════════════════════

echo "=========================================="
echo "  Vietmetric News Collector v1.0"
echo "  Thu thap & Phan tich thong tin quoc te"
echo "=========================================="
echo ""

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "[LOI] Khong tim thay Python 3. Vui long cai dat Python 3.9+."
    exit 1
fi

cd "$(dirname "$0")"

# Cài đặt thư viện
echo "[1/3] Cai dat thu vien Python..."
pip install -r backend/requirements.txt --break-system-packages -q 2>/dev/null || \
pip install -r backend/requirements.txt -q

echo ""
echo "[2/3] Khoi dong server..."
echo ""
echo "  Giao dien web:  http://localhost:8000"
echo "  API docs:       http://localhost:8000/docs"
echo ""
echo "  Nhan Ctrl+C de dung server."
echo "=========================================="
echo ""

# Chạy server
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
