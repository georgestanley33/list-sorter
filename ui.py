import time
import customtkinter as ctk
from tkinter import messagebox

# ---- IMPORT YOUR SORT FUNCTIONS HERE ----
# Adjust these imports to match your project structure.
# If your functions are inside main.py, you can do:
# from main import BubbleSort, InsertionSort, SelectionSort, MergeSort, QuickSort
#
# IMPORTANT: if you run ui.py and it imports main.py, make sure main.py
# does NOT auto-run the CLI menu on import. Wrap CLI code in:
# if __name__ == "__main__": ...

from main import BubbleSort, InsertionSort, SelectionSort, MergeSort, QuickSort  # edit if needed


def parse_numbers(text: str) -> list[int]:
    # Accept: "3 10 5" (spaces) and also "3,10,5" (commas)
    cleaned = text.replace(",", " ").strip()
    if not cleaned:
        raise ValueError("Please enter at least one number.")
    return [int(x) for x in cleaned.split()]


def run_sort(method_key: str, data: list[int]) -> tuple[list[int], float]:
    """
    Returns (sorted_list, seconds_elapsed)
    Handles both:
      - functions that return a new list
      - functions that sort in-place and return None
    """
    arr = data.copy()

    start = time.perf_counter()

    if method_key == "bubble":
        out = BubbleSort(arr)
    elif method_key == "insertion":
        out = InsertionSort(arr)
    elif method_key == "selection":
        out = SelectionSort(arr)
    elif method_key == "merge":
        out = MergeSort(arr)
    elif method_key == "quick":
        # If your QuickSort signature is QuickSort(arr, low, high)
        out = QuickSort(arr, 0, len(arr) - 1)
    elif method_key == "python":
        out = sorted(arr)
    else:
        raise ValueError("Unknown method.")

    end = time.perf_counter()

    sorted_arr = out if out is not None else arr
    return sorted_arr, (end - start)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title("Python List Sorter")
        self.geometry("920x560")
        self.minsize(920, 560)

        # ---- Layout ----
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(self, corner_radius=16)
        left.grid(row=0, column=0, padx=18, pady=18, sticky="nsew")
        left.grid_columnconfigure(0, weight=1)

        right = ctk.CTkFrame(self, corner_radius=16)
        right.grid(row=0, column=1, padx=(0, 18), pady=18, sticky="nsew")
        right.grid_columnconfigure(0, weight=1)
        right.grid_rowconfigure(2, weight=1)

        # ---- Left panel ----
        title = ctk.CTkLabel(left, text="Python Sorting Comparison", font=ctk.CTkFont(size=22, weight="bold"))
        title.grid(row=0, column=0, padx=18, pady=(18, 8), sticky="w")

        desc = ctk.CTkLabel(
            left,
            text="Enter numbers, choose an algorithm, and compare timings.\nYou can also run all algorithms on the same input.",
            justify="left",
            text_color=("gray70", "gray70")
        )
        desc.grid(row=1, column=0, padx=18, pady=(0, 14), sticky="w")

        ctk.CTkLabel(left, text="Numbers (space or comma separated)", anchor="w").grid(
            row=2, column=0, padx=18, pady=(6, 6), sticky="ew"
        )
        self.input_box = ctk.CTkTextbox(left, height=90, corner_radius=12)
        self.input_box.grid(row=3, column=0, padx=18, pady=(0, 12), sticky="ew")
        self.input_box.insert("1.0", "3 135 6 6 31 36")

        ctk.CTkLabel(left, text="Algorithm", anchor="w").grid(row=4, column=0, padx=18, pady=(6, 6), sticky="ew")

        self.method_var = ctk.StringVar(value="python")
        self.method_menu = ctk.CTkOptionMenu(
            left,
            values=["python", "bubble", "insertion", "selection", "merge", "quick"],
            variable=self.method_var,
            corner_radius=12
        )
        self.method_menu.grid(row=5, column=0, padx=18, pady=(0, 12), sticky="ew")

        btn_row = ctk.CTkFrame(left, fg_color="transparent")
        btn_row.grid(row=6, column=0, padx=18, pady=(4, 18), sticky="ew")
        btn_row.grid_columnconfigure(0, weight=1)
        btn_row.grid_columnconfigure(1, weight=1)

        self.sort_btn = ctk.CTkButton(btn_row, text="Run Selected", corner_radius=12, command=self.on_run_selected)
        self.sort_btn.grid(row=0, column=0, padx=(0, 10), pady=0, sticky="ew")

        self.all_btn = ctk.CTkButton(btn_row, text="Run All (Compare)", corner_radius=12, command=self.on_run_all)
        self.all_btn.grid(row=0, column=1, padx=(10, 0), pady=0, sticky="ew")

        self.confirm_var = ctk.BooleanVar(value=True)
        self.confirm_check = ctk.CTkCheckBox(left, text="Confirm before running", variable=self.confirm_var)
        self.confirm_check.grid(row=7, column=0, padx=18, pady=(0, 18), sticky="w")

        # ---- Right panel ----
        ctk.CTkLabel(right, text="Output", font=ctk.CTkFont(size=18, weight="bold")).grid(
            row=0, column=0, padx=18, pady=(18, 8), sticky="w"
        )

        self.status = ctk.CTkLabel(right, text="Ready", text_color=("gray70", "gray70"))
        self.status.grid(row=1, column=0, padx=18, pady=(0, 10), sticky="w")

        self.output = ctk.CTkTextbox(right, corner_radius=12)
        self.output.grid(row=2, column=0, padx=18, pady=(0, 18), sticky="nsew")

        self.write_output("Enter numbers and run a sort.\n")

    def confirm(self, msg: str) -> bool:
        if not self.confirm_var.get():
            return True
        return messagebox.askyesno("Confirm", msg)

    def write_output(self, text: str):
        self.output.insert("end", text)
        self.output.see("end")

    def clear_output(self):
        self.output.delete("1.0", "end")

    def get_numbers(self) -> list[int]:
        raw = self.input_box.get("1.0", "end").strip()
        return parse_numbers(raw)

    def on_run_selected(self):
        try:
            data = self.get_numbers()
            method = self.method_var.get()

            if not self.confirm(f"Run '{method}' on:\n{data}\n\nProceed?"):
                self.status.configure(text="Cancelled")
                return

            self.status.configure(text="Running...")
            self.update_idletasks()

            sorted_list, secs = run_sort(method, data)

            self.clear_output()
            self.write_output(f"Method: {method}\n")
            self.write_output(f"Input:  {data}\n")
            self.write_output(f"Output: {sorted_list}\n")
            self.write_output(f"Time:   {secs * 1000:.3f} ms\n")

            self.status.configure(text="Done")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.configure(text="Error")

    def on_run_all(self):
        try:
            data = self.get_numbers()

            if not self.confirm(f"Run ALL algorithms on:\n{data}\n\nProceed?"):
                self.status.configure(text="Cancelled")
                return

            self.status.configure(text="Running all...")
            self.update_idletasks()

            methods = ["python", "bubble", "insertion", "selection", "merge", "quick"]
            results = []

            for m in methods:
                sorted_list, secs = run_sort(m, data)
                results.append((m, secs, sorted_list))

            results.sort(key=lambda x: x[1])

            self.clear_output()
            self.write_output("Results (fastest first)\n")
            self.write_output("-" * 60 + "\n")

            for m, secs, sorted_list in results:
                self.write_output(f"{m:<10}  {secs * 1000:>10.3f} ms  ->  {sorted_list}\n")

            self.status.configure(text="Done")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status.configure(text="Error")


if __name__ == "__main__":
    app = App()
    app.mainloop()