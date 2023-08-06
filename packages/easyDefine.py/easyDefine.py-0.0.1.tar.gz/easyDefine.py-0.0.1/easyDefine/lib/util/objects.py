class Server:
    def __init__(self, data):
        self.json = data

        try: self.prefix: str = data["prefix"]
        except (KeyError, TypeError): self.prefix: str = "Undefined"
        try: self.name: str = data["name"]
        except (KeyError, TypeError): self.name: str = "Undefined"
        try: self.icon: str = data["icon"]
        except (KeyError, TypeError): self.icon: str = "Undefined"
        try: self.description: str = data["description"]
        except (KeyError, TypeError): self.invite: str = "Undefined"
        try: self.invite: str = data["invite"]
        except (KeyError, TypeError): self.invite: str = "Undefined"

        try: self.isBlacklisted: bool = data["blacklisted"]
        except (KeyError, TypeError): self.isBlacklisted: bool = False
        try: self.isFeatured: bool = data["featured"]
        except (KeyError, TypeError): self.isFeatured: bool = False
        try: self.isVerified: int = data["verified"]
        except (KeyError, TypeError): self.isVerified: int = -1

        try: self.serverId: int = data["id"]
        except (KeyError, TypeError): self.serverId: int = -1
        try: self.mongoId: int = data["_id"]
        except (KeyError, TypeError): self.mongoId: int = -1

        try: self.userCount: int = data["users"]
        except (KeyError, TypeError): self.userCount: int = -1
        try: self.bumpCount: int = data["bumps"]
        except (KeyError, TypeError): self.bumpCount: int = -1

        try: self.owner: str = data["owner"]
        except (KeyError, TypeError): self.owner: str = "Undefined"