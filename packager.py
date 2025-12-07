#!/usr/bin/env python3
"""
終極PyInstaller打包器：yt-dlp Python API + 真實進度條版本
100%獨立單一EXE，零依賴！
"""
import subprocess
import platform
import sys
import os
import shutil
import glob

def cleanup_build():
    """清理舊打包檔案"""
    for folder in ["dist", "build"]:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)
    for spec in glob.glob("*.spec"):
        os.remove(spec)
    print("🧹 清理完成")

def ensure_dependencies():
    """確保所有Python依賴"""
    print("📦 檢查依賴...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", 
                          "yt-dlp", "pyinstaller"])
    print("✅ 依賴齊全")

def build_standalone_exe():
    """生成100%獨立單一EXE"""
    cleanup_build()
    ensure_dependencies()
    
    print("🏗️  打包真實進度條版本...")
    print("📦 包含：Python + tkinter + yt-dlp Python API")
    
    cmd = [
        "pyinstaller",
        "--onefile",                    # 單一EXE
        "--windowed",                   # 無控制台
        "--noconsole",                  # 確保無控制台
        "--name", "YouTubeDownloader",
        
        # yt-dlp完整打包
        "--collect-all", "yt_dlp",
        "--hidden-import=yt_dlp",
        "--hidden-import=yt_dlp.YoutubeDL",
        "--hidden-import=yt_dlp.utils",
        
        # tkinter完整支援
        "--collect-all", "tkinter",
        "--hidden-import=tkinter",
        "--hidden-import=tkinter.filedialog",
        "--hidden-import=tkinter.ttk",
        "--hidden-import=tkinter.messagebox",
        
        # 其他必要模組
        "--hidden-import=pathlib",
        "--hidden-import=threading",
        
        # 最佳化
        "--strip",
        "--clean",
        
        "youtube_downloader.py"
    ]
    
    result = subprocess.run(cmd, check=True)
    print("✅ 打包成功！")
    print("🎮 dist/YouTubeDownloader.exe (~65MB)")
    print("🚀 任何Windows雙擊即可用，完美獨立！")
    
    # 顯示檔案資訊
    if os.path.exists("dist/YouTubeDownloader.exe"):
        size = os.path.getsize("dist/YouTubeDownloader.exe") / (1024*1024)
        print(f"📊 檔案大小：{size:.1f} MB")

if __name__ == "__main__":
    if platform.system() != "Windows":
        print("❌ 僅支援Windows打包")
        sys.exit(1)
    
    print("🔥 YouTube Downloader 終極打包器")
    print("📱 真實進度條 0-100% + Python API版本")
    
    try:
        build_standalone_exe()
        print("\n🎉 打包完成！複製 dist/YouTubeDownloader.exe 即可分發")
        print("💡 測試獨立性：刪除conda環境後仍可執行")
    except subprocess.CalledProcessError as e:
        print(f"❌ PyInstaller錯誤：{e}")
        print("💡 請關閉防毒軟體後重試")
    except Exception as e:
        print(f"❌ 打包失敗：{e}")
