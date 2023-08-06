class vanityData:
    def __init__(self, data):
        self.raw = data

        try: self.vanityId: str = data["vanityId"]
        except (KeyError, TypeError): self.vanityId: str = "Undefined"

        try: self.callback: str = data["callback"]
        except (KeyError, TypeError): self.callback: str = "Undefined"  

        try: self.ownerId: str = data["ownerId"]
        except (KeyError, TypeError): self.ownerId: str = "Undefined"  

        try: self.disaled: str = data["disaled"]
        except (KeyError, TypeError): self.disaled: bool = False

# Made by https://wezacon.com - Team Wezacon