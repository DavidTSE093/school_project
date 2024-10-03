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

if __name__ == "__main__":
    main()
