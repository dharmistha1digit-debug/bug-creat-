import os
import shutil
import subprocess
from datetime import datetime
import sys
import re
import tkinter as tk
from tkinter import filedialog

def sanitize_filename(name):
    # Remove invalid characters for Windows/Linux filenames
    return re.sub(r'[\\/*?:"<>|]', "", name).replace(' ', '_')[:50] # Limit length to 50 chars

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding='utf-8')
    print("=== 🐛 GitHub Bug Report Generator ===")
    
    # 1. Get inputs from the user
    module_name = input("1. Enter Project's Module Name: ").strip()
    bug_id = input("2. Enter Bug ID (e.g., OH01): ").strip()
    browser_env = input("3. Enter Browser/Environment (e.g., Chrome / Safari): ").strip()
    description = input("4. Enter Description of the issue:\n   (e.g., The discount text shows 40% in Figma but 30% in preview)\n   > ").strip()
    
    print("5. Select the Image or Video file...")
    print("   (A file selection window will open. If you don't see it, check your taskbar. Cancel to skip.)")
    
    # Open file dialog
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.withdraw()
    media_path = filedialog.askopenfilename(
        title="Select Bug Image or Video (Cancel to skip)",
        filetypes=[("Media Files", "*.png *.jpg *.jpeg *.gif *.webp *.mp4 *.mov *.avi"), ("All Files", "*.*")]
    )
    
    if media_path:
        print(f"   ✅ Selected file: {media_path}")
    else:
        print("   ⏩ No file selected (Skipped).")

    # Remove quotes if the user somehow pasted a path with quotes
    media_path = media_path.strip('"').strip("'")

    # 2. Setup directories to store the reports
    reports_dir = "bug_reports"
    media_dir = os.path.join(reports_dir, "media")
    os.makedirs(media_dir, exist_ok=True)

    # 3. Handle Image / Screen Recording
    media_filename = ""
    if media_path and os.path.exists(media_path):
        _, ext = os.path.splitext(media_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_bug_id = sanitize_filename(bug_id)
        media_filename = f"{safe_bug_id}_{timestamp}{ext}"
        dest_path = os.path.join(media_dir, media_filename)
        shutil.copy2(media_path, dest_path)
        print(f"\n✅ Image/Video copied securely.")
    elif media_path:
        print("\n⚠️ Warning: Image/Video file not found. Proceeding without it.")

    # 4. Generate a Developer-Friendly Markdown (.md) file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_bug_id = sanitize_filename(bug_id)
    safe_module_name = sanitize_filename(module_name)
    report_filename = f"{safe_bug_id}_{safe_module_name}_{timestamp}.md"
    report_path = os.path.join(reports_dir, report_filename)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(f"# 🐛 Bug Report: [{bug_id}] {module_name}\n\n")
        f.write(f"- **Bug ID:** `{bug_id}`\n")
        f.write(f"- **Module:** `{module_name}`\n")
        f.write(f"- **Environment:** {browser_env}\n\n")
        f.write("## 📝 Description\n")
        f.write(f"{description}\n\n")
        
        if media_filename:
            f.write("## 📸 Attachments\n")
            if media_filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                f.write(f"![Bug Screenshot](./media/{media_filename})\n")
            else:
                f.write(f"🎥 [View Screen Recording or Media](./media/{media_filename})\n")
                
    print(f"✅ Developer bug report generated successfully at: {report_path}")

    # 5. Automatically Push to GitHub
    push_to_git = input("\n🚀 Do you want to push this to GitHub now? (y/n): ").strip().lower()
    if push_to_git == 'y':
        try:
            print("\nSyncing with GitHub...")
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"🐛 Add bug report for {bug_id} ({module_name})"], check=True)
            subprocess.run(["git", "push"], check=True)
            print("🎉 Successfully pushed to GitHub! Developers can now see it.")
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Error during Git operations. Make sure this folder is connected to a GitHub repository.")

if __name__ == "__main__":
    main()
