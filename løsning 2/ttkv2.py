import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class GuiApp:
    def __init__(self):
        self._root = ttk.Window(
            title="Command Style GUI",
            themename="flatly",
            size=(600, 400)
        )

        self._nav = ttk.Frame(self._root)
        self._nav.pack(side=TOP, fill=X)

        self._content = ttk.Frame(self._root)
        self._content.pack(fill=BOTH, expand=True)

        self._pages = {}
        self._create_pages()
        self._create_buttons()

        self._show("page1")

    # ---------- public API ----------

    def run(self):
        self._root.mainloop()

    # ---------- navigation commands ----------

    def go_page_1(self):
        self._show("page1")

    def go_page_2(self):
        self._show("page2")

    def go_page_3(self):
        self._show("page3")

    # ---------- internals ----------

    def _show(self, name):
        for page in self._pages.values():
            page.pack_forget()
        self._pages[name].pack(fill=BOTH, expand=True)

    def _create_buttons(self):
        b1 = ttk.Button(self._nav, text="Page 1", command=self.go_page_1)
        b1.pack(side=LEFT, padx=5)

        b2 = ttk.Button(self._nav, text="Page 2", command=self.go_page_2)
        b2.pack(side=LEFT, padx=5)

        b3 = ttk.Button(self._nav, text="Page 3", command=self.go_page_3)
        b3.pack(side=LEFT, padx=5)

    def _create_pages(self):
        self._pages["page1"] = self._make_page("Page 1")
        self._pages["page2"] = self._make_page("Page 2")
        self._pages["page3"] = self._make_page("Page 3")

    def _make_page(self, text):
        frame = ttk.Frame(self._content)
        ttk.Label(frame, text=text, font=("Helvetica", 18)).pack(pady=30)
        return frame
