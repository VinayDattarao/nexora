import os

from flask import Flask
from dotenv import load_dotenv
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()


def create_app():

    app = Flask(__name__)

    # Trust Render reverse proxy headers for correct https scheme and host
    app.wsgi_app = ProxyFix(
        app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
    )

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    app.config["SUPABASE_URL"] = os.getenv("SUPABASE_URL")

    app.config["SUPABASE_ANON_KEY"] = os.getenv(
        "SUPABASE_ANON_KEY"
    )


    from app.routes.auth import auth_bp
    from app.routes.main import main
    
    app.register_blueprint(main)
    app.register_blueprint(auth_bp)
    

    return app


# Default instance for WSGI servers (so both `gunicorn app:app` and `gunicorn run:app` work)
app = create_app()