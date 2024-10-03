import smbus
import time
import qrcode
from PIL import Image
import base64
import os
import socket #get mac address
import fcntl #get mac address
import struct #get mac address

DEVICE_ADDRESS = 0x50  # EEPROM的I2C地址
I2C_BUS = 1            # I2C总线号，通常为1

# 初始化I2C总线
try:
    bus = smbus.SMBus(I2C_BUS)
    print(f"I2C bus {I2C_BUS} initialized.")
except Exception as e:
    print(f"Error initializing I2C bus {I2C_BUS}: {e}")
    exit(1)

def read_eeprom(address, num_bytes):
    try:
        # 读取EEPROM数据
        data = bus.read_i2c_block_data(DEVICE_ADDRESS, address, num_bytes)
        return data
    except Exception as e:
        print(f"Error reading EEPROM at address {address} with {num_bytes} bytes: {e}")
        raise

def data_to_string(data):
    # 将数据转换为ASCII字符串
    ascii_string = ''.join(chr(byte) for byte in data)
    return ascii_string


def get_mac_address(interface='eth0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 使用 ioctl 来获取 MAC 地址
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', bytes(interface[:15], 'utf-8')))
    # 将 MAC 地址格式化为人类可读的字符串
    return ':'.join(['%02x' % b for b in info[18:24]])


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
        # 打印调试信息
        print(f"Using I2C address: {DEVICE_ADDRESS}")
        print(f"Using I2C bus: {I2C_BUS}")
        
        # 读取EEPROM的前8个字节
        data = read_eeprom(0, 8)
        
        # 打印读取到的原始数据
        print(f"Raw data read from EEPROM: {data}")
        
        # 将数据转换为ASCII字符串
        ascii_string = data_to_string(data)
        print("Password:", ascii_string)

    except Exception as e:
        print("Error:", str(e))

    try:
        # 获取Mac Address和生成Token
        # 调用函数以抓取 eth0 的 MAC 地址
        mac_address = get_mac_address('eth0')
        print(f"MAC Address: {mac_address}")
        
        token = generate_token()
        
        # 构造QRCode URL
        qrcode_url = f"https://tekpass.com.tw/sso?receiver=fcm://{mac_address}:TPYZU&token={token}"
        print("QRCode URL:", qrcode_url)
        
        # 生成并显示QR码
        img = create_qrcode(qrcode_url)
        
        # 显示QR码
        img.show()
        
        # 将 URL 和 token 保存到文件
        with open('token.txt', 'w') as file:
            #file.write(f"URL: {qrcode_url}\n")
            file.write(f"Token: {token}\n")
        print("URL and Token have been saved to token.txt")

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
