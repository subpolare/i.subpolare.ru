import bjoern, os

from app import app 

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "5000"))

if __name__ == "__main__":
    bjoern.run(app, HOST, PORT)