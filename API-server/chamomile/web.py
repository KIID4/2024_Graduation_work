from flask import Flask, send_file
from flask_restful import Resource, Api
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
api = Api(app)


class Images(Resource):
    def get(self, filename):
        try:
            return send_file(
                os.getenv("IMAGE_DIR") + f"/{filename}.jpg", mimetype="image/png"
            )
        except Exception as e:
            return str(e)


api.add_resource(Images, "/images/<string:filename>")

if __name__ == "__main__":
    app.run()
