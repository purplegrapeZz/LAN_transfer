# -*- coding: utf-8 -*-
from http.server import SimpleHTTPRequestHandler, HTTPServer
from io import BytesIO
import os
import socket


def get_ips():
	ips = set()

	for info in socket.getaddrinfo(socket.gethostname(), None):
		ip = info[4][0]

		if (
			"." in ip
			# and not ip.startswith("127.")
			# and not ip.startswith("169.254.")
		):ips.add(ip)
	return ips

class UploadHandler(SimpleHTTPRequestHandler):
	def list_directory(self, path):
		self._inject_upload = True
		f = super().list_directory(path)
		self._inject_upload = False
		data = f.read()
		upload_html = b'''
			<h3>Upload</h3>
			<form method="POST" enctype="multipart/form-data">
				<input type="file" name="file">
				<button type="submit">upload</button>
			</form>
			'''
		data = data.replace(b"</body>\n</html>\n", upload_html + b"</body>\n</html>\n")
		return BytesIO(data)

	def send_header(self, keyword, value):
		if getattr(self, "_inject_upload", False) and keyword.lower() == "content-length":
			return
		return super().send_header(keyword, value)

	def do_POST(self):
		length = int(self.headers["Content-Length"])
		content_type = self.headers.get("Content-Type", "")
		if "boundary=" not in content_type:
			self.send_error(400, "Bad request")
			return
		boundary = content_type.split("boundary=")[1].encode()
		body = self.rfile.read(length)
		save_dir = self.translate_path(self.path)
		if not os.path.isdir(save_dir):
			save_dir = os.path.dirname(save_dir)
		for part in body.split(b"--" + boundary):
			if b'filename="' not in part:
				continue
			header, file_data = part.split(b"\r\n\r\n", 1)
			filename = header.split(b'filename="')[1].split(b'"')[0]
			filename = os.path.basename(filename.decode(errors="ignore"))
			if not filename:
				continue
			file_data = file_data.rsplit(b"\r\n", 1)[0]
			save_path = os.path.join(save_dir, filename)
			with open(save_path, "wb") as f:
				f.write(file_data)
			print("Upload:", save_path)
		self.send_response(303)
		self.send_header("Location", self.path)
		self.end_headers()


port = 5000
ips = get_ips()
# print(ips)

print('--------------------------------------------------------------------')
print('Open the following address in browser by any device in LAN:')
print(f' * Running on http://127.0.0.1:{port}')
for i in ips:
	print(f' * Running on http://{i}:{port}')
print('--------------------------------------------------------------------')
server = HTTPServer(("0.0.0.0", port), UploadHandler)
server.serve_forever()
