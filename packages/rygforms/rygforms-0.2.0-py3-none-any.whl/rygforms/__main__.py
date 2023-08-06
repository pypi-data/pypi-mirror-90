import flask as f
import authlib.integrations.flask_client
import werkzeug.middleware.proxy_fix
import os
import dotenv

dotenv.find_dotenv(raise_error_if_not_found=True)

app = f.Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

oauth = authlib.integrations.flask_client.OAuth(app=app)
ryg_login = oauth.register(
    name="ryg_login",
    api_base_url=os.getenv("API_BASE_URL"),  # https://ryg.eu.auth0.com
    authorize_url=os.getenv("AUTHORIZE_URL"),  # https://ryg.eu.auth0.com/authorize
    access_token_url=os.getenv("ACCESS_TOKEN_URL"),  # https://ryg.eu.auth0.com/oauth/token
    server_metadata_url=os.getenv("SERVER_METADATA_URL"),  # https://ryg.eu.auth0.com/.well-known/openid-configuration
    client_kwargs={
        "scope": "profile email openid",
    },
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv("CLIENT_SECRET")
)

reverse_proxy_app = werkzeug.middleware.proxy_fix.ProxyFix(app=app, x_for=1, x_proto=0, x_host=1, x_port=0, x_prefix=0)


@app.route("/<string:form_user>/<string:form_id>")
def page_form(form_user: str, form_id: str):
    f.session["form_user"] = form_user
    f.session["form_id"] = form_id
    return ryg_login.authorize_redirect(redirect_uri=f.url_for("page_auth", _external=True), audience="")


@app.route("/authorize")
def page_auth():
    ryg_login.authorize_access_token()
    userdata = ryg_login.get("userinfo").json()
    form_user = f.session["form_user"]
    form_id = f.session["form_id"]
    user_name = userdata["name"]
    user_sub = userdata["sub"]
    return f.redirect(f"https://{form_user}.typeform.com/to/{form_id}#name={user_name}&sub={user_sub}")


if __name__ == "__main__":
    # noinspection PyUnreachableCode
    if __debug__:
        app.run(debug=True, host="127.0.0.1", port=30012)
    else:
        raise Exception("This app shouldn't be run standalone in production mode.")
