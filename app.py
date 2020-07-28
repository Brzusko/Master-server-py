from flask import  Flask, request, jsonify, session;
from GameServers.GameServer import GameServer;
from GameServers.ServerHandler import ServerHandler;
from GameServers.Utils.Utils import *
from GameServers.superview import game_service_view;
from Panel.PanelView import panel_view;
from DiscordBot.DiscordClient import DiscordHandler;
import firebase_admin;
from firebase_admin import credentials;
import globals
import os
# data.server_name, data.address, data.max_players, data.max_count, data.port
# TOKEN, SECRET_KEY

app = Flask(__name__);
app.register_blueprint(game_service_view);
app.register_blueprint(panel_view);
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

d_bot = DiscordHandler();
cred = credentials.Certificate('./vektor-key.json');

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://vektor-platform.firebaseio.com/',
    'databaseAuthVariableOverride': None
});

app.secret_key = os.environ['SECRET_KEY'];


def register_master_servers():
    globals.master_servers['Pong'] = ServerHandler(10);

    for key, master_server in globals.master_servers.items():
        master_server.start();


if __name__ == "__main__":
    globals.init();
    register_master_servers();
    d_bot.start();
    app.run(threaded=True, host='0.0.0.0');

