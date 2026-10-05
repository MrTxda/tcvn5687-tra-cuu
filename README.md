# TCVN 5687:2024 — Tra cứu nhanh TG-ĐHKK

Công cụ tra cứu nhanh tiêu chuẩn **TCVN 5687:2024** *Thông gió – Điều hòa không khí: Yêu cầu thiết kế*,
gồm **web app** (dùng trên trình duyệt, offline 100%) và **chương trình dòng lệnh Python**.

## Dùng online

🌐 **https://mrtxda.github.io/tcvn5687-tra-cuu/**

*(Bật GitHub Pages cho repo: Settings → Pages → Deploy from a branch → main / (root). Repo private cần tài khoản Pro mới dùng được Pages; nếu không, chuyển repo sang Public.)*

## Dùng offline (không cần mạng)

Tải file `web/index.html` (bản 1 file duy nhất, dữ liệu nhúng sẵn) về máy/điện thoại → mở bằng trình duyệt là dùng ngay.

Hoặc tự build từ mã nguồn:

```bash
git clone https://github.com/MrTxda/tcvn5687-tra-cuu.git
cd tcvn5687-tra-cuu
python3 web/build.py            # -> web/index.html (bản offline 1 file)
python3 web/build.py --split    # -> index.html + data/tcvn5687_data.js (bản online)
```

## Tuyên bố miễn trách nhiệm

> Công cụ này chỉ phục vụ mục đích **tra cứu nhanh và tham khảo cá nhân**.
>
> - **Không thể thay thế** văn bản TCVN 5687:2024 chính thức.
> - **Không sử dụng làm căn cứ** khi thiết kế/thẩm duyệt hồ sơ.
> - Luôn đối chiếu với văn bản gốc theo số trang ghi kèm mỗi kết quả.

## Dùng web app

Mở file [`web/index.html`](web/index.html) bằng trình duyệt (máy tính/điện thoại) — 1 file duy nhất, không cần mạng, không cần cài đặt. Trên GitHub, bản online dùng file [`index.html`](index.html) ở thư mục gốc (nạp dữ liệu từ `data/tcvn5687_data.js`, cùng nội dung).

| Tab | Chức năng |
|-----|-----------|
| 🏠 Theo phòng | Nhập tên phòng (gõ không dấu được) → gom toàn bộ yêu cầu áp dụng: gió tươi (E.1), bội số trao đổi khí (F.1), thông số nhiệt–ẩm (Phụ lục A), kèm ô tính nhanh |
| 🧮 Tính nhanh | 3 máy tính: gió tươi theo người/diện tích, bội số × thể tích, rò rỉ ống gió Bảng 1 |
| 🏷️ Phân loại | Wizard 8 bước lập phiếu phân loại hệ thống TG-ĐHKK (Điều 4.7.1 + cấp TSTT 5.2.2) + phân loại van gió/van khói/van ngăn cháy |
| 🔍 Tìm kiếm | Tìm tự do trong 306 điều khoản, 36 thuật ngữ, toàn bộ bảng số liệu |
| 📚 Bảng tra | Xem trọn các bảng E.1, F.1, A.1/A.2, G.1, H.1, phân loại van, hệ thống chống khói Điều 7 |

Sửa giao diện: chỉnh `web/template.html` rồi chạy `python3 web/build.py` để build lại `web/index.html`
(dữ liệu được nhúng thẳng vào file duy nhất).

## Dùng dòng lệnh (Python, không cần cài thêm gì)

```bash
python3 tcvn5687.py                  # menu tương tác
python3 tcvn5687.py giotuoi "phong hop"
python3 tcvn5687.py dieu 6.2
python3 tcvn5687.py thuatngu "van khoi"
python3 tcvn5687.py boiso "phong hoc"
python3 tcvn5687.py phanloai
```

## Nguồn dữ liệu

`data/tcvn5687_data.json` — trích xuất có cấu trúc từ văn bản TCVN 5687:2024 (Xuất bản lần 1, Hà Nội 2024):
306 điều khoản/mục, 36 thuật ngữ Điều 3, Bảng E.1 (55 loại phòng), F.1, A.1/A.2, G.1, H.1,
Bảng 1 (rò rỉ ống gió), phân loại van (3.32–3.34), 12 hệ thống chống khói Điều 7.

Chi tiết xem [HUONG_DAN.md](HUONG_DAN.md).
