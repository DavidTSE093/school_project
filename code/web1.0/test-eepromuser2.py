import smbus
import time
import qrcode
from PIL import Image
import base64
import os
import socket  # 获取 MAC 地址
import fcntl   # 获取 MAC 地址
import struct   # 获取 MAC 地址

DEVICE_ADDRESS = 0x50  # EEPROM 的 I2C 地址
I2C_BUS = 1            # I2C 总线号，通常为 1

id = "test-YVNEbmZiUyZr"
pin = "908343"
xlh = "M0BVIbuI7NQFSPgeSQhuX60HlgswwmF881kwutF-orJ7iruu3tkL7ikhO_ApmATeuxyDCRIc-HxuoZYp_7PT0c1q7ZI2GbgsqMdybEGyLUTwBrZO9JTHCoWUBC4WWgxZMD6v3YrTn8Hm1Qf_nCZeGbV3PodMHCk7"

# 初始化 I2C 总线
try:
    bus = smbus.SMBus(I2C_BUS)
except Exception as e:
    print("初始化 I2C 总线时出错:", str(e))

def read_eeprom(address, num_bytes):
    # 从 EEPROM 读取数据
    try:
        data = bus.read_i2c_block_data(DEVICE_ADDRESS, address, num_bytes)
        return data
    except Exception as e:
        print(f"读取 EEPROM 时出错: 地址 {address}，字节数 {num_bytes}: {e}")
        raise

def data_to_string(data):
    # 将数据转换为 ASCII 字符串
    ascii_string = ''.join(chr(byte) for byte in data)
    return ascii_string

def get_mac_address(interface='eth0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 使用 ioctl 来获取 MAC 地址
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', bytes(interface[:15], 'utf-8')))
    # 将 MAC 地址格式化为人类可读的字符串
    return ':'.join(['%02x' % b for b in info[18:24]])

def generate_token():
    # 随机生成 64 bytes 并进行 base64 编码
    random_bytes = os.urandom(64)
    token = base64.urlsafe_b64encode(random_bytes).decode('utf-8')
    return token

def create_qrcode(data):
    # 生成 QR 码
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
        print(f"使用的 I2C 地址: {DEVICE_ADDRESS}")
        print(f"使用的 I2C 总线: {I2C_BUS}")
        
        # 读取 EEPROM 的前 8 个字节
        data = read_eeprom(0, 8)
        
        # 打印读取到的原始数据
        print(f"从 EEPROM 读取的原始数据: {data}")
        
        # 将数据转换为 ASCII 字符串
        ascii_string = data_to_string(data)
        print("密码:", ascii_string)

    except Exception as e:
        print("错误:", str(e))

    try:
        # 获取 MAC 地址和生成 Token
        mac_address = get_mac_address('eth0')
        print(f"MAC 地址: {mac_address}")
        
        token = generate_token()
        
        # 构造 QR 码 URL
        qrcode_url = f"https://tekpass.com.tw/sso?receiver=fcm://{mac_address}:TPYZU&token={token}"
        print("QR 码 URL:", qrcode_url)
        
        # 生成并显示 QR 码
        img = create_qrcode(qrcode_url)
        '''img.show()'''
        img.save('static/uploads/qrcode.png')  # 保存到指定位置
        # 将 URL 和 token 保存到文件
        with open('token.txt', 'w') as file:
            file.write(f"Token: {token}\n")
        print("URL 和 Token 已保存到 token.txt")

    except Exception as e:
        print("错误:", str(e))

if __name__ == "__main__":
    main()
