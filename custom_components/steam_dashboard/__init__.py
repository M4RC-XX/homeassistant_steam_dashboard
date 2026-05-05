"""Die Steam Dashboard Integration."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

# Wir werden später "sensor" nutzen, um unsere Entitäten zu erstellen
PLATFORMS = ["sensor"]

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
  """Richtet das Steam Dashboard aus einem Config Entry ein."""
  hass.data.setdefault(DOMAIN, {})
  
  # Hier speichern wir später unseren DataUpdateCoordinator
  hass.data[DOMAIN][entry.entry_id] = entry.data
  
  await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
  return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
  """Entfernt einen Config Entry."""
  unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
  if unload_ok:
      hass.data[DOMAIN].pop(entry.entry_id)

  return unload_ok