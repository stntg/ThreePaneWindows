Real-World Applications
=======================

This section provides complete, real-world examples that demonstrate how to build professional applications using ThreePaneWindows.

Text Editor Application
-----------------------

A complete text editor with file management:

.. code-block:: python

    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    import os
    from threepanewindows import EnhancedDockableThreePaneWindow, PaneConfig

    class TextEditorApp:
        """A complete text editor application."""
        
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Professional Text Editor")
            self.root.geometry("1200x800")
            
            self.current_file = None
            self.file_modified = False
            
            self.setup_ui()
            
        def setup_ui(self):
            """Set up the user interface."""
            # Create menu
            self.create_menu()
            
            # Configure panes
            file_config = PaneConfig(
                title="File Explorer",
                icon="📁",
                default_width=250,
                min_width=200,
                detachable=True
            )
            
            editor_config = PaneConfig(
                title="Editor",
                icon="📝",
                detachable=False
            )
            
            outline_config = PaneConfig(
                title="Document Outline",
                icon="📋",
                default_width=200,
                min_width=150,
                detachable=True
            )
            
            # Create enhanced window
            self.window = EnhancedDockableThreePaneWindow(
                self.root,
                left_config=file_config,
                center_config=editor_config,
                right_config=outline_config,
                left_builder=self.build_file_explorer,
                center_builder=self.build_editor,
                right_builder=self.build_outline,
                theme_name="blue"
            )
            self.window.pack(fill=tk.BOTH, expand=True)
            
            # Status bar
            self.status_bar = tk.Label(self.root, text="Ready", 
                                     relief=tk.SUNKEN, anchor=tk.W)
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
            
        def create_menu(self):
            """Create the application menu."""
            menubar = tk.Menu(self.root)
            
            # File menu
            file_menu = tk.Menu(menubar, tearoff=0)
            file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
            file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
            file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
            file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=self.save_as_file)
            file_menu.add_separator()
            file_menu.add_command(label="Exit", command=self.exit_app)
            menubar.add_cascade(label="File", menu=file_menu)
            
            # Edit menu
            edit_menu = tk.Menu(menubar, tearoff=0)
            edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.undo)
            edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.redo)
            edit_menu.add_separator()
            edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut)
            edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy)
            edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste)
            menubar.add_cascade(label="Edit", menu=edit_menu)
            
            # View menu
            view_menu = tk.Menu(menubar, tearoff=0)
            view_menu.add_command(label="Word Wrap", command=self.toggle_word_wrap)
            view_menu.add_command(label="Line Numbers", command=self.toggle_line_numbers)
            menubar.add_cascade(label="View", menu=view_menu)
            
            self.root.config(menu=menubar)
            
            # Keyboard bindings
            self.root.bind('<Control-n>', lambda e: self.new_file())
            self.root.bind('<Control-o>', lambda e: self.open_file())
            self.root.bind('<Control-s>', lambda e: self.save_file())
            
        def build_file_explorer(self, frame):
            """Build the file explorer panel."""
            # Toolbar
            toolbar = tk.Frame(frame, bg="#f0f0f0", height=30)
            toolbar.pack(fill=tk.X)
            toolbar.pack_propagate(False)
            
            tk.Button(toolbar, text="📁", command=self.browse_folder).pack(side=tk.LEFT, padx=5, pady=2)
            tk.Button(toolbar, text="🔄", command=self.refresh_files).pack(side=tk.LEFT, padx=2, pady=2)
            
            # File tree
            self.file_tree = ttk.Treeview(frame)
            file_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.file_tree.yview)
            self.file_tree.configure(yscrollcommand=file_scroll.set)
            
            self.file_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            file_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
            
            # Bind double-click to open file
            self.file_tree.bind('<Double-1>', self.on_file_double_click)
            
            # Load initial directory
            self.load_directory(os.getcwd())
            
        def build_editor(self, frame):
            """Build the main editor panel."""
            # Editor toolbar
            editor_toolbar = tk.Frame(frame, bg="#e0e0e0", height=35)
            editor_toolbar.pack(fill=tk.X)
            editor_toolbar.pack_propagate(False)
            
            # File info
            self.file_label = tk.Label(editor_toolbar, text="Untitled", 
                                     font=("Arial", 10, "bold"), bg="#e0e0e0")
            self.file_label.pack(side=tk.LEFT, padx=10, pady=5)
            
            # Editor frame
            editor_frame = tk.Frame(frame)
            editor_frame.pack(fill=tk.BOTH, expand=True)
            
            # Line numbers (optional)
            self.line_frame = tk.Frame(editor_frame, bg="#f8f8f8", width=40)
            self.line_numbers = tk.Text(self.line_frame, width=4, bg="#f8f8f8", fg="#666",
                                      font=("Consolas", 11), state=tk.DISABLED, wrap=tk.NONE)
            
            # Main text editor
            self.text_editor = tk.Text(editor_frame, wrap=tk.WORD, font=("Consolas", 12),
                                     undo=True, maxundo=50)
            
            # Scrollbars
            v_scroll = tk.Scrollbar(editor_frame, orient=tk.VERTICAL, command=self.text_editor.yview)
            h_scroll = tk.Scrollbar(editor_frame, orient=tk.HORIZONTAL, command=self.text_editor.xview)
            self.text_editor.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
            
            # Pack editor components
            self.text_editor.grid(row=0, column=1, sticky="nsew")
            v_scroll.grid(row=0, column=2, sticky="ns")
            h_scroll.grid(row=1, column=1, sticky="ew")
            
            editor_frame.grid_rowconfigure(0, weight=1)
            editor_frame.grid_columnconfigure(1, weight=1)
            
            # Bind text changes
            self.text_editor.bind('<KeyPress>', self.on_text_change)
            self.text_editor.bind('<Button-1>', self.update_cursor_position)
            self.text_editor.bind('<KeyRelease>', self.update_cursor_position)
            
        def build_outline(self, frame):
            """Build the document outline panel."""
            tk.Label(frame, text="Document Outline", font=("Arial", 11, "bold")).pack(pady=5)
            
            # Outline tree
            self.outline_tree = ttk.Treeview(frame)
            outline_scroll = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.outline_tree.yview)
            self.outline_tree.configure(yscrollcommand=outline_scroll.set)
            
            self.outline_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            outline_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
            
            # Document stats
            stats_frame = tk.LabelFrame(frame, text="Statistics", font=("Arial", 10, "bold"))
            stats_frame.pack(fill=tk.X, padx=5, pady=5)
            
            self.stats_labels = {}
            stats = ["Lines", "Words", "Characters"]
            for stat in stats:
                stat_frame = tk.Frame(stats_frame)
                stat_frame.pack(fill=tk.X, padx=5, pady=2)
                
                tk.Label(stat_frame, text=f"{stat}:", font=("Arial", 9)).pack(side=tk.LEFT)
                self.stats_labels[stat] = tk.Label(stat_frame, text="0", font=("Arial", 9, "bold"))
                self.stats_labels[stat].pack(side=tk.RIGHT)
            
            self.update_stats()
            
        # File operations
        def new_file(self):
            """Create a new file."""
            if self.check_save_changes():
                self.text_editor.delete(1.0, tk.END)
                self.current_file = None
                self.file_modified = False
                self.file_label.config(text="Untitled")
                self.update_title()
                
        def open_file(self):
            """Open a file."""
            if self.check_save_changes():
                filename = filedialog.askopenfilename(
                    title="Open File",
                    filetypes=[("Text files", "*.txt"), ("Python files", "*.py"), ("All files", "*.*")]
                )
                if filename:
                    try:
                        with open(filename, 'r', encoding='utf-8') as file:
                            content = file.read()
                            self.text_editor.delete(1.0, tk.END)
                            self.text_editor.insert(1.0, content)
                            self.current_file = filename
                            self.file_modified = False
                            self.file_label.config(text=os.path.basename(filename))
                            self.update_title()
                            self.update_outline()
                    except Exception as e:
                        messagebox.showerror("Error", f"Could not open file: {str(e)}")
                        
        def save_file(self):
            """Save the current file."""
            if self.current_file:
                try:
                    content = self.text_editor.get(1.0, tk.END + '-1c')
                    with open(self.current_file, 'w', encoding='utf-8') as file:
                        file.write(content)
                    self.file_modified = False
                    self.update_title()
                    self.status_bar.config(text=f"Saved: {self.current_file}")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not save file: {str(e)}")
            else:
                self.save_as_file()
                
        def save_as_file(self):
            """Save the file with a new name."""
            filename = filedialog.asksaveasfilename(
                title="Save As",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("Python files", "*.py"), ("All files", "*.*")]
            )
            if filename:
                self.current_file = filename
                self.save_file()
                self.file_label.config(text=os.path.basename(filename))
                
        # Edit operations
        def undo(self):
            try:
                self.text_editor.edit_undo()
            except tk.TclError:
                pass
                
        def redo(self):
            try:
                self.text_editor.edit_redo()
            except tk.TclError:
                pass
                
        def cut(self):
            try:
                self.text_editor.event_generate("<<Cut>>")
            except tk.TclError:
                pass
                
        def copy(self):
            try:
                self.text_editor.event_generate("<<Copy>>")
            except tk.TclError:
                pass
                
        def paste(self):
            try:
                self.text_editor.event_generate("<<Paste>>")
            except tk.TclError:
                pass
                
        # Utility methods
        def check_save_changes(self):
            """Check if changes need to be saved."""
            if self.file_modified:
                result = messagebox.askyesnocancel("Save Changes", 
                                                 "Do you want to save changes to the current document?")
                if result is True:
                    self.save_file()
                    return True
                elif result is False:
                    return True
                else:
                    return False
            return True
            
        def on_text_change(self, event=None):
            """Handle text changes."""
            self.file_modified = True
            self.update_title()
            self.root.after_idle(self.update_stats)
            self.root.after_idle(self.update_outline)
            
        def update_title(self):
            """Update the window title."""
            title = "Professional Text Editor"
            if self.current_file:
                title += f" - {os.path.basename(self.current_file)}"
            else:
                title += " - Untitled"
            if self.file_modified:
                title += " *"
            self.root.title(title)
            
        def update_stats(self):
            """Update document statistics."""
            content = self.text_editor.get(1.0, tk.END + '-1c')
            lines = content.count('\n') + 1 if content else 0
            words = len(content.split()) if content else 0
            chars = len(content)
            
            self.stats_labels["Lines"].config(text=str(lines))
            self.stats_labels["Words"].config(text=str(words))
            self.stats_labels["Characters"].config(text=str(chars))
            
        def update_outline(self):
            """Update document outline."""
            # Clear existing outline
            for item in self.outline_tree.get_children():
                self.outline_tree.delete(item)
                
            # Parse content for headings (simple example)
            content = self.text_editor.get(1.0, tk.END)
            lines = content.split('\n')
            
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if line.startswith('#'):
                    level = len(line) - len(line.lstrip('#'))
                    heading = line.lstrip('# ').strip()
                    if heading:
                        self.outline_tree.insert("", "end", text=f"Line {i}: {heading}")
                        
        def update_cursor_position(self, event=None):
            """Update cursor position in status bar."""
            cursor_pos = self.text_editor.index(tk.INSERT)
            line, col = cursor_pos.split('.')
            self.status_bar.config(text=f"Line {line}, Column {int(col)+1}")
            
        # File explorer methods
        def load_directory(self, path):
            """Load directory contents into file tree."""
            # Clear existing items
            for item in self.file_tree.get_children():
                self.file_tree.delete(item)
                
            try:
                for item in sorted(os.listdir(path)):
                    item_path = os.path.join(path, item)
                    if os.path.isdir(item_path):
                        self.file_tree.insert("", "end", text=f"📁 {item}", values=[item_path])
                    else:
                        self.file_tree.insert("", "end", text=f"📄 {item}", values=[item_path])
            except PermissionError:
                messagebox.showerror("Error", "Permission denied accessing directory")
                
        def on_file_double_click(self, event):
            """Handle double-click on file tree."""
            selection = self.file_tree.selection()
            if selection:
                item = selection[0]
                file_path = self.file_tree.item(item, "values")[0]
                if os.path.isfile(file_path):
                    if self.check_save_changes():
                        try:
                            with open(file_path, 'r', encoding='utf-8') as file:
                                content = file.read()
                                self.text_editor.delete(1.0, tk.END)
                                self.text_editor.insert(1.0, content)
                                self.current_file = file_path
                                self.file_modified = False
                                self.file_label.config(text=os.path.basename(file_path))
                                self.update_title()
                                self.update_outline()
                        except Exception as e:
                            messagebox.showerror("Error", f"Could not open file: {str(e)}")
                            
        def browse_folder(self):
            """Browse for a folder."""
            folder = filedialog.askdirectory()
            if folder:
                self.load_directory(folder)
                
        def refresh_files(self):
            """Refresh file list."""
            # Implementation would refresh current directory
            pass
            
        def toggle_word_wrap(self):
            """Toggle word wrap in editor."""
            current_wrap = self.text_editor.cget("wrap")
            new_wrap = tk.NONE if current_wrap == tk.WORD else tk.WORD
            self.text_editor.config(wrap=new_wrap)
            
        def toggle_line_numbers(self):
            """Toggle line numbers display."""
            # Implementation would show/hide line numbers
            pass
            
        def exit_app(self):
            """Exit the application."""
            if self.check_save_changes():
                self.root.quit()
                
        def run(self):
            """Run the application."""
            self.root.protocol("WM_DELETE_WINDOW", self.exit_app)
            self.root.mainloop()

    if __name__ == "__main__":
        app = TextEditorApp()
        app.run()

Image Viewer Application
------------------------

A complete image viewer with thumbnail browser:

.. code-block:: python

    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox
    from PIL import Image, ImageTk
    import os
    from threepanewindows import DockableThreePaneWindow

    class ImageViewerApp:
        """A complete image viewer application."""
        
        def __init__(self):
            self.root = tk.Tk()
            self.root.title("Professional Image Viewer")
            self.root.geometry("1200x800")
            
            self.current_image = None
            self.image_list = []
            self.current_index = 0
            
            self.setup_ui()
            
        def setup_ui(self):
            """Set up the user interface."""
            self.create_menu()
            
            # Create dockable layout
            self.window = DockableThreePaneWindow(
                self.root,
                side_width=200,
                left_builder=self.build_thumbnail_panel,
                center_builder=self.build_image_viewer,
                right_builder=self.build_info_panel
            )
            self.window.pack(fill=tk.BOTH, expand=True)
            
            # Status bar
            self.status_bar = tk.Label(self.root, text="Ready", 
                                     relief=tk.SUNKEN, anchor=tk.W)
            self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
            
        def create_menu(self):
            """Create the application menu."""
            menubar = tk.Menu(self.root)
            
            # File menu
            file_menu = tk.Menu(menubar, tearoff=0)
            file_menu.add_command(label="Open Image", command=self.open_image)
            file_menu.add_command(label="Open Folder", command=self.open_folder)
            file_menu.add_separator()
            file_menu.add_command(label="Exit", command=self.root.quit)
            menubar.add_cascade(label="File", menu=file_menu)
            
            # View menu
            view_menu = tk.Menu(menubar, tearoff=0)
            view_menu.add_command(label="Zoom In", command=self.zoom_in)
            view_menu.add_command(label="Zoom Out", command=self.zoom_out)
            view_menu.add_command(label="Fit to Window", command=self.fit_to_window)
            view_menu.add_command(label="Actual Size", command=self.actual_size)
            menubar.add_cascade(label="View", menu=view_menu)
            
            self.root.config(menu=menubar)
            
        def build_thumbnail_panel(self, frame):
            """Build the thumbnail browser panel."""
            tk.Label(frame, text="🖼️ Thumbnails", font=("Arial", 11, "bold")).pack(pady=5)
            
            # Thumbnail listbox
            self.thumbnail_listbox = tk.Listbox(frame, font=("Arial", 9))
            thumb_scroll = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.thumbnail_listbox.yview)
            self.thumbnail_listbox.configure(yscrollcommand=thumb_scroll.set)
            
            self.thumbnail_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
            thumb_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
            
            # Bind selection
            self.thumbnail_listbox.bind('<<ListboxSelect>>', self.on_thumbnail_select)
            
        def build_image_viewer(self, frame):
            """Build the main image viewer panel."""
            # Viewer toolbar
            toolbar = tk.Frame(frame, bg="#f0f0f0", height=40)
            toolbar.pack(fill=tk.X)
            toolbar.pack_propagate(False)
            
            # Navigation buttons
            tk.Button(toolbar, text="⬅️ Previous", command=self.previous_image).pack(side=tk.LEFT, padx=5, pady=5)
            tk.Button(toolbar, text="➡️ Next", command=self.next_image).pack(side=tk.LEFT, padx=5, pady=5)
            
            # Zoom controls
            tk.Button(toolbar, text="🔍+ Zoom In", command=self.zoom_in).pack(side=tk.LEFT, padx=5, pady=5)
            tk.Button(toolbar, text="🔍- Zoom Out", command=self.zoom_out).pack(side=tk.LEFT, padx=5, pady=5)
            tk.Button(toolbar, text="📐 Fit", command=self.fit_to_window).pack(side=tk.LEFT, padx=5, pady=5)
            
            # Image display area
            self.image_frame = tk.Frame(frame, bg="gray")
            self.image_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            # Canvas for image display
            self.image_canvas = tk.Canvas(self.image_frame, bg="white")
            
            # Scrollbars for large images
            v_scroll = tk.Scrollbar(self.image_frame, orient=tk.VERTICAL, command=self.image_canvas.yview)
            h_scroll = tk.Scrollbar(self.image_frame, orient=tk.HORIZONTAL, command=self.image_canvas.xview)
            self.image_canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)
            
            self.image_canvas.grid(row=0, column=0, sticky="nsew")
            v_scroll.grid(row=0, column=1, sticky="ns")
            h_scroll.grid(row=1, column=0, sticky="ew")
            
            self.image_frame.grid_rowconfigure(0, weight=1)
            self.image_frame.grid_columnconfigure(0, weight=1)
            
        def build_info_panel(self, frame):
            """Build the image information panel."""
            tk.Label(frame, text="ℹ️ Image Info", font=("Arial", 11, "bold")).pack(pady=5)
            
            # Image info display
            info_frame = tk.LabelFrame(frame, text="Properties", font=("Arial", 10, "bold"))
            info_frame.pack(fill=tk.X, padx=5, pady=5)
            
            self.info_labels = {}
            properties = ["Filename", "Size", "Dimensions", "Format", "Mode"]
            
            for prop in properties:
                prop_frame = tk.Frame(info_frame)
                prop_frame.pack(fill=tk.X, padx=5, pady=2)
                
                tk.Label(prop_frame, text=f"{prop}:", font=("Arial", 9), width=10, anchor="w").pack(side=tk.LEFT)
                self.info_labels[prop] = tk.Label(prop_frame, text="-", font=("Arial", 9), anchor="w")
                self.info_labels[prop].pack(side=tk.LEFT, fill=tk.X, expand=True)
                
        # Image operations
        def open_image(self):
            """Open a single image file."""
            filename = filedialog.askopenfilename(
                title="Open Image",
                filetypes=[
                    ("Image files", "*.jpg *.jpeg *.png *.gif *.bmp *.tiff"),
                    ("JPEG files", "*.jpg *.jpeg"),
                    ("PNG files", "*.png"),
                    ("All files", "*.*")
                ]
            )
            if filename:
                self.load_image(filename)
                
        def open_folder(self):
            """Open a folder and load all images."""
            folder = filedialog.askdirectory(title="Select Image Folder")
            if folder:
                self.load_folder(folder)
                
        def load_folder(self, folder_path):
            """Load all images from a folder."""
            image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff')
            self.image_list = []
            
            try:
                for filename in os.listdir(folder_path):
                    if filename.lower().endswith(image_extensions):
                        self.image_list.append(os.path.join(folder_path, filename))
                        
                # Update thumbnail list
                self.thumbnail_listbox.delete(0, tk.END)
                for image_path in self.image_list:
                    self.thumbnail_listbox.insert(tk.END, os.path.basename(image_path))
                    
                if self.image_list:
                    self.current_index = 0
                    self.load_image(self.image_list[0])
                    self.thumbnail_listbox.selection_set(0)
                    
            except Exception as e:
                messagebox.showerror("Error", f"Could not load folder: {str(e)}")
                
        def load_image(self, image_path):
            """Load and display an image."""
            try:
                # Load image
                self.current_image = Image.open(image_path)
                self.display_image()
                self.update_image_info(image_path)
                self.status_bar.config(text=f"Loaded: {os.path.basename(image_path)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not load image: {str(e)}")
                
        def display_image(self):
            """Display the current image on canvas."""
            if self.current_image:
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(self.current_image)
                
                # Clear canvas
                self.image_canvas.delete("all")
                
                # Display image
                self.image_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
                self.image_canvas.image = photo  # Keep a reference
                
                # Update scroll region
                self.image_canvas.configure(scrollregion=self.image_canvas.bbox("all"))
                
        def update_image_info(self, image_path):
            """Update image information display."""
            if self.current_image:
                filename = os.path.basename(image_path)
                file_size = os.path.getsize(image_path)
                size_str = f"{file_size:,} bytes"
                
                self.info_labels["Filename"].config(text=filename)
                self.info_labels["Size"].config(text=size_str)
                self.info_labels["Dimensions"].config(text=f"{self.current_image.width} x {self.current_image.height}")
                self.info_labels["Format"].config(text=self.current_image.format or "Unknown")
                self.info_labels["Mode"].config(text=self.current_image.mode)
                
        # Navigation
        def previous_image(self):
            """Show previous image."""
            if self.image_list and self.current_index > 0:
                self.current_index -= 1
                self.load_image(self.image_list[self.current_index])
                self.thumbnail_listbox.selection_clear(0, tk.END)
                self.thumbnail_listbox.selection_set(self.current_index)
                
        def next_image(self):
            """Show next image."""
            if self.image_list and self.current_index < len(self.image_list) - 1:
                self.current_index += 1
                self.load_image(self.image_list[self.current_index])
                self.thumbnail_listbox.selection_clear(0, tk.END)
                self.thumbnail_listbox.selection_set(self.current_index)
                
        def on_thumbnail_select(self, event):
            """Handle thumbnail selection."""
            selection = self.thumbnail_listbox.curselection()
            if selection and self.image_list:
                index = selection[0]
                self.current_index = index
                self.load_image(self.image_list[index])
                
        # Zoom operations
        def zoom_in(self):
            """Zoom in on the image."""
            if self.current_image:
                width, height = self.current_image.size
                new_width = int(width * 1.2)
                new_height = int(height * 1.2)
                self.current_image = self.current_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                self.display_image()
                
        def zoom_out(self):
            """Zoom out on the image."""
            if self.current_image:
                width, height = self.current_image.size
                new_width = int(width * 0.8)
                new_height = int(height * 0.8)
                if new_width > 10 and new_height > 10:  # Minimum size
                    self.current_image = self.current_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    self.display_image()
                    
        def fit_to_window(self):
            """Fit image to window size."""
            # Implementation would resize image to fit canvas
            pass
            
        def actual_size(self):
            """Show image at actual size."""
            if self.image_list and self.current_index < len(self.image_list):
                self.load_image(self.image_list[self.current_index])
                
        def run(self):
            """Run the application."""
            self.root.mainloop()

    if __name__ == "__main__":
        app = ImageViewerApp()
        app.run()

Key Features of Real-World Applications
---------------------------------------

These complete applications demonstrate:

1. **Professional Architecture**: Well-organized code structure
2. **Full Menu Integration**: Complete menu systems with keyboard shortcuts
3. **File Management**: Opening, saving, and managing files
4. **User Experience**: Status bars, toolbars, and responsive interfaces
5. **Error Handling**: Proper exception handling and user feedback
6. **State Management**: Tracking application state and user preferences
7. **Multi-Panel Coordination**: Panels working together seamlessly

Application Patterns
--------------------

Common patterns in professional applications:

**Document-Based Applications**
- File explorer for navigation
- Main editor/viewer in center
- Properties/tools on the side

**Media Applications**
- Thumbnail browser
- Main display area
- Information and controls

**Development Tools**
- Project explorer
- Code editor
- Output/debugging panels

Best Practices Demonstrated
---------------------------

1. **Separation of Concerns**: UI, business logic, and data handling separated
2. **Event-Driven Architecture**: Proper event handling and callbacks
3. **User Feedback**: Status updates and error messages
4. **Keyboard Shortcuts**: Full keyboard navigation support
5. **Responsive Design**: Layouts that adapt to window resizing
6. **Professional Polish**: Attention to details like icons and styling

Next Steps
----------

Use these examples as starting points for your own applications:

- Modify the layouts to suit your needs
- Add your own business logic
- Customize the appearance and theming
- Extend with additional features
- Integrate with external libraries and services

For more specific examples, see:

- :doc:`custom_widgets` - Creating specialized panel content
- :doc:`theming_examples` - Advanced styling and theming