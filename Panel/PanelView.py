from firebase_admin import db;
from flask import Blueprint, request, jsonify, session
from GameServers.Utils.Utils import *
import os;
import jwt;
import datetime;

panel_view = Blueprint('panel_view', __name__);


@panel_view.route('/panel/login', methods = ['POST'])
def login_to_panel():

    data = request.get_json();

    if {'password'} <= set(data):
        if data['password'] == os.environ['PASSWORD']:
            generated_bytes = os.urandom(64);
            decoded_bytes = generated_bytes.decode('latin1');
            token = jwt.encode({"data": decoded_bytes}, os.environ['SECRET_KEY'], algorithm='HS256');
            session['panel'] = token;
            return jsonify(generate_success_message('SUCCESSFULLY_LOGGED_IN', {
                "token": token
            }));
        else:
            return jsonify(generate_failed_message("WRONG_PASSWORD"))
    else:
        return jsonify(generate_failed_message("MISSING_DATA_IN_DICT"))


@panel_view.route('/panel/ban_server', methods=['POST'])
def ban_server():
    data = request.get_json();
    if {'address', 'token'} <= set(data):
        if not check_if_is_logged(data['token']):
            return jsonify(generate_failed_message('USER_IS_NOT_LOGGED_IN'));
        db_ref = db.reference('/master_server/banned_servers');
        address = data['address'].replace(".", "d");
        banned_db_ref = db_ref.child(address);
        res = banned_db_ref.set({
            "address": data['address'],
            "timestamp": datetime.datetime.now().timestamp()
        });
        return jsonify(generate_success_message('SUCCESSFULLY_BANNED_SERVER'))


@panel_view.route('/panel/view_banned_servers', methods=['GET'])
def view_banned_servers():
    db_ref = db.reference('/master_server/banned_servers')
    db_res = db_ref.get();

    return jsonify(generate_success_message("SUCCESSFULLY_FETCHED_BANNED_SERVERS", db_res));


@panel_view.route('/panel/view_meeting', methods = ['GET'])
def view_meeting_panel():
    db_ref = db.reference('/master_server');
    meeting_ref = db_ref.child('current_meeting');
    meeting_info = meeting_ref.get();

    if meeting_info is not None:
        return jsonify(generate_success_message('SUCCESSFULLY_FETCHED_MEETING', meeting_info));
    else:
        return jsonify(generate_failed_message('COULNDT_FIND_MEETING_IN_FIREBASE'));


@panel_view.route('/panel/update_meeting', methods = ['POST'])
def update_meeting_panel():
    data = request.get_json();

    if {'meeting_title', 'meeting_desc', 'token'} <= set(data):
        if not check_if_is_logged(data['token']):
            return jsonify(generate_failed_message("USER_IS_NOT_LOGGED_IN"));
        db_ref = db.reference('/master_server')
        child_ref = db_ref.child('current_meeting');
        child_ref.set({
            "meeting_title": data['meeting_title'],
            "meeting_desc": data['meeting_desc']
        })

        return generate_success_message('SUCCESSFULLY_UPDATED_MEETING_INFO');
    else:
        return jsonify(generate_failed_message('MISSING_DATA_IN_DICT'));

    pass;


def check_if_is_logged(token):
    if 'panel' in session:
        user_token_decoded = jwt.decode(token, os.environ['SECRET_KEY'], algorithms='HS256');
        session_token_decoded = jwt.decode(session['panel'], os.environ['SECRET_KEY'], algorithms='HS256');

        if user_token_decoded['data'] == session_token_decoded['data']:
            return True;
        return False;