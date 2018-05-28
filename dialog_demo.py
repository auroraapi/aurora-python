import auroraapi as aurora
from auroraapi.dialog import Dialog

aurora.config.app_id    = "86bba6383f2a46de52baf1f78495a321"
aurora.config.app_token = "JTeV2lPEOMUwrAEFeLu4fZNGzIPMgLC"

d = Dialog("ec8a4fda52b5")
d.set_function("first", lambda c: True)
d.set_function("second", lambda c: False)
d.run()
