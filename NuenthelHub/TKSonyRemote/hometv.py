"""Holds HomeTV Class for use with TKSonyRemote"""


class HomeTV:
    """Class to represent a Sony TV and its network information"""
    def __init__(self, name: str, ip_address: str, pin: str = "0000"):
        self.name = name
        self.ip_address = ip_address
        self.pin = pin

    def set_pin(self, pin: int) -> None:
        """Set HomeTV pin number"""
        self.pin = pin

    def set_name(self, name: str) -> None:
        """Set name of HomeTV"""
        self.name = name
