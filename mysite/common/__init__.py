import time
from datetime import datetime, timezone, timedelta


bjtz = timezone(timedelta(hours=8))
bjtznow = lambda: datetime.now(tz=bjtz)

if __name__ == '__main__':
    for i in range(2):
        print(bjtz, bjtznow())
        time.sleep(3)
