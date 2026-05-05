"""Sensoren für das Steam Dashboard."""
import logging
from datetime import timedelta

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_API_KEY, CONF_STEAM_ID
from .steam_api import SteamAPIClient

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Richtet die Steam Sensoren aus dem Config Entry ein."""
    api_key = config_entry.data[CONF_API_KEY]
    steam_id = config_entry.data[CONF_STEAM_ID]
    session = async_get_clientsession(hass)

    api_client = SteamAPIClient(api_key, steam_id, session)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Steam Dashboard Coordinator",
        update_method=api_client.fetch_data,
        update_interval=timedelta(minutes=5),
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities([
        SteamMainSensor(coordinator, steam_id),
        SteamLevelSensor(coordinator, steam_id),
        SteamGameCountSensor(coordinator, steam_id),
        SteamPlaytimeTotalSensor(coordinator, steam_id),
        SteamPlaytimeRecentSensor(coordinator, steam_id),
        SteamFriendsSensor(coordinator, steam_id),
        SteamBanSensor(coordinator, steam_id),
        SteamLastLogoffSensor(coordinator, steam_id),
        SteamAccountCreatedSensor(coordinator, steam_id)
    ])


class SteamBaseSensor(CoordinatorEntity, SensorEntity):
    """Eine Basis-Klasse, um doppelten Code zu vermeiden."""
    def __init__(self, coordinator, steam_id, key, name, icon, unit=None, device_class=None):
        super().__init__(coordinator)
        self._key = key
        self._attr_unique_id = f"{steam_id}_{key}"
        self._attr_name = name
        self._attr_icon = icon
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class

    @property
    def native_value(self):
        return self.coordinator.data.get(self._key)


class SteamMainSensor(CoordinatorEntity, SensorEntity):
    """Der Hauptsensor (Status)."""
    def __init__(self, coordinator, steam_id):
        super().__init__(coordinator)
        self._steam_id = steam_id
        self._attr_unique_id = f"{steam_id}_status"
        self._attr_icon = "mdi:steam"

    @property
    def name(self):
        personaname = self.coordinator.data.get("personaname", self._steam_id)
        return f"Steam ({personaname})"

    @property
    def native_value(self):
        return self.coordinator.data.get("state")

    @property
    def entity_picture(self):
        return self.coordinator.data.get("avatar")

# --- Neue und aktualisierte Sensoren ---

class SteamLevelSensor(SteamBaseSensor):
    def __init__(self, coordinator, steam_id):
        super().__init__(coordinator, steam_id, "level", "Steam Level", "mdi:chevron-triple-up")

class SteamGameCountSensor(SteamBaseSensor):
    def __init__(self, coordinator, steam_id):
        super().__init__(coordinator, steam_id, "game_count", "Steam Spiele", "mdi:controller-classic")

class SteamPlaytimeTotalSensor(SteamBaseSensor):
    def __init__(self, coordinator, steam_id):
        super().__init__(coordinator, steam_id, "playtime_total", "Spielzeit Gesamt", "mdi:clock", unit="h")

class SteamPlaytimeRecentSensor(SteamBaseSensor):
    def __init__(self, coordinator, steam_id):
        super().__init__(coordinator, steam_id, "playtime_2weeks", "Spielzeit (Letzte 2 Wochen)", "mdi:clock-fast", unit="h")

class SteamFriendsSensor(SteamBaseSensor):
    def __init__(self, coordinator, steam_id):
        super().__init__(coordinator, steam_id, "friends_count", "Steam Freunde", "mdi:account-group")

class SteamBanSensor(SteamBaseSensor):
    def __init__(self, coordinator, steam_id):
        super().__init__(coordinator, steam_id, "ban_status", "Steam Bann-Status", "mdi:gavel")

class SteamLastLogoffSensor(SteamBaseSensor):
    def __init__(self, coordinator, steam_id):
        super().__init__(coordinator, steam_id, "last_logoff", "Zuletzt online", "mdi:history", device_class=SensorDeviceClass.TIMESTAMP)

class SteamAccountCreatedSensor(SteamBaseSensor):
    def __init__(self, coordinator, steam_id):
        super().__init__(coordinator, steam_id, "time_created", "Account erstellt am", "mdi:calendar-star", device_class=SensorDeviceClass.TIMESTAMP)