from bluepy.btle import Peripheral, BTLEGattError

from ilcctl.errors import ServiceNotFound, CharacteristicNotFound


class IlcBluetoothBulb:
    """
    Class for interacting with light bulbs
    """
    def __init__(self, address, srv_uuid=0xffd5, ch_uuid=0xffd9):
        self._address = address.upper()
        self._dev = Peripheral(self._address)
        self._srv_uuid = srv_uuid
        self._ch_uuid = ch_uuid

    def __del__(self):
        self.cleanup()

    def get_characteristic(self):
        """
        Method for accessing the characteristic of light color and and power state

        :return: Characteristic for setting light color and power state
        :rtype: Characteristic
        """
        return self._dev.getServiceByUUID(self._srv_uuid).getCharacteristics(self._ch_uuid)[0]

    def cleanup(self):
        """
        Method for proper disconnect
        """
        if hasattr(self, '_dev') and self._dev:
            self._dev.disconnect()
            self._dev = None

    def set_color(self, red, green, blue):
        """
        Method for changing the color of the light bulb

        :param red: Red color content
        :type red: int
        :param green: Green color content
        :type green: int
        :param blue: Blue color content
        :type blue: int
        """
        self.send_command(bytearray([0x56, red, green, blue, 0x00, 0xf0, 0xaa]))

    def turn_off(self):
        """
        Method for turning off the light bulb
        """
        self.send_command(bytearray([0xcc, 0x24, 0x33]))

    def turn_on(self):
        """
        Method for turning on the light bulb
        """
        self.send_command(bytearray([0xcc, 0x23, 0x33]))

    def white_light(self, brightness=255):
        """
        Method for turn on warm white led with certain intensity

        :param brightness: Intensity of the white light
        :type brightness: int
        """
        self.send_command(bytearray([0x56, 0x00, 0x00, 0x00, brightness, 0x0f, 0xaa]))

    def send_command(self, cmd):
        """
        Method for sending control commands to the light bulb

        :param cmd: Command as a array of bytes
        :type cmd: bytearray
        """
        try:
            self.get_characteristic().write(bytearray(cmd))
        except BTLEGattError:
            raise ServiceNotFound(self._srv_uuid)
        except IndexError:
            raise CharacteristicNotFound(self._ch_uuid)
