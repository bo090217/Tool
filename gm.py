import smtplib
import time
import os
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import pyfiglet

# Hàm tải ảnh từ URL với việc thử lại khi gặp lỗi
def download_image(image_url, image_name, retries=3, delay=5):
    attempt = 0
    while attempt < retries:
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                with open(image_name, 'wb') as f:
                    f.write(response.content)
                print(f"📷 Đã tải ảnh thành công từ {image_url}")
                return image_name
            else:
                print(f"❌ Lỗi khi tải ảnh. Mã trạng thái HTTP: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌ Lỗi khi tải ảnh: {e}")
            attempt += 1
            print(f"💡 Thử lại lần {attempt} sau {delay} giây...")
            time.sleep(delay)
    
    print("❌ Không thể tải ảnh sau nhiều lần thử.")
    return None

# Hàm gửi email với đính kèm ảnh
def send_email(sender, app_pass, subject, body, to, image_path=None):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = ", ".join(to)

    # Thêm nội dung email
    msg.attach(MIMEText(body, 'plain'))

    # Đính kèm ảnh nếu có
    if image_path:
        try:
            with open(image_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(image_path))
                msg.attach(img)
        except Exception as e:
            print(f"❌ Lỗi khi đính kèm ảnh: {e}")
            return

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, app_pass)
            server.sendmail(sender, to, msg.as_string())
        print(f"📨 Đã gửi email tới: {', '.join(to)}")
    except Exception as e:
        print(f"❌ Lỗi khi gửi email: {e}")

# Hàm in banner với hiệu ứng màu sắc
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
print_colorful_banner(banner)  # In banner có hiệu ứng màu xanh đậm-nhạt ở đầu nhập thông tin

# In hộp thông tin màu sắc
print_colorful_box()

# Hàm bắt đầu quy trình gửi spam
def start_spam_sequence():
    # Cấu hình thông tin tài khoản Gmail
    sender_email = input("Nhập địa chỉ Gmail của bạn: ")
    app_password = input("Nhập mật khẩu ứng dụng Gmail của bạn: ")

    # Cấu hình nội dung email
    subject = input("Nhập tiêu đề email: ")
    body = input("Nhập nội dung email: ")
    recipients = input("Nhập email người nhận (cách nhau bởi dấu phẩy): ").split(',')
    
    # Đường dẫn đến ảnh mặc định
    image_path = "duyhieu.png"
    
    # Kiểm tra nếu ảnh không tồn tại
    if not os.path.exists(image_path):
        print("❌ Không tìm thấy ảnh 'duyhieu.png' trong thư mục hiện tại.")
        image_path = None  # Không gửi ảnh nếu không tìm thấy tệp

    # Thời gian delay giữa các email (tính bằng giây)
    delay = float(input("Nhập thời gian delay giữa các email (tính bằng giây): "))

    # Vòng lặp gửi email spam
    count = 0
    while True:
        # Thêm số thứ tự vào tiêu đề cho các email tiếp theo
        subject_with_count = f"{subject} {count}" if count > 0 else subject
        send_email(sender_email, app_password, subject_with_count, body, recipients, image_path)
        count += 1
        time.sleep(delay)

# Chạy quy trình gửi email spam
if __name__ == "__main__":
    start_spam_sequence()
