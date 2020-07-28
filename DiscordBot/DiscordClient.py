import os
import discord
import threading
from firebase_admin import db;
import time;


class DiscordHandler(threading.Thread):
    def __init__(self):
        super(DiscordHandler, self).__init__();
        self.lock = threading.Lock();
        self.bot = DiscordClient();
        self.semaphore = threading.Semaphore(1);
        self.can_run = True;
        self.bot_is_running = False;

    def init_bot(self):
        if not self.bot_is_running:
            self.bot_is_running = True;
            self.bot.run(os.environ['TOKEN']);

    def run(self) -> None:
        while self.can_run:
            self.semaphore.acquire();
            self.init_bot();


class DiscordClient(discord.Client):

    def __init__(self, **options):
        super().__init__(**options)
        self.user_fetcher = UsersFetcher(self, 10);

    def fetch_users(self):

        for guild in self.guilds:
            if guild.name == os.environ['SERVER']:
                counter = 0;
                for member in guild.members:
                    for role in member.roles:
                        if role.name == os.environ['ROLE']:
                            counter = counter + 1;
                db_ref = db.reference('/master_server')
                child_ref = db_ref.child('counter')
                child_ref.set({
                    "count": counter
                });

    async def on_member_join(self, member):
        await self.send_message(member, "Test");


    async def on_ready(self):
        self.user_fetcher.start();


class UsersFetcher(threading.Thread):
    def __init__(self, discord:DiscordClient, tick:int):
        super(UsersFetcher, self).__init__();
        self.discord_client = discord;
        self.lock = threading.Lock();
        self.tickrate = tick;

    def run(self):
        while(True):
            self.discord_client.fetch_users();
            time.sleep(self.tickrate)
            pass;