import os, time, threading, json, random
from zlapi import ZaloAPI, ThreadType
from zlapi.models import Message, Mention

def show_banner():
    print("=" * 60)
    print("        ZALO TOOL - SPAM NHÂY TAG KHÔNG FAKE SOẠN")
    print("=" * 60)

def display_loading(text="[*] Loading", delay=0.5, dot_count=3):
    for i in range(1, dot_count + 1):
        print(text + "." * i)
        time.sleep(delay)

def parse_selection(input_str, max_index):
    try:
        numbers = [int(i.strip()) for i in input_str.split(',')]
        return [n for n in numbers if 1 <= n <= max_index]
    except:
        print("❌ Định dạng không hợp lệ!")
        return []

class Bot(ZaloAPI):
    def __init__(self, imei, session_cookies):
        super().__init__('api_key', 'secret_key', imei, session_cookies)

    def fetch_groups(self):
        try:
            all_groups = self.fetchAllGroups()
            group_list = []
            for group_id in all_groups.gridVerMap:
                group_info = self.fetchGroupInfo(group_id)
                group_name = group_info.gridInfoMap[group_id]["name"]
                group_list.append({'id': group_id, 'name': group_name})
            return group_list
        except Exception as e:
            print(f"Lỗi lấy danh sách nhóm: {e}")
            return []

    def fetch_members(self, group_id):
        try:
            group_info = self.fetchGroupInfo(group_id)
            if not group_info or group_id not in group_info.gridInfoMap:
                print(f"Không lấy được thông tin nhóm {group_id}")
                return []
            mem_ver_list = group_info.gridInfoMap[group_id]["memVerList"]
            member_ids = [mem.split("_")[0] for mem in mem_ver_list]
            members = []
            for user_id in member_ids:
                try:
                    user_info = self.fetchUserInfo(user_id)
                    user_data = user_info.changed_profiles[user_id]
                    members.append({'id': user_data['userId'], 'name': user_data['displayName']})
                except:
                    members.append({'id': user_id, 'name': f"[Lỗi: {user_id}]"})
            return members
        except Exception as e:
            print(f"Lỗi lấy thành viên: {e}")
            return []

def tag_user_from_nhay(client, target_uid, thread_id, target_name, delay, imei, session_cookies, stop_event):
    try:
        with open("nhay.txt", "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("⚠️ Không tìm thấy file nhay.txt")
        return

    if not lines:
        print("⚠️ nhay.txt không có nội dung!")
        return

    typing_api = ZaloAPI('api_key', 'secret_key', imei, session_cookies)

    def spam_loop():
        count = 0
        while not stop_event.is_set():
            for content in lines:
                if stop_event.is_set():
                    print("⏹️ Dừng spam bởi stop_event.")
                    return

                typing_time = random.uniform(2, 5)
                print(f"[Fake Soạn] {content} ({typing_time:.1f}s)")

                try:
                    typing_api.set_typing_real(thread_id, ThreadType.GROUP)
                except:
                    pass

                time.sleep(typing_time)

                mention_text = f" @{target_name}"
                full_text = content + mention_text
                mention = Mention(
                    target_uid,
                    offset=len(content) + 1,
                    length=len(mention_text.strip())
                )

                try:
                    client.send(Message(text=full_text, mention=mention), thread_id, ThreadType.GROUP)
                    count += 1
                    print(f"[✓] ({count}) Gửi thành công tới nhóm: {thread_id}, tag: {target_name}")
                except Exception as e:
                    print(f"[!] Lỗi gửi: {e}")

                time.sleep(max(delay - typing_time, 0.5))

    threading.Thread(target=spam_loop, daemon=True).start()

    
def main():
    show_banner()
    display_loading()

    imei = input("📱 Nhập IMEI: ")
    cookie_str = input("🍪 Nhập Cookie: ")
    try:
        session_cookies = eval(cookie_str)
        if not isinstance(session_cookies, dict):
            raise ValueError("Cookie không đúng định dạng")
    except:
        print("❌ Cookie không hợp lệ!")
        return

    try:
        delay = float(input("⏱️ Tổng delay giữa mỗi dòng gửi (giây) [mặc định 10]: ") or 10)
    except:
        delay = 10

    stop_event = threading.Event()  # Initialize stop_event

    bot = Bot(imei, session_cookies)
    groups = bot.fetch_groups()
    if not groups:
        return

    print("\n📋 Danh sách nhóm:")
    for i, g in enumerate(groups, 1):
        print(f"{i}. {g['name']} | ID: {g['id']}")

    raw = input("📌 Nhập số nhóm (VD: 1): ") or "1"
    selected = parse_selection(raw, len(groups))
    if not selected:
        return

    for i in selected:
        group_id = groups[i - 1]['id']
        members = bot.fetch_members(group_id)

        print(f"\n👥 Thành viên nhóm {group_id}:")
        for j, m in enumerate(members, 1):
            print(f"{j}. {m['name']} | {m['id']}")

        stt_mem = input("🎯 Nhập STT người bạn muốn tag: ")
        try:
            index = int(stt_mem) - 1
            user = members[index]
            print(f"👉 Đang gửi cho: {user['name']} ({user['id']})")
            tag_user_from_nhay(bot, user['id'], group_id, user['name'], delay, imei, session_cookies, stop_event)  # Pass stop_event
        except Exception as e:
            print(f"❌ Lỗi chọn người: {e}")

    while True:
        time.sleep(1000)

if __name__ == "__main__":
    main()
