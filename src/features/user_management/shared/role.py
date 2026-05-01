class Role:
    """A class representing a user role in the system."""

    def __init__(self, role_id: str, name: str, description: str):
        self.role_id = role_id
        self.name = name
        self.description = description
