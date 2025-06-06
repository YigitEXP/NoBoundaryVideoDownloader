import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import yt_dlp
import os
import webbrowser


class NoBoundaryFreeDownloader(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.root.title("NoBoundaryFree")
        self.root.geometry("500x300")
        self.root.resizable(True, True)

        messagebox.showinfo(
            message="To avoid the problem of losing the downloaded file, you can create a folder and select the download path as that folder.",
            icon='info'
        )

        self.label = tk.Label(self.root, text="Please enter a URL")
        self.label.pack(pady=20)

        self.url_entry = tk.Entry(self.root, width=60)
        self.url_entry.pack(pady=20)

        self.download_button = tk.Button(self.root, text="Download this video", command=self.start_download)
        self.download_button.pack(pady=20)

        self.status_label = tk.Label(self.root, text="Non Active")
        self.status_label.pack(pady=20)

        self.github_button = tk.Button(self.root, text="Visit My GitHub", command=self.visit_github, background="black", foreground="white")
        self.github_button.place(relx=0.01, rely=0.80, anchor="w")

        self.linkedin_button = tk.Button(self.root, text="Visit My LinkedIn", command=self.visit_linkedin, background="#0A66C2", foreground="white")
        self.linkedin_button.place(relx=0.01, rely=0.93, anchor="w")

    def visit_github(self):
        webbrowser.open_new_tab("https://github.com/YigitEXP")

    def visit_linkedin(self):
        webbrowser.open_new_tab("https://www.linkedin.com/in/yi%C4%9Fit-can-akt%C3%BCrk-6b48262b6/")

    def start_download(self):
        self.download_button.config(bg='cyan')
        threading.Thread(target=self.download_video, daemon=True).start()

    def download_video(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "URL cannot be empty")
            return
        path = filedialog.askdirectory()
        if not path:
            messagebox.showerror("Error", "Path cannot be empty")
            return

        self.status_label.config(text=f"Downloading to {path}")

        ytdlp_options = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'outtmpl': os.path.join(path, '%(title).40s_Akturk_.%(ext)s'),
            'noplaylist': True,
            'progress_hooks': [self.hook],
            'ffmpeg_location': None
        }

        try:
            with yt_dlp.YoutubeDL(ytdlp_options) as ydl:
                ydl.download([url])
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}")

    def hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', '0%').strip()
            self.status_label.config(text=f"Downloading {percent}")
        elif d['status'] == 'finished':
            self.status_label.config(text="Download Complete")
            self.download_button.config(bg='green',fg='white')



if __name__ == "__main__":
    root = tk.Tk()
    app = NoBoundaryFreeDownloader(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
