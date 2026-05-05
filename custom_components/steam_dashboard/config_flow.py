"""Config flow für Steam Dashboard."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant

from .const import DOMAIN, CONF_API_KEY, CONF_STEAM_ID

DATA_SCHEMA = vol.Schema({
  vol.Required(CONF_STEAM_ID): str,
  vol.Required(CONF_API_KEY): str,
})

async def validate_input(hass: HomeAssistant, data: dict) -> dict:
  """Validiere die Eingaben des Nutzers."""
  steam_id = data[CONF_STEAM_ID]
  
  # Eine Steam64 ID besteht immer aus exakt 17 Ziffern
  if len(steam_id) != 17 or not steam_id.isdigit():
      raise ValueError("invalid_steam_id")
  
  # In der nächsten Phase fügen wir hier einen echten API-Testaufruf hinzu, 
  # um zu prüfen, ob der API-Key gültig ist.
  
  return {"title": f"Steam Profil ({steam_id})"}

class SteamDashboardConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
  """Handle a config flow for Steam Dashboard."""

  VERSION = 1

  async def async_step_user(self, user_input=None):
      """Behandelt den initialen Setup-Schritt."""
      errors = {}

      if user_input is not None:
          try:
              info = await validate_input(self.hass, user_input)
              return self.async_create_entry(title=info["title"], data=user_input)
          except ValueError:
              errors["base"] = "invalid_steam_id"
          except Exception:  # pylint: disable=broad-except
              errors["base"] = "unknown"

      return self.async_show_form(
          step_id="user", data_schema=DATA_SCHEMA, errors=errors
      )