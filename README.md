<p align="center">
  <img src="images/logo.png" width="100" height="100" alt="Steam Dashboard Logo">
</p>

# Steam Dashboard Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/hacs/integration)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> [!TIP]
> **Deutschsprachige Anleitung:** Eine deutsche Version dieser Dokumentation findest du [weiter unten](#-deutsche-anleitung).

An unofficial but powerful Home Assistant integration for Steam. This integration allows you to monitor your Steam profile, track your gaming habits, and view your account status directly from your smart home dashboard.

## ✨ Features

* **Live Status:** Instantly see if you are Online, Offline, Away, or currently playing a specific game (including your profile avatar).
* **Gaming Statistics:** Tracks your total owned games, overall playtime, and playtime within the last 2 weeks.
* **Profile Details:** Displays your current Steam Level, Account Creation date, and Last Logoff timestamp.
* **Community & Security:** Monitor your friends count and check your current VAC/Community Ban status.
* **Privacy Aware:** Automatically detects if a profile is set to private and handles hidden data gracefully without throwing errors.

---

## 🛠️ Prerequisites

To use this integration, you need two things: your **Steam ID64** and a free **Steam Web API Key**.

1. Log in to the [Steam Developer API page](https://steamcommunity.com/dev/apikey) and generate a new Web API Key.
2. Find your **Steam ID64** (a 17-digit number). You can use tools like [steamid.io](https://steamid.io/) to easily convert your custom profile URL into the required ID64 format.
3. **Important Privacy Note:** For the integration to fetch data like playtime, level, and friends, your Steam profile's **Privacy Settings** (Game Details and Friends List) must be set to **Public**.

---

## 📦 Installation via HACS

1. Open Home Assistant and navigate to **HACS**.
2. Click the three dots in the top right corner and select **Custom repositories**.
3. Paste the URL of this repository and select **Integration** as the category.
4. Search for "Steam Dashboard" in HACS and click **Download**.
5. **Restart** Home Assistant.

---

## ⚙️ Configuration

1. Go to **Settings -> Devices & Services**.
2. Click **Add Integration** and search for **Steam Dashboard**.
3. Enter your 17-digit **Steam ID64**.
4. Paste your **Steam Web API Key**.
5. Click Submit. Your Steam sensors will instantly appear!

---

## 🇩🇪 Deutsche Anleitung

### Voraussetzungen
Du benötigst einen kostenlosen **Steam Web API Key** ([hier erstellen](https://steamcommunity.com/dev/apikey)) und deine **Steam ID64** (eine 17-stellige Zahl, herauszufinden z.B. über steamid.io). 
**Wichtig:** Damit alle Sensoren (wie Spielzeit und Freunde) Werte anzeigen, müssen die Privatsphäreeinstellungen deines Steam-Profils ("Spieldetails" und "Freundesliste") auf **Öffentlich** gestellt sein!

### Installation
Füge dieses Repository als "Benutzerdefiniertes Repository" in HACS (Kategorie: Integration) hinzu, lade es herunter und starte Home Assistant zwingend neu.

### Einrichtung
Gehe auf *Einstellungen -> Geräte & Dienste* und klicke auf *Integration hinzufügen*. Suche nach "Steam Dashboard". Trage dort deine Steam ID64 und deinen API Key ein. 

---

## 📝 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

*Disclaimer: This project is not affiliated with or endorsed by Valve Corporation or Steam.*