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
#with open( 'txt_data\\' + 'mac_address_user.txt', 'r') as file:
    #mac_address = file.read().strip()
#print(f"MAC Address received: {mac_address}")

mac_address = "dc:a6:32:88:96:07"
path = f"/sso/{mac_address}:TPYZU"

# 從 Firebase 讀取數據
sso_data = db.child(path).get(user['idToken']).val()

if sso_data:
    # 保存 sso_id 到文件
    sso_id = sso_data['sso_id']
    with open( 'txt_data\\' + 'sso_id.txt', 'w') as f:
        f.write(sso_id)

    # 保存 sso_token 到文件
    sso_token = sso_data['sso_token']
    with open( 'txt_data\\' + 'sso_token.txt', 'w') as f:
        f.write(sso_token)

    print("SSO data saved successfully.")
else:
    print("No data found.")
#mac_地址目前使用的是固定值，之後要改成讀取檔案的方式，但目前讀檔成功但是無法將值傳入到firebase，可能是沒有資料。