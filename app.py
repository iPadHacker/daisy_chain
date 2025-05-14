import http.server
import socketserver
import os
import urllib.parse

# Define the port
PORT = 8000

# Project root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths to templates and static files
TEMPLATES_DIR = os.path.join(ROOT_DIR, "templates")
STATIC_DIR = os.path.join(ROOT_DIR, "static")

# Daisy Chain Password System
class DaisyChainPasswordSystem:
    def __init__(self, seed):
        """
        Initializes the system with a seed value.
        """
        if not (0 <= seed < 2**16):
            raise ValueError("Seed must be a 16-bit integer (0-65535).")
        self.seed = seed
        self.password = self.generate_password()

    def generate_password(self):
        """
        Generates a static 16-bit password based on the seed.
        """
        data = f"{self.seed}-static-password"
        hashed = sum(ord(char) for char in data)  # Simple hash using character sum
        return hashed & 0xFFFF  # Ensure it's 16-bit

    def verify_password(self, provided_password):
        """
        Verifies if the provided password matches the generated password.
        """
        return provided_password == self.password


# Initialize the password system
password_system = DaisyChainPasswordSystem(seed=12345)

# In-memory "database" for users
users = {}


# Custom HTTP request handler
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        """
        Handle GET requests (serve HTML templates or static files).
        """
        if self.path == "/":
            self.serve_file("index.html")
        elif self.path == "/signup":
            self.serve_file("signup.html")
        elif self.path == "/signin":
            self.serve_file("signin.html")
        elif self.path == "/access":
            self.serve_file("access.html")
        else:
            # Serve static files (CSS, JS, etc.)
            super().do_GET()

    def do_POST(self):
        """
        Handle POST requests (form submissions).
        """
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length).decode("utf-8")
        form_data = urllib.parse.parse_qs(post_data)

        if self.path == "/signup":
            self.handle_signup(form_data)
        elif self.path == "/signin":
            self.handle_signin(form_data)
        elif self.path == "/secure":
            self.handle_secure_access(form_data)
        else:
            self.send_error(404, "Not Found")

    def serve_file(self, filename):
        """
        Serve an HTML file from the templates directory.
        """
        file_path = os.path.join(TEMPLATES_DIR, filename)
        if os.path.exists(file_path):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open(file_path, "rb") as file:
                self.wfile.write(file.read())
        else:
            self.send_error(404, "File Not Found")

    def handle_signup(self, form_data):
        """
        Handle the sign-up form submission.
        """
        username = form_data.get("username", [""])[0]
        password = form_data.get("password", [""])[0]
        if username in users:
            self.respond_with_json({"success": False, "message": "Username already exists!"})
        else:
            users[username] = password
            self.respond_with_json({"success": True, "message": "Sign-up successful!"})

    def handle_signin(self, form_data):
        """
        Handle the sign-in form submission.
        """
        username = form_data.get("username", [""])[0]
        password = form_data.get("password", [""])[0]
        if username in users and users[username] == password:
            daisy_password = password_system.password
            self.respond_with_json({"success": True, "daisy_password": daisy_password, "message": "Sign-in successful!"})
        else:
            self.respond_with_json({"success": False, "message": "Invalid username or password!"})

    def handle_secure_access(self, form_data):
        """
        Handle the secure access form submission.
        """
        try:
            entered_password = int(form_data.get("daisy_password", [""])[0])
        except ValueError:
            self.respond_with_json({"success": False, "message": "Invalid password format!"})
            return

        if password_system.verify_password(entered_password):
            professional_codes = {
                "CodeX123": "Access to secure database",
                "AlphaBeta42": "Encryption key for internal systems",
                "GammaDelta99": "API key for cloud access"
            }
            self.respond_with_json({"success": True, "codes": professional_codes})
        else:
            self.respond_with_json({"success": False, "message": "Invalid Daisy Chain Password!"})

    def respond_with_json(self, response_data):
        """
        Send a JSON response to the client.
        """
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(str(response_data).replace("'", '"'), "utf-8"))


# Start the server
with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()