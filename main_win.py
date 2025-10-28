# PrevU 1.1 for MS Windows by mikeph_ 2025
import os
import ctypes
from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk # Pylance sucks


class WallpaperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PrevU 1.1 for MS Windows")
        self.root.geometry("800x600")
        self.root.configure(bg="#202020")

        self.images = []
        self.selected_image = None

        top_frame = Frame(root, bg="#202020")
        top_frame.pack(fill=X, pady=10)

        Button(
            top_frame, text="About", command=self.about,
            bg="#404040", fg="white"
        ).pack(side=LEFT, padx=5)

        Button(
            top_frame, text="Select Folder", command=self.load_folder,
            bg="#404040", fg="white"
        ).pack(side=LEFT, padx=5)

        self.set_button = Button(
            top_frame, text="Set as Wallpaper",
            command=self.set_wallpaper,
            bg="#1E90FF", fg="white", state=DISABLED
        )
        self.set_button.pack(side=LEFT, padx=5)

        # Preview
        self.preview = Label(root, bg="#202020")
        self.preview.pack(fill=BOTH, expand=True)

        self.text1 = Label(
            self.preview,
            text="Press 'Select Folder' to load wallpapers",
            fg="white", bg="#202020",
            font=("Segoe UI", 14, "italic")
        )
        self.text1.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Scrollable Thumbnails
        self.canvas = Canvas(root, bg="#202020", highlightthickness=0)
        self.scrollbar = Scrollbar(root, orient=VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas, bg="#202020")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        # scroll with mouse - hope it works
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def about(self):
        messagebox.showinfo(
            "About",
            "PrevU 1.1 by mikeph_ (2025)\n"
            "A simple wallpaper browser for Microsoft Windows.\n"
            "For more info, visit: https://github.com/mikeph52"
        )

    def load_folder(self):
        folder = filedialog.askdirectory(title="Select Image Folder")
        if not folder:
            return

        self.text1.place_forget()
        self.images = []
        self.selected_image = None

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for file in os.listdir(folder):
            if file.lower().endswith((".jpg", ".jpeg", ".png", ".bmp", ".gif")):
                self.images.append(os.path.join(folder, file))

        if not self.images:
            messagebox.showwarning("No Images Found", "No supported image files in this folder.")
            return

        for img_path in self.images:
            try:
                img = Image.open(img_path)
                img.thumbnail((100, 100))
                img_tk = ImageTk.PhotoImage(img)
                label = Label(self.scrollable_frame, image=img_tk, bg="#202020")
                label.image = img_tk
                label.pack(side=LEFT, padx=5, pady=5)
                label.bind("<Button-1>", lambda e, path=img_path: self.show_preview(path))
            except Exception as e:
                print(f"Error loading image {img_path}: {e}")

    def show_preview(self, img_path):
        self.selected_image = img_path
        img = Image.open(img_path)
        img.thumbnail((600, 400))
        img_tk = ImageTk.PhotoImage(img)
        self.preview.configure(image=img_tk)
        self.preview.image = img_tk
        self.set_button.config(state=NORMAL)

    def set_wallpaper(self):
        if not self.selected_image:
            messagebox.showwarning("No Image Selected", "Please select an image first.")
            return

        try:
            abs_path = os.path.abspath(self.selected_image)
            ctypes.windll.user32.SystemParametersInfoW(20, 0, abs_path, 3)
            messagebox.showinfo("Success!!!", f"Wallpaper set successfully:\n{abs_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set wallpaper: {e}")


# main
if __name__ == "__main__":
    root = Tk()
    # root.iconbitmap("prevuico.ico")  # To Fix 
    app = WallpaperApp(root)
    root.mainloop()
