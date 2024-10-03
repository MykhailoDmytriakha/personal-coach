import os
import json
from ..utils.config import get_config

class UserProfile:
    def __init__(self):
        config = get_config()
        self.profile_folder = config.get('user_profile_folder', 'user_profiles')
        os.makedirs(self.profile_folder, exist_ok=True)
# need to implement to receive data about user and store to SQLite

    