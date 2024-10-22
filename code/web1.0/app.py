from flask import Flask, render_template, request, redirect, url_for
import os
import subprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # 上传文件夹
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # 确保上传文件夹存在

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # 执行 Python 脚本
            result = subprocess.run(['python3', 'test-eepromuser2.py'], capture_output=True, text=True)
            print("脚本输出:", result.stdout)  # 打印输出以调试
            print("脚本错误:", result.stderr)   # 打印错误信息

        except Exception as e:
            print("运行脚本时出错:", str(e))

        return redirect(url_for('index'))  # 重定向回主页

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
