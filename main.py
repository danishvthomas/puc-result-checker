import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta

BOT_TOKEN   = "8774137507:AAFRsdXTb342GX8zJkuGZphRjkIf3G7aOvA"
CHAT_ID     = "1832034904"
CHECK_EVERY = 20 * 60

CHECK_URL = "https://karresults.nic.in"
KEYWORDS  = ["2nd puc", "puc 2", "2026"]

def get_ist_time():
    ist = datetime.utcnow() + timedelta(hours=5, minutes=30)
    day_str  = ist.strftime("%A")           # Tuesday
    date_str = ist.strftime("%d %b %Y")     # 08 Apr 2026
    time_str = ist.strftime("%I:%M %p")     # 06:35 AM
    return day_str, date_str, time_str

def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": message})
        print(f"✅ Telegram sent!")
    except Exception as e:
        print(f"❌ Error: {e}")

def is_result_live():
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(CHECK_URL, headers=headers, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")
        for link in soup.find_all("a", href=True):
            text = link.get_text().lower()
            if any(k in text for k in KEYWORDS) and "result" in text:
                return True, link.get_text().strip()
        return False, None
    except Exception as e:
        print(f"❌ Site error: {e}")
        return False, None

# ── START ────────────────────────────────
print("🚀 PUC Result Checker started!")
day, date, time_ist = get_ist_time()
send_telegram(
    f"🚀 Bot Started!\n"
    f"📅 {day}, {date}\n"
    f"🕐 {time_ist} IST\n\n"
    f"Checking karresults.nic.in every 20 minutes for Karnataka 2nd PUC Result 2026..."
)

# ── MAIN LOOP ────────────────────────────
check_count = 0
while True:
    check_count += 1
    day, date, time_ist = get_ist_time()
    print(f"[Check #{check_count}] {day}, {date} {time_ist} IST — Checking...")

    found, link_text = is_result_live()

    if found:
        day, date, time_ist = get_ist_time()
        send_telegram(
            f"🎉 Karnataka 2nd PUC Result 2026 is LIVE!\n\n"
            f"📅 {day}, {date}\n"
            f"🕐 {time_ist} IST\n\n"
            f"📌 {link_text}\n"
            f"🔗 Check now: https://karresults.nic.in"
        )
        print("🎉 Result found! Notification sent.")
        break
    else:
        send_telegram(
            f"⏳ Check #{check_count}\n"
            f"📅 {day}, {date}\n"
            f"🕐 {time_ist} IST\n\n"
            f"Result not yet live. Will check again in 20 minutes."
        )
        print(f"   ⏳ Not live yet. Next check in 20 mins...\n")
        time.sleep(CHECK_EVERY)
