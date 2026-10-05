# TCVN 5687:2024 — Chương trình tra cứu & phân loại nhanh TG-ĐHKK

Chương trình dòng lệnh (chỉ dùng thư viện chuẩn Python, không cần cài thêm gì),
giúp tra cứu nhanh các số liệu hay dùng nhất của tiêu chuẩn TCVN 5687:2024
*Thông gió – Điều hòa không khí: Yêu cầu thiết kế*.

## Chạy chương trình

```bash
cd ~/workspace/tcvn5687
python3 tcvn5687.py            # mở menu tương tác
```

Hoặc gọi nhanh từng chức năng:

```bash
python3 tcvn5687.py dieu 6.2              # tra cứu điều 6.2 (hoặc bất kỳ số điều nào)
python3 tcvn5687.py dieu "thong gio su co"
python3 tcvn5687.py thuatngu "van khoi"   # tra cứu thuật ngữ Điều 3 (gõ không dấu vẫn được)
python3 tcvn5687.py giotuoi "phong hop"   # tra cứu + tính lưu lượng gió tươi (Bảng E.1)
python3 tcvn5687.py boiso "phong hoc"     # tra cứu + tính theo bội số trao đổi khí (Bảng F.1)
python3 tcvn5687.py thongso               # thông số tính toán trong nhà (Bảng A.1/A.2)
python3 tcvn5687.py phanloai              # lập phiếu phân loại hệ thống TG-ĐHKK (Điều 4.7)
python3 tcvn5687.py van                   # phân loại van gió / van khói / van ngăn cháy
python3 tcvn5687.py chongkhoi             # hệ thống chống khói Điều 7 + Bảng G.1/H.1
python3 tcvn5687.py rori                  # lượng gió rò rỉ qua khe hở ống gió (Bảng 1)
```

## Các chức năng chính

| # | Chức năng | Nguồn trong tiêu chuẩn |
|---|-----------|------------------------|
| 1 | Tra cứu 306 điều/mục/phụ lục theo số điều hoặc từ khóa | Mục lục + toàn văn |
| 2 | Tra cứu 36 thuật ngữ, định nghĩa | Điều 3 (trang 8–13) |
| 3 | Gió tươi theo loại phòng (55 loại) + **tính nhanh** m³/h theo số người/diện tích | Bảng E.1 (trang 70–72) |
| 4 | Bội số trao đổi không khí (14 loại) + **tính nhanh** m³/h theo thể tích phòng | Bảng F.1 (trang 73) |
| 5 | Nhiệt độ, độ ẩm, tốc độ gió tiện nghi/giới hạn theo mùa | Bảng A.1/A.2 (trang 39–41) |
| 6 | **Phiếu phân loại hệ thống**: 8 tiêu chí Điều 4.7.1 + cấp TSTT I/II/III (Điều 5.2.2), có lưu ra file | Điều 4.7, 5.2.2 |
| 7 | Phân loại van gió / van khói / van ngăn cháy (thường mở, thường đóng, kép) | Điều 3.32–3.34 |
| 8 | 12 hệ thống/thiết bị chống khói; chênh lệch áp suất; hệ số theo chiều rộng cửa | Điều 7, Bảng G.1 (tr.77), H.1 (tr.79) |
| 9 | Lượng gió rò rỉ/thâm nhập qua khe hở ống gió theo cấp độ kín và áp suất | Bảng 1 (trang 24) |
| 10 | Định hướng các bảng giới hạn tiếp xúc hóa chất/bụi | Phụ lục D (trang 66–69) |

## Lưu ý

- Tìm kiếm **không phân biệt dấu** tiếng Việt: gõ `phong ngu`, `van ngan chay` đều được.
- Trong phiếu phân loại (chức năng 6): mục **[TC]** là trích nguyên văn tiêu chuẩn,
  mục **[TK]** là gợi ý tham khảo thực tế thiết kế (tiêu chuẩn không liệt kê chi tiết).
- Hình 1 trong file gốc chỉ tồn tại dạng ảnh nên chương trình dùng 8 tiêu chí
  nguyên văn Điều 4.7.1 thay thế.
- Số liệu trong chương trình trích từ file `TCVN5687-ThongGio.DHKK-BanHanh.21022024.md`;
  khi cần viện dẫn chính thức, đối chiếu lại số trang ghi kèm mỗi kết quả.

## Web app tra cứu (mới)

Mở file **`web/index.html`** bằng trình duyệt (máy tính hoặc điện thoại) — 1 file duy
nhất, chạy **offline 100%**, không cần mạng, không cần Python. Làm theo kiểu repo
`Hvdo42/qcvn06-tra-cuu` (tab tra cứu theo đối tượng + tìm kiếm tự do + bảng tra).

5 tab:

1. **🏠 Theo phòng** — nhập tên phòng (gõ không dấu được) → gom toàn bộ yêu cầu áp
   dụng: gió tươi E.1, bội số F.1, thông số nhiệt–ẩm Phụ lục A, kèm ô tính nhanh.
2. **🧮 Tính nhanh** — 3 máy tính: gió tươi (E.1), bội số × thể tích (F.1),
   rò rỉ ống gió (Bảng 1, có gợi ý chọn cấp K/BT theo 6.11.8).
3. **🏷️ Phân loại** — wizard phân loại hệ thống TG-ĐHKK (8 bước, có nút chép phiếu)
   + phân loại van gió/van khói/van ngăn cháy.
4. **🔍 Tìm kiếm** — tìm tự do trong 306 điều khoản, 36 thuật ngữ, các bảng số liệu;
   lọc theo nhóm.
5. **📚 Bảng tra** — xem toàn bộ bảng E.1, F.1, A.1/A.2, G.1, H.1, phân loại van,
   hệ thống chống khói Điều 7, Phụ lục D.

Sửa giao diện: chỉnh `web/template.html` rồi chạy `python3 web/build.py` để build
lại `web/index.html` (dữ liệu được nhúng thẳng vào file).

## Cấu trúc thư mục

```
~/workspace/tcvn5687/
├── tcvn5687.py              # chương trình chính (CLI)
├── HUONG_DAN.md             # file này
├── data/
│   └── tcvn5687_data.json   # dữ liệu trích xuất từ tiêu chuẩn (14 nhóm)
└── web/
    ├── index.html           # web app 1 file, mở là chạy offline
    ├── template.html        # mã nguồn giao diện (sửa ở đây)
    └── build.py             # build index.html từ template + data
```
