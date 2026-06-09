from __future__ import annotations

from seat_reservation_system.seat_store import SeatStore
from seat_reservation_system.seats import SEAT_IDS

import tkinter as tk
from tkinter import ttk, font, simpledialog, messagebox, filedialog

import math

class ReservationApp:
    COL = 5

    def __init__(self, root: tk.Tk, store: SeatStore) -> None:

        self.store = store
        
        self.default_font = font.nametofont("TkDefaultFont")
        self.default_font.configure(family="NanumGothic", size=12)

        root.title("Seat Reservation System")

        ttk.Label(root, text="좌석 예약 시스템").pack(pady=16)

        container = ttk.Frame(root)
        container.pack(fill="both", expand=True)

        self.seat_frame = ttk.Frame(container)
        self.seat_frame.pack(fill="both", expand=True)

        self.stats_var = tk.StringVar(value="단어를 불러오는 중...")

        ttk.Label(root, textvariable=self.stats_var).pack(pady=(16, 6))

        ttk.Button(root, text="예약 내역 저장", command=self.save).pack(pady=16)

        self.reload()


    def reload(self) -> None:
        for widget in self.seat_frame.winfo_children():
            widget.destroy()

        for idx, s in enumerate(self.store.list_seats()):
            id = s[0]
            if s[1] is None:
                text = f"{id}"
            else:
                text = f"✓ {id}"

            ttk.Button(self.seat_frame, text=text, command=lambda seat=s: self.click(seat)).grid(
                row= idx // self.COL, column= idx % self.COL, padx=5, pady=5
            )


        stats = self.store.stats()
        self.stats_var.set(
            "Total: {total}, Reserved: {reserved}, Available: {available}".format(
                **stats
            )
        )


    def click(self, seat) -> None:
        if seat[1] is None:
            name = simpledialog.askstring("좌석 예약", "이름을 입력하세요")
            if name.strip():
                seat_id, name = self.store.reserve(seat[0], name)
                messagebox.showinfo("예약 완료", f"{seat_id}번 좌석에 {name} 으로 예약했습니다.")
            else:
                messagebox.showwarning("예약 불가", "이름을 입력해주세요.")

        else:
            result = messagebox.askyesno("예약 취소", f"{seat[0]}번 좌석에 {seat[1]} 으로 예약이 되어있습니다.\n취소하시겠습니까?")
            if result:
                seat_id, name = self.store.cancel(seat[0], seat[1])
                messagebox.showinfo("예약 완료", f"{seat_id}번 좌석의 {seat[1]} 의 예약을 취소했습니다.")

        self.reload()


    def save(self) -> None:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="예약 내역을 저장할 위치를 선택하세요"
        )

        if not file_path:
            return

        try:
            self.store.save(file_path)
        except Exception as e:
            messagebox.showerror("오류", f"저장 중 문제가 발생했습니다:\n{e}")