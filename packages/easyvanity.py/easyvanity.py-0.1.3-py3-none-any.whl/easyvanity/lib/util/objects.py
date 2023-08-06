class vanityData:
    def __init__(self, data):
        self.raw = data

        try: self.vanityId: str = data["vanityId"]
        except (KeyError, TypeError): self.vanityId: str = "Undefined"

        try: self.callback: str = data["callback"]
        except (KeyError, TypeError): self.callback: str = "Undefined"  

        try: self.ownerId: str = data["ownerId"]
        except (KeyError, TypeError): self.ownerId: str = "Undefined"  

        try: self.disabled: str = data["disabled"]
        except (KeyError, TypeError): self.disabled: bool = False

class ownerVanities:
    def __init__(self, data):
        self.raw = data

        self.vanityId = []
        self.callback = []
        self.ownerId = []
        self.disabled = []

    @property
    def ownerVanities(self):
        for x in self.raw:

            try: self.vanityId.append(x["vanityId"])
            except (KeyError, TypeError): self.vanityId.append(None)

            try: self.callback.append(x["callback"])
            except (KeyError, TypeError): self.callback.append(None)

            try: self.ownerId.append(x["ownerId"])
            except (KeyError, TypeError): self.ownerId.append(None)

            try: self.disabled.append(x["disabled"])
            except (KeyError, TypeError): self.disabled.append(None)

        return self
# Made by https://wezacon.com - Team Wezacon