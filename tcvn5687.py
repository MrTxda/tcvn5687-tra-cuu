#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TCVN 5687:2024 - Chuong trinh tra cuu & phan loai nhanh he thong TG-DHKK
(Thong gio - Dieu hoa khong khi / Ventilation and Air conditioning)

Chay:  python3 tcvn5687.py            -> che do menu tuong tac
      python3 tcvn5687.py giotuoi "phong hop"
      python3 tcvn5687.py dieu 6.2
      python3 tcvn5687.py thuatngu "van ngan chay"
      python3 tcvn5687.py boiso "phong hoc"
      python3 tcvn5687.py --help

Du lieu: data/tcvn5687_data.json (trich tu file TCVN5687-ThongGio.DHKK-BanHanh.21022024.md)
Chi dung thu vien chuan cua Python, khong can cai them gi.
"""

import json
import os
import sys
import textwrap
import unicodedata

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "tcvn5687_data.json")

try:
    with open(DATA_PATH, encoding="utf-8") as f:
        DATA = json.load(f)
except FileNotFoundError:
    sys.exit(f"Khong tim thay file du lieu: {DATA_PATH}")


# ---------------------------------------------------------------- Tien ich
def khong_dau(s):
    """Bo dau tieng Viet de tim kiem khong phan biet dau."""
    if s is None:
        return ""
    s = unicodedata.normalize("NFD", str(s)).replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in s if unicodedata.category(c) != "Mn").lower()


def parse_so(s):
    """'1,5' -> 1.5 ; '-' -> None ; '12-14' -> (12.0, 14.0)."""
    if s is None:
        return None
    s = str(s).strip().replace(",", ".")
    if s in ("", "-", "–", "—"):
        return None
    if "-" in s[1:]:
        parts = [p for p in s.replace("–", "-").replace("—", "-").split("-") if p.strip()]
        try:
            nums = [float(p) for p in parts]
        except ValueError:
            return None
        if len(nums) == 2:
            return (nums[0], nums[1])
        return None
    try:
        return float(s)
    except ValueError:
        return None


def fmt_so(x):
    if x is None:
        return "-"
    if isinstance(x, tuple):
        return f"{fmt_so(x[0])} - {fmt_so(x[1])}"
    return f"{x:g}"


def tieu_de(text, char="="):
    line = char * 64
    print(f"\n{line}\n{text}\n{line}")


def dong_ke():
    print("-" * 64)


def goi_y(text, width=64):
    for para in str(text).split("\n"):
        for ln in textwrap.wrap(para.strip(), width=width) if para.strip() else [""]:
            print("  " + ln)


def hoi(prompt, default=""):
    try:
        s = input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return default
    return s if s else default


def hoi_so(prompt):
    while True:
        s = hoi(prompt)
        v = parse_so(s)
        if isinstance(v, (int, float)):
            return float(v)
        print("  -> Nhap so (vd: 25 hoac 12,5).")


def tim_kiem(rows, keyword, fields):
    """Tim kiem khong dau, xep hang theo vi tri xuat hien."""
    kw = khong_dau(keyword)
    if not kw:
        return list(rows)
    kq = []
    for r in rows:
        hay = " ".join(khong_dau(r.get(f, "")) for f in fields)
        pos = hay.find(kw)
        if pos >= 0:
            kq.append((pos, r))
    kq.sort(key=lambda x: x[0])
    return [r for _, r in kq]


def chon_trong_danh_sach(items, hien_thi, tieu_de_text="Chon muc:"):
    """items: list; hien_thi(item)->str. Tra ve item hoac None."""
    print(f"\n{tieu_de_text}")
    for i, it in enumerate(items, 1):
        print(f"  {i}. {hien_thi(it)}")
    while True:
        s = hoi("Nhap so thu tu (Enter = huy): ")
        if not s:
            return None
        if s.isdigit() and 1 <= int(s) <= len(items):
            return items[int(s) - 1]
        print("  -> So khong hop le.")


# ------------------------------------------------- 1. Tra cuu dieu khoan
def tra_cuu_dieu(tu_khoa=None):
    clauses = DATA["clauses"]
    if tu_khoa is None:
        tu_khoa = hoi('Nhap so dieu (vd "6.2", "7.11") hoac tu khoa: ')
    if not tu_khoa:
        return
    kw = tu_khoa.strip()
    # Uu tien khop chinh xac so dieu
    chinh_xac = [c for c in clauses if khong_dau(c.get("so", "")) == khong_dau(kw)]
    if chinh_xac:
        kq = chinh_xac
    else:
        kq = tim_kiem(clauses, kw, ["so", "tieu_de"])[:20]
    if not kq:
        print(f'Khong tim thay dieu khoan nao voi "{tu_khoa}".')
        return
    tieu_de(f'TRA CUU DIEU KHOAN - "{tu_khoa}" ({len(kq)} ket qua)')
    for c in kq:
        dong_ke()
        print(f'Dieu {c.get("so")}: {c.get("tieu_de")}  [trang {c.get("trang")}]')
        if c.get("ghi_chu"):
            goi_y("Ghi chu: " + c["ghi_chu"])
    dong_ke()
    print("(Noi dung chi tiet xem trong file goc theo so trang.)")


# ------------------------------------------------- 2. Tra cuu thuat ngu
def tra_cuu_thuat_ngu(tu_khoa=None):
    terms = DATA["glossary"]
    if tu_khoa is None:
        tu_khoa = hoi('Nhap tu khoa (vd "van khoi", "thong gio"): ')
    if not tu_khoa:
        return
    kq = tim_kiem(terms, tu_khoa, ["ten_vi", "ten_en", "dinh_nghia"])[:15]
    if not kq:
        print(f'Khong tim thay thuat ngu nao voi "{tu_khoa}".')
        return
    tieu_de(f'THUAT NGU DIEU 3 - "{tu_khoa}" ({len(kq)} ket qua)')
    for t in kq:
        dong_ke()
        ten = t.get("ten_vi", "")
        en = t.get("ten_en", "")
        print(f'{t.get("so")}. {ten}' + (f" ({en})" if en else "") + f'  [trang {t.get("trang")}]')
        goi_y(t.get("dinh_nghia", ""))
    dong_ke()


# ------------------------------------------------- 3. Gio tuoi (Bang E.1)
def tra_cuu_gio_tuoi(tu_khoa=None):
    bang = DATA["bangE1"]
    rows = bang["hang"]
    if tu_khoa is None:
        tu_khoa = hoi('Nhap loai phong (vd "phong hop", "phong ngu", "nha bep"): ')
    if not tu_khoa:
        return
    kq = tim_kiem(rows, tu_khoa, ["ten_phong"])[:15]
    if not kq:
        print(f'Khong tim thay loai phong nao voi "{tu_khoa}".')
        return
    tieu_de("LUU LUONG GIO TUOI - BANG E.1 (trang 70-72)")
    for r in kq:
        dong_ke()
        print(f'* {r["ten_phong"]}')
        print(f'  Dien tich binh quan : {r["dien_tich_m2_nguoi"]} m2/nguoi')
        print(f'  Gio tuoi yeu cau    : {r["luong_kk_m3h_nguoi"]} m3/h.nguoi'
              f'  |  {r["luong_kk_m3h_m2"]} m3/h.m2')
        if r.get("ghi_chu"):
            goi_y("Ghi chu: " + r["ghi_chu"])
    dong_ke()

    chon = None
    if len(kq) == 1:
        chon = kq[0]
    elif hoi("Tinh nhanh luu luong cho 1 loai phong? (c/k): ", "k").lower().startswith("c"):
        chon = chon_trong_danh_sach(kq, lambda r: r["ten_phong"], "Chon loai phong de tinh:")
    if chon:
        tinh_gio_tuoi(chon)


def tinh_gio_tuoi(r):
    q_nguoi = parse_so(r["luong_kk_m3h_nguoi"])
    q_m2 = parse_so(r["luong_kk_m3h_m2"])
    print(f'\nTINH NHANH - {r["ten_phong"]}')
    if isinstance(q_nguoi, (int, float)):
        n = hoi_so("Nhap so nguoi su dung: ")
        q = q_nguoi * n
        print(f"=> Luu luong gio tuoi toi thieu: {fmt_so(q_nguoi)} x {fmt_so(n)}"
              f" = {fmt_so(q)} m3/h")
    elif isinstance(q_m2, (int, float)):
        s = hoi_so("Nhap dien tich san (m2): ")
        q = q_m2 * s
        print(f"=> Luu luong gio tuoi toi thieu: {fmt_so(q_m2)} x {fmt_so(s)}"
              f" = {fmt_so(q)} m3/h")
    else:
        print("Bang khong cho gia tri dinh luong cho loai phong nay.")
    print("(Theo Bang E.1, TCVN 5687:2024)")


# ------------------------------------------------- 4. Boi so trao doi KK (Bang F.1)
def tra_cuu_boi_so(tu_khoa=None):
    bang = DATA["bangF1"]
    rows = bang["hang"]
    if tu_khoa is None:
        tu_khoa = hoi('Nhap loai phong/cong trinh (vd "cong so", "phong hoc"): ')
    if not tu_khoa:
        return
    kq = tim_kiem(rows, tu_khoa, ["loai_phong_khong_gian"])[:15]
    if not kq:
        print(f'Khong tim thay voi "{tu_khoa}".')
        return
    tieu_de("SO LAN TRAO DOI KHONG KHI - BANG F.1 (trang 73)")
    for r in kq:
        dong_ke()
        print(f'* {r["loai_phong_khong_gian"]}: {r["so_lan_trao_doi"]} {r.get("don_vi", "lan/h")}')
        if r.get("ghi_chu"):
            goi_y("Ghi chu: " + r["ghi_chu"])
    dong_ke()

    chon = kq[0] if len(kq) == 1 else None
    if chon is None and hoi("Tinh nhanh luu luong thong gio? (c/k): ", "k").lower().startswith("c"):
        chon = chon_trong_danh_sach(kq, lambda r: r["loai_phong_khong_gian"])
    if chon:
        n = parse_so(chon["so_lan_trao_doi"])
        if isinstance(n, (int, float)):
            v = hoi_so("Nhap the tich phong (m3) [dai x rong x cao]: ")
            print(f"=> Luu luong thong gio: {fmt_so(n)} x {fmt_so(v)} = {fmt_so(n * v)} m3/h")
            print("(Theo Bang F.1, TCVN 5687:2024)")


# ------------------------------------------------- 5. Thong so tinh toan trong nha (A.1/A.2)
def tra_cuu_thong_so():
    tieu_de("THONG SO TINH TOAN KHONG KHI TRONG NHA (PHU LUC A)")
    print("  1. Bang A.1 - Nha o & cong trinh cong cong (trang 39)")
    print("  2. Bang A.2 - Cong trinh y te / dac thu (trang 40-41)")
    s = hoi("Chon bang (1/2): ", "1")
    bang = DATA["bangA1"] if s.strip() != "2" else DATA["bangA2"]
    rows = bang["hang"]
    # Gom cac lua chon 'mua'
    muas = []
    for r in rows:
        if r["mua"] not in muas:
            muas.append(r["mua"])
    mua = muas[0]
    if len(muas) > 1:
        print("\nChon dieu kien:")
        for i, m in enumerate(muas, 1):
            print(f"  {i}. {m}")
        s2 = hoi("Nhap so: ", "1")
        if s2.isdigit() and 1 <= int(s2) <= len(muas):
            mua = muas[int(s2) - 1]
    loc = [r for r in rows if r["mua"] == mua]
    tieu_de(f'{mua.upper()} ({len(loc)} muc)')
    for r in loc:
        dong_ke()
        print(f'* {r["phong"]}')
        print(f'  Nhiet do tien nghi : {r["nhiet_do_tien_nghi"]} °C'
              f'   | Gioi han cho phep: {r["nhiet_do_gioi_han_cho_phep"]} °C')
        print(f'  Toc do gio tien nghi: {r["toc_do_gio_tien_nghi"]} m/s'
              f' | Toi da cho phep: {r["toc_do_gio_toi_da_cho_phep"]} m/s')
        print(f'  Do am tuong doi   : {r["do_am_tuong_doi"]} %')
    dong_ke()


# ------------------------------------------------- 6. Phan loai he thong TG-DHKK
def phan_loai_he_thong():
    tieu_de("PHAN LOAI HE THONG TG-DHKK (Dieu 4.7, Hinh 1 - trang 15,16)")
    print("Tra loi cac cau hoi de lap PHIEU PHAN LOAI he thong.")
    print("(Cac muc co chu [TC] la trich nguyen van tieu chuan;\n"
          " muc [TK] la goi y tham khao thuc te thiet ke.)")
    phieu = {}

    # a - nguyen van
    print('\n[TC] a) Muc dich su dung:')
    print("  1. Dieu hoa tien nghi")
    print("  2. Dieu hoa cong nghe")
    s = hoi("Chon (1/2): ", "1")
    phieu["a) Muc dich su dung [TC]"] = "Dieu hoa tien nghi" if s.strip() != "2" else "Dieu hoa cong nghe"

    # Cap TSTT theo 5.2.2 - nguyen van
    print("\n[TC] Cap TSTT ngoai troi (Dieu 5.2.2):")
    print("  1. Cap I   (m = 35 h/nam; Kbd = 0,996) - cong trinh co cong nang dac biet quan trong")
    print("  2. Cap II  (m = 150-200 h/nam; Kbd = 0,983-0,977) - cong trinh cong nang thong thuong")
    print("  3. Cap III (m = 350-400 h/nam; Kbd = 0,960-0,954) - khong doi hoi cao ve nhiet am")
    s = hoi("Chon (1/2/3): ", "2")
    cap = {"1": "Cap I", "2": "Cap II", "3": "Cap III"}.get(s.strip(), "Cap II")
    phieu["Cap TSTT ngoai troi (5.2.2) [TC]"] = cap

    # b - tinh chat quan trong: suy tu cap
    phieu["b) Tinh chat quan trong [TC]"] = {"Cap I": "Dac biet quan trong",
                                             "Cap II": "Thong thuong",
                                             "Cap III": "Khong doi hoi cao"}[cap]

    # c - tinh tap trung
    print("\n[TK] c) Tinh tap trung:")
    print("  1. Tap trung (trung tam - 1 gian may cap cho nhieu phong/khu vuc)")
    print("  2. Cuc bo (doc lap tung phong - vd: may lanh cuc bo, multi)")
    s = hoi("Chon (1/2): ", "1")
    phieu["c) Tinh tap trung [TK]"] = "Tap trung (trung tam)" if s.strip() != "2" else "Cuc bo"

    # d - cach lam lanh
    print("\n[TK] d) Cach lam lanh khong khi:")
    print("  1. Gian tiep qua nuoc lanh (chiller / AHU, FCU)")
    print("  2. Truc tiep bang moi chat lanh bay hoi (DX, VRV/VRF, may lanh cuc bo)")
    s = hoi("Chon (1/2): ", "1")
    phieu["d) Cach lam lanh khong khi [TK]"] = ("Gian tiep (nuoc lanh)"
                                                if s.strip() != "2" else "Truc tiep (DX/VRV/VRF)")

    # e - cach phan phoi
    print("\n[TK] e) Cach phan phoi khong khi:")
    print("  1. Toan gio (all-air)")
    print("  2. Gio - nuoc (air-water, vd: FCU + gio tuoi trung tam)")
    s = hoi("Chon (1/2): ", "1")
    phieu["e) Cach phan phoi khong khi [TK]"] = "Toan gio" if s.strip() != "2" else "Gio - nuoc"

    # f - nang suat lanh: tu nhap
    ns = hoi("\n[TK] f) Nang suat lanh (kW hoac TR, Enter de bo qua): ")
    phieu["f) Nang suat lanh [TK]"] = ns if ns else "(chua xac dinh)"

    # g - nguyen van
    print("\n[TC] g) Chuc nang:")
    print("  1. Chi lam lanh")
    print("  2. Lam lanh va suoi am")
    s = hoi("Chon (1/2): ", "1")
    phieu["g) Chuc nang [TC]"] = "Chi lam lanh" if s.strip() != "2" else "Lam lanh va suoi am"

    # h - cach bo tri dan lanh: tu nhap
    dl = hoi("\n[TK] h) Cach bo tri dan lanh (vd: am tran noi ong gio / treo tuong / dat san / cassette): ")
    phieu["h) Cach bo tri dan lanh [TK]"] = dl if dl else "(chua xac dinh)"

    tieu_de("PHIEU PHAN LOAI HE THONG TG-DHKK")
    for k, v in phieu.items():
        print(f"- {k}: {v}")
    dong_ke()
    print("Can cu: Dieu 4.7.1 (a-h), Dieu 5.2.2, Hinh 1 - TCVN 5687:2024.")
    if hoi("\nLuu phieu ra file text? (c/k): ", "k").lower().startswith("c"):
        ten = hoi("Ten file (vd phieu_phan_loai.txt): ", "phieu_phan_loai.txt")
        with open(ten, "w", encoding="utf-8") as f:
            f.write("PHIEU PHAN LOAI HE THONG TG-DHKK (TCVN 5687:2024)\n")
            f.write("=" * 60 + "\n")
            for k, v in phieu.items():
                f.write(f"- {k}: {v}\n")
            f.write("Can cu: Dieu 4.7.1 (a-h), Dieu 5.2.2, Hinh 1.\n")
        print(f"Da luu: {os.path.abspath(ten)}")


# ------------------------------------------------- 7. Phan loai van
def phan_loai_van():
    tieu_de("PHAN LOAI VAN (Dieu 3.32 - 3.34)")
    print("Tra loi de xac dinh loai van theo tieu chuan:")
    print("  1. Van phan nhanh ong gio tai moi tang tu ong gom dung,")
    print("     ngan khoi quay nguoc vao ong gom -> VAN GIO (Damper, 3.32)")
    print("  2. Van tren lo mo gieng hut khoi o hanh lang/sanh,")
    print("     thuong DONG, chiu lua E -> VAN KHOI (Smoke damper, 3.33)")
    print("  3. Van che chan kenh thong gio / lo mo ket cau bao che,")
    print("     chiu lua EI -> VAN NGAN CHAY (Fire damper, 3.34)")
    s = hoi("Van cua ban thuoc truong hop nao (1/2/3): ", "3")
    v = DATA["van_types"]
    if s.strip() == "1":
        t = v[0]
    elif s.strip() == "2":
        t = v[1]
    else:
        t = v[2]
    dong_ke()
    print(f'* {t["loai_van"]}')
    goi_y(t["dinh_nghia"])
    if t.get("cac_dang_con"):
        print("\n  Cac dang con:")
        for d_ in t["cac_dang_con"]:
            print(f"   - {d_}")
    elif "ngan chay" in khong_dau(t["loai_van"]):
        print("\n  Van ngan chay gom 3 dang (3.34):")
        print("   - Van ngan chay thuong MO (dong khi co chay)")
        print("   - Van ngan chay thuong DONG (mo khi co chay hoac sau chay)")
        print("   - Van ngan chay KEP (dong khi co chay va mo sau chay)")
    dong_ke()


# ------------------------------------------------- 8. Bao ve chong khoi (Dieu 7)
def chong_khoi():
    while True:
        tieu_de("BAO VE CHONG KHOI KHI CO CHAY (Dieu 7)", char="-")
        print("  1. Liet ke cac he thong/thiet bi chong khoi (Dieu 7)")
        print("  2. Tra cuu chenh lech ap suat - Bang G.1 (trang 77)")
        print("  3. Tra cuu he so theo chieu rong cua - Bang H.1 (trang 79)")
        print("  0. Quay lai")
        s = hoi("Chon: ", "0")
        if s == "1":
            systems = DATA["dieu7_systems"]
            tieu_de(f"HE THONG CHONG KHOI - DIEU 7 ({len(systems)} muc)")
            for i, x in enumerate(systems, 1):
                dong_ke()
                print(f"{i}. {x['loai_he_thong']}  [{x.get('dieu_khoan', '')}]")
                goi_y(x.get("mo_ta_ngan", ""))
            dong_ke()
        elif s == "2":
            bang = DATA["bangG1"]
            print("\nBang G.1 - Chenh lech ap suat qua cac bo phan can khoi:")
            for r in bang["hang"]:
                dong_ke()
                print(f'* {r["doi_tuong"]} | Tran cao {r["chieu_cao_tran"]} m'
                      f' -> {r["chenh_lech_ap_suat"]} {r.get("don_vi", "Pa")}')
                if r.get("ghi_chu"):
                    goi_y("Ghi chu: " + r["ghi_chu"])
            dong_ke()
        elif s == "3":
            bang = DATA["bangH1"]
            rows = bang["hang"]
            print("\nLoai cong trinh: 1. Nha o   2. Nha cong cong")
            s2 = hoi("Chon (1/2): ", "1")
            loai = "Nha o" if s2.strip() != "2" else "Nha cong cong"
            loc = [r for r in rows if khong_dau(loai) in khong_dau(r.get("loai_cong_trinh", ""))]
            tieu_de(f"BANG H.1 - HE SO THEO CHIEU RONG CUA ({loai.upper()})")
            for r in loc:
                print(f'  Cua rong {r["chieu_rong_cua"]}: he so = {r["he_so"]}')
            dong_ke()
        else:
            return


# ------------------------------------------------- 9. Ro ri ong gio (Bang 1)
def tra_cuu_ro_ri():
    bang = DATA["bang1"]
    print(f'\n{bang["tieu_de"]} [trang {bang.get("trang")}]')
    print(f'Don vi: {bang.get("don_vi_cot_gia_tri")}')
    print("Cap do kin: 1. BT   2. K")
    s = hoi("Chon cap do kin (1/2): ", "1")
    cap = "BT" if s.strip() != "2" else "K"
    row = next((r for r in bang["hang"] if r.get("cap_do_kin") == cap), None)
    if not row:
        print("Khong co du lieu.")
        return
    p = hoi_so("Nhap ap suat tinh du tai vi tri sat quat (Pa): ")
    cols = [c for c in bang["cot"][1:] if parse_so(c) is not None]
    gan = min(cols, key=lambda c: abs(parse_so(c) - p))
    gt = row["gia_tri"].get(gan)
    print(f"=> Cap {cap}, ap suat gan nhat {gan} Pa: {gt} m3/h cho 1 m2 dien tich khai trien ong")
    if bang.get("ghi_chu"):
        goi_y("Ghi chu: " + str(bang["ghi_chu"])[:400])


# ------------------------------------------------- 10. Bang D (dinh huong)
def bang_d_info():
    tieu_de("CAC BANG PHU LUC D - GIOI HAN TIEP XUC (trang 66-69)")
    for b in DATA["bangD"]:
        dong_ke()
        print(f'* {b["ten_bang"]}: {b["tieu_de"]}')
        print(f'  Trang {b["trang"]} - {b["so_hang"]} hang')
    dong_ke()
    print("Chi tiet tung chat xem truc tiep trong file tieu chuan theo so trang.")


# ------------------------------------------------- Menu & CLI
def menu():
    while True:
        tieu_de("TCVN 5687:2024 - TRA CUU & PHAN LOAI NHANH TG-DHKK")
        print("  1. Tra cuu dieu khoan (theo so dieu / tu khoa)")
        print("  2. Tra cuu thuat ngu (Dieu 3)")
        print("  3. Gio tuoi theo loai phong + tinh nhanh (Bang E.1)")
        print("  4. Boi so trao doi khong khi + tinh nhanh (Bang F.1)")
        print("  5. Thong so tinh toan trong nha (Bang A.1 / A.2)")
        print("  6. Phan loai he thong TG-DHKK (Dieu 4.7)")
        print("  7. Phan loai van: van gio / van khoi / van ngan chay")
        print("  8. Bao ve chong khoi khi co chay (Dieu 7, Bang G.1/H.1)")
        print("  9. Luong gio ro ri ong gio (Bang 1)")
        print("  10. Bang gioi han tiep xuc hoa chat/bui (Phu luc D)")
        print("  0. Thoat")
        s = hoi("Chon chuc nang: ", "0")
        if s == "1":
            tra_cuu_dieu()
        elif s == "2":
            tra_cuu_thuat_ngu()
        elif s == "3":
            tra_cuu_gio_tuoi()
        elif s == "4":
            tra_cuu_boi_so()
        elif s == "5":
            tra_cuu_thong_so()
        elif s == "6":
            phan_loai_he_thong()
        elif s == "7":
            phan_loai_van()
        elif s == "8":
            chong_khoi()
        elif s == "9":
            tra_cuu_ro_ri()
        elif s == "10":
            bang_d_info()
        elif s == "0":
            print("Tam biet!")
            return
        else:
            print("Lua chon khong hop le.")
        hoi("\nNhan Enter de tiep tuc...")


def in_huong_dan():
    print(__doc__)


def main(argv):
    if len(argv) == 1:
        menu()
        return
    cmd = khong_dau(argv[1])
    arg = " ".join(argv[2:]).strip() or None
    if cmd in ("-h", "--help", "help"):
        in_huong_dan()
    elif cmd in ("dieu", "dieukhoan"):
        tra_cuu_dieu(arg)
    elif cmd in ("thuatngu", "thuat_ngu", "glossary"):
        tra_cuu_thuat_ngu(arg)
    elif cmd in ("giotuoi", "gio_tuoi", "e1"):
        tra_cuu_gio_tuoi(arg)
    elif cmd in ("boiso", "boi_so", "f1"):
        tra_cuu_boi_so(arg)
    elif cmd in ("thongso", "thong_so", "a1", "a2"):
        tra_cuu_thong_so()
    elif cmd in ("phanloai", "phan_loai"):
        phan_loai_he_thong()
    elif cmd == "van":
        phan_loai_van()
    elif cmd in ("chongkhoi", "chong_khoi", "khoi"):
        chong_khoi()
    elif cmd in ("rori", "ro_ri", "bang1"):
        tra_cuu_ro_ri()
    elif cmd == "menu":
        menu()
    else:
        print(f"Lenh khong ro: {argv[1]}")
        in_huong_dan()


if __name__ == "__main__":
    main(sys.argv)
