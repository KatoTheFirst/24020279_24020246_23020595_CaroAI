# Caro AI

Ứng dụng chơi cờ Caro với trí tuệ nhân tạo sử dụng thuật toán Minimax kết hợp Alpha-Beta Pruning.

---

## Yêu cầu hệ thống

- Python 3.10 trở lên
- Tkinter (thường đã có sẵn khi cài Python)

Kiểm tra bằng lệnh:

```bash
python --version
python -m tkinter
```

---

## Cài đặt

**Bước 1 — Tải source code**

```bash
git clone https://github.com/your-repo/caro-ai.git
cd caro-ai
```

**Bước 2 — Cài thư viện kiểm thử** *(chỉ cần nếu muốn chạy test)*

```bash
pip install pytest
```

---

## Chạy chương trình

```bash
python main_gui.py
```

Giao diện đồ họa sẽ mở ra. Người chơi đóng vai **X** và đi trước, AI đóng vai **O**.

---

## Chạy kiểm thử

**Chạy toàn bộ test cases:**

```bash
python -m pytest tests/ -v
```

**Chạy riêng từng module:**

```bash
# Test logic game
python -m pytest tests/test_logic.py -v

# Test AI agent
python -m pytest tests/test_minimax_lv2.py -v
```

**Kết quả mong đợi:** 83 PASSED, 2 XFAIL (bug đã ghi nhận, không phải lỗi).

---

## Đánh giá trọng số AI

Để so sánh hiệu quả các bộ trọng số hàm đánh giá bằng cách cho AI tự đấu với nhau:

```bash
python benchmark_weights.py
```

Chương trình sẽ chạy vòng tròn giữa 6 bộ trọng số (~30 ván, mất khoảng 1–2 phút) và in ra bảng xếp hạng. Để thêm bộ trọng số mới, chỉnh danh sách `CANDIDATES` trong file `benchmark_weights.py`.

---

## Cấu trúc thư mục

```
caro-ai/
├── main_gui.py              # Điểm khởi chạy chương trình
├── gui.py                   # Giao diện đồ họa Tkinter
├── benchmark_weights.py     # Công cụ đánh giá trọng số AI
├── pytest.ini               # Cấu hình pytest
├── caro_ai/
│   ├── logic.py             # Logic game (bàn cờ, thắng/thua/hòa)
│   └── ai/
│       └── minimax_lv2.py   # AI agent (Minimax + Alpha-Beta)
└── tests/
    ├── test_logic.py        # 44 test cases cho logic game
    └── test_minimax_lv2.py  # 41 test cases cho AI agent
```
