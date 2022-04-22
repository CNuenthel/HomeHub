""" Holds RemoteControl Class """
# Create TV object
from TKSonyRemote.hometv import HomeTV
from bravia_tv import BraviaRC


class RemoteControl:
    """
    Connects and sends commands to an instantiated TV object

    Works only for Sony Bravia tv's 2013 or newer.

    The following settings must be activated on your TV:
    Network & Internet Settings
        Remote Start {activated}
        Remote Device Settings -- Control Remotely {activated}

    """
    def __init__(self, television: HomeTV):
        self.rc = BraviaRC(television.ip_address)
        self.tv = television
        self.is_connected = False
        self._connect()

    def _connect(self) -> bool:
        """
        Creates an instance connection between app and TV

        First time connection requires device registration, set tv.pin to pin displayed on tv
        and rerun connection to successfully register
        """
        self.is_connected = self.rc.connect(self.tv.pin, "N-Fam Hub", "N-Fam Hub")
        return self.is_connected

    def get_connection(self) -> bool:
        """Returns connection attribute"""
        return self.is_connected

    def set_volume(self, vol: int) -> int:
        """
        Sets volume to given integer

        vol: Integer value to set volume to
        """
        self.rc.set_volume_level(volume=(vol/100))
        return vol

    def get_apps(self) -> dict:
        """Returns available apps on TV"""
        return self.rc.load_app_list()

    def get_power_status(self) -> str:
        """Returns current power status of TV"""
        return self.rc.get_power_status()  # returns "active" if on

    def get_current_volume(self) -> int:
        """Returns current volume value"""
        if self.get_power_status() == "active":
            return self.rc.get_volume_info()["volume"]

    def get_power_stats(self) -> str:
        return self.rc.get_power_status()

    def toggle_power(self) -> bool:
        """Turns TV off if on or on if off"""
        status = self.get_power_status()
        if status == "active":
            self.rc.turn_off()
            return True
        elif status == "standby":
            self.rc.turn_on()
            return False

    def toggle_pause(self):
        """Pauses current app on TV or plays if currently paused"""
        self.rc.media_pause()

    def open_app(self, app_name):
        """Opens desired app"""
        self.rc.start_app(app_name)

    def nav_command(self, command: str):
        """Looks up and sends IRCC command through HTTP"""
        ircc_dict = {
            "up": "AAAAAQAAAAEAAAB0Aw==",
            "down": "AAAAAQAAAAEAAAB1Aw==",
            "left": "AAAAAQAAAAEAAAA0Aw==",
            "right": "AAAAAQAAAAEAAAAzAw==",
            "confirm": "AAAAAQAAAAEAAABlAw==",
            "home": "AAAAAQAAAAEAAABgAw==",
            "back": "AAAAAQAAAAEAAABgAw=="
        }

        if command in ircc_dict.keys():
            self.rc.send_req_ircc(ircc_dict[command])
        else:
            raise KeyError(f"{command} not found in command dictionary")

