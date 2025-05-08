import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import re
import time
import gettext
import os

# Initialize gettext for internationalization
gettext.bindtextdomain('course_description', './locales')
gettext.textdomain('course_description')
_ = gettext.gettext

class CourseDescriptionCreator:
    def __init__(self, root):
        self.root = root
        self.root.title(_("Course Description"))
        self.create_widgets()
        
        # Auto-save feature
        self.auto_save_interval = 60  # Auto-save interval in seconds
        self.auto_save_thread = threading.Thread(target=self.auto_save_draft, daemon=True)
        self.auto_save_thread.start()

    def create_widgets(self):
        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(True, True)

        # Labels and input fields
        tk.Label(self.root, text=_("Course Title:"), font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.title_entry = tk.Entry(self.root, font=("Arial", 14), width=50)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text=_("Image URL (optional):"), font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.img_url_entry = tk.Entry(self.root, font=("Arial", 14), width=50)
        self.img_url_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.root, text=_("Description:"), font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.description_text = tk.Text(self.root, font=("Arial", 14), width=50, height=5)
        self.description_text.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.root, text=_("Course Objectives:"), font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.objectives_entry = tk.Entry(self.root, font=("Arial", 14), width=50)
        self.objectives_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.root, text=_("Number of Chapters:"), font=("Arial", 14)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.num_chapters_entry = tk.Entry(self.root, font=("Arial", 14), width=50)
        self.num_chapters_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.root, text=_("Estimated Duration:"), font=("Arial", 14)).grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.duration_entry = tk.Entry(self.root, font=("Arial", 14), width=50)
        self.duration_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(self.root, text=_("Assessment Methods:"), font=("Arial", 14)).grid(row=6, column=0, padx=10, pady=5, sticky="w")
        self.assessment_entry = tk.Entry(self.root, font=("Arial", 14), width=50)
        self.assessment_entry.grid(row=6, column=1, padx=10, pady=5)

        # Live preview section
        tk.Label(self.root, text=_("Live Preview:"), font=("Arial", 14)).grid(row=7, column=0, padx=10, pady=5, sticky="w")
        self.preview_text = tk.Text(self.root, font=("Arial", 14), width=50, height=10)
        self.preview_text.grid(row=7, column=1, padx=10, pady=5)

        # Buttons
        tk.Button(self.root, text=_("Generate Course Description"), command=self.generate_course_description, font=("Arial", 14)).grid(row=8, column=0, columnspan=2, pady=10)

        tk.Label(self.root, text=_("Save Location:"), font=("Arial", 14)).grid(row=9, column=0, padx=10, pady=5, sticky="w")
        self.save_location_entry = tk.Entry(self.root, font=("Arial", 14), width=50)
        self.save_location_entry.grid(row=9, column=1, padx=10, pady=5)
        tk.Button(self.root, text=_("Browse"), command=self.browse_save_location, font=("Arial", 14)).grid(row=9, column=2, padx=10, pady=5)
        
        # Update live preview regularly
        self.update_live_preview()

    def browse_save_location(self):
        title = self.title_entry.get()
        home_directory = os.path.expanduser("~")
        os.makedirs(os.path.join(home_directory,f"{title.upper()}"),exist_ok = True)

        folder_path = filedialog.askdirectory(title=_("Select Save Location"))
        if folder_path:
            self.save_location_entry.delete(0, tk.END)
            self.save_location_entry.insert(0, folder_path)

    def update_live_preview(self):
        title = self.title_entry.get()
        description = self.description_text.get("1.0", "end").strip()
        objectives = self.objectives_entry.get()
        num_chapters = self.num_chapters_entry.get()
        duration = self.duration_entry.get()
        assessment = self.assessment_entry.get()
        preview_content = f"""
        Course Title: {title}
        Description: {description}
        Objectives: {objectives}
        Number of Chapters: {num_chapters}
        Estimated Duration: {duration}
        Assessment Methods: {assessment}
        """

        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert("1.0", preview_content)

        # Update live preview every second
        self.root.after(1000, self.update_live_preview)




    def generate_course_description(self):
        title = self.title_entry.get()
        img_url = self.img_url_entry.get()
        description = self.description_text.get("1.0", "end").strip()
        objectives = self.objectives_entry.get()
        num_chapters = self.num_chapters_entry.get()
        duration = self.duration_entry.get()
        assessment = self.assessment_entry.get()
        save_location = self.save_location_entry.get()
        
        if not title or not description:
            messagebox.showwarning(_("Input Error"), _("Title and Description are required fields."))
            return

        if not save_location:
            messagebox.showwarning(_("Input Error"), _("Please select a save location."))
            return

        if not re.match("^[a-zA-Z0-9_ ]*$", title):
            messagebox.showwarning(_("Input Error"), _("File name should not contain special characters."))
            return

        file_path = f"{save_location}/README.md"
        with open(file_path, "a") as file:
            file.write('\n')
            file.write(f'    Title: {title}\n')
            file.write(f'    Image {img_url if img_url else 'default.jpg'} \n')
            file.write(f'    Description: {description}\n')
            file.write(f'+++++++++++++++++++++++++++++++++++++++++++    Course Overview     ++++++++++++++++++++++++++++++++++++++++++++++++++\n')
            file.write(f'    Objective : {objectives}\n')
            file.write(f'    Number Of Chapters: {num_chapters}\n')
            file.write(f'Duration : {duration} \n')
            file.write(f'Assement Type :{assessment}\n')

        file_path = f"{save_location}/{title}.html"            
        with open(file_path, "w", encoding="utf-8") as file:
            file.write('       <!DOCTYPE html>\n')
            file.write('        <html lang="en">\n')
            file.write('        <head>\n')
            file.write('            <meta charset="UTF-8">\n')
            file.write('            <meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
            file.write(f'            <title>{title} - Course Details</title>\n')
            file.write('            <link rel="stylesheet" href="https://elitelearnersacademy.com/CSS/bootstrap.min.css"> \n')            
            file.write('            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"> \n')
            file.write('            <link rel="stylesheet" href="https://elitelearnersacademy.com/LEARNING/styl.css">  \n')
            file.write('            <style>\n')
            file.write('                /* General styles */\n')
            file.write('                .page-container {\n')
            file.write('                    padding: 20px;\n')
            file.write('                }\n')
            file.write('                .course-detail {\n')
            file.write('                    background: white;\n')
            file.write('                    padding: 20px;\n')
            file.write('                    border-radius: 8px;\n')
            file.write('                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);\n')
            file.write('                }\n')
            file.write('                .course-detail h2 {\n')
            file.write('                    margin-top: 0;\n')
            file.write('                }\n')
            file.write('                .course-detail img {\n')
            file.write('                    max-width: 100%;\n')
            file.write('                    height: auto;\n')
            file.write('                    border-radius: 8px;\n')
            file.write('                }\n')
            file.write('                .form-group {\n')
            file.write('                    margin-bottom: 15px;\n')
            file.write('                }\n')
            file.write('                .form-group label {\n')
            file.write('                    display: block;\n')
            file.write('                    margin-bottom: 5px;\n')
            file.write('                }\n')
            file.write('                .form-group select, .form-group input[type="checkbox"] {\n')
            file.write('                    width: 100%;\n')
            file.write('                    padding: 10px;\n')
            file.write('                    border: 1px solid #ccc;\n')
            file.write('                    border-radius: 4px;\n')
            file.write('                }\n')
            file.write('                button {\n')
            file.write('                    padding: 10px 15px;\n')
            file.write('                    background-color: #5cb85c;\n')
            file.write('                    color: white;\n')
            file.write('                    border: none;\n')
            file.write('                    border-radius: 4px;\n')
            file.write('                    cursor: pointer;\n')
            file.write('                }\n')
            file.write('                button:hover {\n')
            file.write('                    background-color: #4cae4c;\n')
            file.write('                }\n')
            file.write('                /* Responsive styles */\n')
            file.write('                @media (max-width: 768px) {\n')
            file.write('                    .header nav ul {\n')
            file.write('                        display: flex;\n')
            file.write('                        flex-direction: column;\n')
            file.write('                        align-items: flex-start;\n')
            file.write('                    }\n')
            file.write('                    .header nav ul li {\n')
            file.write('                        margin: 5px 0;\n')
            file.write('                    }\n')
            file.write('                    .course-detail {\n')
            file.write('                        padding: 15px;\n')
            file.write('                    }\n')
            file.write('                }\n')
            file.write('            </style>\n')
            file.write('        </head>\n')
            file.write('        <body> \n')
            file.write('\n')
            file.write('<header class="header">\n')
            file.write('    <div class="logo-and-title">\n')
            file.write('       <a href="https://elitelearnersacademy.com/" class="navbar-brand d-flex align-items-center">\n')
            file.write('         <img src="https://elitelearnersacademy.com/ASSETS/logo.jpg" width="20" height="20" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" aria-hidden="true" class="me-2" viewBox="0 0 24 24"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/>ELA\n')
            file.write('      </a>\n')
            file.write('    </div>\n')
            file.write('    <nav class="nav">\n')
            file.write('        <ul>\n')
            file.write('            <li><a href="https://elitelearnersacademy.com/">Home</a></li>\n')
            file.write('            <li><a href="cors.php">Main</a></li>\n')
            file.write('        </ul>\n')
            file.write('    </nav>\n')
            file.write('</header>\n')
            file.write('<main class="container">\n')
            file.write(' <div class="page-container">\n')
            file.write('    <div class="course-detail">\n')
            file.write(f"        <h2><?php echo htmlspecialchars($course'Title']); ?></h2>\n")
            file.write(f"        <img src='<?php echo htmlspecialchars($course['ImgURL'] ?: 'default.jpg'); ?>' alt='<?php echo htmlspecialchars($course['Title']); ?>'>\n")
            file.write("        <!-- <p><strong>Instructor:</strong> <?php echo htmlspecialchars($instructor['Name']); ?></p> -->\n")
            file.write("       <!-- <p><strong>Instructor Bio:</strong> <?php echo htmlspecialchars($instructor['Bio']); ?></p> -->\n")
            file.write(f"        <p><?php echo htmlspecialchars($course['Description']); ?></p>\n")
            file.write('\n')
            file.write('        <h3>Course Overview</h3>\n')
            file.write("        <p class='card' style='padding:2rem;'><strong>Course Objectives:</strong> <?php echo htmlspecialchars($courseDetails['Objectives']); ?></p>\n")
            file.write(f"        <p><strong>Number of Chapters:</strong> <?php echo htmlspecialchars($courseDetails['NumChapters']); ?></p>\n")
            file.write(f"        <p><strong>Estimated Duration:</strong> <?php echo htmlspecialchars($courseDetails[''Duration']); ?></p>\n")
            file.write("        <p><strong>Prerequisites:</strong> <?php echo htmlspecialchars($courseDetails['Prerequisites']); ?></p>\n")
            file.write("        <p><strong>Learning Format:</strong> <?php echo htmlspecialchars($courseDetails['Format']); ?></p>\n")
            file.write(f"        <p><strong>Assessment Methods:</strong> <?php echo htmlspecialchars($courseDetails['Assessment']); ?></p>\n")
            file.write("        <p><strong>Community Support:</strong> <?php echo htmlspecialchars($courseDetails['Community']); ?></p>\n")
            file.write('\n')
            file.write('        <h3>Enroll in this Course</h3>\n')
            file.write('        <form id="enrollmentForm" action="javascript:void(0);">\n')
            file.write('            <input type="hidden" name="courseId" value="<?php echo $courseId; ?>">\n')
            file.write('            <input type="hidden" name="userId" value="<?php echo $userId; ?>">\n')
            file.write('\n')
            file.write('            <div class="form-group">\n')
            file.write('                <input type="checkbox" name="terms" id="terms" required>\n')
            file.write('                <label for="terms">I agree to the <a href="/terms" target="_blank">terms and conditions</a>.</label>\n')
            file.write('                <span id="termsFeedback" class="error-message"></span>\n')
            file.write('            </div>\n')
            file.write('\n')
            file.write('            <button type="submit">Enroll Now</button>\n')
            file.write('            <div id="confirmation" class="hidden"></div>\n')
            file.write('        </form>\n')
            file.write('    </div>\n')
            file.write('</div>\n')
            file.write('</main>\n')
            file.write('<footer class="py-5" style="padding:2rem">\n')
            file.write('    <div class="row">\n')
            file.write('      <div class="col-6 col-md-2 mb-3">\n')
            file.write('        <h5>Services</h5>\n')
            file.write('        <ul class="nav flex-column">\n')
            file.write('          <li class="nav-item mb-2"><a href="#" class="nav-link p-0 text-body-secondary">Courses</a></li>\n')
            file.write('          <li class="nav-item mb-2"><a href="https://elitelearnersacademy.com/HTML/F-EDU.html" class="nav-link p-0 text-body-secondary">Students Abroad</a></li>\n')
            file.write('          <li class="nav-item mb-2"><a href="https://elitelearnersacademy.com/HTML/F-EDU.html" class="nav-link p-0 text-body-secondary">Local students</a></li>\n')
            file.write('          <li class="nav-item mb-2"><a href="https://elitelearnersacademy.com/HTML/Orientation.html" class="nav-link p-0 text-body-secondary">Orientaion</a></li>\n')
            file.write('          <li class="nav-item mb-2"><a href="https://elitelearnersacademy.com/HTML/Blogs.html" class="nav-link p-0 text-body-secondary">Blogs</a></li>\n')
            file.write('        </ul>\n')
            file.write('      </div>\n')
            file.write('\n')
            file.write('      <div class="col-6 col-md-2 mb-3">\n')
            file.write('        <h5>Operation</h5>\n')
            file.write('        <ul class="nav flex-column">\n')
            file.write('          <li class="nav-item mb-2"><a href="#Pricing-container" class="nav-link p-0 text-body-secondary">Pricing</a></li>\n')
            file.write('          <li class="nav-item mb-2"><a href="https://elitelearnersacademy.com/HTML/customer_service_center/index_Terms&Conditions.html" class="nav-link p-0 text-body-secondary">Terms&Conditions</a></li>\n')
            file.write('          <li class="nav-item mb-2"><a href="#faq" class="nav-link p-0 text-body-secondary">FAQs</a></li>\n')
            file.write('          <li class="nav-item mb-2"><a href="#" class="nav-link p-0 text-body-secondary"></a></li>\n')
            file.write('          <li class="nav-item mb-2"><a href="https://elitelearnersacademy.com/HTML/customer_service_center/index.html" class="nav-link p-0 text-body-secondary">Support</a></li>\n')
            file.write('        </ul>\n')
            file.write('      </div>\n')
            file.write('\n')
            file.write('      <div class="col-6 col-md-2 mb-3">\n')
            file.write('        <h5>Contacts</h5>\n')
            file.write('        <ul class="nav flex-column">\n')
            file.write('          <li class="nav-item mb-2"><a href="" class="nav-link p-0 text-body-secondary">ELA ,bavard hassan 2,mohammedia</a></li>\n')
            file.write('          <li class="nav-item mb-2"><a href="mailto:elitelearnersacademy2024@gmail.com" class="nav-link p-0 text-body-secondary">elitelearnersacademy2024@gmail.com</a></li>\n')
            file.write('          <li class="nav-item mb-2"><a href="phone:+2127123456789" class="nav-link p-0 text-body-secondary">+2127123456789</a></li>\n')
            file.write('          <li class="nav-item mb-2"><a href="#" class="nav-link p-0 text-body-secondary">About</a></li>\n')
            file.write('        </ul>\n')
            file.write('      </div>\n')
            file.write('                 <div class="col-md-5 offset-md-1 mb-3">\n')
            file.write('                   <form id="subscriptionForm">\n')
            file.write('                   <h5>Subscribe to our newsletter</h5>\n')
            file.write("                     <p>Monthly digest of what's new and exciting from us.</p>\n")
            file.write('                     <div class="d-flex flex-column flex-sm-row w-100 gap-2">\n')
            file.write('                     <label for="email" class="visually-hidden">Email address</label>\n')
            file.write('                     <input type="email" class="form-control" id="email" name="email" required>\n')
            file.write('                     <button class="btn btn-primary" type="submit">Subscribe</button>\n')
            file.write('                      </div>\n')
            file.write('                     </form>\n')
            file.write('                     <p id="message" class="text-center mt-3"></p>\n')
            file.write('                   </div>\n')
            file.write('    </div>\n')
            file.write('\n')
            file.write('    <div class="d-flex flex-column flex-sm-row justify-content-between py-4 my-4 border-top">\n')
            file.write('      <p>© 2025 Elite Learners Academy, Inc. All rights reserved.</p>\n')
            file.write('      <ul class="list-unstyled d-flex">\n')
            file.write('        <li class="ms-3"><a class="link-body-emphasis" href="#"><svg class="bi" width="24" height="24"><use xlink:href="#twitter"></use></svg></a></li>\n')
            file.write('        <li class="ms-3"><a class="link-body-emphasis" href="#"><svg class="bi" width="24" height="24"><use xlink:href="#instagram"></use></svg></a></li>\n')
            file.write('        <li class="ms-3"><a class="link-body-emphasis" href="#"><svg class="bi" width="24" height="24"><use xlink:href="#facebook"></use></svg></a></li>\n')
            file.write('      </ul>\n')
            file.write('    </div>\n')
            file.write('</footer>\n')
            file.write('<script>\n')
            file.write("document.getElementById('enrollmentForm').addEventListener('submit', function(event) {\n")
            file.write('    event.preventDefault(); // Prevent default form submission\n')
            file.write('\n')
            file.write('    const formData = new FormData(this);\n')
            file.write('    const jsonPayload = {\n')
            file.write("        courseId: formData.get('courseId'),\n")
            file.write("        userId: formData.get('userId') // optional if you are using session on server side\n")
            file.write('    };\n')
            file.write('\n')
            file.write("    fetch('enroll_with_progress.php', {\n")
            file.write("        method: 'POST',\n")
            file.write('        body: JSON.stringify(jsonPayload),\n')
            file.write('        headers: {\n')
            file.write("            'Content-Type': 'application/json'\n")
            file.write('        }\n')
            file.write('    })\n')
            file.write('    .then(response => response.json())\n')
            file.write('    .then(data => {\n')
            file.write("        const confirmationDiv = document.getElementById('confirmation');\n")
            file.write("        confirmationDiv.classList.remove('hidden');\n")
            file.write('        if (data.success) {\n')
            file.write("            confirmationDiv.innerHTML = '<p>Enrollment successful! Check your email for confirmation.</p>';\n")
            file.write("            confirmationDiv.style.color = 'green';\n")
            file.write('        } else {\n')
            file.write('            confirmationDiv.innerHTML = `<p>Error: ${data.message}</p>`;\n')
            file.write("            confirmationDiv.style.color = 'red';\n")
            file.write('        }\n')
            file.write('    })\n')
            file.write('    .catch(error => {\n')
            file.write("        console.error('Error:', error);\n")
            file.write("        const confirmationDiv = document.getElementById('confirmation');\n")
            file.write("        confirmationDiv.innerHTML = '<p>An error occurred. Please try again later.</p>';\n")
            file.write("       confirmationDiv.style.color = 'red';\n")
            file.write('    });\n')
            file.write('});\n')
            file.write('</script>\n')
            file.write('\n')
            file.write('</body>\n')
            file.write('</html>\n')


        messagebox.showinfo(_("Success"), _("Course description saved successfully."))
        self.root.quit()
        self.root.destroy()

    def auto_save_draft(self):
        while True:
            time.sleep(self.auto_save_interval)
            # Implement auto-save logic here (if needed)

if __name__ == "__main__":
    root = tk.Tk()
    app = CourseDescriptionCreator(root)
    root.mainloop()
