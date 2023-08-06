import datetime
import os

import jwt
from fittrackee import appLog, bcrypt, db
from fittrackee.tasks import reset_password_email
from flask import Blueprint, current_app, jsonify, request
from sqlalchemy import exc, or_
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from ..activities.utils_files import get_absolute_file_path
from .models import User
from .utils import (
    authenticate,
    check_passwords,
    display_readable_file_size,
    get_readable_duration,
    register_controls,
    verify_extension_and_size,
)
from .utils_token import decode_user_token

auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    """
    register a user

    **Example request**:

    .. sourcecode:: http

      POST /api/auth/register HTTP/1.1
      Content-Type: application/json

    **Example responses**:

    - successful registration

    .. sourcecode:: http

      HTTP/1.1 201 CREATED
      Content-Type: application/json

      {
        "auth_token": "JSON Web Token",
        "message": "Successfully registered.",
        "status": "success"
      }

    - error on registration

    .. sourcecode:: http

      HTTP/1.1 400 BAD REQUEST
      Content-Type: application/json

      {
        "message": "Errors: Valid email must be provided.\\n",
        "status": "error"
      }

    :<json string username: user name (3 to 12 characters required)
    :<json string email: user email
    :<json string password: password (8 characters required)
    :<json string password_conf: password confirmation

    :statuscode 201: Successfully registered.
    :statuscode 400:
        - Invalid payload.
        - Sorry. That user already exists.
        - Errors:
            - 3 to 12 characters required for usernanme.
            - Valid email must be provided.
            - Password and password confirmation don't match.
            - 8 characters required for password.
    :statuscode 403:
        Error. Registration is disabled.
    :statuscode 500:
        Error. Please try again or contact the administrator.

    """
    if not current_app.config.get('is_registration_enabled'):
        response_object = {
            'status': 'error',
            'message': 'Error. Registration is disabled.',
        }
        return jsonify(response_object), 403
    # get post data
    post_data = request.get_json()
    if (
        not post_data
        or post_data.get('username') is None
        or post_data.get('email') is None
        or post_data.get('password') is None
        or post_data.get('password_conf') is None
    ):
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400
    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    password_conf = post_data.get('password_conf')

    try:
        ret = register_controls(username, email, password, password_conf)
    except TypeError as e:
        db.session.rollback()
        appLog.error(e)

        response_object = {
            'status': 'error',
            'message': 'Error. Please try again or contact the administrator.',
        }
        return jsonify(response_object), 500
    if ret != '':
        response_object = {'status': 'error', 'message': ret}
        return jsonify(response_object), 400

    try:
        # check for existing user
        user = User.query.filter(
            or_(User.username == username, User.email == email)
        ).first()
        if not user:
            # add new user to db
            new_user = User(username=username, email=email, password=password)
            new_user.timezone = 'Europe/Paris'
            db.session.add(new_user)
            db.session.commit()
            # generate auth token
            auth_token = new_user.encode_auth_token(new_user.id)
            response_object = {
                'status': 'success',
                'message': 'Successfully registered.',
                'auth_token': auth_token,
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'error',
                'message': 'Sorry. That user already exists.',
            }
            return jsonify(response_object), 400
    # handler errors
    except (exc.IntegrityError, exc.OperationalError, ValueError) as e:
        db.session.rollback()
        appLog.error(e)

        response_object = {
            'status': 'error',
            'message': 'Error. Please try again or contact the administrator.',
        }
        return jsonify(response_object), 500


@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    """
    user login

    **Example request**:

    .. sourcecode:: http

      POST /api/auth/login HTTP/1.1
      Content-Type: application/json

    **Example responses**:

    - successful login

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "auth_token": "JSON Web Token",
        "message": "Successfully logged in.",
        "status": "success"
      }

    - error on login

    .. sourcecode:: http

      HTTP/1.1 404 NOT FOUND
      Content-Type: application/json

      {
        "message": "Invalid credentials.",
        "status": "error"
      }

    :<json string email: user email
    :<json string password_conf: password confirmation

    :statuscode 200: Successfully logged in.
    :statuscode 404: Invalid credentials.
    :statuscode 500: Error. Please try again or contact the administrator.

    """
    # get post data
    post_data = request.get_json()
    if not post_data:
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        # check for existing user
        user = User.query.filter(User.email == email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            # generate auth token
            auth_token = user.encode_auth_token(user.id)
            response_object = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'auth_token': auth_token,
            }
            return jsonify(response_object), 200
        else:
            response_object = {
                'status': 'error',
                'message': 'Invalid credentials.',
            }
            return jsonify(response_object), 404
    # handler errors
    except (exc.IntegrityError, exc.OperationalError, ValueError) as e:
        db.session.rollback()
        appLog.error(e)
        response_object = {
            'status': 'error',
            'message': 'Error. Please try again or contact the administrator.',
        }
        return jsonify(response_object), 500


@auth_blueprint.route('/auth/logout', methods=['GET'])
@authenticate
def logout_user(auth_user_id):
    """
    user logout

    **Example request**:

    .. sourcecode:: http

      GET /api/auth/logout HTTP/1.1
      Content-Type: application/json

    **Example responses**:

    - successful logout

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "message": "Successfully logged out.",
        "status": "success"
      }

    - error on login

    .. sourcecode:: http

      HTTP/1.1 401 UNAUTHORIZED
      Content-Type: application/json

      {
        "message": "Provide a valid auth token.",
        "status": "error"
      }

    :reqheader Authorization: OAuth 2.0 Bearer Token

    :statuscode 200: Successfully logged out.
    :statuscode 401: Provide a valid auth token.

    """
    # get auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
        resp = User.decode_auth_token(auth_token)
        if not isinstance(auth_user_id, str):
            response_object = {
                'status': 'success',
                'message': 'Successfully logged out.',
            }
            return jsonify(response_object), 200
        else:
            response_object = {'status': 'error', 'message': resp}
            return jsonify(response_object), 401
    else:
        response_object = {
            'status': 'error',
            'message': 'Provide a valid auth token.',
        }
        return jsonify(response_object), 401


@auth_blueprint.route('/auth/profile', methods=['GET'])
@authenticate
def get_authenticated_user_profile(auth_user_id):
    """
    get authenticated user info

    **Example request**:

    .. sourcecode:: http

      GET /api/auth/profile HTTP/1.1
      Content-Type: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "data": {
          "admin": false,
          "bio": null,
          "birth_date": null,
          "created_at": "Sun, 14 Jul 2019 14:09:58 GMT",
          "email": "sam@example.com",
          "first_name": null,
          "language": "en",
          "last_name": null,
          "location": null,
          "nb_activities": 6,
          "nb_sports": 3,
          "picture": false,
          "sports_list": [
              1,
              4,
              6
          ],
          "timezone": "Europe/Paris",
          "total_distance": 67.895,
          "total_duration": "6:50:27",
          "username": "sam",
          "weekm": false
        },
        "status": "success"
      }

    :reqheader Authorization: OAuth 2.0 Bearer Token

    :statuscode 200: success.
    :statuscode 401:
        - Provide a valid auth token.
        - Signature expired. Please log in again.
        - Invalid token. Please log in again.

    """
    user = User.query.filter_by(id=auth_user_id).first()
    response_object = {'status': 'success', 'data': user.serialize()}
    return jsonify(response_object), 200


@auth_blueprint.route('/auth/profile/edit', methods=['POST'])
@authenticate
def edit_user(auth_user_id):
    """
    edit authenticated user

    **Example request**:

    .. sourcecode:: http

      POST /api/auth/profile/edit HTTP/1.1
      Content-Type: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "data": {
          "admin": false,
          "bio": null,
          "birth_date": null,
          "created_at": "Sun, 14 Jul 2019 14:09:58 GMT",
          "email": "sam@example.com",
          "first_name": null,
          "language": "en",
          "last_name": null,
          "location": null,
          "nb_activities": 6,
          "nb_sports": 3,
          "picture": false,
          "sports_list": [
              1,
              4,
              6
          ],
          "timezone": "Europe/Paris",
          "total_distance": 67.895,
          "total_duration": "6:50:27",
          "username": "sam"
          "weekm": true,
        },
        "message": "User profile updated.",
        "status": "success"
      }

    :<json string first_name: user first name
    :<json string last_name: user last name
    :<json string location: user location
    :<json string bio: user biography
    :<json string birth_date: user birth date (format: ``%Y-%m-%d``)
    :<json string password: user password
    :<json string password_conf: user password confirmation
    :<json string timezone: user time zone
    :<json string weekm: does week start on Monday?
    :<json string language: language preferences

    :reqheader Authorization: OAuth 2.0 Bearer Token

    :statuscode 200: User profile updated.
    :statuscode 400:
        - Invalid payload.
        - Password and password confirmation don't match.
    :statuscode 401:
        - Provide a valid auth token.
        - Signature expired. Please log in again.
        - Invalid token. Please log in again.
    :statuscode 500: Error. Please try again or contact the administrator.

    """
    # get post data
    post_data = request.get_json()
    user_mandatory_data = {
        'first_name',
        'last_name',
        'bio',
        'birth_date',
        'language',
        'location',
        'timezone',
        'weekm',
    }
    if not post_data or not post_data.keys() >= user_mandatory_data:
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400
    first_name = post_data.get('first_name')
    last_name = post_data.get('last_name')
    bio = post_data.get('bio')
    birth_date = post_data.get('birth_date')
    language = post_data.get('language')
    location = post_data.get('location')
    password = post_data.get('password')
    password_conf = post_data.get('password_conf')
    timezone = post_data.get('timezone')
    weekm = post_data.get('weekm')

    if password is not None and password != '':
        message = check_passwords(password, password_conf)
        if message != '':
            response_object = {'status': 'error', 'message': message}
            return jsonify(response_object), 400
        password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()

    try:
        user = User.query.filter_by(id=auth_user_id).first()
        user.first_name = first_name
        user.last_name = last_name
        user.bio = bio
        user.language = language
        user.location = location
        user.birth_date = (
            datetime.datetime.strptime(birth_date, '%Y-%m-%d')
            if birth_date
            else None
        )
        if password is not None and password != '':
            user.password = password
        user.timezone = timezone
        user.weekm = weekm
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'User profile updated.',
            'data': user.serialize(),
        }
        return jsonify(response_object), 200

    # handler errors
    except (exc.IntegrityError, exc.OperationalError, ValueError) as e:
        db.session.rollback()
        appLog.error(e)
        response_object = {
            'status': 'error',
            'message': 'Error. Please try again or contact the administrator.',
        }
        return jsonify(response_object), 500


@auth_blueprint.route('/auth/picture', methods=['POST'])
@authenticate
def edit_picture(auth_user_id):
    """
    update authenticated user picture

    **Example request**:

    .. sourcecode:: http

      POST /api/auth/picture HTTP/1.1
      Content-Type: multipart/form-data

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "message": "User picture updated.",
        "status": "success"
      }

    :form file: image file (allowed extensions: .jpg, .png, .gif)

    :reqheader Authorization: OAuth 2.0 Bearer Token

    :statuscode 200: User picture updated.
    :statuscode 400:
        - Invalid payload.
        - No file part.
        - No selected file.
        - File extension not allowed.
    :statuscode 401:
        - Provide a valid auth token.
        - Signature expired. Please log in again.
        - Invalid token. Please log in again.
    :statuscode 413: Error during picture update: file size exceeds 1.0MB.
    :statuscode 500: Error during picture update.

    """
    try:
        response_object, response_code = verify_extension_and_size(
            'picture', request
        )
    except RequestEntityTooLarge as e:
        appLog.error(e)
        max_file_size = current_app.config['MAX_CONTENT_LENGTH']
        response_object = {
            'status': 'fail',
            'message': 'Error during picture update, file size exceeds '
            f'{display_readable_file_size(max_file_size)}.',
        }
        return jsonify(response_object), 413
    if response_object['status'] != 'success':
        return jsonify(response_object), response_code

    file = request.files['file']
    filename = secure_filename(file.filename)
    dirpath = os.path.join(
        current_app.config['UPLOAD_FOLDER'], 'pictures', str(auth_user_id)
    )
    if not os.path.exists(dirpath):
        os.makedirs(dirpath)
    absolute_picture_path = os.path.join(dirpath, filename)
    relative_picture_path = os.path.join(
        'pictures', str(auth_user_id), filename
    )

    try:
        user = User.query.filter_by(id=auth_user_id).first()
        if user.picture is not None:
            old_picture_path = get_absolute_file_path(user.picture)
            if os.path.isfile(get_absolute_file_path(old_picture_path)):
                os.remove(old_picture_path)
        file.save(absolute_picture_path)
        user.picture = relative_picture_path
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'User picture updated.',
        }
        return jsonify(response_object), 200

    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        appLog.error(e)
        response_object = {
            'status': 'fail',
            'message': 'Error during picture update.',
        }
        return jsonify(response_object), 500


@auth_blueprint.route('/auth/picture', methods=['DELETE'])
@authenticate
def del_picture(auth_user_id):
    """
    delete authenticated user picture

    **Example request**:

    .. sourcecode:: http

      DELETE /api/auth/picture HTTP/1.1
      Content-Type: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 204 NO CONTENT
      Content-Type: application/json

    :reqheader Authorization: OAuth 2.0 Bearer Token

    :statuscode 204: picture deleted
    :statuscode 401:
        - Provide a valid auth token.
        - Signature expired. Please log in again.
        - Invalid token. Please log in again.
    :statuscode 500: Error during picture deletion.

    """
    try:
        user = User.query.filter_by(id=auth_user_id).first()
        picture_path = get_absolute_file_path(user.picture)
        if os.path.isfile(picture_path):
            os.remove(picture_path)
        user.picture = None
        db.session.commit()

        response_object = {'status': 'no content'}
        return jsonify(response_object), 204

    except (exc.IntegrityError, ValueError) as e:
        db.session.rollback()
        appLog.error(e)
        response_object = {
            'status': 'fail',
            'message': 'Error during picture deletion.',
        }
        return jsonify(response_object), 500


@auth_blueprint.route('/auth/password/reset-request', methods=['POST'])
def request_password_reset():
    """
    handle password reset request

    **Example request**:

    .. sourcecode:: http

      POST /api/auth/password/reset-request HTTP/1.1
      Content-Type: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "message": "Password reset request processed.",
        "status": "success"
      }

    :<json string email: user email

    :statuscode 200: Password reset request processed.
    :statuscode 400: Invalid payload.

    """
    post_data = request.get_json()
    if not post_data or post_data.get('email') is None:
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400
    email = post_data.get('email')

    user = User.query.filter(User.email == email).first()
    if user:
        password_reset_token = user.encode_password_reset_token(user.id)
        ui_url = current_app.config['UI_URL']
        email_data = {
            'expiration_delay': get_readable_duration(
                current_app.config.get('PASSWORD_TOKEN_EXPIRATION_SECONDS'),
                'en' if user.language is None else user.language,
            ),
            'username': user.username,
            'password_reset_url': (
                f'{ui_url}/password-reset?token={password_reset_token}'  # noqa
            ),
            'operating_system': request.user_agent.platform,
            'browser_name': request.user_agent.browser,
        }
        user_data = {
            'language': user.language if user.language else 'en',
            'email': user.email,
        }
        reset_password_email.send(user_data, email_data)
    response_object = {
        'status': 'success',
        'message': 'Password reset request processed.',
    }
    return jsonify(response_object), 200


@auth_blueprint.route('/auth/password/update', methods=['POST'])
def update_password():
    """
    update user password

    **Example request**:

    .. sourcecode:: http

      POST /api/auth/password/update HTTP/1.1
      Content-Type: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "message": "Password updated.",
        "status": "success"
      }

    :<json string password: password (8 characters required)
    :<json string password_conf: password confirmation
    :<json string token: password reset token

    :statuscode 200: Password updated.
    :statuscode 400: Invalid payload.
    :statuscode 401: Invalid token.
    :statuscode 500: Error. Please try again or contact the administrator.

    """
    post_data = request.get_json()
    if (
        not post_data
        or post_data.get('password') is None
        or post_data.get('password_conf') is None
        or post_data.get('token') is None
    ):
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400
    password = post_data.get('password')
    password_conf = post_data.get('password_conf')
    token = post_data.get('token')

    invalid_token_response_object = {
        'status': 'error',
        'message': 'Invalid token. Please request a new token.',
    }
    try:
        user_id = decode_user_token(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return jsonify(invalid_token_response_object), 401

    message = check_passwords(password, password_conf)
    if message != '':
        response_object = {'status': 'error', 'message': message}
        return jsonify(response_object), 400

    user = User.query.filter(User.id == user_id).first()
    if not user:
        return jsonify(invalid_token_response_object), 401
    try:
        user.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Password updated.',
        }
        return jsonify(response_object), 200

    except (exc.OperationalError, ValueError) as e:
        db.session.rollback()
        appLog.error(e)
        response_object = {
            'status': 'error',
            'message': 'Error. Please try again or contact the administrator.',
        }
        return jsonify(response_object), 500
