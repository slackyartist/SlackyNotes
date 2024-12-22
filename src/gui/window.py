import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import fitz


class Window:

    _default_width = 720
    _default_height = 720
    _window = None
    _header = None
    _body = None
    _footer = None
    _pdf_path = ""
    _pdf_document = None
    _page_number = 0
    _image_tk = None

    def __init__(self):
        self._window = tk.Tk()
        self._window.title("SlackyNotes")
        self._window.geometry(f"{str(self._default_width)}x{str(self._default_height)}")
        self._render_window()
        self._window.mainloop()

    def _render_window(self):
        for child in self._window.winfo_children():
            child.destroy()

        self._header = tk.Frame(
            self._window,
        )
        self._body = tk.Frame(
            self._window,
        )
        self._footer = tk.Frame(
            self._window,
        )

        self._header.pack(fill="x")
        self._body.pack(fill="both", expand=True)
        self._footer.pack(fill="x")

        self._render_header()
        self._render_body()
        self._render_footer()

    def _render_header(self):
        for child in self._header.winfo_children():
            child.destroy()

        left_buttons = [
            tk.Button(
                self._header,
                text="Open PDF",
                command=self._command_open_pdf,
            ),
            tk.Button(
                self._header,
                text="Highlight Text",
            ),
            tk.Button(
                self._header,
                text="Add Text",
            ),
            tk.Button(
                self._header,
                text="Erase",
            ),
        ]
        right_buttons = [
            tk.Button(
                self._header,
                text="Save PDF",
            ),
        ]

        for button in left_buttons:
            button.pack(side="left")
        for button in right_buttons:
            button.pack(side="right")

    def _render_body(self):
        for child in self._body.winfo_children():
            child.destroy()

        if not self._pdf_document:
            return

        canvas = tk.Canvas(self._body)
        canvas.pack(fill="both", expand=True)

        scroll = tk.Scrollbar(
            canvas,
            orient="vertical",
            command=canvas.yview,
        )
        scroll.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scroll.set)

        frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=frame, anchor="nw")

        page = self._pdf_document.load_page(self._page_number)
        pixmap = page.get_pixmap()
        image = Image.frombytes("RGB", [pixmap.width, pixmap.height], pixmap.samples)
        self._image_tk = ImageTk.PhotoImage(image)

        label = tk.Label(frame, image=self._image_tk)
        label.pack()

        frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))


    def _render_footer(self):
        for child in self._footer.winfo_children():
            child.destroy()

        if not self._pdf_document:
            return

        elements = [
            tk.Button(
                self._footer,
                text="Previous",
                command=self._command_previous_page,
            ),
            tk.Button(
                self._footer,
                text="Next",
                command=self._command_next_page,
            ),
            tk.Label(
                self._footer,
                text=f"Page Number: {self._page_number + 1}",
            ),
        ]

        for element in elements:
            element.pack(side="left")

    def _command_open_pdf(self):
        pdf_files = filedialog.askopenfilenames(
            title="Open PDF file",
            filetypes=[("PDF files", "*.pdf")],
        )

        if not pdf_files:
            return

        self._pdf_path = pdf_files[0]
        try:
            self._pdf_document = fitz.open(self._pdf_path)
        except Exception as e:
            print(f"Error opening PDF: {e}")
            return

        self._page_number = 0
        self._render_body()
        self._render_footer()

    def _command_next_page(self):
        if self._page_number < len(self._pdf_document) - 1:
            self._page_number += 1
            self._render_body()
            self._render_footer()

    def _command_previous_page(self):
        if self._page_number > 0:
            self._page_number -= 1
            self._render_body()
            self._render_footer()
