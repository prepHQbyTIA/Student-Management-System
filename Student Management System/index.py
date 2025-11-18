import json
import os
import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import datetime
import random



class StudentManager:
    def __init__(self, filename="students.json"):
        self.filename = filename
        self.students = self.load_data()
    
    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                return json.load(f)
        return {}
    
    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.students, f, indent=2)
    
    def add_student(self, student_id, name, grade, email="", phone=""):
        self.students[student_id] = {
            "name": name, 
            "grade": grade, 
            "email": email, 
            "phone": phone,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.save_data()
        return True
    
    def update_student(self, student_id, **kwargs):
        if student_id in self.students:
            for key, value in kwargs.items():
                if value:
                    self.students[student_id][key] = value
            self.students[student_id]["modified"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_data()
            return True
        return False
    
    def delete_student(self, student_id):
        if student_id in self.students:
            del self.students[student_id]
            self.save_data()
            return True
        return False
    
    def search_students(self, query):
        results = []
        for sid, info in self.students.items():
            if (query.lower() in info['name'].lower() or 
                query.lower() in sid.lower() or 
                query.lower() in info.get('email', '').lower() or
                query in info.get('phone', '')):
                results.append((sid, info))
        return results

class StudentGUI:
    def __init__(self):
        self.manager = StudentManager()
        self.root = tk.Tk()
        self.root.title("🎓 Student Management System - Advanced Edition")
        self.root.geometry("1400x800")
        self.root.state('zoomed')
        self.root.configure(bg='#0f0f1e')
        self.colors = {
            'bg': '#f0f4f8',
            'sidebar': '#1e3a8a',
            'card': '#ffffff',
            'card_hover': '#f8fafc',
            'primary': '#2563eb',
            'success': '#10b981',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'info': '#8b5cf6',
            'text': '#1e293b',
            'text_light': '#64748b',
            'border': '#e2e8f0',
            'shadow': '#cbd5e1',
            'accent': '#06b6d4'
        }
        self.setup_styles()
        self.setup_ui()
        self.animate_startup()
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TFrame', background=self.colors['bg'])
        style.configure('Card.TFrame', background=self.colors['card'], relief='flat')
        style.configure('TLabel', background=self.colors['bg'], foreground=self.colors['text'], 
                       font=('Segoe UI', 10))
        
        # Professional Treeview
        style.configure('Modern.Treeview', 
                       background='#ffffff',
                       foreground=self.colors['text'],
                       fieldbackground='#ffffff',
                       borderwidth=1,
                       font=('Segoe UI', 10),
                       rowheight=35)
        style.configure('Modern.Treeview.Heading',
                       background=self.colors['sidebar'],
                       foreground='#ffffff',
                       borderwidth=0,
                       font=('Segoe UI', 11, 'bold'),
                       relief='flat')
        style.map('Modern.Treeview',
                 background=[('selected', self.colors['primary'])],
                 foreground=[('selected', '#ffffff')])
        style.map('Modern.Treeview.Heading',
                 background=[('active', self.colors['primary'])])
        
        self.root.after(100, self.setup_tree_tags)
    
    def create_modern_button(self, parent, text, command, bg_color, row, col):
        btn = tk.Button(parent, text=text, command=command,
                       bg=bg_color, fg='white', font=('Segoe UI', 10, 'bold'),
                       relief='flat', cursor='hand2', padx=18, pady=12,
                       activebackground=self.lighten_color(bg_color),
                       activeforeground='white', bd=0, highlightthickness=0)
        btn.grid(row=row, column=col, padx=4)
        
        def on_enter(e):
            btn.config(bg=self.lighten_color(bg_color))
        def on_leave(e):
            btn.config(bg=bg_color)
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def lighten_color(self, color):
        r, g, b = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        r, g, b = min(255, r + 30), min(255, g + 30), min(255, b + 30)
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def setup_tree_tags(self):
        try:
            self.tree.tag_configure('oddrow', background='#ffffff')
            self.tree.tag_configure('evenrow', background='#f8f9fa')
        except:
            pass
    
    def create_stat_card(self, parent, title, value, icon, color, row, col, click_action=None):
        outer = tk.Frame(parent, bg=self.colors['bg'])
        outer.grid(row=row, column=col, padx=8, pady=8, sticky='nsew')
        
        shadow = tk.Frame(outer, bg='#e2e8f0', height=3)
        shadow.pack(side='bottom', fill='x')
        
        card = tk.Frame(outer, bg='#ffffff', cursor='hand2', highlightthickness=1, highlightbackground='#e2e8f0')
        card.pack(fill='both', expand=True)
        
        top_accent = tk.Frame(card, bg=color, height=3)
        top_accent.pack(fill='x')
        
        content = tk.Frame(card, bg='#ffffff')
        content.pack(fill='both', expand=True, padx=15, pady=15)
        
        icon_frame = tk.Frame(content, bg=color, width=55, height=55)
        icon_frame.pack(side='left', padx=(0, 15))
        icon_frame.pack_propagate(False)
        
        icon_label = tk.Label(icon_frame, text=icon, bg=color, 
                             fg='#ffffff', font=('Segoe UI', 24, 'bold'))
        icon_label.place(relx=0.5, rely=0.5, anchor='center')
        
        text_frame = tk.Frame(content, bg='#ffffff')
        text_frame.pack(side='left', fill='both', expand=True)
        
        value_label = tk.Label(text_frame, text=value, bg='#ffffff',
                              fg=self.colors['text'], font=('Segoe UI', 28, 'bold'))
        value_label.pack(anchor='w')
        
        title_label = tk.Label(text_frame, text=title, bg='#ffffff',
                              fg=self.colors['text_light'], font=('Segoe UI', 10))
        title_label.pack(anchor='w', pady=(2, 0))
        
        def on_enter(e):
            card.config(bg='#fafbfc', highlightthickness=2, highlightbackground=color)
            content.config(bg='#fafbfc')
            text_frame.config(bg='#fafbfc')
            title_label.config(bg='#fafbfc')
            value_label.config(bg='#fafbfc')
        
        def on_leave(e):
            card.config(bg='#ffffff', highlightthickness=1, highlightbackground='#e2e8f0')
            content.config(bg='#ffffff')
            text_frame.config(bg='#ffffff')
            title_label.config(bg='#ffffff')
            value_label.config(bg='#ffffff')
        
        def on_click(e):
            if click_action:
                click_action()
        
        for widget in [card, content, text_frame, value_label, title_label, icon_label]:
            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
            widget.bind('<Button-1>', on_click)
        
        return card
    
    def animate_startup(self):
        self.root.attributes('-alpha', 0.0)
        self.fade_in()
    
    def fade_in(self, alpha=0.0):
        if alpha < 1.0:
            alpha += 0.05
            self.root.attributes('-alpha', alpha)
            self.root.after(20, lambda: self.fade_in(alpha))
        else:
            self.root.attributes('-alpha', 1.0)
    
    def setup_ui(self):
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill='both', expand=True)
        
        # Modern Header with gradient
        header = tk.Frame(main_frame, bg=self.colors['sidebar'], height=70)
        header.pack(fill='x')
        
        header_content = tk.Frame(header, bg=self.colors['sidebar'])
        header_content.pack(fill='both', expand=True, padx=30, pady=15)
        
        # Logo and title
        left_section = tk.Frame(header_content, bg=self.colors['sidebar'])
        left_section.pack(side='left')
        
        # Load logo image
        try:
            self.logo_photo = tk.PhotoImage(file='iot-logo.png').subsample(5, 5)
            logo_label = tk.Label(left_section, image=self.logo_photo, bg=self.colors['sidebar'])
            logo_label.pack(side='left', padx=(0, 15))
        except:
            # Fallback if logo not found
            logo_frame = tk.Frame(left_section, bg='#3b82f6', width=50, height=50, 
                                 highlightthickness=2, highlightbackground='#ffffff')
            logo_frame.pack(side='left', padx=(0, 15))
            logo_frame.pack_propagate(False)
            tk.Label(logo_frame, text='LOGO', bg='#3b82f6', fg='#ffffff', 
                    font=('Arial', 8, 'bold')).place(relx=0.5, rely=0.5, anchor='center')
        
        title_frame = tk.Frame(left_section, bg=self.colors['sidebar'])
        title_frame.pack(side='left')
        
        title = tk.Label(title_frame, text="🎓 Student Management System",
                        bg=self.colors['sidebar'], fg='#ffffff',
                        font=('Segoe UI', 20, 'bold'))
        title.pack(anchor='w')
        
        subtitle = tk.Label(title_frame, text="Manage your students with ease and efficiency",
                           bg=self.colors['sidebar'], fg='#93c5fd',
                           font=('Segoe UI', 10))
        subtitle.pack(anchor='w', pady=(3, 0))
        
        # Content area
        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Stats cards
        stats_frame = tk.Frame(content_frame, bg=self.colors['bg'])
        stats_frame.pack(fill='x', pady=(0, 15))
        
        for i in range(4):
            stats_frame.columnconfigure(i, weight=1)
        
        self.total_card = self.create_stat_card(stats_frame, "Total Students", "0", 
                                                "👥", self.colors['primary'], 0, 0, 
                                                self.show_all_students)
        self.grade_card = self.create_stat_card(stats_frame, "Active Grades", "4",
                                               "📚", self.colors['success'], 0, 1,
                                               self.show_grade_breakdown)
        self.recent_card = self.create_stat_card(stats_frame, "Added Today", "0",
                                                "📅", self.colors['warning'], 0, 2,
                                                self.show_today_students)
        self.search_card = self.create_stat_card(stats_frame, "Search Results", "0",
                                                "🔍", self.colors['danger'], 0, 3,
                                                self.clear_search_filter)
        
        # Control panel with search and buttons
        control_shadow = tk.Frame(content_frame, bg='#e2e8f0', height=3)
        control_shadow.pack(fill='x', pady=(0, 0))
        
        control_frame = tk.Frame(content_frame, bg='#ffffff', highlightthickness=1, highlightbackground='#e2e8f0')
        control_frame.pack(fill='x', pady=(0, 15))
        
        control_content = tk.Frame(control_frame, bg='#ffffff')
        control_content.pack(fill='x', padx=20, pady=15)
        
        # Search bar with modern design
        search_frame = tk.Frame(control_content, bg='#ffffff')
        search_frame.pack(side='left', fill='x', expand=True)
        
        tk.Label(search_frame, text="Search Students", bg='#ffffff',
                fg=self.colors['text'], font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(0, 8))
        
        search_container = tk.Frame(search_frame, bg='#f1f5f9', highlightthickness=1, highlightbackground='#cbd5e1')
        search_container.pack(fill='x')
        
        search_icon = tk.Label(search_container, text="🔍", bg='#f1f5f9',
                              fg=self.colors['text_light'], font=('Segoe UI', 15))
        search_icon.pack(side='left', padx=(18, 10))
        
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(search_container, textvariable=self.search_var,
                               bg='#f1f5f9', fg=self.colors['text'],
                               font=('Segoe UI', 12), relief='flat', bd=0,
                               insertbackground=self.colors['primary'], highlightthickness=0)
        search_entry.pack(side='left', fill='both', expand=True, pady=12, padx=(0, 18))
        search_entry.bind('<KeyRelease>', self.on_search)
        
        def on_focus_in(e):
            search_container.config(highlightbackground=self.colors['primary'], highlightthickness=2)
        def on_focus_out(e):
            search_container.config(highlightbackground='#cbd5e1', highlightthickness=1)
        
        search_entry.bind('<FocusIn>', on_focus_in)
        search_entry.bind('<FocusOut>', on_focus_out)
        
        # Action buttons
        btn_frame = tk.Frame(control_content, bg='#ffffff')
        btn_frame.pack(side='right', padx=(30, 0))
        
        tk.Label(btn_frame, text="Actions", bg='#ffffff',
                fg=self.colors['text'], font=('Segoe UI', 11, 'bold')).pack(anchor='w', pady=(0, 8))
        
        btn_container = tk.Frame(btn_frame, bg='#ffffff')
        btn_container.pack()
        
        self.create_modern_button(btn_container, "➕ Add", self.add_student, 
                                 self.colors['success'], 0, 0)
        self.create_modern_button(btn_container, "✏️ Edit", self.edit_student,
                                 self.colors['warning'], 0, 1)
        self.create_modern_button(btn_container, "🗑️ Delete", self.delete_student,
                                 self.colors['danger'], 0, 2)
        self.create_modern_button(btn_container, "🔄 Refresh", self.refresh_list,
                                 self.colors['primary'], 0, 3)
        
        # Table container with modern design
        table_shadow = tk.Frame(content_frame, bg='#e2e8f0', height=3)
        table_shadow.pack(fill='x')
        
        table_container = tk.Frame(content_frame, bg='#ffffff', highlightthickness=1, highlightbackground='#e2e8f0')
        table_container.pack(fill='both', expand=True)
        
        table_header = tk.Frame(table_container, bg='#ffffff')
        table_header.pack(fill='x', padx=20, pady=(15, 8))
        
        tk.Label(table_header, text="📊 Student Records", bg='#ffffff',
                fg=self.colors['text'], font=('Segoe UI', 14, 'bold')).pack(side='left')
        
        tree_frame = tk.Frame(table_container, bg='#ffffff')
        tree_frame.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        columns = ('ID', 'Name', 'Grade', 'Email', 'Phone', 'Created')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings',
                                style='Modern.Treeview', selectmode='browse')
        
        self.tree.heading('ID', text='🆔 STUDENT ID')
        self.tree.heading('Name', text='👤 FULL NAME')
        self.tree.heading('Grade', text='🎓 GRADE')
        self.tree.heading('Email', text='📧 EMAIL')
        self.tree.heading('Phone', text='📱 PHONE')
        self.tree.heading('Created', text='📅 DATE ADDED')
        
        self.tree.column('ID', width=120, anchor='center')
        self.tree.column('Name', width=200)
        self.tree.column('Grade', width=100, anchor='center')
        self.tree.column('Email', width=250)
        self.tree.column('Phone', width=150, anchor='center')
        self.tree.column('Created', width=180, anchor='center')
        
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')
        
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)
        
        self.tree.bind('<Motion>', self.on_tree_hover)
        self.tree.bind('<Double-1>', lambda e: self.edit_student())
        
        # Add alternating row colors
        self.tree.tag_configure('oddrow', background='#ffffff')
        self.tree.tag_configure('evenrow', background='#f9fafb')
        
        # Footer
        footer_shadow = tk.Frame(content_frame, bg='#e2e8f0', height=3)
        footer_shadow.pack(fill='x', pady=(15, 0))
        
        footer = tk.Frame(content_frame, bg='#ffffff', highlightthickness=1, highlightbackground='#e2e8f0')
        footer.pack(fill='x')
        
        self.status_var = tk.StringVar()
        status = tk.Label(footer, textvariable=self.status_var,
                         bg='#ffffff', fg=self.colors['text_light'],
                         font=('Segoe UI', 9))
        status.pack(pady=10)
        
        self.refresh_list()
    
    def on_tree_hover(self, event):
        tree = event.widget
        item = tree.identify_row(event.y)
        if item:
            tree.selection_set(item)
    
    def refresh_list(self):
        self.manager.students = self.manager.load_data()
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Count students added today
        today = datetime.now().strftime("%Y-%m-%d")
        added_today = 0
        unique_grades = set()
        
        count = 0
        for sid, info in self.manager.students.items():
            tag = 'evenrow' if count % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=(
                sid, info.get('name', ''), info.get('grade', ''), 
                info.get('email', ''), info.get('phone', ''), 
                info.get('created', '')
            ), tags=(tag,))
            count += 1
            
            # Check if added today
            created = info.get('created', '')
            if created.startswith(today):
                added_today += 1
            
            # Count unique grades
            grade = info.get('grade', '')
            if grade:
                unique_grades.add(grade)
        
        total = len(self.manager.students)
        self.update_stat_card(self.total_card, str(total))
        self.update_stat_card(self.recent_card, str(added_today))
        self.update_stat_card(self.grade_card, str(len(unique_grades)))
        self.status_var.set(f"✅ Loaded {total} student records successfully")
    
    def update_stat_card(self, card, value):
        for widget in card.winfo_children():
            if isinstance(widget, tk.Frame) and widget.cget('bg') == '#ffffff':
                for child in widget.winfo_children():
                    if isinstance(child, tk.Frame):
                        for label in child.winfo_children():
                            if isinstance(label, tk.Label):
                                font_info = label.cget('font')
                                if isinstance(font_info, tuple) and len(font_info) > 1 and font_info[1] == 32:
                                    label.config(text=value)
                                    return
    
    def on_search(self, event=None):
        query = self.search_var.get()
        if not query:
            self.refresh_list()
            return
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        results = self.manager.search_students(query)
        for sid, info in results:
            self.tree.insert('', 'end', values=(
                sid, info['name'], info['grade'], 
                info.get('email', ''), info.get('phone', ''), 
                info.get('created', '')
            ))
        
        self.status_var.set(f"🔍 Found {len(results)} student(s)")
        self.update_stat_card(self.search_card, str(len(results)))
    
    def add_student(self):
        dialog = StudentDialog(self.root, "Add Student")
        self.root.wait_window(dialog.dialog)
        if dialog.result:
            data = dialog.result
            if data['id'] in self.manager.students:
                messagebox.showerror("Error", "Student ID already exists!")
                return
            
            self.manager.add_student(
                student_id=data['id'],
                name=data['name'],
                grade=data['grade'],
                email=data['email'],
                phone=data['phone']
            )
            self.refresh_list()
            messagebox.showinfo("✅ Success", "Student added successfully!")
    
    def edit_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("⚠️ Warning", "Please select a student to edit.")
            return
        
        item = self.tree.item(selected[0])
        student_id = str(item['values'][0])
        
        self.manager.students = self.manager.load_data()
        
        if student_id not in self.manager.students:
            messagebox.showerror("Error", "Student not found!")
            self.refresh_list()
            return
        
        student_data = self.manager.students[student_id]
        
        dialog = StudentDialog(self.root, "Edit Student", student_data, student_id)
        self.root.wait_window(dialog.dialog)
        if dialog.result:
            data = dialog.result
            self.manager.update_student(student_id, **{k:v for k,v in data.items() if k != 'id'})
            self.refresh_list()
            messagebox.showinfo("✅ Success", "Student updated successfully!")
    
    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("⚠️ Warning", "Please select a student to delete.")
            return
        
        item = self.tree.item(selected[0])
        student_id = str(item['values'][0])
        student_name = item['values'][1]
        
        if messagebox.askyesno("🗑️ Confirm Delete", 
                              f"Are you sure you want to delete:\n\nStudent: {student_name}\nID: {student_id}\n\nThis action cannot be undone!"):
            if self.manager.delete_student(student_id):
                self.refresh_list()
                messagebox.showinfo("✅ Success", "Student deleted successfully!")
    
    def show_all_students(self):
        self.search_var.set('')
        self.refresh_list()
        messagebox.showinfo("👥 Total Students", 
                           f"Total number of students in the system: {len(self.manager.students)}\n\nAll students are displayed in the table below.")
    
    def show_grade_breakdown(self):
        grades = {}
        for sid, info in self.manager.students.items():
            grade = info.get('grade', 'Unknown')
            grades[grade] = grades.get(grade, 0) + 1
        
        breakdown = "\n".join([f"{grade}: {count} student(s)" for grade, count in sorted(grades.items())])
        messagebox.showinfo("📚 Grade Breakdown", 
                           f"Students by Grade:\n\n{breakdown}\n\nTotal Grades: {len(grades)}")
    
    def show_today_students(self):
        today = datetime.now().strftime("%Y-%m-%d")
        today_students = []
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        count = 0
        for sid, info in self.manager.students.items():
            created = info.get('created', '')
            if created.startswith(today):
                tag = 'evenrow' if count % 2 == 0 else 'oddrow'
                self.tree.insert('', 'end', values=(
                    sid, info.get('name', ''), info.get('grade', ''), 
                    info.get('email', ''), info.get('phone', ''), 
                    info.get('created', '')
                ), tags=(tag,))
                today_students.append(info.get('name', ''))
                count += 1
        
        if today_students:
            names = "\n".join([f"{i+1}. {name}" for i, name in enumerate(today_students)])
            self.status_var.set(f"📅 Showing {len(today_students)} student(s) added today")
            messagebox.showinfo("📅 Students Added Today", 
                               f"Students added today ({datetime.now().strftime('%B %d, %Y')}):\n\n{names}")
        else:
            self.refresh_list()
            messagebox.showinfo("📅 Students Added Today", 
                               "No students were added today.")
    
    def clear_search_filter(self):
        self.search_var.set('')
        self.refresh_list()
    
    def run(self):
        self.root.mainloop()

class StudentDialog:
    def __init__(self, parent, title, data=None, student_id=None):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("600x580")
        self.dialog.configure(bg='#f0f4f8')
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - 300
        y = (self.dialog.winfo_screenheight() // 2) - 290
        self.dialog.geometry(f"+{x}+{y}")
        
        # Header
        header = tk.Frame(self.dialog, bg='#1e3a8a', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        icon = "📝" if "Add" in title else "✏️"
        tk.Label(header, text=f"{icon} {title}",
                bg='#1e3a8a', fg='#ffffff',
                font=('Segoe UI', 20, 'bold')).pack(expand=True)
        
        # Main content with card
        content = tk.Frame(self.dialog, bg='#f0f4f8')
        content.pack(fill='both', expand=True, padx=30, pady=25)
        
        # Form card
        card = tk.Frame(content, bg='#ffffff', highlightthickness=1, highlightbackground='#cbd5e1')
        card.pack(fill='both', expand=True)
        
        form_frame = tk.Frame(card, bg='#ffffff')
        form_frame.pack(fill='both', expand=True, padx=30, pady=25)
        
        fields = [
            ("🆔 Student ID", 'id_var', student_id or '', student_id is not None, "Enter unique student ID"),
            ("👤 Full Name", 'name_var', data.get('name', '') if data else '', False, "Enter student's full name"),
            ("🎓 Grade", 'grade_var', data.get('grade', '') if data else '', False, "Enter grade (e.g., 10th, 12th)"),
            ("📧 Email Address", 'email_var', data.get('email', '') if data else '', False, "Enter email address"),
            ("📱 Phone Number", 'phone_var', data.get('phone', '') if data else '', False, "Enter phone number with country code")
        ]
        
        for i, (label_text, var_name, value, readonly, placeholder) in enumerate(fields):
            field_container = tk.Frame(form_frame, bg='#ffffff')
            field_container.pack(fill='x', pady=(0 if i == 0 else 12, 0))
            
            tk.Label(field_container, text=label_text,
                    bg='#ffffff', fg='#1e293b',
                    font=('Segoe UI', 10, 'bold'), anchor='w').pack(fill='x', pady=(0, 6))
            
            var = tk.StringVar(value=value)
            setattr(self, var_name, var)
            
            entry_frame = tk.Frame(field_container, bg='#f8fafc', highlightthickness=1, highlightbackground='#cbd5e1')
            entry_frame.pack(fill='x')
            
            entry = tk.Entry(entry_frame, textvariable=var,
                           bg='#f8fafc', fg='#1e293b',
                           font=('Segoe UI', 11), relief='flat', bd=0,
                           insertbackground='#2563eb', highlightthickness=0)
            entry.pack(fill='x', padx=14, pady=10, ipady=4)
            
            if readonly:
                entry.config(state='readonly', fg='#2563eb', bg='#e0e7ff')
            
            def on_focus_in(e, ef=entry_frame):
                ef.config(highlightbackground='#2563eb', highlightthickness=2, bg='#ffffff')
                e.widget.config(bg='#ffffff')
            def on_focus_out(e, ef=entry_frame):
                ef.config(highlightbackground='#cbd5e1', highlightthickness=1, bg='#f8fafc')
                e.widget.config(bg='#f8fafc')
            
            if not readonly:
                entry.bind('<FocusIn>', on_focus_in)
                entry.bind('<FocusOut>', on_focus_out)
        
        # Buttons
        btn_frame = tk.Frame(content, bg='#f0f4f8')
        btn_frame.pack(fill='x', pady=(20, 0))
        
        save_btn = tk.Button(btn_frame, text="✔️ Save Student", command=self.save,
                            bg='#10b981', fg='white', font=('Segoe UI', 11, 'bold'),
                            relief='flat', cursor='hand2', pady=14, activebackground='#059669', bd=0)
        save_btn.pack(side='left', fill='x', expand=True, padx=(0, 8))
        
        cancel_btn = tk.Button(btn_frame, text="✖ Cancel", command=self.dialog.destroy,
                              bg='#6b7280', fg='white', font=('Segoe UI', 11, 'bold'),
                              relief='flat', cursor='hand2', pady=14, activebackground='#4b5563', bd=0)
        cancel_btn.pack(side='left', fill='x', expand=True, padx=(8, 0))
        
        self.dialog.bind('<Return>', lambda e: self.save())
        self.dialog.bind('<Escape>', lambda e: self.dialog.destroy())
    
    def save(self):
        if not self.id_var.get().strip() or not self.name_var.get().strip():
            messagebox.showerror("❌ Error", "Student ID and Name are required!")
            return
        
        self.result = {
            'id': self.id_var.get().strip(),
            'name': self.name_var.get().strip(),
            'grade': self.grade_var.get().strip(),
            'email': self.email_var.get().strip(),
            'phone': self.phone_var.get().strip()
        }
        self.dialog.destroy()

if __name__ == "__main__":
    app = StudentGUI()
    app.run()
