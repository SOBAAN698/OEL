from app import app
import os

if __name__ == "__main__":
    # Bind to 0.0.0.0 to allow access inside Docker container
    host = os.environ.get("FLASK_HOST", "0.0.0.0")
    port = int(os.environ.get("FLASK_PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "True").lower() == "true"
    
    app.run(host=host, port=port, debug=debug)
