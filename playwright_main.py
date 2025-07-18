import os
import glob
from playwright.sync_api import sync_playwright
import time

# === CREDENTIALS ===
EMAIL = "subhanikhubaib23@gmail.com"
PASSWORD = "Hello@123"
SCRIPT_PATH = "/files/script.txt"
#SCRIPT_PATH = r"D:\\podcast_automation\\script.txt"

download_dir = "/files"
#download_dir = r"D:\podcast_automation"
new_name = "podcast.wav"
new_path = os.path.join(download_dir, new_name)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(accept_downloads=True)#, downloads_path=download_dir)
    page = context.new_page()

    # === Open NotebookLM ===
    page.goto("https://notebooklm.google.com/")

    # === Google Sign-in ===
    page.fill("#identifierId", EMAIL)
    page.click("text=Next")
    page.wait_for_timeout(3000)
    page.fill("input[name=Passwd]", PASSWORD)
    page.click("text=Next")
    page.wait_for_timeout(5000)
    print("✅ Logged in successfully.")

    # === Click "Create New" ===
    page.wait_for_selector("button")
    page.locator("button").nth(1).click()
    print("✅ Clicked 'Create New'")
    page.wait_for_timeout(5000)

    # ✅ Direct Upload
    upload_button = page.locator("button[aria-label='Upload sources from your computer']")
    upload_button.wait_for(state="visible", timeout=10000)
    upload_button.click()
    print("✅ Clicked 'Upload sources from your computer'")

    file_input = page.locator("input[type='file']")
    file_input.wait_for(state="attached", timeout=10000)
    file_input.set_input_files(SCRIPT_PATH)
    print("✅ File uploaded successfully")
    page.wait_for_timeout(3000)

    # === Generate
    generate_button = page.locator("button:has-text('Generate')")
    generate_button.wait_for(state="visible", timeout=15000)
    generate_button.click()
    print("🎬 Clicked Generate")
    page.wait_for_timeout(200000)

    # ✅ Click 3-dot Menu
    all_buttons = page.locator("button")
    print("✅ Found total buttons:", all_buttons.count())
    all_buttons.nth(21).click()
    print("✅ Clicked 3-dot menu")
    page.wait_for_timeout(2000)

    # ✅ Handle download properly
    download_option = page.get_by_role("menuitem", name="Download", exact=True)
    download_option.wait_for(state="visible", timeout=10000)

    with page.expect_download() as download_info:
        download_option.click()
        print("✅ Clicked Download Option")

    download = download_info.value
    download.save_as(new_path)
    print(f"✅ File downloaded and saved directly as '{new_path}' ✅ All Done.")

    page.wait_for_timeout(120000)

    browser.close()

# ✅ Rename the most recent .wav file after download
wav_files = glob.glob(os.path.join(download_dir, "*.wav"))
if not wav_files:
    raise FileNotFoundError("❌ No .wav files found in the download folder.")

latest_file = max(wav_files, key=os.path.getctime)
os.rename(latest_file, new_path)
print(f"✅ Renamed '{latest_file}' to '{new_path}' ✅ All Done.")
