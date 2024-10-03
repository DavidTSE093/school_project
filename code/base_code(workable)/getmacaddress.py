import socket
import fcntl
import struct

def get_mac_address(interface='eth0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 使用 ioctl 来获取 MAC 地址
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', bytes(interface[:15], 'utf-8')))
    # 将 MAC 地址格式化为人类可读的字符串
    return ':'.join(['%02x' % b for b in info[18:24]])

# 调用函数以抓取 eth0 的 MAC 地址
mac_address = get_mac_address('eth0')
print(mac_address)
