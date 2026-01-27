import tkinter as tk
from tkinter import messagebox
from database import Database

class GuiApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("D&D Class Browser")
        self.root.geometry("700x500")
        
        self.db = Database()
        self.search_results = []
        
        # Navigation
        nav = tk.Frame(self.root, bg="lightgray", pady=5)
        nav.pack(fill=tk.X, padx=5)
        tk.Button(nav, text="🔍 Search", command=lambda: self.show_page("page1"), width=15).pack(side=tk.LEFT, padx=3)
        tk.Button(nav, text="📋 Results", command=lambda: self.show_page("page2"), width=15).pack(side=tk.LEFT, padx=3)
        tk.Button(nav, text="➕ Create", command=lambda: self.show_page("page3"), width=15).pack(side=tk.LEFT, padx=3)
        
        # Content area
        self.content = tk.Frame(self.root)
        self.content.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.show_page("page1")

    def show_page(self, page):
        for widget in self.content.winfo_children():
            widget.destroy()
        
        if page == "page1":
            self.page_search()
        elif page == "page2":
            self.page_results()
        elif page == "page3":
            self.page_create()

    def page_search(self):
        tk.Label(self.content, text="Search D&D Classes", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=10)
        
        tk.Label(self.content, text="Enter search term:").pack(anchor=tk.W)
        search_var = tk.StringVar()
        entry = tk.Entry(self.content, textvariable=search_var, width=40, font=("Arial", 10))
        entry.pack(fill=tk.X, pady=5)
        entry.focus()
        
        def search():
            term = search_var.get()
            if not term.strip():
                messagebox.showwarning("Warning", "Enter a search term")
                return
            self.search_results = self.db.search(term)
            if not self.search_results:
                messagebox.showinfo("Info", "No results found")
            else:
                self.show_page("page2")
        
        btn_frame = tk.Frame(self.content)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Search", command=search, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Load All", command=lambda: (setattr(self, 'search_results', self.db.load_all()), self.show_page("page2")), width=12).pack(side=tk.LEFT, padx=5)

    def page_results(self):
        tk.Label(self.content, text=f"Results ({len(self.search_results)})", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=10)
        
        if not self.search_results:
            tk.Label(self.content, text="No results", fg="gray").pack(pady=20)
            return
        
        canvas = tk.Canvas(self.content, bg="white", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.content, orient=tk.VERTICAL, command=canvas.yview)
        frame = tk.Frame(canvas, bg="white")
        
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        for result in self.search_results:
            item = tk.Frame(frame, bg="white", relief=tk.RAISED, borderwidth=1)
            item.pack(fill=tk.X, pady=3, padx=3)
            tk.Label(item, text=f"• {result.class_name}", font=("Arial", 10, "bold"), bg="white").pack(anchor=tk.W, padx=5, pady=2)
            tk.Label(item, text=f"  Ability: {result.class_ability}", font=("Arial", 9), bg="white").pack(anchor=tk.W, padx=5)
            desc = result.class_description if result.class_description else "No description"
            tk.Label(item, text=f"  {desc[:70]}...", font=("Arial", 9), bg="white", fg="darkblue").pack(anchor=tk.W, padx=5, pady=2)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def page_create(self):
        tk.Label(self.content, text="Create New Class", font=("Arial", 14, "bold")).pack(anchor=tk.W, pady=10)
        
        fields = {}
        for label in ["Class Name:", "Class Ability:", "Description:"]:
            tk.Label(self.content, text=label).pack(anchor=tk.W, pady=5)
            var = tk.StringVar()
            entry = tk.Entry(self.content, textvariable=var, width=40, font=("Arial", 10))
            entry.pack(fill=tk.X, pady=2)
            fields[label] = var
        
        def create():
            name = fields["Class Name:"].get().strip()
            ability = fields["Class Ability:"].get().strip()
            desc = fields["Description:"].get().strip()
            
            if not all([name, ability, desc]):
                messagebox.showwarning("Warning", "Fill all fields")
                return
            
            try:
                self.db.insert(name, ability, desc)
                messagebox.showinfo("Success", f"Created: {name}")
                for var in fields.values():
                    var.set("")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        
        btn_frame = tk.Frame(self.content)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Create", command=create, width=12).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear", command=lambda: [var.set("") for var in fields.values()], width=12).pack(side=tk.LEFT, padx=5)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GuiApp()
    app.run()
