'''
import firebase_admin
from firebase_admin import credentials, auth, db
import requests

# 从文件 "token.txt" 中读取 mac_address
with open('token.txt', 'r') as file:
    mac_address = file.read().strip()  # 去掉首尾的空格或换行符
print(f"MAC Address received: {mac_address}")

# Firebase configuration and initialization
cred = credentials.Certificate("path/to/serviceAccountKey.json")  # Replace with the path to your Firebase Admin SDK JSON file
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://cmorecard-f8cc0-default-rtdb.firebaseio.com/'
})

# Authenticate with email and password
email = "yzu_ee@tekpass.com.tw"
password = "V@b0nox%W!u8lh%O%!f!2!Z$"
auth_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=AIzaSyDzrGMkK5QYZe7l8CLFZwhfZ6J4avMk7I4"

data = {
    'email': email,
    'password': password,
    'returnSecureToken': True
}

response = requests.post(auth_url, json=data)
if response.status_code == 200:
    user_data = response.json()
    user_id = user_data['localId']
    id_token = user_data['idToken']
    print(f"User ID: {user_id}")

    # Reference the database and retrieve data
    ref_path = f"/sso/{mac_address}:TPYZU"
    ref = db.reference(ref_path)

    # 使用读取的 mac_address
    print(f"Using MAC address: {mac_address}")

    data = ref.get()
    if data:
        # 保存 sso_id 到文件
        sso_id = data.get('sso_id')
        print("sso_id:", sso_id)
        with open('sso_id.txt', 'w') as f:
            f.write(sso_id)

        # 保存 sso_token 到文件
        sso_token = data.get('sso_token')
        print("sso_token:", sso_token)
        with open('sso_token.txt', 'w') as f:
            f.write(sso_token)
    else:
        print('沒有資料')

else:
    print(f"Error: {response.status_code}, Message: {response.text}")
'''
'''
import pyrebase

# Define the variable
mac_address = "some value"

# Firebase 配置
firebaseConfig = {
    "apiKey": "AIzaSyDzrGMkK5QYZe7l8CLFZwhfZ6J4avMk7I4",
    "authDomain": "cmorecard-f8cc0.firebaseapp.com",
    "databaseURL": "https://cmorecard-f8cc0-default-rtdb.firebaseio.com/",
    "projectId": "cmorecard-f8cc0",
    "storageBucket": "cmorecard-f8cc0.appspot.com",
    "messagingSenderId": "485043221890",
    "appId": "1:485043221890:web:7e3d30568f39b7f024cb9b",
    "measurementId": "G-ET19TYZ0P7"
}

# 初始化 Firebase
firebase = pyrebase.initialize_app(firebaseConfig)

# 獲取認證對象
auth = firebase.auth()

# 使用電子郵件和密碼進行登錄
email = "yzu_ee@tekpass.com.tw"
password = "V@b0nox%W!u8lh%O%!f!2!Z$"
user = auth.sign_in_with_email_and_password(email, password)

# 打印登錄成功的用戶信息
print("User ID Token:", user['idToken'])

# 獲取 Firebase Realtime Database 參照
db = firebase.database()

# 打开文件并读取第四行
#with open('mac_address_user.txt', 'r') as file:
    #mac_address = file.read().strip()
#print(f"MAC Address received: {mac_address}")

mac_address = "dc:a6:32:88:96:07"
path = f"/sso/{mac_address}:TPYZU"

# 從 Firebase 讀取數據
sso_data = db.child(path).get(user['idToken']).val()

if sso_data:
    # 保存 sso_id 到文件
    sso_id = sso_data['sso_id']
    with open('sso_id.txt', 'w') as f:
        f.write(sso_id)

    # 保存 sso_token 到文件
    sso_token = sso_data['sso_token']
    with open('sso_token.txt', 'w') as f:
        f.write(sso_token)

    print("SSO data saved successfully.")
else:
    print("No data found.")
'''
import subprocess

file_path = './'

# read token.txt and get the Mac Address
with open(file_path + r'mac_address_user.txt', 'r') as file:
    mac_address = file.read().strip()
    #print(f"add:{mac_address}")

# 使用 subprocess 调用 node 来执行 index.js，并传递参数Mac address
try:
    result = subprocess.run(['node', f'{file_path}index.js', mac_address], capture_output=True, text=True, check=True)
    
    # 输出执行结果
    print("Script output:\n", result.stdout)
    
except subprocess.CalledProcessError as e:
    print(f"Error running script: {e}")
    print(f"Script error output:\n{e.stderr}")