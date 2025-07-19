import os
import asyncio
import aiohttp
import random
import sys
import time
import pyfiglet
from colorama import Fore, Style, init

init(autoreset=True)

CHANNEL_COLORS = [Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTBLUE_EX]
MAX_CONCURRENT_REQUESTS = 3

# Function to print the colorful lines with alternating colors
def print_colorful_line(text):
    colors = ['\033[94m', '\033[96m', '\033[97m']
    reset = '\033[0m'
    result = ''
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        result += color + char
    return result + reset

# Function to print the colorful box with developer information
def print_colorful_box():
    reset = '\033[0m'
    text_lines = [
        "DEVELOPER : Nguyễn Hiếu",
        "ADMIN BY : Nguyễn Hiếu",
        "DISCORD : frv_23th04"
    ]
    
    # Calculate the max length of the text lines to center them
    max_len = max(len(line) for line in text_lines)
    padding = 30  # Adjust this value to widen or narrow the box
    top_bottom = "═" * (max_len + 4)

    print('\033[96m' + "╔" + top_bottom + "╗" + reset)
    for line in text_lines:
        colorful = print_colorful_line(line)
        # Center the text in the box
        padding_left = (max_len + 4 - len(line)) // 2
        padding_right = max_len + 4 - len(line) - padding_left
        print('\033[94m' + "║" + ' ' * padding_left + colorful + ' ' * padding_right + "║" + reset)
    print('\033[96m' + "╚" + top_bottom + "╝" + reset)

# Function to show the menu with the choices
def print_instructions():
    instructions = f"""
{Fore.LIGHTCYAN_EX + Style.BRIGHT}═══════ HƯỚNG DẪN SỬ DỤNG TOOL SPAM DISCORD ═══════
{Fore.WHITE}Chọn một trong các chức năng sau:
{Fore.LIGHTMAGENTA_EX}1: Treo ngôn Discord
{Fore.LIGHTMAGENTA_EX}2: Nhây (tag hoặc để trống)
{Fore.LIGHTMAGENTA_EX}3: Nhây với Fake Soạn
{Fore.LIGHTMAGENTA_EX}4: Réo tên (có fake soạn)
{Fore.LIGHTCYAN_EX}Nhập số 1, 2, 3 hoặc 4 để chọn chức năng:
"""
    print(instructions)

async def validate_token(token):
    url = "https://discord.com/api/v10/users/@me"
    headers = {"Authorization": token}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return response.status == 200

async def load_tokens_from_file(token_file):
    if not os.path.exists(token_file):
        print(f"{Fore.LIGHTRED_EX}[ERROR] File token '{token_file}' không tồn tại!")
        return []
    with open(token_file, 'r', encoding='utf-8') as file:
        tokens = [t.strip() for t in file.read().splitlines() if t.strip()]
    if not tokens:
        print(f"{Fore.LIGHTRED_EX}[ERROR] File token '{token_file}' trống!")
    return tokens

async def handle_response(response, channel_id, message, token):
    token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token
    message_words = message.split()
    message_preview = " ".join(message_words[:5]) + "..." if len(message_words) > 10 else message

    try:
        if response.status == 200:
            print(f"{Fore.LIGHTGREEN_EX}[SUCCESS] Gửi tin nhắn thành công - Token: {token_preview}")
            return 0
        elif response.status == 429:
            retry_after = (await response.json()).get("retry_after", 1)
            print(f"{Fore.LIGHTYELLOW_EX}[INFO] Token {token_preview} bị giới hạn, chờ {retry_after}s")
            return retry_after
        elif response.status == 401:
            print(f"{Fore.LIGHTRED_EX}[ERROR] Token {token_preview} không hợp lệ!")
            return 0
        elif response.status in [500, 502, 408]:
            print(f"{Fore.LIGHTRED_EX}[ERROR] Lỗi server {response.status} - Token: {token_preview}")
            return 5
        else:
            print(f"{Fore.LIGHTRED_EX}[ERROR] Lỗi {response.status} - Token: {token_preview}")
            return 5
    except Exception as e:
        print(f"{Fore.LIGHTRED_EX}[ERROR] Lỗi xử lý phản hồi: {str(e)[:50]}...")
        return 5

def get_valid_input(prompt, valid_func, error_message="Input không hợp lệ, vui lòng thử lại."):
    while True:
        user_input = input(f"{Fore.LIGHTCYAN_EX}{prompt}{Style.RESET_ALL}")
        if valid_func(user_input):
            return user_input
        print(f"{Fore.LIGHTRED_EX}{error_message}")

def is_valid_delay(input_str):
    try:
        delay = float(input_str)
        return delay > 0
    except ValueError:
        return False

def is_valid_number(input_str):
    try:
        float(input_str)
        return True
    except ValueError:
        return False

def is_valid_channel_id(input_str):
    return input_str.isdigit()

async def check_file_exists(file_path):
    exists = os.path.exists(file_path)
    if not exists:
        print(f"{Fore.LIGHTRED_EX}[ERROR] File '{file_path}' không tồn tại!")
    return exists

async def spam_message(token, channel_id, message, delay, color, semaphore):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    message = message[:2000]  
    token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token

    async with aiohttp.ClientSession() as session:
        while True:
            try:
                async with semaphore:
                    async with session.post(url, json={"content": message}, headers=headers) as response:
                        retry_after = await handle_response(response, channel_id, message, token)
                        if retry_after:
                            await asyncio.sleep(retry_after)
                        else:
                            await asyncio.sleep(delay + random.uniform(0.5, 1.5))
            except Exception as e:
                print(f"{Fore.LIGHTRED_EX}[ERROR] Token {token_preview}: {str(e)[:50]}...")
                await asyncio.sleep(1)

async def spam_message_nhay(token, channel_id, messages, delay, color, mention_user, user_ids, semaphore):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token
    mention_string = " ".join([f"<@{user_id}>" for user_id in user_ids]) if mention_user else ""

    async with aiohttp.ClientSession() as session:
        while True:
            for message in messages:
                try:
                    async with semaphore:
                        message_to_send = f"{mention_string} {message}" if mention_user else message
                        async with session.post(url, json={"content": message_to_send}, headers=headers) as response:
                            retry_after = await handle_response(response, channel_id, message, token)
                            if retry_after:
                                await asyncio.sleep(retry_after)
                            await asyncio.sleep(delay + random.uniform(0.5, 1.5))
                except Exception as e:
                    print(f"{Fore.LIGHTRED_EX}[ERROR] Token {token_preview}: {str(e)[:50]}...")
                    await asyncio.sleep(1)

async def fake_typing_and_send_message(token, channel_id, messages, delay, color, mention_user, user_ids, semaphore, name_to_call=None):
    headers = {"Authorization": token, "Content-Type": "application/json"}
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    typing_url = f"https://discord.com/api/v10/channels/{channel_id}/typing"
    token_preview = token[:5] + "..." + token[-5:] if len(token) > 10 else token
    mention_string = " ".join([f"<@{user_id}>" for user_id in user_ids]) if mention_user else ""

    async with aiohttp.ClientSession() as session:
        while True:
            for message in messages:
                try:
                    if name_to_call:
                        message = message.replace("{name}", name_to_call)
                    async with session.post(typing_url, headers=headers):
                        for _ in message:
                            sys.stdout.flush()
                            await asyncio.sleep(0.05)
                    async with semaphore:
                        message_to_send = f"{mention_string} {message}" if mention_user else message
                        async with session.post(url, json={"content": message_to_send}, headers=headers) as response:
                            retry_after = await handle_response(response, channel_id, message, token)
                            if retry_after:
                                await asyncio.sleep(retry_after)
                        await asyncio.sleep(delay)
                except Exception as e:
                    print(f"{Fore.LIGHTRED_EX}[ERROR] Token {token_preview}: {str(e)[:50]}...")
                    await asyncio.sleep(1)

async def main():
    # Clear the screen at the start of the program
    os.system('cls' if os.name == 'nt' else 'clear')

    # Display the banner and the colorful box
    banner = pyfiglet.figlet_format("Nguyen Hieu", font="big")
    print(Fore.LIGHTCYAN_EX + banner)  # Display the banner
    print_colorful_box()  # Display the colorful box with developer info

    print_instructions()

    choice = get_valid_input("Chọn chức năng (1-4): ", lambda x: x in ["1", "2", "3", "4"], "Lựa chọn không hợp lệ!")

    mention_user = False
    name_to_call = None
    if choice in ["2", "3", "4"]:
        mention_user = input(f"{Fore.LIGHTYELLOW_EX}Có muốn tag người dùng? (y/n): {Style.RESET_ALL}").strip().lower() == 'y'
    if mention_user:
        user_ids = input(f"{Fore.LIGHTYELLOW_EX}Nhập ID người dùng (cách nhau bởi dấu phẩy): {Style.RESET_ALL}").split(',')
        user_ids = [uid.strip() for uid in user_ids if uid.strip()]
    else:
        user_ids = []
    if choice == "4":
        name_to_call = input(f"{Fore.LIGHTYELLOW_EX}Nhập tên cần réo: {Style.RESET_ALL}").strip()

    channel_ids = []
    while True:
        channel_id = input(f"{Fore.LIGHTCYAN_EX}Nhập ID kênh (hoặc 'done' để kết thúc): {Style.RESET_ALL}").strip().lower()
        if channel_id == "done":
            break
        if is_valid_channel_id(channel_id):
            channel_ids.append(channel_id)
        else:
            print(f"{Fore.LIGHTRED_EX}ID kênh không hợp lệ!")

    tokens_map = {}
    for idx, channel_id in enumerate(channel_ids):
        color = CHANNEL_COLORS[idx % len(CHANNEL_COLORS)]
        token_file = input(f"{color}Nhập file token cho kênh {channel_id}: {Style.RESET_ALL}")
        if not await check_file_exists(token_file):
            continue
        tokens = await load_tokens_from_file(token_file)
        valid_tokens = [t for t in tokens if await validate_token(t)]
        if not valid_tokens:
            print(f"{Fore.LIGHTRED_EX}[ERROR] Không có token hợp lệ trong file {token_file}!")
            continue
        tokens_map[channel_id] = valid_tokens

    if not tokens_map:
        print(f"{Fore.LIGHTRED_EX}[ERROR] Không có kênh hoặc token hợp lệ để tiếp tục!")
        return

    txt_files = [f for f in os.listdir() if f.endswith('.txt')]
    if not txt_files:
        print(f"{Fore.LIGHTRED_EX}[ERROR] Không tìm thấy file .txt nào trong thư mục!")
        return

    print(f"{Fore.LIGHTCYAN_EX + Style.BRIGHT}═══════ DANH SÁCH FILE TIN NHẮN ═══════")
    for idx, file in enumerate(txt_files, 1):
        print(f"{Fore.LIGHTBLUE_EX}{idx}: {file}")
    try:
        file_indexes = input(f"{Fore.LIGHTYELLOW_EX}Chọn file tin nhắn (số thứ tự, cách nhau bởi dấu phẩy): {Style.RESET_ALL}")
        file_indexes = [int(i) - 1 for i in file_indexes.split(',') if i.strip()]
        if any(index < 0 or index >= len(txt_files) for index in file_indexes):
            print(f"{Fore.LIGHTRED_EX}[ERROR] Chỉ số file không hợp lệ!")
            return
    except ValueError:
        print(f"{Fore.LIGHTRED_EX}[ERROR] Vui lòng nhập số hợp lệ!")
        return

    files_content = []
    for file_index in file_indexes:
        with open(txt_files[file_index], 'r', encoding='utf-8') as file:
            files_content.append(file.read().strip())

    print(f"{Fore.LIGHTMAGENTA_EX + Style.BRIGHT}═══════ BẮT ĐẦU SPAM ═══════")
    print(f"{Fore.LIGHTCYAN_EX}[CONFIG] Số kênh: {len(channel_ids)} | Số file tin nhắn: {len(files_content)}")
    
    tasks = []
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)
    for idx, (channel_id, tokens) in enumerate(tokens_map.items()):
        color = CHANNEL_COLORS[idx % len(CHANNEL_COLORS)]
        for i, token in enumerate(tokens):
            try:
                delay = float(input(f"{color}Nhập delay cho token thứ {i + 1} (kênh {channel_id}): {Style.RESET_ALL}"))
                if choice == "1":
                    tasks.append(spam_message(token, channel_id, files_content[i % len(files_content)], delay, color, semaphore))
                elif choice == "2":
                    messages = files_content[i % len(files_content)].splitlines()
                    tasks.append(spam_message_nhay(token, channel_id, messages, delay, color, mention_user, user_ids, semaphore))
                elif choice in ["3", "4"]:
                    messages = files_content[i % len(files_content)].splitlines()
                    tasks.append(fake_typing_and_send_message(token, channel_id, messages, delay, color, mention_user, user_ids, semaphore, name_to_call))
            except ValueError:
                print(f"{Fore.LIGHTRED_EX}[ERROR] Delay không hợp lệ cho token thứ {i + 1}!")
                return

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())