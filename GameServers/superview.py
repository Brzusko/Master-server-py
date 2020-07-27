from flask import Blueprint;

from flask import  Flask, request, jsonify;
from GameServers.Utils.Utils import *
from app import master_servers;


game_service_view = Blueprint('game_service_view', __name__);

@game_service_view.route('/')
def hello_world():
    return 'Hello, World';


@game_service_view.route('/servers/<string:server>')
def fetch_all_servers(server):
    master_server = master_servers.get(server);
    if master_server is None:
        return jsonify(generate_failed_message("MASTER_SERVER_NOT_FOUND"));
    else:
        servers = master_server.get_server_list();
        return jsonify(generate_success_message("SUCCESSFULLY_FOUNDED_SERVERS", servers));


@game_service_view.route('/servers/register/<string:server>', methods=['POST'])
def register_server(server):
    master_server = master_servers.get(server);

    if master_server is None:
        return jsonify(generate_failed_message("MASTER_SERVER_NOT_FOUND"));
    else:
        data = request.get_json();
        status = master_server.register_server(data);

        if status == "ADDED":
            message_back = generate_success_message("ADDED");
        else:
            message_back = generate_failed_message(status);

        return message_back;


@game_service_view.route('/servers/detailed_info/<string:server>/<string:address>/<string:port>', methods=['GET'])
def get_server_detailed_data(server, address, port):

    master_server = master_servers.get(server);

    if server is None:
        return jsonify(generate_failed_message('MASTER_SERVER_NOT_FOUND'));
    else:
        result = master_server.get_server_detailed_data(address, port);
        if result == "SERVER_NOT_FOUND":
            return jsonify(generate_failed_message('SERVER_NOT_FOUND'));
        else:
            return jsonify(generate_success_message('SUCCESSFULLY_FOUNDED_DETAILS', result));


@game_service_view.route('/servers/basic_info/<string:server>/<string:address>/<string:port>', methods=['GET'])
def get_server_basic_data(server, address, port):
    master_server = master_servers.get(server);

    if master_server is None:
        return jsonify(generate_failed_message('MASTER_SERVER_NOT_FOUND'));
    else:
        result = master_server.get_server_basic_data(address, port);
        if result == "SERVER_NOT_FOUND":
            return jsonify(generate_failed_message('SERVER_NOT_FOUND'));
        else:
            return jsonify(generate_success_message('SUCCESSFULLY_FOUNDED_BASIC', result));


@game_service_view.route('/servers/update_server/<string:server>/<string:address>/<string:port>', methods=['POST'])
def update_server(server, address, port):
    master_server = master_servers.get(server);

    if master_server is None:
        return jsonify(generate_failed_message('MASTER_SERVER_NOT_FOUND'));
    else:
        data = request.get_json();
        players = data.get('players');
        result = master_server.update_server(address, port, players);

        if result == "SERVER_NOT_FOUND":
            return jsonify(generate_failed_message(result));
        else:
            return jsonify(generate_success_message(result));