"""Steam API Client für Home Assistant."""
import aiohttp
import logging
from datetime import datetime, timezone

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://api.steampowered.com"

class SteamAPIClient:
    """Klasse zur Kommunikation mit der Steam API."""

    def __init__(self, api_key: str, steam_id: str, session: aiohttp.ClientSession):
        self.api_key = api_key
        self.steam_id = steam_id
        self.session = session

    async def fetch_data(self) -> dict:
        """Holt alle benötigten Daten von Steam."""
        data = {
            "visibility": "Unbekannt",
            "state": "Unbekannt",
            "personaname": "Unbekannt",
            "avatar": None,
            "level": None,
            "game_count": None,
            "playtime_total": None,
            "playtime_2weeks": None,
            "friends_count": None,
            "ban_status": "Unbekannt",
            "last_logoff": None,
            "time_created": None
        }

        try:
            # 1. Spieler-Zusammenfassung (Online-Status, Zeiten, Sichtbarkeit)
            summary_url = f"{BASE_URL}/ISteamUser/GetPlayerSummaries/v0002/?key={self.api_key}&steamids={self.steam_id}"
            async with self.session.get(summary_url) as response:
                if response.status == 200:
                    summary_json = await response.json()
                    if "response" in summary_json and "players" in summary_json["response"] and len(summary_json["response"]["players"]) > 0:
                        player = summary_json["response"]["players"][0]
                        
                        data["personaname"] = player.get("personaname", "Unbekannt")
                        data["avatar"] = player.get("avatarfull")
                        
                        # Zeitstempel umwandeln (für Home Assistant)
                        if "lastlogoff" in player:
                            data["last_logoff"] = datetime.fromtimestamp(player["lastlogoff"], tz=timezone.utc)
                        if "timecreated" in player:
                            data["time_created"] = datetime.fromtimestamp(player["timecreated"], tz=timezone.utc)
                        
                        # 1 = Privat, 3 = Öffentlich
                        visibility = player.get("communityvisibilitystate", 1)
                        if visibility != 3:
                            data["visibility"] = "Privat"
                            data["state"] = "Privat"
                            return data # Bei privaten Profilen können wir hier abbrechen
                        
                        data["visibility"] = "Öffentlich"
                        
                        if "gameextrainfo" in player:
                            data["state"] = f"Spielt: {player['gameextrainfo']}"
                        else:
                            personastate = player.get("personastate", 0)
                            states = {0: "Offline", 1: "Online", 2: "Beschäftigt", 3: "Abwesend", 4: "Snooze", 5: "Looking to Trade", 6: "Looking to Play"}
                            data["state"] = states.get(personastate, "Unbekannt")

            # 2. Level abrufen
            level_url = f"{BASE_URL}/IPlayerService/GetBadges/v1/?key={self.api_key}&steamid={self.steam_id}"
            async with self.session.get(level_url) as response:
                if response.status == 200:
                    level_json = await response.json()
                    if "response" in level_json and "player_level" in level_json["response"]:
                        data["level"] = level_json["response"]["player_level"]

            # 3. Anzahl Spiele & Spielzeit gesamt
            games_url = f"{BASE_URL}/IPlayerService/GetOwnedGames/v0001/?key={self.api_key}&steamid={self.steam_id}"
            async with self.session.get(games_url) as response:
                if response.status == 200:
                    games_json = await response.json()
                    if "response" in games_json and "games" in games_json["response"]:
                        data["game_count"] = games_json["response"]["game_count"]
                        # Steam liefert Spielzeit in Minuten. Wir rechnen in Stunden um.
                        total_mins = sum(game.get("playtime_forever", 0) for game in games_json["response"]["games"])
                        data["playtime_total"] = round(total_mins / 60, 1)

            # 4. Spielzeit letzte 2 Wochen
            recent_url = f"{BASE_URL}/IPlayerService/GetRecentlyPlayedGames/v0001/?key={self.api_key}&steamid={self.steam_id}"
            async with self.session.get(recent_url) as response:
                if response.status == 200:
                    recent_json = await response.json()
                    if "response" in recent_json and "games" in recent_json["response"]:
                        recent_mins = sum(game.get("playtime_2weeks", 0) for game in recent_json["response"]["games"])
                        data["playtime_2weeks"] = round(recent_mins / 60, 1)

            # 5. Anzahl Freunde
            friends_url = f"{BASE_URL}/ISteamUser/GetFriendList/v0001/?key={self.api_key}&steamid={self.steam_id}&relationship=friend"
            async with self.session.get(friends_url) as response:
                if response.status == 200:
                    friends_json = await response.json()
                    if "friendslist" in friends_json and "friends" in friends_json["friendslist"]:
                        data["friends_count"] = len(friends_json["friendslist"]["friends"])

            # 6. Bann-Status (VAC / Community)
            bans_url = f"{BASE_URL}/ISteamUser/GetPlayerBans/v1/?key={self.api_key}&steamids={self.steam_id}"
            async with self.session.get(bans_url) as response:
                if response.status == 200:
                    bans_json = await response.json()
                    if "players" in bans_json and len(bans_json["players"]) > 0:
                        p_bans = bans_json["players"][0]
                        is_vac_banned = p_bans.get("VACBanned", False)
                        is_comm_banned = p_bans.get("CommunityBanned", False)
                        if is_vac_banned or is_comm_banned:
                            data["ban_status"] = "Gebannt"
                        else:
                            data["ban_status"] = "Sauber"

        except Exception as e:
            _LOGGER.error("Fehler beim Abrufen der Steam Daten: %s", e)

        return data