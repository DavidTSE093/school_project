
import os
import json
import base64
import subprocess
from Crypto.Cipher import AES

file_path = r'D:\\USER\\desktop\\school-project\\raw_code'

def urlsafe_b64decode_nopad(data):
    padding_needed = 4 - (len(data) % 4)
    if padding_needed != 4:
        data += "=" * padding_needed
    return base64.urlsafe_b64decode(data)

def decrypt(ciphertext, key, iv, mode):
    encobj = AES.new(key, mode, nonce=iv)
    return encobj.decrypt(ciphertext)

# 读取 test-account.json 文件
with open(file_path + r'\\test-account.json', 'r') as file:
    account_data = json.load(file)

server_id = account_data['id']
server_xlh = account_data['xlh']
server_pin = account_data['pin']

# 读取 sso_id 和 sso_token
with open(file_path + r'txt_data\\sso_id.txt', 'r') as file:
    sso_id_base64url = file.read().strip()

with open(file_path + r'txt_data\\sso_token.txt', 'r') as file:
    sso_token = file.read().strip()

# 读取和解析 token 用作解密密钥和 IV
with open(file_path + r'txt_data\\token_user.txt', 'r') as file:
    Token_txt = file.read().strip()
    params_token = urlsafe_b64decode_nopad(Token_txt)
    #token_lines = file.readlines()
    #for line in token_lines:
    #    if "Token: " in line:
    #        params_token = urlsafe_b64decode_nopad(line.split("Token: ")[1].strip())
    #        break  # 找到后跳出循环
    
        
#print("!" + str(params_token) + "!")
# 检查 token 长度
if len(params_token) < 48:
    raise ValueError("Token is too short. Ensure the token is at least 48 bytes long.")

# 解密 sso_id 以获取 user_id
key = params_token[:32]  # token 前 32 bytes 当 key
iv = params_token[32:48]  # token 接续 16 bytes 当 iv (nonce)

sso_id = urlsafe_b64decode_nopad(sso_id_base64url)
user_id_bytes = decrypt(sso_id, key, iv, AES.MODE_GCM)

# 打印解密出来的原始字节数据
print(f"user_id_bytes (raw): {user_id_bytes}")

# 解码处理
user_id_hex = user_id_bytes[:27].hex()
print(f"user_id (hex): {user_id_hex}")

# 现在有了 user_id 和 sso_token（作为 user_token）
user_token = sso_token

# 打印解密信息（可选）
print(f"user_token: {user_token}")

# 组合命令并执行
command = [
    os.path.join(file_path, "sso-backend-arm64"),
    server_id,
    server_xlh,
    server_pin,
    user_id_hex,  # 使用hex格式传递
    user_token
]

# 打印命令以供调试
print(f"Executing command: {command}")

# 确保文件存在
if os.path.exists(command[0]):
    # 执行命令
    subprocess.run(command)
else:
    print(f"Executable not found: {command[0]}")
'''
import json
import base64
import os

import binascii

from Crypto.Cipher import AES


def urlsafe_b64encode_nopad(data):
    return base64.urlsafe_b64encode(data).rstrip(b'=')

def urlsafe_b64decode_nopad(data):
    padding = 4 - (len(data) % 4)
    data = data + ("=" * padding)
    return base64.urlsafe_b64decode(data)

# AES-GCM 不需驗證 auth-tag
def decrypt(ciphertext,key,iv,mode):
  encobj = AES.new(key,  mode, iv)
  return (encobj.decrypt(ciphertext))


# QRCode 內網址的參數 token
parmas_token = bytearray([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64])
print("token",len(parmas_token))

_key = parmas_token[:32] # token 前 32bytes 當 key
print("key length",len(_key))
print_key = binascii.hexlify(bytearray(_key))
print("The hex string after conversion : " + str(print_key))
_iv = parmas_token[32:48] # token 接續 16bytes 當 iv
print("iv length",len(_iv))
print_iv = binascii.hexlify(bytearray(_iv))
print("The hex string after conversion : " + str(print_iv))


# FCM 取得的 sso_id
#sso_id = urlsafe_b64decode_nopad('VOEn0r3Cnw1G0gm9gZ-XL56E0BrWEYP2ZL8Z9yOEcnl2f2C3GQYrlGAFRA')
sso_id = urlsafe_b64decode_nopad('IjcpdaDjzK7OH5MESoqKCuwPn549AUH9kEUsND1Nw9mEU5ertVHSWgcvHQ')
print_enc = binascii.hexlify(bytearray(sso_id))
print("The hex string after conversion : " + str(print_enc))

# AES-GCM 解密
raw = decrypt(sso_id, _key, _iv, AES.MODE_GCM)

print_raw = binascii.hexlify(bytearray(raw))
print("The hex string after conversion : " + str(print_raw))
# 取前 27 bytes 為 apex-id
#print (raw[:27].decode('utf-8'))
print(raw[:27].hex())
'''
#解密測試