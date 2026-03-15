from datetime import datetime

from ignis.utils import Poll

time = Poll(timeout=500, callback=lambda _: datetime.now().strftime("%H:%M:%S"))
