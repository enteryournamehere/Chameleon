from pymongo import MongoClient
import objects
import logging
import os
import json


class Database:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Database init")
        self.db = MongoClient()
        self.db = self.db["chameleonbot"]
        self.cards = {}
        for filename in os.listdir('./decks'):
            if filename.endswith(".json"):
                deck_name = filename[:-5]
                self.cards[deck_name] = json.load(open('./decks/' + filename))
        self.shutdown = False

    # get part group

    def get_language_chat(self, chat_id):
        group = self.db["groups"].find_one({"id": chat_id})
        if group:
            return group["lang"]
        else:
            self.db["groups"].insert_one(vars(objects.Group(chat_id)))
            return "en"

    def get_deck_chat(self, chat_id):
        return self.db["groups"].find_one({"id": chat_id})["deck"]

    def get_deck(self, deck_name):
        return self.cards[deck_name]

    def get_fewer_setting(self, chat_id):
        return self.db["groups"].find_one({"id": chat_id})["fewer"]

    def get_more_setting(self, chat_id):
        return self.db["groups"].find_one({"id": chat_id})["more"]

    def get_all_settings(self, chat_id):
        group = self.db["groups"].find_one({"id": chat_id})
        if not group:
            self.db["groups"].insert_one(vars(objects.Group(chat_id)))
            group = vars(objects.Group(chat_id))
        entries_to_remove = {"id", "games_played", "_id"}
        for k in entries_to_remove:
            group.pop(k, None)
        return group

    def get_pin_setting(self, chat_id):
        return self.db["groups"].find_one({"id": chat_id})["pin"]

    def get_restrict_setting(self, chat_id):
        return self.db["groups"].find_one({"id": chat_id})["restrict"]

    def get_new_id(self, chat_id):
        existing = self.db["groups"].find_one({"old_id": chat_id})
        if existing:
            return existing["id"]

    def get_nextgame_ids(self, chat_id):
        return self.db["groups"].find_one({"id": chat_id})["nextgame"]

    def get_group_title(self, chat_id):
        to_return = {"title": "", "link": ""}
        group = self.db["groups"].find_one({"id": chat_id})
        to_return.update({"title": group["title"], "link": group["link"]})
        return to_return

    # get part player
    def get_new_player(self, player_ids):
        for player_id in player_ids:
            player = self.db["players"].find_one({"id": player_id})
            if player:
                if player["games_played"] == 0:
                    return True
            else:
                return True
        return False

    def get_language_player(self, user_id):
        player = self.db["players"].find_one({"id": user_id})
        if player:
            return player["lang"]
        else:
            self.db["players"].insert_one(vars(objects.Player(user_id)))
            return "en"

    def get_pm_player(self, user_id):
        # possible start point
        player = self.db["players"].find_one({"id": user_id})
        if not player:
            self.db["players"].insert_one(vars(objects.Player(user_id)))
            player = {"pm": False}
        return player["pm"]

    # insert part groups

    def end_game(self, chat_id, players, chameleon, winners, starter=False):
        self.db["groups"].update_one({"id": chat_id}, {"$inc": {"games_played": 1}})
        for player in players:
            updated = self.db["players"].find_one_and_update({"id": player}, {"$inc": {"games_played": 1}})
            if not updated:
                self.db["players"].insert_one(vars(objects.Player(player, 1)))
        self.db["players"].update_one({"id": chameleon}, {"$inc": {"been_chameleon": 1}})
        self.db["players"].update_many({"id": {"$in": winners}}, {"$inc": {"games_won": 1}})
        if starter:
            self.db["players"].update_one({"id": starter}, {"$inc": {"games_started": 1}})
        self.db["players"].update_one({"id": players[0]}, {"$inc": {"starter": 1}})

    def end_tournament(self, chat_id, players, winners):
        self.db["groups"].update_one({"id": chat_id}, {"$inc": {"tournaments_played": 1}})
        self.db["players"].update_many({"id": {"$in": players}}, {"$inc": {"tournaments_played": 1}})
        self.db["players"].update_many({"id": {"$in": winners}}, {"$inc": {"tournaments_won": 1}})

    def insert_group_lang(self, chat_id, lang):
        self.db["groups"].update_one({"id": chat_id}, {"$set": {"lang": lang}})

    def insert_group_deck(self, chat_id, deck):
        self.db["groups"].update_one({"id": chat_id}, {"$set": {"deck": deck}})

    def insert_group_fewer(self, chat_id):
        group = self.db["groups"].find_one({"id": chat_id})
        if group["fewer"]:
            self.db["groups"].update_one({"id": chat_id}, {"$set": {"fewer": False}})
            return False
        else:
            self.db["groups"].update_one({"id": chat_id}, {"$set": {"fewer": True}})
            return True

    def insert_group_more(self, chat_id):
        group = self.db["groups"].find_one({"id": chat_id})
        if group["more"]:
            self.db["groups"].update_one({"id": chat_id}, {"$set": {"more": False}})
            return False
        else:
            self.db["groups"].update_one({"id": chat_id}, {"$set": {"more": True}})
            return True

    def insert_group_tournament(self, chat_id):
        group = self.db["groups"].find_one({"id": chat_id})
        if group["tournament"]:
            self.db["groups"].update_one({"id": chat_id}, {"$set": {"tournament": False}})
            return False
        else:
            self.db["groups"].update_one({"id": chat_id}, {"$set": {"tournament": True}})
            return True

    def insert_group_pin(self, chat_id):
        group = self.db["groups"].find_one({"id": chat_id})
        if group["pin"]:
            self.db["groups"].update_one({"id": chat_id}, {"$set": {"pin": False}})
            return False
        else:
            self.db["groups"].update_one({"id": chat_id}, {"$set": {"pin": True}})
            return True

    def insert_group_restrict(self, chat_id):
        group = self.db["groups"].find_one({"id": chat_id})
        if group["restrict"]:
            self.db["groups"].update_one({"id": chat_id}, {"$set": {"restrict": False}})
            return False
        else:
            self.db["groups"].update_one({"id": chat_id}, {"$set": {"restrict": True}})
            return True

    def insert_group_new_id(self, old_id, new_id):
        self.db["groups"].update_one({"id": old_id}, {"$set": {"id": new_id, "old_id": old_id}})

    def insert_group_nextgame(self, chat_id, player_id):
        result = self.db["groups"].update_one({"id": chat_id}, {"$addToSet": {"nextgame": player_id}})
        if result.modified_count == 0:
            self.db["groups"].update_one({"id": chat_id}, {"$pull": {"nextgame": player_id}})
            return False
        return True

    def remove_group_nextgame(self, chat_id, player_ids):
        self.db["groups"].update_one({"id": chat_id}, {"$pull": {"nextgame": {"$in": player_ids}}})

    def insert_group_title(self, chat_id, title, link):
        self.db["groups"].update_one({"id": chat_id}, {"$set": {"title": title, "link": link}})

    # insert part player

    def insert_player_pm(self, user_id, boolean):
        self.db["players"].update_one({"id": user_id}, {"$set": {"pm": boolean}})

    def insert_player_lang(self, user_id, lang):
        self.db["players"].update_one({"id": user_id}, {"$set": {"lang": lang}})

    def init_shutdown(self):
        self.shutdown = True

    # reload part

    def reload_decks(self):
        self.cards = {}
        for filename in os.listdir('./decks'):
            if filename.endswith(".json"):
                deck_name = filename[:-5]
                self.cards[deck_name] = json.load(open('./decks/' + filename))


database = Database()
