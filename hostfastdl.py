from flask import Flask, send_from_directory, render_template_string
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import multiprocessing
import socket
import os

app = Flask(__name__)

# Get local IP more reliably
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # This doesn't actually create a connection
        s.connect(('10.255.255.255', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

local_ip = get_local_ip()

# Create a secure authorizer that only allows downloads
authorizer = DummyAuthorizer()
authorizer.add_anonymous(os.getcwd(), perm='elr')  # Only allow download permissions

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
        <li><a href="{{url_for('serve_files', path=path + '/' + file)}}">{{file}}</a></li>
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
        
        if os.path.isdir(requested_path):
            files = sorted(os.listdir(requested_path))
            return render_template_string(
                DIRECTORY_TEMPLATE,
                path=requested_path,
                files=files
            )
        else:
            # Set correct MIME type for bzip2 files (common in Source downloads)
            mimetype = None
            if path.endswith('.bz2'):
                mimetype = 'application/x-bzip2'
                
            return send_from_directory(
                '.',
                requested_path,
                mimetype=mimetype
            )
    except Exception as e:
        return f"Error: {str(e)}", 404

def start_ftp_server():
    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = "Source Engine FastDL FTP Server"
    
    server = FTPServer(('0.0.0.0', 21), handler)
    server.serve_forever()

if __name__ == '__main__':
    # Start FTP server in separate process
    ftp_server_process = multiprocessing.Process(target=start_ftp_server)
    ftp_server_process.start()
    
    # Start HTTP server
    app.run(host='0.0.0.0', port=5000, debug=False)
