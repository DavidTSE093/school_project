import time
import qrcode
from PIL import Image
import base64
import os

def get_mac_address():
    # 使用提供的Mac Address
    return "dc:a6:32:88:96:07"

def generate_token():
    # 随机生成64 bytes并进行base64编码
    random_bytes = os.urandom(64)
    token = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
    return token

def create_qrcode(data):
    # 生成QR码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill='black', back_color='white')
    return img

def main():
    try:
        # 获取Mac Address和生成Token
        mac_address = get_mac_address()
        token = generate_token()
        
        # 构造QRCode URL
        qrcode_url = f"https://tekpass.com.tw/sso?receiver=fcm://{mac_address}:TPYZU&token={token}"
        print("QRCode URL:", qrcode_url)
        
        # 生成并显示QR码
        img = create_qrcode(qrcode_url)
        
        # 显示QR码
        img.show()
        
        # 保存QR码到文件
        #img.save("qrcode.png")
        #print("QR code has been saved to qrcode.png")
        
        # 将 URL 和 token 保存到文件
        with open('token.txt', 'w') as file:
            #file.write(f"URL: {qrcode_url}\n")
            file.write(f"Token: {token}\n")
        print("URL and Token have been saved to token.txt")

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
