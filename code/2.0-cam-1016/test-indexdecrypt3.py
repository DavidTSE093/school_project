import os
import socket
import fcntl
import struct
import json
import base64
import subprocess
import binascii
from Crypto.Cipher import AES
import time #for count 10 seconds
import importlib.util #for id,xlh,pin
import threading
from flask import Flask, Response
import uuid
import socket
import cv2

'''---------------------------------------------------------------------------------------'''

app = Flask(__name__)

# 全局變量，用來控制視訊鏡頭狀態
is_camera_active = False


# 取得視訊鏡頭畫面的函數
def get_camera_feed():
    global is_camera_active
    cap = cv2.VideoCapture(0)  # 開啟相機 (0 是第一個相機)
    
    while is_camera_active:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 將畫面編碼成JPEG
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # 將影像串流傳遞給客戶端
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    cap.release()

# Flask路由，提供串流畫面
@app.route('/video_feed')
def video_feed():
    return Response(get_camera_feed(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 啟動相機的function
def activate_camera():
    global is_camera_active
    is_camera_active = True
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)).start()

# 驗證成功後呼叫此函數
def on_auth_success():
    print("驗證成功，啟用視訊鏡頭")
    IP1 = get_ip_address()
    print('Please connect to : http://' + IP1 +':5000/video_feed')
    activate_camera()

'''---------------------------------------------------------------------------------------'''


def get_mac_address(interface='eth0'):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 使用 ioctl 来获取 MAC 地址
    info = fcntl.ioctl(s.fileno(), 0x8927, struct.pack('256s', bytes(interface[:15], 'utf-8')))
    # 将 MAC 地址格式化为人类可读的字符串
    return ':'.join(['%02x' % b for b in info[18:24]])

mac_address = get_mac_address()
print(f"MAC Address: {mac_address}")

os.system(f'node test-index.js {mac_address}')

def get_ip_address():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))  # Google Public DNS
        ip_address = sock.getsockname()[0]
    finally:
        sock.close()
    return ip_address

# URL-safe Base64 解碼
def urlsafe_b64decode_nopad(data):
    padding = 4 - (len(data) % 4)
    data = data + ("=" * padding)
    return base64.urlsafe_b64decode(data)

# AES 解密函數
def decrypt(ciphertext, key, iv, mode):
    encobj = AES.new(key, mode, iv)
    return encobj.decrypt(ciphertext)


def execute_and_check():
    # 載入 test-eepromuser2.py 並讀取變量
    file_path = 'test-eepromuser2.py'
    spec = importlib.util.spec_from_file_location("test_eepromuser2", file_path)
    test_eepromuser2 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(test_eepromuser2)

    # 從載入的腳本中讀取變量
    server_id = test_eepromuser2.id
    server_xlh = test_eepromuser2.xlh
    server_pin = test_eepromuser2.pin


    # 讀取 sso_id 和 sso_token
    with open('sso_id.txt', 'r') as file:
        sso_id_base64url = file.read().strip()

    with open('sso_token.txt', 'r') as file:
        sso_token = file.read().strip()

    # 讀取和解析 token 用作解密密鑰和 IV
    with open('token.txt', 'r') as file:
        token_lines = file.readlines()
        for line in token_lines:
            if "Token: " in line:
                parmas_token = urlsafe_b64decode_nopad(line.split("Token: ")[1].strip())

    # 解密 sso_id 以獲取 user_id
    key = parmas_token[:32]  # token 前 32bytes 當 key
    iv = parmas_token[32:48]  # token 接續 16bytes 當 iv

    sso_id = urlsafe_b64decode_nopad(sso_id_base64url)
    user_id_bytes = decrypt(sso_id, key, iv, AES.MODE_GCM)
    user_id = user_id_bytes[:27].decode('utf-8')  # 使用解密出的前 27 bytes 作為 user_id

    # 現在有了 user_id 和 sso_token（作為 user_token）
    user_token = sso_token

    # 組合命令並執行
    command = [
        "/home/abc/Desktop/raspi-base/sso-backend-arm64",
        server_id,
        server_xlh,
        server_pin,
        user_id,
        user_token
    ]

    # 執行命令並獲取輸出
    result = subprocess.run(command, capture_output=True, text=True)
    
    # 解析輸出 (假設輸出為 JSON 格式)
    try:
        output = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": "Invalid output format"}

    return output


def main():
    for attempt in range(6):
        start_time = time.time()  # 記錄開始時間
        result = execute_and_check()

        if result.get("result") == True:
            print('{"result": true},"驗證成功"')
            on_auth_success()
            return True
        elif "error" in result and result["error"]:  # 確認 "error" 中有值
            print(f"嘗試第 {attempt + 1} 次失敗，錯誤訊息: {result['error']}")
            
        elif result.get("result") == False:
            print(f"嘗試第 {attempt + 1} 次失敗，result 為 false")
            
        elapsed_time = time.time() - start_time  # 計算執行時間
        if elapsed_time > 10:  # 檢查是否超過10秒
            print(f"超時，嘗試第 {attempt + 1} 次失敗")
            
    print('{"result": false}, "請重新驗證"')
    return False
'''
執行最多六次操作：這個函式會透過 for 迴圈最多執行六次操作。
在每次迴圈中，它都會呼叫一個名為 execute_and_check() 的函式，該函式會執行一些處理並返回一個結果 result。
檢查 result 的結果：
檢查 result 為 True：表示驗證成功，程式會輸出「驗證成功」並返回 True，然後跳出迴圈。

檢查是否有錯誤：
"error" in result：確保 result 裡確實包含 error 這個欄位。
result["error"]：確認 error 欄位中有具體的錯誤訊息。 error 中有值且不是空字串、None 或其他空的狀態。

檢查 result 為 False：會輸出嘗試失敗的訊息，並在第六次嘗試後同樣要求重新驗證並返回 False。
'''

# 執行主程式
if __name__ == "__main__":
    main()


