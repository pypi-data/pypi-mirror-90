import click
from bluepy.btle import BTLEDisconnectError

from ilcctl.bulb import IlcBluetoothBulb
from ilcctl.errors import ResourceNotFound


def convert_color(hex_color):
    """
    Helper method for converting hex color code into a triple of integer values

    :param hex_color: Hex color code as a string
    :type hex_color: str
    :return: Converted color
    :rtype: list
    """
    cleaned_color = hex_color.replace('0x', '')
    if len(cleaned_color) != 6:
        raise ValueError
    return [int(cleaned_color[i:i + 2], base=16) for i in range(0, len(cleaned_color), 2)]


@click.group()
def cli():
    pass


@cli.command(help='Command for changing the color')
@click.argument('mac_addr', type=str, )
@click.argument('hex_color', type=str, )
def setcolor(mac_addr, hex_color):
    try:
        red, green, blue = convert_color(hex_color)
    except ValueError:
        click.echo('Invalid color code', err=True)
        return

    bulb = None
    try:
        bulb = IlcBluetoothBulb(mac_addr)
        bulb.set_color(red, green, blue)
    except BTLEDisconnectError:
        click.echo('Failed to connect to light bulb', err=True)
    except ResourceNotFound as e:
        click.echo(str(e), err=True)
    finally:
        if bulb:
            bulb.cleanup()


@cli.command(help='Command for turning light bulb on and off')
@click.argument('mac_addr', type=str, )
@click.argument('state', type=str, )
def powerstate(mac_addr, state):
    bulb = None
    try:
        bulb = IlcBluetoothBulb(mac_addr)
        method = bulb.turn_on if state.lower() in ['on', '1'] else bulb.turn_off
        method()
    except BTLEDisconnectError:
        click.echo('Failed to connect to light bulb', err=True)
    except ResourceNotFound as e:
        click.echo(str(e), err=True)
    finally:
        if bulb:
            bulb.cleanup()


@cli.command(help='Command for sending a raw byte sequence to the light bulb')
@click.argument('mac_addr', type=str, )
@click.argument('cmd', type=str, )
def sendcmd(mac_addr, cmd):
    bulb = None
    try:
        bulb = IlcBluetoothBulb(mac_addr)
        cmd = cmd.replace('0x', '')
        if len(cmd) % 2 != 0:
            click.echo('Invalid byte sequence', err=True)
        else:
            bulb.send_command(bytearray([int(cmd[i:i + 2], base=16) for i in range(0, len(cmd), 2)]))
    except BTLEDisconnectError:
        click.echo('Failed to connect to light bulb', err=True)
    except ResourceNotFound as e:
        click.echo(str(e), err=True)
    finally:
        if bulb:
            bulb.cleanup()


@cli.command(help='Command for turn on warm white led with certain intensity')
@click.argument('mac_addr', type=str, )
@click.option('--brightness', type=int, default=255, help='Brightness level between 0 and 255')
def whitelight(mac_addr, brightness):
    bulb = None
    try:
        bulb = IlcBluetoothBulb(mac_addr)
        brightness = 0 if brightness < 0 else (255 if brightness > 255 else brightness)
        bulb.white_light(brightness)
    except BTLEDisconnectError:
        click.echo('Failed to connect to light bulb', err=True)
    except ResourceNotFound as e:
        click.echo(str(e), err=True)
    finally:
        if bulb:
            bulb.cleanup()
