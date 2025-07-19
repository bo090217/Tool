import time
import telebot
import os
import pyfiglet

# Hàm in banner với pyfiglet và hiệu ứng màu xanh đậm-nhạt
def print_colorful_banner(banner_text):
    lines = banner_text.split("\n")
    for line in lines:
        print(print_colorful_line(line))

# Hàm in dòng màu sắc
def print_colorful_line(text):
    colors = ['\033[94m', '\033[96m']  # Màu xanh đậm và nhạt
    reset = '\033[0m'
    result = ''
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        result += color + char
    return result + reset

# Hộp thông tin nhiều màu
def print_colorful_box():
    reset = '\033[0m'
    text_lines = [
        "DEVELOPER : Nguyễn Hiếu",
        "ADMIN BY : Nguyễn Hiếu",
        "DISCORD : frv_23th04"
    ]
    max_len = max(len(line) for line in text_lines) + 4
    top_bottom = "═" * max_len

    print('\033[96m' + "╔" + top_bottom + "╗" + reset)
    for line in text_lines:
        colorful = print_colorful_line(line)
        padding = max_len - len(line)
        print('\033[94m' + "║  " + colorful + ' ' * (padding - 2) + "║" + reset)
    print('\033[96m' + "╚" + top_bottom + "╝" + reset)

# Xóa màn hình và in banner với pyfiglet
os.system('clear')  # Sử dụng clear để làm sạch màn hình
banner = pyfiglet.figlet_format("Nguyen Hieu", font="big")
print_colorful_banner(banner)  # In banner có hiệu ứng màu xanh đậm-nhạt

# In hộp thông tin nhiều màu
print_colorful_box()

# Đọc nội dung tin nhắn từ file người dùng nhập vào
def read_message(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            message = f.read().strip()  # Đọc nội dung trong file và loại bỏ khoảng trắng thừa
        return message
    except Exception as e:
        print(f"Lỗi khi đọc file tin nhắn: {e}")
        return None

# Nhập thông tin cấu hình trực tiếp khi chạy chương trình
TOKEN = input("Nhập Token Bot Telegram: ")
GROUP_ID = input("Nhập ID nhóm (dạng -100xxxxxxx): ")
DELAY = int(input("Nhập thời gian delay giữa các tin nhắn (giây): "))

# Yêu cầu người dùng nhập tên file tin nhắn
message_file = input("Nhập tên file tin nhắn (ví dụ: message.txt): ")
MESSAGE = read_message(message_file)  # Đọc nội dung từ file người dùng nhập

# Nhập link ảnh
IMAGE_URL = input("Nhập link ảnh (hoặc để trống nếu không gửi ảnh): ")

# Kiểm tra xem có thiếu thông tin gì không
if not TOKEN or not GROUP_ID:
    print("Token hoặc Group ID không hợp lệ!")
    exit()

if MESSAGE is None:
    print("Không có nội dung tin nhắn trong file!")
    exit()

# Giới hạn độ dài của caption (tin nhắn kèm ảnh) không vượt quá 1024 ký tự
MAX_CAPTION_LENGTH = 1024
if len(MESSAGE) > MAX_CAPTION_LENGTH:
    MESSAGE = MESSAGE[:MAX_CAPTION_LENGTH]  # Cắt bớt nếu tin nhắn quá dài

# Khởi tạo bot
bot = telebot.TeleBot(TOKEN)

# Hàm gửi tin nhắn kèm ảnh
def send_message():
    try:
        if IMAGE_URL:  # Nếu có link ảnh, gửi tin nhắn kèm theo ảnh
            bot.send_photo(GROUP_ID, IMAGE_URL, caption=MESSAGE)
            print(f"Đã gửi tin nhắn và ảnh: {MESSAGE}")
        else:  # Nếu không có ảnh, chỉ gửi tin nhắn
            bot.send_message(GROUP_ID, MESSAGE)
            print(f"Đã gửi tin nhắn: {MESSAGE}")
    except Exception as e:
        print(f"Lỗi khi gửi tin nhắn hoặc ảnh: {e}")

# Chạy liên tục và gửi tin nhắn đến khi dừng
while True:
    send_message()
    time.sleep(DELAY)  # Delay giữa các lần gửi tin nhắn
