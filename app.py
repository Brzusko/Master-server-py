from flask import  Flask, request, jsonify;
from GameServers.GameServer import GameServer;
from GameServers.ServerHandler import ServerHandler;
from GameServers.Utils.Utils import *
from GameServers.superview import game_service_view;
# data.server_name, data.address, data.max_players, data.max_count, data.port

master_servers = {}

app = Flask(__name__);
app.register_blueprint(game_service_view);

def register_master_servers():
    master_servers['Pong'] = ServerHandler(10);

    for key, master_server in master_servers.items():
        master_server.start();


if __name__ == "__main__":
    register_master_servers();
    app.run(threaded=True, host='0.0.0.0');