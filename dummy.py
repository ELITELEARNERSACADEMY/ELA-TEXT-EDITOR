import tkinter as tk
from tkinter import messagebox
import os

class Creator:
    def __init__(self):
        self.system_theme = self.detect_system_theme()
        self.introduction_window()
        self.slide_size = 0 
        self.count_slides = 0
        self.file_dir = ''
        self.courseTitle =''
    
    def detect_system_theme(self):
        """
        Detect the system theme (light or dark) for Windows, macOS, and Linux.
        Returns:
        str: 'light' or 'dark' based on the detected theme.
        """
        try:
            import platform
            import subprocess

            system = platform.system()

            if system == "Windows":
                try:
                    from winreg import OpenKey, QueryValueEx, HKEY_CURRENT_USER

                    key = OpenKey(HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                    value = QueryValueEx(key, "AppsUseLightTheme")[0]
                    return 'light' if value == 1 else 'dark'
                except Exception as e:
                    print(f"Error detecting Windows theme: {e}")
                    return 'light'

            elif system == "Darwin":  # macOS
                try:
                    result = subprocess.run(
                        ["defaults", "read", "-g", "AppleInterfaceStyle"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    return 'dark' if "Dark" in result.stdout else 'light'
                except Exception as e:
                    print(f"Error detecting macOS theme: {e}")
                    return 'light'

            elif system == "Linux":
                try:
                    result = subprocess.run(
                        ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    return 'dark' if "dark" in result.stdout.lower() else 'light'
                except Exception as e:
                    print(f"Error detecting Linux theme: {e}")
                    return 'light'

            else:
                print(f"Unsupported platform: {system}")
                return 'light'

        except Exception as e:
            print(f"Error detecting system theme: {e}")
            return 'light'

    def introduction_window(self):
        self.root = tk.Tk()
        self.root.title("Elite Learners Academy")

        # Adjust background and text color based on theme
        bg_color = "#2e2e2e" if self.system_theme == 'dark' else "#f4f4f4"
        self.root.config(bg=bg_color)

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(True, True)

        label_bg = bg_color
        label_fg = "#ffffff" if self.system_theme == 'dark' else "#000000"

        self.create_label_entry("Course Title:", label_bg, label_fg, "title_entry")
        self.create_label_entry("Duration (in hours):", label_bg, label_fg, "duration_entry")
        self.create_label_entry("Author Name:", label_bg, label_fg, "author_entry")
        self.create_label_entry("Number of Modules:", label_bg, label_fg, "module_entry")

        # Course Overview
        tk.Label(self.root, text="Course Overview:", font=("Arial", 18), bg=label_bg, fg=label_fg).pack(anchor="nw", padx=20, pady=5)
        self.course_overview = tk.Text(self.root, font=("Arial", 18), height=7, wrap="word", bd=2, relief="solid")
        self.course_overview.pack(padx=20, pady=5)

        button_bg = "#4CAF50" if self.system_theme == 'light' else "#444444"
        button_fg = "white"

        tk.Button(
            self.root,
            text="Start",
            font=("Arial", 12),
            bg=button_bg,
            fg=button_fg,
            bd=0,
            relief="flat",
            command=self.start_course
        ).pack(pady=20)

        self.root.mainloop()

    def create_label_entry(self, label_text, label_bg, label_fg, attr_name):
        tk.Label(self.root, text=label_text, font=("Arial", 18), bg=label_bg, fg=label_fg).pack(anchor="w", padx=20, pady=5)
        entry = tk.Entry(self.root, font=("Arial", 18), width=30, bd=2, relief="solid")
        entry.pack(padx=20, pady=5)
        setattr(self, attr_name, entry)


    def start_course(self):
        title = self.title_entry.get().strip()
        duration = self.duration_entry.get().strip()
        author = self.author_entry.get().strip()
        modules = self.module_entry.get().strip()
        overview = self.course_overview.get("1.0", "end").strip()

        self.courseTitle = title

        if not title or not duration or not author or not modules.isdigit() or not overview:
            messagebox.showwarning("Input Error", "Please fill all fields correctly!")
            return

        self.modules = int(modules)
        self.current_module = 1
        self.count_slides = 0        
        self.directory(title,int(modules))
        self.mkfile(f"{self.file_dir}/index.html")
        self.writeFile(f"{self.file_dir}/index.html", title, duration, author, self.modules, overview)
        self.handler(f"{self.file_dir}/AUTH/")


        messagebox.showinfo("File Created", "description.html file has been created successfully.")
        self.root.destroy()
        self.module_window()


    def mkfile(self, fileName):
        try:
            with open(fileName, 'x') as f:
                pass
        except FileExistsError:
            print(f"{fileName} already exists.")



    def module_window(self):
        self.root = tk.Tk()
        self.root.title(f"Module {self.current_module}")
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(True, True)
        # Adjust background and text color based on theme
        if self.system_theme == 'dark':
            self.root.config(bg="#2e2e2e")
        else:
            self.root.config(bg="#f4f4f4")


        label_bg = "#2e2e2e" if self.system_theme == 'dark' else "#f4f4f4"
        label_fg = "#ffffff" if self.system_theme == 'dark' else "#000000"

        tk.Label(self.root, text=f"Module {self.current_module}", font=("Arial", 24), bg=label_bg,fg=label_fg).pack(pady=10)
        tk.Label(self.root, text="Enter number of slides (at most 30):", font=("Arial", 18), bg=label_bg,fg=label_fg).pack(pady=5)

        self.slides_entry = tk.Entry(self.root, font=("Arial", 18), width=10, bd=2, relief="solid")
        self.slides_entry.pack(pady=5)

        button_bg = "#2196F3" if self.system_theme == 'light' else "#444444"
        button_fg = "white"

        tk.Button(
            self.root,
            text="Next",
            font=("Arial", 12),
            bg=button_bg,
            fg=button_fg,
            bd=0,
            relief="flat",
            command=self.create_slides
        ).pack(pady=20)

        self.root.mainloop()
            
    def create_slides(self):
        slides = self.slides_entry.get().strip()
        if not slides.isdigit() or int(slides) > 30:
            messagebox.showwarning("Input Error", "Please enter a valid number of slides!")
            return

        self.slides = int(slides)
        self.root.destroy()
        self.slide_window()

    def slide_window(self):
        self.root = tk.Tk()
        self.root.title(f"Slides for Module {self.current_module}")
        self.root.geometry("800x600")
        # Adjust background and text color based on theme
        if self.system_theme == 'dark':
            self.root.config(bg="#2e2e2e")
        else:
            self.root.config(bg="#f4f4f4")

        self.width= self.root.winfo_screenwidth()               
        self.height= self.root.winfo_screenheight()               
        self.root.geometry("%dx%d" % (self.width, self.height))
        self.root.resizable(True, True)


        canvas = tk.Canvas(self.root, bg="white")
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        scrollable_frame = tk.Frame(canvas, bg="#f4f4f4")
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        self.slide_data_dict = []
        self.slide_size = self.slides
        for slide in range(1, self.slides + 1):
            tk.Label(scrollable_frame, text=f"Slide {slide}", font=("Arial", 24), bg="#f4f4f4").pack(pady=10)

            slide_data = {}
            slide_data["header"] = self.create_input_field(scrollable_frame, "Header:")
            slide_data["mediaFileUrl"] = self.create_input_field(scrollable_frame, "Media File url:")
            slide_data["paragraph"] = self.create_text_area(scrollable_frame, "Paragraph:")
            slide_data["question"] = self.create_input_field(scrollable_frame, "Question:")

            for option in ['A', 'B', 'C', 'D']:
                slide_data[f"opt{option}"] = self.create_input_field(scrollable_frame, f"Option {option}:")

            slide_data["answer"] = self.create_input_field(scrollable_frame, "Correct Answer:")
            self.slide_data_dict.append(slide_data)

        tk.Button(
            scrollable_frame,
            text="Save & Next",
            font=("Arial", 14),
            bg="#4CAF50",
            fg="white",
            bd=0,
            relief="flat",
            command=self.save_and_next
        ).pack(pady=20)

        self.root.mainloop()

    def create_input_field(self, parent, label_text):
        tk.Label(parent, text=label_text, font=("Arial", 18), bg="#f4f4f4").pack(anchor="w", padx=10, pady=5)
        entry = tk.Entry(parent, font=("Arial", 12), width=50, bd=2, relief="solid")
        entry.pack(pady=5)
        return entry

    def create_text_area(self, parent, label_text):
        tk.Label(parent, text=label_text, font=("Arial", 18), bg="#f4f4f4").pack(anchor="w", padx=10, pady=5)
        text_area = tk.Text(parent, font=("Arial", 12), width=100, height=6, bd=2, relief="solid")
        text_area.pack(pady=5)
        return text_area
    def directory(self,parent,child):
        home_directory = os.path.expanduser("~")
        parent = parent.upper()
        self.file_dir = os.path.join(home_directory, parent)
        file_directory = os.path.join(home_directory, parent)
        os.makedirs(self.file_dir, exist_ok=True)
        os.makedirs(file_directory, exist_ok=True)
        os.makedirs(os.path.join(file_directory,f"ASSETS"),exist_ok = True)
        os.makedirs(os.path.join(file_directory,f"AUTH"),exist_ok = True)
        
        for i in range(1,child+1):
            os.makedirs(os.path.join(file_directory,f"module{i}"),exist_ok = True)

    def save_and_next(self):
         for i, slide_data in enumerate(self.slide_data_dict):
             if i == self.slide_size-1:
                nextSlideName = f"celebration.html"
                self.celebration(f"{self.file_dir}/module{self.current_module}/")
             else:
                nextSlideName = f"module_{self.current_module}_slide_{i + 2}.html"
    
             if i >= 1 :
                 previousslide = f"module_{self.current_module}_slide_{i}.html"
    
             else:    
                 previousslide = ''
              #tracking the total number of slides
             self.count_slides += 1
    
             self.writeFileSlide(
                 f"{self.file_dir}/module{self.current_module}/module_{self.current_module}_slide_{i + 1}.html",
                 f"module_{self.current_module}_slide_{i + 1}.html",
                 slide_data["header"].get(),
                 slide_data["mediaFileUrl"].get(),
                 slide_data["paragraph"].get("1.0", "end").strip(),
                 slide_data["question"].get(),
                 slide_data["optA"].get(),
                 slide_data["optB"].get(),
                 slide_data["optC"].get(),
                 slide_data["optD"].get(),
                 slide_data["answer"].get(),
                 nextSlideName,
                 previousslide,
                 self.current_module,
                 self.count_slides  # slide number
             )
             
    
         if self.current_module < self.modules:
             if messagebox.askyesno("Confirmation", "Proceed to the next module? You cannot go back."):
                 self.current_module += 1
                 self.root.destroy()
                 self.module_window()
         else:
             messagebox.showinfo("Completion", "All modules completed and saved.")
             self.root.quit()
             self.root.destroy()
         
         
    def writeFile(self, fileName, title, duration, author, modules, overview):
        with open(f"{self.file_dir}/README.md", "a") as file:
            file.write('\n')
            file.write(f'    Author: {author}\n')
            file.write(f'    Module: {modules} \n')
            file.write(f'    Overview: {overview}\n')


        with open(fileName, 'w') as f:            
            f.write(f'<!doctype html>\n')
            f.write(f'<html lang="en" data-bs-theme="auto">\n')
            f.write(f'  <head><script src="https://elitelearnersacademy.com/JS/color-modes.js"></script>\n')
            f.write(f'\n')
            f.write(f'    <meta charset="utf-8">\n')
            f.write(f'    <meta name="viewport" content="width=device-width, initial-scale=1">\n')
            f.write(f'    <meta name="description" content="">\n')
            f.write(f'    <meta name="author" content="Mark Otto, Jacob Thornton, and Bootstrap contributors">\n')
            f.write(f'    <meta name="generator" content="Hugo 0.122.0">\n')
            f.write(f'    <title>{title}</title>\n')
            f.write(f'\n')
            f.write(f'    <link rel="canonical" href="https://elitelearnersacademy.com/">\n')
            f.write(f'\n')
            f.write(f'\n')
            f.write(f'<link href="https://elitelearnersacademy.com/CSS/bootstrap.min.css" rel="stylesheet">\n')
            f.write(f'\n')
            f.write(f'    <style>\n')
            f.write('      .bd-placeholder-img {\n')
            f.write(f'        font-size: 1.125rem;\n')
            f.write(f'        text-anchor: middle;\n')
            f.write(f'        -webkit-user-select: none;\n')
            f.write(f'        -moz-user-select: none;\n')
            f.write(f'        user-select: none;\n')
            f.write('      }\n')
            f.write(f'\n')
            f.write('      @media (min-width: 768px) {\n')
            f.write('        .bd-placeholder-img-lg {\n')
            f.write(f'          font-size: 3.5rem;\n')
            f.write('        }\n')
            f.write('      }\n')
            f.write(f'\n')
            f.write('      .b-example-divider {\n')
            f.write(f'        width: 100%;\n')
            f.write(f'        height: 3rem;\n')
            f.write(f'        background-color: rgba(0, 0, 0, .1);\n')
            f.write(f'        border: solid rgba(0, 0, 0, .15);\n')
            f.write(f'        border-width: 1px 0;\n')
            f.write(f'        box-shadow: inset 0 .5em 1.5em rgba(0, 0, 0, .1), inset 0 .125em .5em rgba(0, 0, 0, .15);\n')
            f.write('      }\n')
            f.write(f'\n')
            f.write('      .b-example-vr {\n')
            f.write(f'        flex-shrink: 0;\n')
            f.write(f'        width: 1.5rem;\n')
            f.write(f'        height: 100vh;\n')
            f.write('      }\n')
            f.write(f'\n')
            f.write('      .bi {\n')
            f.write(f'        vertical-align: -.125em;\n')
            f.write(f'        fill: currentColor;\n')
            f.write('      }\n')
            f.write(f'\n')
            f.write('      .nav-scroller {\n')
            f.write(f'        position: relative;\n')
            f.write(f'        z-index: 2;\n')
            f.write(f'        height: 2.75rem;\n')
            f.write(f'        overflow-y: hidden;\n')
            f.write('      }\n')
            f.write(f'\n')
            f.write('      .nav-scroller .nav {\n')
            f.write(f'        display: flex;\n')
            f.write(f'        flex-wrap: nowrap;\n')
            f.write(f'        padding-bottom: 1rem;\n')
            f.write(f'        margin-top: -1px;\n')
            f.write(f'        overflow-x: auto;\n")\n')
            f.write(f'        text-align: center;\n')
            f.write(f'        white-space: nowrap;\n')
            f.write(f'        -webkit-overflow-scrolling: touch;\n')
            f.write('      }\n')
            f.write(f'\n')
            f.write('      .btn-bd-primary {\n')
            f.write(f'        --bd-violet-bg: #712cf9;\n')
            f.write(f'        --bd-violet-rgb: 112.520718, 44.062154, 249.437846;\n')
            f.write(f'\n')
            f.write(f'        --bs-btn-font-weight: 600;\n')
            f.write(f'        --bs-btn-color: var(--bs-white);\n')
            f.write(f'        --bs-btn-bg: var(--bd-violet-bg);\n')
            f.write(f'        --bs-btn-border-color: var(--bd-violet-bg);\n')
            f.write(f'        --bs-btn-hover-color: var(--bs-white);\n')
            f.write(f'        --bs-btn-hover-bg: #6528e0;\n')
            f.write(f'        --bs-btn-hover-border-color: #6528e0;\n')
            f.write(f'        --bs-btn-focus-shadow-rgb: var(--bd-violet-rgb);\n')
            f.write(f'        --bs-btn-active-color: var(--bs-btn-hover-color);\n')
            f.write(f'        --bs-btn-active-bg: #5a23c8;\n')
            f.write(f'        --bs-btn-active-border-color: #5a23c8;\n')
            f.write('      }\n')
            f.write(f'\n')
            f.write('      .bd-mode-toggle {\n')
            f.write(f'        z-index: 1500;\n')
            f.write('      }\n')
            f.write(f'\n')
            f.write('      .bd-mode-toggle .dropdown-menu .active .bi {\n')
            f.write(f'        display: block !important;\n')
            f.write('      }\n')
            f.write(f'    </style>\n')
            f.write(f'\n')
            f.write(f'    \n')
            f.write(f'    <!-- Custom styles for this template -->\n')
            f.write(f'    <link href="https://elitelearnersacadmy.com/CSS/sidebars.css" rel="stylesheet">\n')
            f.write(f'  </head>\n')
            f.write("<body style='width:100%; margin:0;'>\n")
            f.write("\n")
            f.write('  <nav class="navbar navbar-expand-md bg-dark sticky-top border-bottom" data-bs-theme="dark">\n')
            f.write('    <div class="container">\n')
            f.write("      <a class='navbar-brand d-md-none' href='#'>\n")
            f.write("        <img  src='https://elitelearnersacademy.com/ASSETS/logo.jpg' class='bi' width='24' height='24'/>\n")
            f.write("\n")
            f.write("      </a>\n")
            f.write('      <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvas" aria-controls="offcanvas" aria-label="Toggle navigation">\n')
            f.write('        <span class="navbar-toggler-icon"></span>\n')
            f.write("      </button>\n")
            f.write('      <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvas" aria-labelledby="offcanvasLabel">\n')
            f.write('        <div class="offcanvas-header">\n')
            f.write('          <h5 class="offcanvas-title" id="offcanvasLabel">Elite Leaners Academy</h5>\n')
            f.write('          <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>\n')
            f.write("        </div>\n")
            f.write("        \n")
            f.write('        <div class="offcanvas-body">\n')
            f.write('          <ul class="navbar-nav flex-grow-1 justify-content-between">\n')
            f.write('            <li class="nav-item">\n')
            f.write('              <a href="https://elitelearnersacademy.com/" class="navbar-brand ">\n')
            f.write('                <img src="https://elitelearnersacademy.com/ASSETS/logo.jpg" width="20" height="20" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" aria-hidden="true" class="me-2" viewBox="0 0 24 24"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>Elite learners Academy\n')
            f.write("             </a>\n")
            f.write("            </li>\n")
            f.write('            <li class="nav-item"><a class="nav-link" href="https://elitelearnersacademy.com/LEARNING/chat.php">Discuss</a></li>\n')
            f.write('            <li class="nav-item"><a class="nav-link" href="#">ClassRoom</a></li>\n')
            f.write('            <li class="nav-item"><a class="nav-link" href="#">Join Live</a></li>\n')
            f.write('            <li class="nav-item"><a class="nav-link" id="certificateLink" href="#"  target="_blank" >Certificate</a></li>\n')
            f.write('            <li class="nav-item"><a class="nav-link" id="certificateLink" href="https://elitelearnersacademy.com/LEARNING/user_progress.php"  target="_blank" >View Progress</a></li>\n')            
            f.write('            <li class="nav-item"><a class="nav-link" href="https://elitelearnersacademy.com/LEARNING/my_courses.php">Previous</a></li>\n')
            f.write("          </ul>\n")
            f.write("        </div>\n")
            f.write("      </div>\n")
            f.write("    </div>\n")
            f.write(" \n </nav>")
  
            f.write(f'\n')
            f.write(f'\n')
            f.write(f'<main class="d-flex flex-nowrap">\n')
            f.write(f'  <div class="d-flex flex-column align-items-stretch flex-shrink-0 bg-body-tertiary" style="width: 25vw;"></div>\n')
            f.write(f'  <div class="b-example-divider b-example-vr"></div>\n')
            f.write(f'  <div class="d-flex flex-column align-items-stretch flex-shrink-0 bg-body-tertiary" style="width: 50vw;">\n')
            f.write(f'\n')
            f.write(f'    <div  class="d-flex align-items-center flex-shrink-0 p-3 link-body-emphasis text-decoration-none border-bottom">\n')
            f.write(f'      <img src="{self.file_dir}/ASSETS/logo.png" alt="logo" class="bi" width="40" height="32" role="img" />\n')
            f.write(f'      <span class="fs-5 fw-semibold"></span>\n')
            f.write(f'    </div>\n') 
            f.write(f'    <div class="list-group list-group-flush border-bottom scrollarea">\n')
            f.write(f'      <div class="mb-1">\n')
            f.write(f'        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#OV" aria-expanded="false">\n')
            f.write(f'          Overview \n')
            f.write(f'        </button>\n')
            f.write(f'        <div class="collapse" id="OV">\n')
            f.write(f'\n')
            f.write(f'      <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">\n')
            f.write(f"\n")
            f.write(f'          <li> ')
            f.write(f'                 <div class="col-10 mb-1 text-wrap small" >{overview} .By {author},{duration} hour course</div>\n')
            f.write(f"          </li>\n")
            f.write(f"\n")
            f.write(f"  </ul>\n")
            f.write(f"\n")
            f.write(f"     </div>\n")
            f.write(f"    </div>\n")
            f.write(f"    </div>\n")

            f.write(f'\n')

            f.write(f'\n')
            f.write(f'\n')

            for module in range(1,modules+1):                        
                                    f.write(f'    <div class="list-group list-group-flush border-bottom scrollarea">\n')
                                    f.write(f'\n')
                                    f.write(f'      <div class="mb-1">\n')
                                    f.write(f'        <button class="btn btn-toggle d-inline-flex align-items-center rounded border-0 collapsed" data-bs-toggle="collapse" data-bs-target="#{module}" aria-expanded="false">\n')
                                    f.write(f'          Module {module}\n')
                                    f.write(f'        </button>\n')
                                    f.write(f'        <div class="collapse" id="{module}">\n')
                                    f.write(f'\n')
                                    f.write(f'      <ul class="btn-toggle-nav list-unstyled fw-normal pb-1 small">\n')
                                    f.write(f"\n")
                                    f.write(f'          <li> <a href="{self.file_dir}/module{module}/module_{module}_slide_1.html" class="list-group-item list-group-item-action active py-3 lh-sm" aria-current="true">\n')
                                    f.write(f'                  <div class="d-flex w-100 align-items-center justify-content-between">\n')
                                    f.write(f'                   <strong class="mb-1 text-wrap">Module {module}</strong>\n')
                                    f.write(f"                 </div>\n")
                                    f.write(f'                 <div class="col-10 mb-1 small">content</div>\n')
                                    f.write(f"              </a>\n")
                                    f.write(f"          </li>\n")
                                    f.write(f"\n")
                                    f.write(f"  </ul>\n")
                                    f.write(f"\n")
                                    f.write(f"     </div>\n")
                                    f.write(f"    </div>\n")
                                    f.write(f"    </div>\n")
                                    
                                    
            f.write(f"\n")
            f.write(f'  <div class="d-flex flex-column align-items-stretch flex-shrink-0 bg-body-tertiary" style="width: 25Svw;"></div>\n')
            f.write(f"</main>\n")
            f.write(f'<script src="https://elitelearnersacademy.com/JS/bootstrap.bundle.min.js"></script>\n')
            f.write(f'<script src="https://elitelearnersacademy.com/JS/sidebars.js"></script>\n')
            f.write("<script>\n");
            f.write("               // Function to fetch and display the overall course progress\n");
            f.write("               function fetchCourseProgress(courseTitle) {\n");
            f.write("                 // Make an AJAX GET request to handler.php\n");
            f.write(f"                 fetch('{self.file_dir}/AUTH/handler.php?courseTitle=' + encodeURIComponent(courseTitle))\n");
            f.write("                   .then(response => response.json())\n");
            f.write("                   .then(data => {\n");
            f.write("                     // Check if the response contains progress data\n");
            f.write("                     if (data.progress) {\n");
            f.write("                       // Update the progress percentage in the HTML\n");
            f.write("                       document.getElementById('progressPercentage').innerText = data.progress + '%';\n");
            f.write("                     } else if (data.error) {\n");
            f.write("                       // Handle error if the course was not found\n");
            f.write("                       console.error('Error fetching course progress:', data.error);\n");
            f.write("                     }\n");
            f.write("                   })\n");
            f.write("                   .catch(error => {\n");
            f.write("                     console.error('Error:', error);\n");
            f.write("                   });\n");
            f.write("               }\n");
            f.write("             \n");
            f.write("               // Call the function when the page loads, passing the course title\n");
            f.write("               document.addEventListener('DOMContentLoaded', function() {\n");
            f.write("                 fetchCourseProgress('Ela-Python'); // Replace with your actual course title\n");
            f.write("               });\n");
            f.write("</script>\n");
            f.write(f"\n")
            f.write(f"</body>\n")
            f.write(f"\n")
            f.write(f"</html>\n")
                         
            
            
            
            
    def writeFileSlide(self, fileName,slide_name, header, mediaFileUrl, paragraph, question, optA, optB, optC, optD, answer,nextSlideName,previousslide,moduleID,slideID):
        try:
            with open(fileName, 'x') as f:
                 print()
        except:
               print('file already exists')
        #Changing the media name to directory


        with open(fileName, 'w') as f:
                f.write(f"<!Doctype html>\n")
                f.write(f"<html lang = 'en'>")
                f.write(f"<head>\n")
                f.write(f"  <meta charset='utf-8'>\n")
                f.write(f"  <meta http-equiv='X-UA-Compatible' content='IE=edge,chrome=1'>\n")
                f.write(f"  <meta name='viewport' content='width=device-width, initial-scale=1'>\n")
                f.write(f"  <meta name='description' content='online courses,elearning platform ,Quizs'/>\n")
                f.write(f"  <meta name='author' content='elitelearnersacademy' />\n")
                f.write(f"  <meta name='generator' content='Hugo 0.122.0'>\n")
                f.write(f'  <link rel="stylesheet" href="https://elitelearnersacademy.com/CSS/bootstrap.min.css" type="text/CSS">  \n')                
                f.write(f"     <title>{header}</title>\n")
                f.write(f"<head>\n")
                f.write(f"<body>\n")
                f.write(f"   <main class='container'>\n")
                if header:
                     f.write(f"<h3 class='display-4 fst-italic'>{header}</h3>\n")                
                #media extension  
                video_formats = ["mp4","webm","ogg","mov","mkv","avi","flv","m4v","3gp","wmv"]
                photo_formats = ["jpg","jpeg","png","gif","webp","bmp","svg","ico","tiff","tif","apng","avif"]
                document_formats = ["html","htm","pdf","txt","xml","xhtml","csv","json","svg","docx","xlsx","ods","odt","rtf","yaml","md"]
                audio_formats = ["mp3","ogg","wav","aac","m4a","flac","webm","opus"]

                mediaExtension =''

                #media type logic
                if mediaFileUrl:
                     #getting the media extension
                     for i in range(1,len(mediaFileUrl)):
                          if mediaFileUrl[-i] == '.':
                                break
                          else:
                               mediaExtension = mediaExtension + mediaFileUrl[-i]
     
                     mediaExtension = mediaExtension[::-1]       

                     if mediaExtension in document_formats:
                           f.write(f"<embed type='text/html' src='../ASSETS/{mediaFileUrl}' alt='img' style='width='100%' height:80vh;'>\n")
                     elif mediaExtension in photo_formats:
                           f.write(f"<img type='image/jpg' src='../ASSETS/{mediaFileUrl}' alt='img' width='100%' height='500px'>\n")
                     elif mediaExtension in audio_formats:
                           f.write(f'<div class="card p-4 shadow-lg d-flex justify-content-center align-items-center" style="width: 100%; height: 60vh;" >\n')                       
                           f.write(f'<iframe width="560" height="315" src="../ASSETS/{mediaFileUrl}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>\n')
                           f.write(f"</div>\n")                   
                     elif mediaExtension in video_formats:
                           f.write(f'<div class="card p-4 shadow-lg d-flex justify-content-center align-items-center" style="width: 100%; height: 60vh;" >\n')                                               
                           f.write(f'<iframe width="560" height="315" src="../ASSETS/{mediaFileUrl}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>\n')
                           f.write(f"</div>\n")                   
                     else:
                           f.write(f'<div class="card p-4 shadow-lg d-flex justify-content-center align-items-center" style="width: 100%; height: 60vh;" >\n')                                               
                           f.write(f'    <iframe width="560" height="315" src="{mediaFileUrl}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>\n')
                           f.write(f"</div>\n")                   

                if paragraph:
                     f.write(f"  <div class='p-4 p-md-5 mb-4 text-wrap rounded text-body-emphasis bg-body-secondary' >{paragraph}</div>\n")
                #if no question, continue button to be deployed 
                if not question:
                      if previousslide:
                                f.write(f"                  <a class='btn btn-lg btn-primary' href='{previousslide}' role='button'>previous</a>\n")                                                               
                      f.write(f"<button class='btn btn-success rounded-pill px-3' onclick = \"location.href = '{nextSlideName}';\" style='margin:2rem 3rem 2rem 70vw'>Continue</button>")

                if question:
                     f.write(f'<div class="d-flex flex-column flex-md-row p-4 gap-4 py-md-5 align-items-center justify-content-center">\n')                    
                #take quations
                     f.write(f'         <form class="card p-4 shadow-lg d-flex justify-content-center align-items-center " style="width: 100%; height: 50vh;" >\n')
                     f.write(f"             <ol>\n")
                     f.write(f"             <li>\n")
                     f.write(f"         <p id='question' class='text-wrap'>{question}</p>\n")
                     #if there four MCQ
                     if optA and optB and optC and optD:
                           f.write(f"                  <input type='radio' id='A' name = 'opt' placeholder = '{optA}' value = '{optA}' />\n")
                           f.write(f"                  <label class='form-label' for='A' class='text-wrap'>{optA}</label><br/>\n")
                           f.write(f"                  <input type='radio' id='B' name = 'opt' placeholder = '{optB}' value = '{optB}' />\n")
                           f.write(f"                  <label class='form-label' for='B' class='text-wrap'>{optB}</label><br/>\n")
                           f.write(f"                  <input type='radio' id='C' name = 'opt' placeholder = '{optC}' value = '{optC}' />\n")
                           f.write(f"                  <label class='form-label' for='C' class='text-wrap'>{optC}</label><br/>\n")
                           f.write(f"                  <input type='radio' id='D' name = 'opt' placeholder = '{optD}' value = '{optD}' />\n")
                           f.write(f"                  <label class='form-label' for='D' class='text-wrap'>{optD}</label><br/>\n")
                           f.write(f"                  <p id='result'></p>\n")
                           if previousslide:
                                f.write(f"                  <a class='btn btn-lg btn-primary' href='{previousslide}' role='button'>previous</a>\n")                                                                      
                           f.write(f"                  <button class='btn btn-primary btn-lg px-4 me-sm-3' id='submitButton' type='button' onclick='checkAnswer()'>Submit</button>\n")
                           f.write(f"                  <button class='btn btn-success rounded-pill px-3' id='nextButton' type='button' disabled onclick='goToNextQuestion()'>Next</button>\n")
                     #if its one word answer 
                     elif not optA and not optB and not optC and  not optD:
                           f.write(f"                  <input type='text' id='userAnswer' name = 'opt'  placeholder='Type your answer'/>\n")
                           f.write(f"                  <p id='result'></p>\n") 
                           if previousslide:
                                f.write(f"                  <a class='btn btn-lg btn-primary' href='{previousslide}' role='button'>previous</a>\n")                                           
                           f.write(f"                  <button class='btn btn-primary btn-lg px-4 me-sm-3' id='submitButton' type='button' onclick='checkAnswer()'>Submit</button>\n")                 
                           f.write(f"                  <button class='btn btn-success rounded-pill px-3' id='nextButton' type='button' disabled onclick='goToNextQuestion()'>Next</button>\n")                            
                     #if boolean
                     else:
                           f.write(f"                  <input type='radio' id='A' name = 'opt' placeholder = '{optA}' value = '{optA}'/>\n")
                           f.write(f"                  <label class='form-label' for='A' class='text-wrap'>{optA}</label><br/>\n")                           
                           f.write(f"                  <input type='radio' id='B' name = 'opt' placeholder = '{optB}'value = '{optB}' />\n")
                           f.write(f"                  <label class='form-label' for='option1' class='text-wrap'>{optB}</label><br/>\n")                           
                           f.write(f"                  <p id='result'></p>\n")
                           if previousslide:
                                f.write(f"                  <a class='btn btn-lg btn-primary' href='{previousslide}' role='button'>previous</a>\n")
                                             
                           f.write(f"                  <button  class='btn btn-primary btn-lg px-4 me-sm-3' id='submitButton' type='button' onclick='checkAnswer()'>Submit</button>\n")
                           f.write(f"                  <button class='btn btn-success rounded-pill px-3'  id='nextButton' type='button' disabled onclick='goToNextQuestion()'>Next</button>\n")
                     f.write(f"             </li>\n")
                     f.write(f"             </ol>\n")
                
                     f.write(f"</form>\n")
                     f.write(f"</div>\n")  
                f.write(f"\n")                    
                f.write(f" \n")
                f.write(f"   </main>\n")
                #answers verification logic JS
                if question :
                        if optA and optB : 
                                  f.write(f"         <script>\n")
                                  f.write("         function checkAnswer() {\n")
                                  f.write(f"         // Correct answer\n")
                                  f.write(f"         const correctAnswer = '{answer}';\n")
                                  f.write(f"                                           \n")
                                  f.write(f"         // Get all checkboxes and result elements\n")
                                  f.write(f'         const checkboxes = document.querySelectorAll(\'input[name="opt')
                                  f.write(f'"]\');\n')
                                  f.write(f"         const result = document.getElementById('result');\n")
                                  f.write(f"         const nextButton = document.getElementById('nextButton');\n")
                                  f.write(f"         const submitButton = document.getElementById('submitButton');\n")
                        
                                  f.write(f"         let selectedValue = null;\n")
                                  f.write(f"         let isCorrect = false;\n")
                                  f.write(f"         \n")
                                  f.write(f"         // Check which checkbox is selected\n")
                                  f.write("         checkboxes.forEach((checkbox) => {\n")
                                  f.write("         if (checkbox.checked) {\n")
                                  f.write(f"         selectedValue = checkbox.value;\n")
                                  f.write("         }\n")
                                  f.write(f"         // Reset the border style for all options\n")
                                  f.write(f"         checkbox.nextElementSibling.style.border = 'none';\n")
                                  f.write("         });\n")
                                  f.write(f"         \n")
                                  f.write(f"         // Validate the answer\n")
                                  f.write("         if (selectedValue === correctAnswer) {\n")
                                  f.write(f"         isCorrect = true;\n")
                                  f.write(f"         result.textContent = 'Correct!';\n")
                                  f.write(f"         result.style.color = 'green';\n")
                                  f.write(f"         \n")
                                  f.write(f"                 // Highlight the correct option\n")
                                  f.write('         document.querySelector(`input[value="${correctAnswer')
                                  f.write('}"]`).nextElementSibling.style.border =\n')
                                  f.write(f"         '2px solid green';\n")
                                  f.write(f"         \n")
                                  f.write(f'         nextButton.disabled = false; // Enable the "Next" button\n')
                                  f.write(f'         submitButton.disabled = true; // Disable the "Submit" button\n')
                                  f.write("         } else {\n")
                                  f.write(f"         result.textContent = 'Incorrect, please try again.';\n")
                                  f.write(f"         result.style.color = 'red';\n")
                                  f.write(f"         \n")
                                  f.write(f"         // Highlight the selected option with red if incorrect\n")
                                  f.write("         if (selectedValue) {\n")
                                  f.write('         document.querySelector(`input[value="${selectedValue')
                                  f.write('}"]`).nextElementSibling.style.border =\n')
                                  f.write(f"         '2px solid red';\n")
                                  f.write("         }\n")
                                  f.write(f"         \n")
                                  f.write(f'         nextButton.disabled = true; // Keep the "Next" button disabled\n')
                                  f.write("         }\n")
                                  f.write("         }\n")
                                  f.write(f"         \n")
                                  f.write("         function goToNextQuestion() {\n")
                                  f.write(f"         window.location.href = '{nextSlideName}';\n")
                                  f.write(f"         // Logic to navigate to the next question\n")
                                  f.write("         }\n")
                                  f.write(f"         </script>\n")
                                  f.write(f"                                         \n")
                        else:
                                  f.write(f"<script>\n")                            
                                  f.write('        function checkAnswer() {\n')
                                  f.write('            // Correct answer\n')
                                  f.write(f"            const correctAnswer = '{answer}'; \n")
                                  f.write('\n')
                                  f.write('            // Get user input and result elements\n')
                                  f.write('            const userInput = document.getElementById("userAnswer");\n')
                                  f.write('            const result = document.getElementById("result");\n')
                                  f.write('            const nextButton = document.getElementById("nextButton");\n')
                                  f.write('            const submitButton = document.getElementById("submitButton");\n')
                                  f.write('\n')
                                  f.write('            // Trim and normalize user input (case insensitive)\n')
                                  f.write('            const userAnswer = userInput.value.trim().toLowerCase();\n')
                                  f.write('            const expectedAnswer = correctAnswer.trim().toLowerCase();\n')
                                  f.write('\n')
                                  f.write('            // Validate the answer\n')
                                  f.write('            if (userAnswer === expectedAnswer) {\n')
                                  f.write('                result.textContent = "Correct!";\n')
                                  f.write('                result.style.color = "green";\n')
                                  f.write('                userInput.style.border = "2px solid green";\n')
                                  f.write('\n')
                                  f.write('                // Enable "Next" button and disable "Submit"\n')
                                  f.write('                nextButton.disabled = false;\n')
                                  f.write('                submitButton.disabled = true;\n')
                                  f.write('            } else {\n')
                                  f.write('                result.textContent = "Incorrect, please try again.";\n')
                                  f.write('                result.style.color = "red";\n')
                                  f.write('                userInput.style.border = "2px solid red";\n')
                                  f.write('\n')
                                  f.write('                // Keep "Next" button disabled\n')
                                  f.write('                nextButton.disabled = true;\n')
                                  f.write('            }\n')
                                  f.write('        }\n')
                                  f.write('\n')
                                  f.write('        function goToNextQuestion() {\n')
                                  f.write(f"            window.location.href = '{nextSlideName}'; \n")
                                  f.write('        }\n')
                                  f.write('</script>\n')


                #handler  database connection
                f.write("            <script>\n")
                f.write("                const continueButton = document.getElementById('continue-button');\n")
                f.write("                continueButton.addEventListener('click', () => {\n")
                f.write(f"                    const title = '{self.courseTitle}';\n")
                f.write(f"                    const moduleTitle = 'Module {moduleID} Slide {slideID} : {header}';\n")
                f.write(f"                    const slideName = '{slide_name}';\n")
                f.write("        \n")
                f.write("                    const data = {\n")
                f.write("                        title: title,\n")
                f.write("                        moduleTitle: moduleTitle,\n")
                f.write("                        slideName: slideName\n")
                f.write("                    };\n")
                f.write("        \n")
                f.write(f"                    fetch('../AUTH/handler.php',  \n")
                f.write("{                        method: 'POST',\n")
                f.write("                        headers: {\n")
                f.write("                            'Content-Type': 'application/json'\n")
                f.write("                        },\n")
                f.write("                        body: JSON.stringify(data)\n")
                f.write("                    })\n")
                f.write("                    .then(response => response.json())\n")
                f.write("                    .then(data => console.log(data))\n")
                f.write("                    .catch(error => console.error('Error:', error))\n")
                f.write("                    .finally(() => {\n")
                f.write(f"                        location.href = '{nextSlideName}';\n")
                f.write("                    });\n")
                f.write("                });\n")
                f.write("         </script>\n")   



                f.write(f"</body>\n")
                f.write(f"</html>\n")

    #The  connection  with database
    def handler(self,file_Directory):
        try:
              with open(file_Directory +'handler.js', 'x') as f:
                 print(file_Directory +'handler.js','created')
              with open(file_Directory +'handler.php', 'x') as f:
                 print(file_Directory +'handler.php','created')   

              with open(file_Directory +'config.php', 'x') as f:
                 print(file_Directory +'config.php','created')   

        except:
               print('file already exists')

        #config.php database connection        
        with open(file_Directory +'config.php', 'w') as f:
                   f.write("<?php\n")
                   f.write('header("Access-Control-Allow-Origin: *");\n')
                   f.write('header("Access-Control-Allow-Methods: GET, POST, OPTIONS");\n')
                   f.write('header("Access-Control-Allow-Headers: Content-Type, Authorization");\n')
                   f.write("\n")
                   f.write("$host = 'localhost'; \n")
                   f.write("$db = 'dabasename_here';\n")
                   f.write("$user = 'user_here'; \n")
                   f.write("$pass = 'password_here'; // your MySQL password\n")
                   f.write("\n")
                   f.write("try {\n")
                   f.write('    $pdo = new PDO("mysql:host=$host;dbname=$db", $user, $pass);\n')
                   f.write("    $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);\n")
                   f.write("} catch (PDOException $e) {\n")
                   f.write("    // Log the error message\n")
                   f.write("    file_put_contents('error_log.txt', $e->getMessage(), FILE_APPEND);\n")
                   f.write("    // Show a generic error message to the user\n")
                   f.write('    die("Connection failed. Please try again later.");\n')
                   f.write("}\n")
                   f.write("?>\n")
 
        #handler.php database connection        
        with open(file_Directory +'handler.php', 'w') as f:
                   f.write("\n")
                   f.write("<?php\n")
                   f.write("session_start();\n")
                   f.write("require 'config.php';  // Assuming this contains the database connection and other settings\n")
                   f.write("\n")
                   f.write("ini_set('display_errors', 1);\n")
                   f.write("ini_set('display_startup_errors', 1);\n")
                   f.write("error_reporting(E_ALL);\n")
                   f.write("\n")
                   f.write("if (!isset($_SESSION['user_id'])) {\n")
                   f.write('    header("Location: login.php");\n')
                   f.write("    exit();\n")
                   f.write("}\n")
                   f.write("\n")
                   f.write("$userId = $_SESSION['user_id'];  // User ID from the session\n")
                   f.write("\n")
                   f.write("// Function to fetch Course, Module, and Slide IDs from the database\n")
                   f.write("function getIds($title, $moduleTitle, $slideName) {\n")
                   f.write("    global $pdo;\n")
                   f.write("\n")
                   f.write('    $sql = "SELECT c.CourseID, m.ModuleID, s.SlideID \n')
                   f.write("            FROM Courses c \n")
                   f.write("            JOIN Modules m ON c.CourseID = m.CourseID \n")
                   f.write("            JOIN Slides s ON m.ModuleID = s.ModuleID \n")
                   f.write('            WHERE c.Title = ? AND m.ModuleTitle = ? AND s.SlideName = ?";\n')
                   f.write("    $stmt = $pdo->prepare($sql);\n")
                   f.write("    $stmt->execute([$title, $moduleTitle, $slideName]);\n")
                   f.write("\n")
                   f.write("    return $stmt->fetch(PDO::FETCH_ASSOC);\n")
                   f.write("}\n")
                   f.write("\n")
                   f.write("// Function to fetch current progress for a user in a course and module\n")
                   f.write("function fetchProgress($userID, $courseID, $moduleID) {\n")
                   f.write("    global $pdo;\n")
                   f.write("\n")
                   f.write('    $sql = "SELECT COUNT(*) as completed_slides \n')
                   f.write("            FROM UserSlideProgress \n")
                   f.write('            WHERE UserID = ? AND CourseID = ? AND ModuleID = ? AND Completed = 1";\n')
                   f.write("    $stmt = $pdo->prepare($sql);\n")
                   f.write("    $stmt->execute([$userID, $courseID, $moduleID]);\n")
                   f.write("    $completedSlides = $stmt->fetchColumn();\n")
                   f.write("\n")
                   f.write('    $sql = "SELECT COUNT(*) as total_slides \n')
                   f.write("            FROM Slides \n")
                   f.write('            WHERE ModuleID = ?";\n')
                   f.write("    $stmt = $pdo->prepare($sql);\n")
                   f.write("    $stmt->execute([$moduleID]);\n")
                   f.write("    $totalSlides = $stmt->fetchColumn();\n")
                   f.write("\n")
                   f.write("    if ($totalSlides > 0) {\n")
                   f.write("        $progressPercentage = ($completedSlides / $totalSlides) * 100;\n")
                   f.write("    } else {\n")
                   f.write("        $progressPercentage = 0;\n")
                   f.write("    }\n")
                   f.write("\n")
                   f.write("    return ['completed_slides' => $completedSlides, 'total_slides' => $totalSlides, 'progressPercentage' => $progressPercentage];\n")
                   f.write("}\n")
                   f.write("\n")
                   f.write("// Function to fetch current progress for a user in a course\n")
                   f.write("function fetchCourseProgress($userID, $courseID) {\n")
                   f.write("    global $pdo;\n")
                   f.write("\n")
                   f.write('    $sql = "SELECT COUNT(*) as total_slides \n')
                   f.write("            FROM Slides \n")
                   f.write("            JOIN Modules ON Slides.ModuleID = Modules.ModuleID \n")
                   f.write('            WHERE Modules.CourseID = ?";\n')
                   f.write("    $stmt = $pdo->prepare($sql);\n")
                   f.write("    $stmt->execute([$courseID]);\n")
                   f.write("    $totalSlides = $stmt->fetchColumn();\n")
                   f.write("\n")
                   f.write('    $sql = "SELECT COUNT(*) as completed_slides \n')
                   f.write("            FROM UserSlideProgress \n")
                   f.write("            JOIN Slides ON UserSlideProgress.SlideID = Slides.SlideID \n")
                   f.write("            JOIN Modules ON Slides.ModuleID = Modules.ModuleID \n")
                   f.write('            WHERE UserSlideProgress.UserID = ? AND Modules.CourseID = ? AND UserSlideProgress.Completed = 1";\n')
                   f.write("    $stmt = $pdo->prepare($sql);\n")
                   f.write("    $stmt->execute([$userID, $courseID]);\n")
                   f.write("    $completedSlides = $stmt->fetchColumn();\n")
                   f.write("\n")
                   f.write("    if ($totalSlides > 0) {\n")
                   f.write("        $progressPercentage = ($completedSlides / $totalSlides) * 100;\n")
                   f.write("    } else {\n")
                   f.write("        $progressPercentage = 0;\n")
                   f.write("    }\n")
                   f.write("\n")
                   f.write("    return ['completed_slides' => $completedSlides, 'total_slides' => $totalSlides, 'progressPercentage' => $progressPercentage];\n")
                   f.write("}\n")
                   f.write("\n")
                   f.write("// Function to update the user's progress\n")
                   f.write("function updateProgress($userID, $courseID, $moduleID, $slideID) {\n")
                   f.write("    global $pdo;\n")
                   f.write("\n")
                   f.write("    // Check if the user has already completed the slide\n")
                   f.write('    $sql = "SELECT * \n')
                   f.write("            FROM UserSlideProgress \n")
                   f.write('            WHERE UserID = ? AND CourseID = ? AND ModuleID = ? AND SlideID = ?";\n')
                   f.write("    $stmt = $pdo->prepare($sql);\n")
                   f.write("    $stmt->execute([$userID, $courseID, $moduleID, $slideID]);\n")
                   f.write("\n")
                   f.write("    if ($stmt->fetch()) {\n")
                   f.write("        // If the user has already completed the slide, do nothing\n")
                   f.write("    } else {\n")
                   f.write("        // If the user has not completed the slide, insert a new record\n")
                   f.write('        $sql = "INSERT INTO UserSlideProgress (UserID, CourseID, ModuleID, SlideID, Completed) \n')
                   f.write('                VALUES (?, ?, ?, ?, 1)";\n')
                   f.write("        $stmt = $pdo->prepare($sql);\n")
                   f.write("        $stmt->execute([$userID, $courseID, $moduleID, $slideID]);\n")
                   f.write("    }\n")
                   f.write("}\n")
                   f.write("\n")
                   f.write("// Function to get the total number of slides for a module\n")
                   f.write("function getModuleSlideCount($moduleID) {\n")
                   f.write("    global $pdo;\n")
                   f.write("\n")
                   f.write('    $stmt = $pdo->prepare("SELECT COUNT(*) FROM Slides WHERE ModuleID = ?");\n')
                   f.write("    $stmt->execute([$moduleID]);\n")
                   f.write("    return $stmt->fetchColumn();\n")
                   f.write("}\n")
                   f.write("\n")
                   f.write("// Function to get the slide index from the Slides table\n")
                   f.write("function getSlideIndex($moduleID, $slideID) {\n")
                   f.write("    global $pdo;\n")
                   f.write("\n")
                   f.write('    $stmt = $pdo->prepare("SELECT SlideIndex FROM Slides WHERE ModuleID = ? AND SlideID = ?");\n')
                   f.write("    $stmt->execute([$moduleID, $slideID]);\n")
                   f.write("    $row = $stmt->fetch(PDO::FETCH_ASSOC);\n")
                   f.write("\n")
                   f.write("    return $row ? $row['SlideIndex'] : 0;\n")
                   f.write("}\n")
                   f.write("\n")
                   f.write("// Function to calculate overall course progress\n")
                   f.write("function getCourseProgress($userID, $courseID) {\n")
                   f.write("    global $pdo;\n")
                   f.write("\n")
                   f.write('    $sql = "SELECT ModuleID FROM Modules WHERE CourseID = ?";\n')
                   f.write("    $stmt = $pdo->prepare($sql);\n")
                   f.write("    $stmt->execute([$courseID]);\n")
                   f.write("    $modules = $stmt->fetchAll(PDO::FETCH_ASSOC);\n")
                   f.write("\n")
                   f.write("    $totalSlides = 0;\n")
                   f.write("    $totalCompletedSlides = 0;\n")
                   f.write("\n")
                   f.write("    foreach ($modules as $module) {\n")
                   f.write("        $moduleID = $module['ModuleID'];\n")
                   f.write("        $progressData = fetchProgress($userID, $courseID, $moduleID);\n")
                   f.write("\n")
                   f.write("        $totalSlides += $progressData['total_slides'];\n")
                   f.write("        $totalCompletedSlides += $progressData['completed_slides'];\n")
                   f.write("    }\n")
                   f.write("\n")
                   f.write("    if ($totalSlides > 0) {\n")
                   f.write("        $courseProgress = ($totalCompletedSlides / $totalSlides) * 100;\n")
                   f.write("    } else {\n")
                   f.write("        $courseProgress = 0;\n")
                   f.write("    }\n")
                   f.write("\n")
                   f.write("    return round($courseProgress, 2);\n")
                   f.write("}\n")
                   f.write("\n")
                   f.write("// Function to update the user's progress in the UserProgress table\n")
                   f.write("function updateUserProgress($userID, $courseID) {\n")
                   f.write("    global $pdo;\n")
                   f.write("\n")
                   f.write("    // Calculate the progress percentage\n")
                   f.write("    $progressData = fetchCourseProgress($userID, $courseID);\n")
                   f.write("    $progressPercentage = $progressData['progressPercentage'];\n")
                   f.write("\n")
                   f.write("    // Check if the user has an existing record in the UserProgress table\n")
                   f.write('    $sql = "SELECT * \n')
                   f.write("            FROM UserProgress \n")
                   f.write('            WHERE UserID = ? AND CourseID = ?";\n')
                   f.write("    $stmt = $pdo->prepare($sql);\n")
                   f.write("    $stmt->execute([$userID, $courseID]);\n")
                   f.write("    $userProgress = $stmt->fetch(PDO::FETCH_ASSOC);\n")
                   f.write("\n")
                   f.write("    if ($userProgress) {\n")
                   f.write("        // If the user has an existing record, update it\n")
                   f.write('        $sql = "UPDATE UserProgress \n')
                   f.write("                SET ProgressPercentage = ?\n")
                   f.write('                WHERE UserID = ? AND CourseID = ?";\n')
                   f.write("        $stmt = $pdo->prepare($sql);\n")
                   f.write("        $stmt->execute([$progressPercentage, $userID, $courseID]);\n")
                   f.write("    } else {\n")
                   f.write("        // If the user does not have an existing record, insert a new one\n")
                   f.write('        $sql = "INSERT INTO UserProgress (UserID, CourseID, ProgressPercentage) \n')
                   f.write('                VALUES (?, ?, ?)";\n')
                   f.write("        $stmt = $pdo->prepare($sql);\n")
                   f.write("        $stmt->execute([$userID, $courseID, $progressPercentage]);\n")
                   f.write("    }\n")
                   f.write("}\n")
                   f.write("\n")
                   f.write("// Handle POST request to update progress\n")
                   f.write("if ($_SERVER['REQUEST_METHOD'] === 'POST') {\n")
                   f.write("    try {\n")
                   f.write("        $data = json_decode(file_get_contents('php://input'), true);\n")
                   f.write("\n")
                   f.write("        if (isset($data['title'], $data['moduleTitle'], $data['slideName'])) {\n")
                   f.write("            $title = $data['title'];\n")
                   f.write("            $moduleTitle = $data['moduleTitle'];\n")
                   f.write("            $slideName = $data['slideName'];\n")
                   f.write("\n")
                   f.write("            $ids = getIds($title, $moduleTitle, $slideName);\n")
                   f.write("\n")
                   f.write("            if ($ids) {\n")
                   f.write("                $courseID = $ids['CourseID'];\n")
                   f.write("                $moduleID = $ids['ModuleID'];\n")
                   f.write("                $slideID = $ids['SlideID'];\n")
                   f.write("\n")
                   f.write("                // Update the user's progress\n")
                   f.write("                updateProgress($userId, $courseID, $moduleID, $slideID);\n")
                   f.write("\n")
                   f.write("                // Update the user's progress in the UserProgress table\n")
                   f.write("                updateUserProgress($userId, $courseID);\n")
                   f.write("\n")
                   f.write("                // Return updated progress as a JSON response\n")
                   f.write("                $progressData = fetchCourseProgress($userId, $courseID);\n")
                   f.write("                echo json_encode(['progress' => $progressData['progressPercentage']]);\n")
                   f.write("            } else {\n")
                   f.write("                echo json_encode(['error' => 'Invalid course, module, or slide']);\n")
                   f.write("            }\n")
                   f.write("        } else {\n")
                   f.write("            echo json_encode(['error' => 'Missing required data']);\n")
                   f.write("        }\n")
                   f.write("    } catch (PDOException $e) {\n")
                   f.write("        echo json_encode(['error' => 'Database error: ' . $e->getMessage()]);\n")
                   f.write("    } catch (Exception $e) {\n")
                   f.write("        echo json_encode(['error' => 'Error: ' . $e->getMessage()]);\n")
                   f.write("    }\n")
                   f.write("}\n")
                   f.write("\n")
                   f.write("// Handle GET request to get overall course progress\n")
                   f.write("if ($_SERVER['REQUEST_METHOD'] === 'GET' && isset($_GET['courseTitle'])) {\n")
                   f.write("    try {\n")
                   f.write("        $courseTitle = $_GET['courseTitle'];\n")
                   f.write("\n")
                   f.write('        $sql = "SELECT CourseID FROM Courses WHERE Title = ?";\n')
                   f.write("        $stmt = $pdo->prepare($sql);\n")
                   f.write("        $stmt->execute([$courseTitle]);\n")
                   f.write("        $course = $stmt->fetch(PDO::FETCH_ASSOC);\n")
                   f.write("\n")
                   f.write("        if ($course) {\n")
                   f.write("            $courseID = $course['CourseID'];\n")
                   f.write("            $courseProgress = getCourseProgress($userId, $courseID);\n")
                   f.write("\n")
                   f.write("            echo json_encode(['progress' => $courseProgress]);\n")
                   f.write("        } else {\n")
                   f.write("            echo json_encode(['error' => 'Course not found']);\n")
                   f.write("        }\n")
                   f.write("    } catch (PDOException $e) {\n")
                   f.write("        echo json_encode(['error' => 'Database error: ' . $e->getMessage()]);\n")
                   f.write("    } catch (Exception $e) {\n")
                   f.write("        echo json_encode(['error' => 'Error: ' . $e->getMessage()]);\n")
                   f.write("    }\n")
                   f.write("    exit();\n")
                   f.write("    }\n")
                   f.write("    ?>\n")



        #handler.js connection  receiver
        with open(file_Directory +'handler.js', 'w') as f:
                   f.write("// handler.js\n")
                   f.write("\n")
                   f.write("// Fetch userID from the server\n")
                   f.write("let userID = null;\n")
                   f.write("\n")
                   f.write("fetch('handler.php')\n")
                   f.write("    .then(response => {\n")
                   f.write("        if (!response.ok) {\n")
                   f.write("            throw new Error('Failed to fetch userID');\n")
                   f.write("        }\n")
                   f.write("        return response.json();\n")
                   f.write("    })\n")
                   f.write("    .then(data => {\n")
                   f.write("        userID = data.userID; // Store the userID globally\n")
                   f.write("        console.log('UserID fetched:', userID); // Optional: Log to confirm it worked\n")
                   f.write("    })\n")
                   f.write("    .catch(error => {\n")
                   f.write("        console.error('Error fetching userID:', error);\n")
                   f.write("        // Optional: Redirect to login if userID cannot be fetched\n")
                   f.write("        //window.location.href = 'https://elitelearnersacademy.com/LEARNING/login.php';\n")
                   f.write("    });\n")
                   f.write("\n")
                   f.write("// Function to send progress data to the server\n")
                   f.write("async function sendProgress(userID, courseID, moduleID, slideID, progressPercentage) {\n")
                   f.write("    try {\n")
                   f.write("        const response = await fetch('handler.php', {\n")
                   f.write("            method: 'POST',\n")
                   f.write("            headers: {\n")
                   f.write("                'Content-Type': 'application/json',\n")
                   f.write("            },\n")
                   f.write("            body: JSON.stringify({\n")
                   f.write("                action: 'sendProgress',\n")
                   f.write("                userID,\n")
                   f.write("                courseID,\n")
                   f.write("                moduleID,\n")
                   f.write("                slideID,\n")
                   f.write("                progressPercentage,\n")
                   f.write("            }),\n")
                   f.write("        });\n")
                   f.write("        const result = await response.json();\n")
                   f.write("        if (result.success) {\n")
                   f.write("            console.log('Progress sent successfully:', result);\n")
                   f.write("        } else {\n")
                   f.write("            console.error('Failed to send progress:', result.message);\n")
                   f.write("        }\n")
                   f.write("    } catch (error) {\n")
                   f.write("        console.error('Error sending progress:', error);\n")
                   f.write("    }\n")
                   f.write("}\n")
                   f.write("\n")
                   f.write("// Function to fetch updated progress and user information\n")
                   f.write("async function fetchProgress(userID, courseID) {\n")
                   f.write("    try {\n")
                   f.write("        const response = await fetch('handler.php', {\n")
                   f.write("            method: 'POST',\n")
                   f.write("            headers: {\n")
                   f.write("                'Content-Type': 'application/json',\n")
                   f.write("            },\n")
                   f.write("            body: JSON.stringify({\n")
                   f.write("                action: 'fetchProgress',\n")
                   f.write("                userID,\n")
                   f.write("                courseID,\n")
                   f.write("            }),\n")
                   f.write("        });\n")
                   f.write("        const result = await response.json();\n")
                   f.write("        if (result.success) {\n")
                   f.write("            console.log('Fetched progress successfully:', result);\n")
                   f.write("            updateUI(result.data);\n")
                   f.write("        } else {\n")
                   f.write("            console.error('Failed to fetch progress:', result.message);\n")
                   f.write("        }\n")
                   f.write("    } catch (error) {\n")
                   f.write("        console.error('Error fetching progress:', error);\n")
                   f.write("    }\n")
                   f.write("}\n")
                   f.write("\n")
                   f.write("// Function to update the HTML UI with fetched data\n")
                   f.write("function updateUI(data) {\n")
                   f.write("    const progressElement = document.getElementById('progressPercentage');\n")
                   f.write("    const usernameElement = document.getElementById('username');\n")
                   f.write("    const profilePictureElement = document.getElementById('profilePicture');\n")
                   f.write("    const certificateLinkElement = document.getElementById('certificateLink');\n")
                   f.write("\n")
                   f.write("    progressElement.textContent = `${data.progressPercentage}%`;\n")
                   f.write("    usernameElement.textContent = `${data.firstName} ${data.lastName}`;\n")
                   f.write("    profilePictureElement.src = data.profilePictureURL;\n")
                   f.write("\n")
                   f.write("    if (data.certificateURL) {\n")
                   f.write("        certificateLinkElement.href = data.certificateURL;\n")
                   f.write("        certificateLinkElement.style.display = 'block';\n")
                   f.write("    } else {\n")
                   f.write("        certificateLinkElement.style.display = 'none';\n")
                   f.write("    }\n")
                   f.write("}\n")




        #celebration 
    def celebration(self,file_Directory):
              with open(file_Directory +'celebration.html', 'w') as f:
                      f.write(f"<!Doctype html>\n")
                      f.write(f'<html  lang="en" data-bs-theme="light">\n')
                      f.write(f'<head> <script src="https://elitelearnersacademy.com/JS/color-modes.js"></script>\n')
                      f.write(f"\n")
                      f.write(f'  <meta charset="utf-8">\n')
                      f.write(f'  <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">\n')
                      f.write(f'  <meta name="viewport" content="width=device-width, initial-scale=1">\n')
                      f.write(f'  <meta name="description" content="online courses,elearning platform ,Quizs"/>\n')
                      f.write(f'  <meta name="author" content="elitelearnersacademy" />\n')
                      f.write(f'  <meta name="generator" content="Hugo 0.122.0">\n')
                      f.write(f'       <title>Congratulations</title>\n')
                      f.write(f'       <link rel="stylesheet" href="https://elitelearnersacademy.com/CSS/celebration.css" type="text/CSS">\n')
                      f.write(f'       <script src="https://elitelearnersacademy.com/JS/celebration.js"></script>\n')
                      f.write(f"       <style>\n")
                      f.write(f"\n")
                      f.write(f"       </style>\n")
                      f.write(f"                 \n")
                      f.write(f"</head>\n")
                      f.write(f"\n")
                      f.write(f"<body>\n")
                      f.write(f"      <header>\n") 
                      f.write(f"\n")
                      f.write(f"      </header>\n")
                      f.write(f"      <main>\n")
                      f.write(f'         <p>Congrats<br><div style="font-size: 24px; text-align: center;"> Brilliant work , hope to see you continue</div> </p>\n')
                      f.write(f"\n")
                      f.write(f'         <button id="button" type="button">\n')
                      f.write(f'          <span id="timer">15</span> \n')
                      f.write(f'          <div class="container">\n')
                      f.write(f'            <div class="loadingspinner">\n')
                      f.write(f'              <div id="square1"></div>\n')
                      f.write(f'              <div id="square2"></div>\n')
                      f.write(f'              <div id="square3"></div>\n')
                      f.write(f'              <div id="square4"></div>\n')
                      f.write(f'              <div id="square5"></div>\n')
                      f.write(f"            </div>\n")
                      f.write(f"          </div>\n")
                      f.write(f"         </button>\n")
                      f.write(f'        <canvas id="confetti"></canvas>\n')
                      f.write(f"\n")
                      f.write(f"<script>\n")
                      f.write("                     window.onload = function () {\n")
                      f.write(f"                    let countdown = 15; // 15 seconds\n")
                      f.write(f"                    const timerElement = document.getElementById('timer');\n")
                      f.write(f"              \n")
                      f.write(f"                    // Update the timer every second\n")
                      f.write("                     const interval = setInterval(() => {\n")
                      f.write(f"                      countdown--;\n")
                      f.write(f"                      timerElement.textContent = countdown;\n")
                      f.write(f"              \n")
                      f.write(f"                      // When countdown reaches 0, redirect to the new page\n")
                      f.write("                      if (countdown === 0) {\n")
                      f.write(f"                        clearInterval(interval); // Stop the timer\n")
                      f.write(f"                        window.location.href = '{self.file_dir}/index.html'; // Replace with your target URL\n")
                      f.write("                      }\n")
                      f.write("                    }, 1000);\n")
                      f.write("                  };\n")
                      f.write(f"              \n")
                      f.write(f"              \n")                      
                      f.write(f"</script>\n")
                      f.write(f"      </main>\n")
                      f.write(f"\n")
                      f.write(f"      <footer></footer>\n")
                      f.write(f"</body>\n")
                      f.write(f"</html>\n")
                
