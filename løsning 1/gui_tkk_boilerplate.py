import ttkbootstrap as ttk
from ttkbootstrap.constants import *


class GuiApp:
    def __init__(self):
        self._root = ttk.Window(
            title="ttkbootstrap App",
            themename="flatly",
            size=(600, 400)
        )

        self._navigation = ttk.Frame(self._root)
        self._navigation.pack(side=TOP, fill=X)

        self._content = ttk.Frame(self._root)
        self._content.pack(fill=BOTH, expand=True)

        self._pages = {}

        self._create_navigation()
        self._create_pages()

        self.show_page("page1")

    # -------------------------
    # Public API (used by main)
    # -------------------------

    def run(self):
        self._root.mainloop()

    def show_page(self, page_name):
        for page in self._pages.values():
            page.pack_forget()

        self._pages[page_name].pack(fill=BOTH, expand=True)

    # -------------------------
    # Internal implementation
    # -------------------------

    def _create_navigation(self):
        btn1 = ttk.Button(self._navigation, text="Page 1")
        btn1.config(command=self._on_page1)
        btn1.pack(side=LEFT, padx=5, pady=5)

        btn2 = ttk.Button(self._navigation, text="Page 2")
        btn2.config(command=self._on_page2)
        btn2.pack(side=LEFT, padx=5, pady=5)

        btn3 = ttk.Button(self._navigation, text="Page 3")
        btn3.config(command=self._on_page3)
        btn3.pack(side=LEFT, padx=5, pady=5)

    def _create_pages(self):
        page1 = ttk.Frame(self._content)
        ttk.Label(page1, text="This is Page 1", font=("Helvetica", 18)).pack(pady=20)

        page2 = ttk.Frame(self._content)
        ttk.Label(page2, text="This is Page 2", font=("Helvetica", 18)).pack(pady=20)

        page3 = ttk.Frame(self._content)
        ttk.Label(page3, text="This is Page 3", font=("Helvetica", 18)).pack(pady=20)

        self._pages["page1"] = page1
        self._pages["page2"] = page2
        self._pages["page3"] = page3

    # -------------------------
    # Button handlers
    # -------------------------

    def _on_page1(self):
        self.show_page("page1")

    def _on_page2(self):
        self.show_page("page2")

    def _on_page3(self):
        self.show_page("page3")
