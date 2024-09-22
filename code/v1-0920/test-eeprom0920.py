'''
import time
import qrcode
from PIL import Image
from pyftdi.i2c import I2cController

DEVICE_ADDRESS = 0x50  # EEPROM的I2C地址
I2C_PORT = 'ftdi://ftdi:232h/1'  # 這是 pyftdi 使用的 USB-I2C 接口地址

# 初始化 I2C 控制器
i2c = I2cController()

try:
    # 連接到 I2C 接口
    i2c.configure(I2C_PORT)
    print(f"I2C interface {I2C_PORT} initialized.")
except Exception as e:
    print(f"Error initializing I2C interface: {e}")
    exit(1)

def read_eeprom(address, num_bytes):
    try:
        # 獲取 EEPROM 設備
        slave = i2c.get_port(DEVICE_ADDRESS)
        # 從指定地址讀取數據
        data = slave.read_from(address, num_bytes)
        return data
    except Exception as e:
        print(f"Error reading EEPROM at address {address} with {num_bytes} bytes: {e}")
        raise

def data_to_string(data):
    # 將數據轉換為ASCII字符串
    ascii_string = ''.join(chr(byte) for byte in data)
    return ascii_string

def main():
    try:
        # 打印調試信息
        print(f"Using I2C address: {DEVICE_ADDRESS}")
        
        # 讀取 EEPROM 的前8個字節
        data = read_eeprom(0, 8)
        
        # 打印讀取到的原始數據
        print(f"Raw data read from EEPROM: {data}")
        
        # 將數據轉換為 ASCII 字符串
        ascii_string = data_to_string(data)
        print("Password:", ascii_string)
        
        # 生成並顯示QR碼
        # img = create_qrcode(ascii_string)
        # img.show()

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()
'''
import smbus
import time
import qrcode
from PIL import Image

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

#def create_qrcode(data):
  # 生成QR码
  #   qr = qrcode.QRCode(
  #       version=1,
  #      error_correction=qrcode.constants.ERROR_CORRECT_L,
  #      box_size=10,
  #      border=4,
  #  )
  #  qr.add_data(data)
  #  qr.make(fit=True)  # 修正 fit 调用方法
    
  # img = qr.make_image(fill='black', back_color='white')
  #  return img

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
        
        # 生成并显示QR码
        # img = create_qrcode(ascii_string)
        # img.show()

    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()