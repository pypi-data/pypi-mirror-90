from understat import UnderstatPlayer
from Utility import Utility
from constants import *
import json

a = UnderstatPlayer(1228)

filter = {
    'season': '2020'
}
t = a.get_player_match_data(**filter)
print(t)
# print(Utility.generate_request_object(Utility.generate_request_url(PLAYER_URL, TEST_PLAYER_ID)).status_code)
# Utility.filter_data({'ranjan':2020})
