import json
import base64
import subprocess
import binascii
from Crypto.Cipher import AES

def urlsafe_b64decode_nopad(data):
    padding = 4 - (len(data) % 4)
    data = data + ("=" * padding)
    return base64.urlsafe_b64decode(data)

def decrypt(ciphertext, key, iv, mode):
    encobj = AES.new(key, mode, iv)
    return encobj.decrypt(ciphertext)

# 读取 test-account.json 文件
with open('/home/a70640/rpi3/test-account.json', 'r') as file:
    account_data = json.load(file)

server_id = account_data['id']
server_xlh = account_data['xlh']
server_pin = account_data['pin']

# 假设在 index.js 运行时，sso_id 和 sso_token 已经保存到了文件中
# 读取 sso_id 和 sso_token
with open('/home/a70640/rpi3/sso_id.txt', 'r') as file:
    sso_id_base64url = file.read().strip()

with open('/home/a70640/rpi3/sso_token.txt', 'r') as file:
    sso_token = file.read().strip()

# 读取和解析 token 用作解密密钥和 IV
with open('/home/a70640/rpi3/token.txt', 'r') as file:
    token_lines = file.readlines()
    for line in token_lines:
        if "Token: " in line:
            parmas_token = urlsafe_b64decode_nopad(line.split("Token: ")[1].strip())

# 解密 sso_id 以获取 user_id
key = parmas_token[:32]  # token 前 32bytes 当 key
iv = parmas_token[32:48]  # token 接续 16bytes 当 iv

sso_id = urlsafe_b64decode_nopad(sso_id_base64url)
user_id_bytes = decrypt(sso_id, key, iv, AES.MODE_GCM)
user_id = user_id_bytes[:27].decode('utf-8')  # 使用解密出的前 27 bytes 作为 user_id

# 现在有了 user_id 和 sso_token（作为 user_token）
user_token = sso_token

# 打印解密信息（可选）
print(f"user_id: {user_id}")
print(f"user_token: {user_token}")

# 组合命令并执行
command = [
    "/home/a70640/rpi3/sso-backend-arm64",
    server_id,
    server_xlh,
    server_pin,
    user_id,
    user_token
]

# 执行命令
subprocess.run(command)
