from src.UnderstatPlayer import UnderstatPlayer
from src.Utility import Utility
from src.constants import *

# a = UnderstatPlayer(1228)
#
# print(a.get_player_match_data())
print(Utility.generate_request_object(Utility.generate_request_url(PLAYER_URL, TEST_PLAYER_ID)).status_code)
