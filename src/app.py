from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from src.resources.login import blp as UserBlueprint
from src.resources.courses_endpoint import blp as CourseBluePrint
from src.resources.mentor_endpoints import blp as MentorBluePrint


def create_app():
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Online Learning System API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config[
        "OPENAPI_SWAGGER_UI_URL"
    ] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "58431264889547771757812184473184401285"
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # user_details = get_item(QUERIES.get("SEARCH_USER_BY_USERNAME"), (identity,))
        return {"user_id": identity[1], "role": identity[0]}

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(CourseBluePrint)
    api.register_blueprint(MentorBluePrint)

    return app
