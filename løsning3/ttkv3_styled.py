import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from database import Database
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class GuiApp:
    # Color palette from main.css
    COLORS = {
        'bg': '#1b1b1b',           # deep charcoal background
        'parchment': '#2a2a2a',    # dark card base
        'accent': '#d4af37',       # metallic gold
        'text_light': '#f5eec7',   # warm light text
        'text_dark': '#d6cfa3',    # soft gold-tan
    }
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("D&D Class Browser")
        self.root.geometry("950x750")
        self.root.configure(bg=self.COLORS['bg'])
        
        # Configure ttk style for scrollbar
        self._configure_ttk_style()
        
        # Set background image
        self._set_background()
        
        self.db = Database()
        self.search_results = []
        
        self._create_widgets()

    def _set_background(self):
        """Set the background image from styling folder"""
        bg_path = BASE_DIR / "styling" / "dndbackground.jpg"
        if bg_path.exists():
            img = Image.open(bg_path)
            # Scale to window size
            img = img.resize((950, 750), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(img)
            
            # Create background label
            bg_label = tk.Label(self.root, image=self.bg_photo, bg=self.COLORS['bg'])
            bg_label.image = self.bg_photo
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()

    def _configure_ttk_style(self):
        """Configure ttk style for dark scrollbar"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            'Dark.Vertical.TScrollbar',
            background=self.COLORS['parchment'],
            troughcolor=self.COLORS['bg'],
            bordercolor=self.COLORS['accent'],
            lightcolor=self.COLORS['parchment'],
            darkcolor=self.COLORS['parchment'],
            arrowcolor=self.COLORS['accent']
        )

    def _create_widgets(self):
        """Create main widget structure"""
        # Header with logo
        header = tk.Frame(self.root, bg=self.COLORS['bg'])
        header.pack(fill=tk.X, padx=20, pady=10)
        
        # Logo
        logo_path = BASE_DIR / "styling" / "dndlogo2.png"
        if logo_path.exists():
            try:
                logo_img = Image.open(logo_path)
                logo_img.thumbnail((80, 80), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_img)
                logo_label = tk.Label(header, image=self.logo_photo, bg=self.COLORS['bg'])
                logo_label.pack()
            except:
                pass
        
        # Title
        title = tk.Label(
            header,
            text="D&D Class Browser",
            font=("Georgia", 22, "bold"),
            bg=self.COLORS['bg'],
            fg=self.COLORS['accent']
        )
        title.pack()
        
        # Tagline
        tagline = tk.Label(
            header,
            text="~ Explore the classes of Dungeons and Dragons ~",
            font=("Georgia", 10, "italic"),
            bg=self.COLORS['bg'],
            fg='#e5d88f'
        )
        tagline.pack()
        
        # Navigation with prettier buttons
        nav = tk.Frame(self.root, bg=self.COLORS['bg'])
        nav.pack(fill=tk.X, padx=15, pady=8)
        
        nav_buttons = [
            ("🔍 Search", lambda: self.show_page("page1")),
            ("📋 Results", lambda: self.show_page("page2")),
            ("➕ Create", lambda: self.show_page("page3")),
        ]
        
        for text, cmd in nav_buttons:
            btn = tk.Button(
                nav,
                text=text,
                command=cmd,
                font=("Arial", 10, "bold"),
                bg=self.COLORS['accent'],
                fg=self.COLORS['bg'],
                padx=18,
                pady=6,
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                activebackground='#e0c35a',
                activeforeground=self.COLORS['bg']
            )
            btn.pack(side=tk.LEFT, padx=8, pady=5)
            self._set_button_hover(btn)
        
        # Content area
        self.content = tk.Frame(self.root, bg=self.COLORS['bg'])
        self.content.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.show_page("page1")

    def _set_button_hover(self, button):
        """Add hover effect to button"""
        def on_enter(e):
            button.config(bg='#e0c35a')
        def on_leave(e):
            button.config(bg=self.COLORS['accent'])
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)

    def show_page(self, page):
        """Switch between pages"""
        for widget in self.content.winfo_children():
            widget.destroy()
        
        if page == "page1":
            self.page_search()
        elif page == "page2":
            self.page_results()
        elif page == "page3":
            self.page_create()

    def page_search(self):
        """Search page"""
        title = tk.Label(
            self.content,
            text="Search D&D Classes",
            font=("Georgia", 15, "bold"),
            bg=self.COLORS['bg'],
            fg=self.COLORS['accent']
        )
        title.pack(pady=12)
        
        search_frame = tk.Frame(self.content, bg=self.COLORS['bg'])
        search_frame.pack(pady=8)
        
        tk.Label(
            search_frame,
            text="Enter search term:",
            font=("Georgia", 10),
            bg=self.COLORS['bg'],
            fg=self.COLORS['text_light']
        ).pack()
        
        search_var = tk.StringVar()
        entry = tk.Entry(
            search_frame,
            textvariable=search_var,
            width=40,
            font=("Arial", 10),
            bg='#222',
            fg=self.COLORS['text_light'],
            insertbackground=self.COLORS['accent'],
            relief=tk.FLAT,
            bd=0
        )
        entry.pack(fill=tk.X, pady=6)
        entry.config(highlightbackground=self.COLORS['accent'], highlightthickness=2)
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
        
        btn_frame = tk.Frame(self.content, bg=self.COLORS['bg'])
        btn_frame.pack(pady=15)
        
        search_btn = tk.Button(
            btn_frame,
            text="Search",
            command=search,
            font=("Arial", 10, "bold"),
            bg=self.COLORS['accent'],
            fg=self.COLORS['bg'],
            padx=16,
            pady=6,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            activebackground='#e0c35a'
        )
        search_btn.pack(side=tk.LEFT, padx=6)
        self._set_button_hover(search_btn)
        
        load_btn = tk.Button(
            btn_frame,
            text="Load All",
            command=lambda: (setattr(self, 'search_results', self.db.load_all()), self.show_page("page2")),
            font=("Arial", 10, "bold"),
            bg=self.COLORS['accent'],
            fg=self.COLORS['bg'],
            padx=16,
            pady=6,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            activebackground='#e0c35a'
        )
        load_btn.pack(side=tk.LEFT, padx=6)
        self._set_button_hover(load_btn)

    def page_results(self):
        """Results display page"""
        title = tk.Label(
            self.content,
            text=f"Results ({len(self.search_results)})",
            font=("Georgia", 15, "bold"),
            bg=self.COLORS['bg'],
            fg=self.COLORS['accent']
        )
        title.pack(pady=8)
        
        if not self.search_results:
            tk.Label(
                self.content,
                text="No results",
                font=("Arial", 10),
                bg=self.COLORS['bg'],
                fg='#888'
            ).pack(pady=30)
            return
        
        # Scrollable frame
        canvas = tk.Canvas(
            self.content,
            bg=self.COLORS['bg'],
            highlightthickness=0,
            relief=tk.FLAT
        )
        scrollbar = ttk.Scrollbar(
            self.content,
            orient=tk.VERTICAL,
            command=canvas.yview,
            style='Dark.Vertical.TScrollbar'
        )
        scrollable_frame = tk.Frame(canvas, bg=self.COLORS['bg'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Display results as cards
        for result in self.search_results:
            card = tk.Frame(
                scrollable_frame,
                bg=self.COLORS['parchment'],
                relief=tk.FLAT,
                bd=0,
                highlightbackground=self.COLORS['accent'],
                highlightthickness=1
            )
            card.pack(fill=tk.X, pady=5, padx=3)
            
            name_label = tk.Label(
                card,
                text=f"• {result.class_name}",
                font=("Georgia", 11, "bold"),
                bg=self.COLORS['parchment'],
                fg=self.COLORS['accent']
            )
            name_label.pack(anchor=tk.W, padx=10, pady=(6, 1))
            
            ability_label = tk.Label(
                card,
                text=f"  Ability: {result.class_ability}",
                font=("Arial", 9),
                bg=self.COLORS['parchment'],
                fg=self.COLORS['text_dark']
            )
            ability_label.pack(anchor=tk.W, padx=10)
            
            desc = result.class_description if result.class_description else "No description"
            desc_label = tk.Label(
                card,
                text=f"  {desc[:85]}",
                font=("Arial", 8),
                bg=self.COLORS['parchment'],
                fg=self.COLORS['text_light'],
                wraplength=650,
                justify=tk.LEFT
            )
            desc_label.pack(anchor=tk.W, padx=10, pady=(1, 6))
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def page_create(self):
        """Create new class page"""
        title = tk.Label(
            self.content,
            text="Create New Class",
            font=("Georgia", 15, "bold"),
            bg=self.COLORS['bg'],
            fg=self.COLORS['accent']
        )
        title.pack(pady=12)
        
        form_frame = tk.Frame(self.content, bg=self.COLORS['bg'])
        form_frame.pack(pady=8)
        
        fields = {}
        field_labels = ["Class Name:", "Class Ability:", "Description:"]
        
        for label_text in field_labels:
            label = tk.Label(
                form_frame,
                text=label_text,
                font=("Georgia", 10),
                bg=self.COLORS['bg'],
                fg=self.COLORS['text_light']
            )
            label.pack(anchor=tk.W, pady=(8, 2))
            
            var = tk.StringVar()
            entry = tk.Entry(
                form_frame,
                textvariable=var,
                width=50,
                font=("Arial", 10),
                bg='#222',
                fg=self.COLORS['text_light'],
                insertbackground=self.COLORS['accent'],
                relief=tk.FLAT,
                bd=0
            )
            entry.pack(fill=tk.X, pady=(0, 6))
            entry.config(highlightbackground=self.COLORS['accent'], highlightthickness=2)
            fields[label_text] = var
        
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
        
        btn_frame = tk.Frame(form_frame, bg=self.COLORS['bg'])
        btn_frame.pack(pady=15)
        
        create_btn = tk.Button(
            btn_frame,
            text="Create",
            command=create,
            font=("Arial", 10, "bold"),
            bg=self.COLORS['accent'],
            fg=self.COLORS['bg'],
            padx=16,
            pady=6,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            activebackground='#e0c35a'
        )
        create_btn.pack(side=tk.LEFT, padx=6)
        self._set_button_hover(create_btn)
        
        clear_btn = tk.Button(
            btn_frame,
            text="Clear",
            command=lambda: [var.set("") for var in fields.values()],
            font=("Arial", 10, "bold"),
            bg=self.COLORS['accent'],
            fg=self.COLORS['bg'],
            padx=16,
            pady=6,
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            activebackground='#e0c35a'
        )
        clear_btn.pack(side=tk.LEFT, padx=6)
        self._set_button_hover(clear_btn)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = GuiApp()
    app.run()
