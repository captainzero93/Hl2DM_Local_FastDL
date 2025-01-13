from flask import Flask, send_from_directory, render_template_string
import socket
import os

app = Flask(__name__)

# Set the fastdl directory path
FASTDL_DIR = os.path.join(os.getcwd(), 'fastdl')

# Get local IP more reliably
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

local_ip = get_local_ip()

# HTML template for directory listing
DIRECTORY_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>FastDL Directory: {{path}}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .file-list { list-style-type: none; padding: 0; }
        .file-list li { padding: 5px 0; }
        .file-list a { text-decoration: none; color: #0066cc; }
        .file-list a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>FastDL Directory: {{path}}</h1>
    <ul class="file-list">
    {% for file in files %}
        <li><a href="/{{path}}/{{file}}">{{file}}</a></li>
    {% endfor %}
    </ul>
</body>
</html>
'''

@app.route('/')
def home():
    return f"""
    <h1>Source Engine FastDL Server</h1>
    <p>Server IP: {local_ip}</p>
    <p>Add to your server.cfg:</p>
    <pre>
    sv_downloadurl "http://{local_ip}:5000"
    sv_allowdownload 1
    sv_allowupload 1
    </pre>
    """

@app.route('/<path:path>')
def serve_files(path):
    try:
        # Sanitize path to prevent directory traversal
        requested_path = os.path.normpath(path).lstrip('/')
        full_path = os.path.join(FASTDL_DIR, requested_path)
        
        print(f"Requested path: {requested_path}")
        print(f"Full path: {full_path}")
        print(f"File exists: {os.path.exists(full_path)}")
        
        if os.path.isdir(full_path):
            files = sorted(os.listdir(full_path))
            return render_template_string(
                DIRECTORY_TEMPLATE,
                path=requested_path,
                files=files
            )
        else:
            directory = os.path.dirname(full_path)
            filename = os.path.basename(full_path)
            print(f"Serving from directory: {directory}")
            print(f"Filename: {filename}")
            
            # Set correct MIME type for bzip2 files
            mimetype = None
            if path.endswith('.bz2'):
                mimetype = 'application/x-bzip2'
            
            return send_from_directory(
                directory,
                filename,
                mimetype=mimetype
            )
    except Exception as e:
        print(f"Error serving file: {str(e)}")
        return f"Error: {str(e)}", 404

if __name__ == '__main__':
    print(f"Serving files from: {FASTDL_DIR}")
    app.run(host='0.0.0.0', port=5000, debug=True)
