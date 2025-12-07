#!/usr/bin/env python3
"""
YouTube Downloader - 真實進度條 0-100%
"""
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
import threading
import sys
import os
from pathlib import Path

class YouTubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Downloader (yt-dlp)")
        self.root.geometry("600x500")
        self.download_path = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="best")
        self.status_var = tk.StringVar(value="Ready")
        
        self.setup_ui()
    
    def setup_ui(self):
        # Path selection
        path_frame = ttk.Frame(self.root, padding="10")
        path_frame.pack(fill="x")
        ttk.Label(path_frame, text="Download Folder:").pack(side="left")
        ttk.Entry(path_frame, textvariable=self.download_path, width=50).pack(side="left", padx=5)
        ttk.Button(path_frame, text="Browse", command=self.browse_folder).pack(side="left")
        
        # URL input
        url_frame = ttk.Frame(self.root, padding="10")
        url_frame.pack(fill="x")
        ttk.Label(url_frame, text="YouTube URL:").pack(anchor="w")
        ttk.Entry(url_frame, textvariable=self.url_var, width=70).pack(pady=5, fill="x")
        
        # Format selection
        format_frame = ttk.Frame(self.root, padding="10")
        format_frame.pack(fill="x")
        ttk.Label(format_frame, text="Format:").pack(anchor="w")
        format_options = [
            "best", "best[height<=720]", "best[height<=480]", 
            "bestvideo[height<=720]+bestaudio/best", "bestaudio",
            "mp4", "webm", "144p", "360p", "480p", "720p", "1080p"
        ]
        ttk.Combobox(format_frame, textvariable=self.format_var, 
                    values=format_options, width=67, state="readonly").pack(pady=5, fill="x")
        
        # Download button
        self.download_btn = ttk.Button(self.root, text="🚀 Download", command=self.start_download)
        self.download_btn.pack(pady=20)
        
        # Progress - 改成確定式 0-100%
        self.progress = ttk.Progressbar(self.root, mode='determinate', maximum=100)
        self.progress.pack(fill="x", padx=20, pady=10)
        
        # Status
        status_frame = ttk.Frame(self.root, padding="10")
        status_frame.pack(fill="both", expand=True)
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, wraplength=550)
        self.status_label.pack()
    
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.download_path.get())
        if folder:
            self.download_path.set(folder)
    
    def start_download(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter YouTube URL")
            return
        
        path = self.download_path.get()
        os.makedirs(path, exist_ok=True)
        
        # UI鎖定
        self.download_btn.config(state="disabled")
        self.progress['value'] = 0
        self.status_var.set("🔄 初始化下載...")
        self.root.update()
        
        # 啟動緒程
        thread = threading.Thread(target=self.download_video, args=(url, path))
        thread.daemon = True
        thread.start()
    
    def download_video(self, url, path):
        def progress_hook(d):
            """yt-dlp進度回調 → 更新GUI"""
            if d['status'] == 'downloading':
                try:
                    percent = float(d.get('_percent_str', '0%').replace('%', ''))
                    self.root.after(0, lambda: self.progress.config(value=percent))
                    self.root.after(0, lambda: self.status_var.set(
                        f"📥 下載中... {d.get('_percent_str', '0%')} "
                        f"({d.get('_total_bytes_str', '0')} / 速度: {d.get('_speed_str', 'N/A')})"
                    ))
                except:
                    pass
            elif d['status'] == 'finished':
                self.root.after(0, lambda: self.status_var.set("✅ 完成！"))
        
        try:
            ydl_opts = {
                'outtmpl': f'{path}/%(title)s.%(ext)s',
                'noplaylist': True,
                'format': self.format_var.get(),
                'progress_hooks': [progress_hook],  # 關鍵：進度回調
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # 最終完成
            self.root.after(0, lambda: self.progress.config(value=100))
            self.root.after(0, lambda: self.status_var.set("🎉 下載完成！"))
            self.root.after(0, lambda: messagebox.showinfo("成功", "影片下載完成！"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("錯誤", str(e)))
            self.root.after(0, lambda: self.status_var.set("❌ 下載失敗"))
        finally:
            # 確保UI重置
            self.root.after(0, self.reset_ui)
    
    def reset_ui(self):
        self.progress.stop()
        self.progress['value'] = 0
        self.download_btn.config(state="normal")
        self.status_var.set("✅ 準備完成")

def main():
    root = tk.Tk()
    app = YouTubeDownloader(root)
    root.mainloop()

if __name__ == "__main__":
    main()
