import os
import shutil

from fittrackee import appLog, db
from flask import Blueprint, jsonify, request, send_file
from sqlalchemy import exc

from ..activities.utils_files import get_absolute_file_path
from .models import Activity, User
from .utils import authenticate, authenticate_as_admin

users_blueprint = Blueprint('users', __name__)

USER_PER_PAGE = 10


@users_blueprint.route('/users', methods=['GET'])
@authenticate
def get_users(auth_user_id):
    """
    Get all users

    **Example request**:

    - without parameters

    .. sourcecode:: http

      GET /api/users HTTP/1.1
      Content-Type: application/json

    - with some query parameters

    .. sourcecode:: http

      GET /api/users?order_by=activities_count&par_page=5  HTTP/1.1
      Content-Type: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "data": {
          "users": [
            {
              "admin": true,
              "bio": null,
              "birth_date": null,
              "created_at": "Sun, 14 Jul 2019 14:09:58 GMT",
              "email": "admin@example.com",
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
              "username": "admin"
            },
            {
              "admin": false,
              "bio": null,
              "birth_date": null,
              "created_at": "Sat, 20 Jul 2019 11:27:03 GMT",
              "email": "sam@example.com",
              "first_name": null,
              "language": "fr",
              "last_name": null,
              "location": null,
              "nb_activities": 0,
              "nb_sports": 0,
              "picture": false,
              "sports_list": [],
              "timezone": "Europe/Paris",
              "total_distance": 0,
              "total_duration": "0:00:00",
              "username": "sam"
            }
          ]
        },
        "status": "success"
      }

    :param integer auth_user_id: authenticate user id (from JSON Web Token)

    :query integer page: page if using pagination (default: 1)
    :query integer per_page: number of users per page (default: 10, max: 50)
    :query string q: query on user name
    :query string order_by: sorting criteria (``username``, ``created_at``,
                            ``activities_count``, ``admin``)
    :query string order: sorting order (default: ``asc``)

    :reqheader Authorization: OAuth 2.0 Bearer Token

    :statuscode 200: success
    :statuscode 401:
        - Provide a valid auth token.
        - Signature expired. Please log in again.
        - Invalid token. Please log in again.

    """
    params = request.args.copy()
    page = 1 if 'page' not in params.keys() else int(params.get('page'))
    per_page = (
        int(params.get('per_page'))
        if params.get('per_page')
        else USER_PER_PAGE
    )
    if per_page > 50:
        per_page = 50
    order_by = params.get('order_by')
    order = params.get('order', 'asc')
    query = params.get('q')
    users_pagination = (
        User.query.filter(
            User.username.like('%' + query + '%') if query else True,
        )
        .order_by(
            User.activities_count.asc()
            if order_by == 'activities_count' and order == 'asc'
            else True,
            User.activities_count.desc()
            if order_by == 'activities_count' and order == 'desc'
            else True,
            User.username.asc()
            if order_by == 'username' and order == 'asc'
            else True,
            User.username.desc()
            if order_by == 'username' and order == 'desc'
            else True,
            User.created_at.asc()
            if order_by == 'created_at' and order == 'asc'
            else True,
            User.created_at.desc()
            if order_by == 'created_at' and order == 'desc'
            else True,
            User.admin.asc()
            if order_by == 'admin' and order == 'asc'
            else True,
            User.admin.desc()
            if order_by == 'admin' and order == 'desc'
            else True,
        )
        .paginate(page, per_page, False)
    )
    users = users_pagination.items
    response_object = {
        'status': 'success',
        'data': {'users': [user.serialize() for user in users]},
        'pagination': {
            'has_next': users_pagination.has_next,
            'has_prev': users_pagination.has_prev,
            'page': users_pagination.page,
            'pages': users_pagination.pages,
            'total': users_pagination.total,
        },
    }
    return jsonify(response_object), 200


@users_blueprint.route('/users/<user_name>', methods=['GET'])
@authenticate
def get_single_user(auth_user_id, user_name):
    """
    Get single user details

    **Example request**:

    .. sourcecode:: http

      GET /api/users/admin HTTP/1.1
      Content-Type: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "data": [
          {
            "admin": true,
            "bio": null,
            "birth_date": null,
            "created_at": "Sun, 14 Jul 2019 14:09:58 GMT",
            "email": "admin@example.com",
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
            "username": "admin"
          }
        ],
        "status": "success"
      }

    :param integer auth_user_id: authenticate user id (from JSON Web Token)
    :param integer user_name: user name

    :reqheader Authorization: OAuth 2.0 Bearer Token

    :statuscode 200: success
    :statuscode 401:
        - Provide a valid auth token.
        - Signature expired. Please log in again.
        - Invalid token. Please log in again.
    :statuscode 404:
        - User does not exist.
    """

    response_object = {'status': 'fail', 'message': 'User does not exist.'}
    try:
        user = User.query.filter_by(username=user_name).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {'users': [user.serialize()]},
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@users_blueprint.route('/users/<user_name>/picture', methods=['GET'])
def get_picture(user_name):
    """get user picture

    **Example request**:

    .. sourcecode:: http

      GET /api/users/admin/picture HTTP/1.1
      Content-Type: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: image/jpeg

    :param integer user_name: user name

    :statuscode 200: success
    :statuscode 404:
        - User does not exist.
        - No picture.

    """
    response_object = {'status': 'not found', 'message': 'No picture.'}
    try:
        user = User.query.filter_by(username=user_name).first()
        if not user:
            response_object = {
                'status': 'fail',
                'message': 'User does not exist.',
            }
            return jsonify(response_object), 404
        if user.picture is not None:
            picture_path = get_absolute_file_path(user.picture)
            return send_file(picture_path)
        return jsonify(response_object), 404
    except Exception:
        return jsonify(response_object), 404


@users_blueprint.route('/users/<user_name>', methods=['PATCH'])
@authenticate_as_admin
def update_user(auth_user_id, user_name):
    """
    Update user to add admin rights

    Only user with admin rights can modify another user

    **Example request**:

    .. sourcecode:: http

      PATCH api/users/<user_name> HTTP/1.1
      Content-Type: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "data": [
          {
            "admin": true,
            "bio": null,
            "birth_date": null,
            "created_at": "Sun, 14 Jul 2019 14:09:58 GMT",
            "email": "admin@example.com",
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
            "username": "admin"
          }
        ],
        "status": "success"
      }

    :param integer auth_user_id: authenticate user id (from JSON Web Token)
    :param string user_name: user name

    :<json boolean admin: does the user have administrator rights

    :reqheader Authorization: OAuth 2.0 Bearer Token

    :statuscode 200: success
    :statuscode 401:
        - Provide a valid auth token.
        - Signature expired. Please log in again.
        - Invalid token. Please log in again.
    :statuscode 403: You do not have permissions.
    :statuscode 404:
        - User does not exist.
    :statuscode 500:
    """
    response_object = {'status': 'fail', 'message': 'User does not exist.'}
    user_data = request.get_json()
    if 'admin' not in user_data:
        response_object = {'status': 'error', 'message': 'Invalid payload.'}
        return jsonify(response_object), 400

    try:
        user = User.query.filter_by(username=user_name).first()
        if not user:
            return jsonify(response_object), 404
        else:
            user.admin = user_data['admin']
            db.session.commit()
            response_object = {
                'status': 'success',
                'data': {'users': [user.serialize()]},
            }
            return jsonify(response_object), 200

    except exc.StatementError as e:
        db.session.rollback()
        appLog.error(e)
        response_object = {
            'status': 'error',
            'message': 'Error. Please try again or contact the administrator.',
        }
        code = 500
    return jsonify(response_object), code


@users_blueprint.route('/users/<user_name>', methods=['DELETE'])
@authenticate
def delete_user(auth_user_id, user_name):
    """
    Delete a user account

    A user can only delete his own account

    An admin can delete all accounts except his account if he's the only
    one admin

    **Example request**:

    .. sourcecode:: http

      DELETE /api/users/john_doe HTTP/1.1
      Content-Type: application/json

    **Example response**:

    .. sourcecode:: http

      HTTP/1.1 204 NO CONTENT
      Content-Type: application/json

    :param integer auth_user_id: authenticate user id (from JSON Web Token)
    :param string user_name: user name

    :reqheader Authorization: OAuth 2.0 Bearer Token

    :statuscode 204: user account deleted
    :statuscode 401:
        - Provide a valid auth token.
        - Signature expired. Please log in again.
        - Invalid token. Please log in again.
    :statuscode 403:
        - You do not have permissions.
        - You can not delete your account, no other user has admin rights.
    :statuscode 404:
        - User does not exist.
    :statuscode 500: Error. Please try again or contact the administrator.

    """
    try:
        auth_user = User.query.filter_by(id=auth_user_id).first()
        user = User.query.filter_by(username=user_name).first()
        if user:
            if user.id != auth_user_id and not auth_user.admin:
                response_object = {
                    'status': 'error',
                    'message': 'You do not have permissions.',
                }
                return response_object, 403
            if (
                user.admin is True
                and User.query.filter_by(admin=True).count() == 1
            ):
                response_object = {
                    'status': 'error',
                    'message': (
                        'You can not delete your account, '
                        'no other user has admin rights.'
                    ),
                }
                return response_object, 403
            for activity in Activity.query.filter_by(user_id=user.id).all():
                db.session.delete(activity)
                db.session.flush()
            user_picture = user.picture
            db.session.delete(user)
            db.session.commit()
            if user_picture:
                picture_path = get_absolute_file_path(user.picture)
                if os.path.isfile(picture_path):
                    os.remove(picture_path)
            shutil.rmtree(
                get_absolute_file_path(f'activities/{user.id}'),
                ignore_errors=True,
            )
            shutil.rmtree(
                get_absolute_file_path(f'pictures/{user.id}'),
                ignore_errors=True,
            )
            response_object = {'status': 'no content'}
            code = 204
        else:
            response_object = {
                'status': 'not found',
                'message': 'User does not exist.',
            }
            code = 404
    except (
        exc.IntegrityError,
        exc.OperationalError,
        ValueError,
        OSError,
    ) as e:
        db.session.rollback()
        appLog.error(e)
        response_object = {
            'status': 'error',
            'message': 'Error. Please try again or contact the administrator.',
        }
        code = 500
    return jsonify(response_object), code
