# from flask import Flask, request, jsonify
# import subprocess

# app = Flask(__name__)

# @app.route('/generate-video', methods=['POST'])
# def generate_video():
#     try:
#         result = subprocess.run(["python", "generating_video.py"], capture_output=True, text=True)
#         return jsonify({
#             "status": "success",
#             "stdout": result.stdout,
#             "stderr": result.stderr
#         })
#     except Exception as e:
#         return jsonify({"status": "error", "error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)










# from flask import Flask, jsonify
# import subprocess

# app = Flask(__name__)

# @app.route('/generate-video', methods=['POST'])
# def generate_video():
#     try:
#         result = subprocess.run(["python", "/files/generating_video.py"], capture_output=True, text=True)

#         return jsonify({
#             "status": "ok",
#             "stdout": result.stdout,
#             "stderr": result.stderr
#         })

#     except Exception as e:
#         return jsonify({"status": "error", "error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)
























# from flask import Flask, jsonify
# import subprocess
# import threading

# app = Flask(__name__)

# def run_script():
#     subprocess.run(["python", "/files/generating_video.py"], capture_output=False)

# @app.route('/generate-video', methods=['POST'])
# def generate_video():
#     try:
#         threading.Thread(target=run_script).start()
#         return jsonify({"status": "started"}), 202

#     except Exception as e:
#         return jsonify({"status": "error", "error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)




















# from flask import Flask, jsonify
# import subprocess

# app = Flask(__name__)

# @app.route('/generate-video', methods=['POST'])
# def generate_video():
#     try:
#         result = subprocess.run(
#             ["python", "/files/generating_video.py"],
#             capture_output=True,
#             text=True
#         )
#         return jsonify({
#             "status": "completed",
#             "stdout": result.stdout,
#             "stderr": result.stderr
#         })

#     except Exception as e:
#         return jsonify({"status": "error", "error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)






























from flask import Flask, jsonify
import subprocess
import os

app = Flask(__name__)

@app.route('/generate-video', methods=['POST'])
def generate_video():
    try:
        result = subprocess.run(
            ["python", os.path.join(os.getcwd(), "generating_video.py")],
            capture_output=True,
            text=True
        )
        return jsonify({
            "status": "completed",
            "stdout": result.stdout,
            "stderr": result.stderr
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

@app.route('/run-playwright', methods=['POST'])
def run_playwright():
    try:
        result = subprocess.run(
            ["python", os.path.join(os.getcwd(), "playwright_main.py")],
            capture_output=True,
            text=True
        )
        return jsonify({
            "status": "completed",
            "stdout": result.stdout,
            "stderr": result.stderr
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)


