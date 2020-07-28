from GameServers.GameServer import GameServer;
from firebase_admin import db;
import threading
import time


class ServerHandler(threading.Thread):
    def __init__(self, tickrate):
        super().__init__()
        self.servers = {};
        self.lock = threading.Lock();
        self.tickrate = tickrate;

    def register_server(self, data):

        if {'address', 'port', 'server_name', 'max_players', 'max_count'} <= set(data):

            formatted_address = data['address'].replace(".", "d");
            db_ref = db.reference('/master_server/banned_servers');
            banned_server_rev = db_ref.child(formatted_address)
            fetched_address = banned_server_rev.get();

            if fetched_address is not None:
                return "FAILED_TO_ADD"

            with self.lock:
                server = self.servers.get(f'{data["address"]}:{data["port"]}');
                if server is None:
                    server = GameServer(data["server_name"], data["address"], data["max_players"], data["max_count"], data["port"]);
                    self.servers[f'{server.address}:{server.port}'] = server;
                    return_message = "ADDED";
                else:
                    return_message = "FAILED_TO_ADD";
            return return_message;

        else:

            return "MISSING_DATA_IN_DICTIONARY";

    def get_server_basic_data(self, address, port):

        with self.lock:
            server = self.servers.get(f'{address}:{port}');
            return_message = ""''

            if server is None:
                return_message = "SERVER_NOT_FOUND"
            else:
                return_message = server.get_basic_data();

            return return_message;

    def get_server_detailed_data(self, address, port):

        with self.lock:
            server = self.servers.get(f'{address}:{port}');

            if server is None:
                return_message = "SERVER_NOT_FOUND";
            else:
                return_message = server.get_detailed_data();
            return return_message;

    def get_server_list(self):
        serialized_servers = [];
        with self.lock:
            for key, server in self.servers.items():
                serialized_servers.append(server.get_basic_data());
        return serialized_servers;

    def update_server(self, address, port, data):
        if data is not None:

            with self.lock:
                server = self.servers.get(f'{address}:{port}');

                if server is None:
                    return "SERVER_NOT_FOUND";
                else:
                    server.update(data);
                    return "SERVER_UPDATED";
        else:
            return 'MISSING_DATA_IN_DICTIONARY';
        pass;

    def run(self):
        while True:
            print('Server tick')
            servers_to_destroy = [];
            with self.lock:
                for key, server in self.servers.items():
                    if server.is_destroyable():
                        servers_to_destroy.append(key);
                    else:
                        server.tick();
                for server_to_destroy in servers_to_destroy:
                    print(f'{server_to_destroy} is deleted from list');
                    del self.servers[server_to_destroy];
            time.sleep(self.tickrate);