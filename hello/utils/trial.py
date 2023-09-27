import re
import hashlib
import base64
import json
import traceback
from datetime import datetime, timedelta





def gen_authorization(client_id, client_secret):
    credential = "{0}:{1}".format(client_id, client_secret)
    credential = base64.b64encode(credential.encode("utf-8")).decode("utf-8")
    return credential


if __name__ == '__main__':
    a = gen_authorization(
        'H4jfey8GBgq9dcyfgRyyjnnOLbzuU4cfXg3FNFd2',
        'EWFoJAWZ0cYb9esP52s4jS7pKkBnTadMUHpXSDPbwZFxX0YRnhSp5rdToQleiBjoXqSyV4Le01rKTKxxEcasiCnZd1TenwDDhCT0zitcyLInLIp61vYOiMhHmdJeopNr'
    )
    print(a)
    a = gen_authorization(
        'gjJgLLKeEx1XCNlOODDXlRf5BXk19OH3OZX4RguE',
        '9KH4Qddl1ngXjx84PWIytXtmEbo4NoOs58E8aliySqVvzqP1pmiVzULN7Cand21BEnnR1EgghPO8iNfoWd09ucsxhQky3Ks0gMY8j2W3J7tI4dcjIqAX7F6iJVEE7Mhq'
    )
    print(a)
    a = gen_authorization(
        'yst09YSUclqW8jegPncR2w3jQboiP46C7Lyd40gX',
        'zScdFaNuBJYQWpg1dY4iyUzXOl6DhrjgoWgXYxEtFY3PsU75aH9LGmuPzmehFmgBFBi7TGVFIeIYf4w07ajdqPi9IRPup0hlNXbQ6NCVtnwIOgOpzdeCFkdNmnQrJDDz'
    )
    print(a)
    a = gen_authorization(
        'customer8',
        'customer8'
    )
    print(a)