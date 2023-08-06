import os
import functools
from . import varsfile
from . import util
from . import wifi


def ssh_file(path):
    print('*** Enabling SSH. ***')
    util.touch(os.path.join(path, 'ssh'))
    print()

DEFAULT_SD_PATH = '/Volumes/boot'

def setup(path='.', sd_path=DEFAULT_SD_PATH, uuid=None, hostname=None, **kw):
    '''You've just flashed a fresh raspbian verson.

    Now you want to:
     - enable ssh so you can access the pi without a keyboard/monitor.
     - setup your wifi network so you can access it via ssh.

    You can specify your own network, or it will default to `s0nycL1f3l1ne`.

    Arguments:
        ssid (str): the wifi ssid
        password (str):the wifi password
        sd_path (str): the path to the sd card. It should always be /Volumes/boot,
            but you never know.
        ssh (bool): whether to enable ssh. Idk why you'd ever want to disable,
            if you do, but use: `--nossh`

    '''
    try:
        if not os.path.exists(sd_path):
            print('*** ERROR - No SD Card found at {} ***'.format(sd_path))
            return

        print('Copying over boot files...')
        util.copytree(path, sd_path)
        print()

        var = varsfile.Vars(os.path.join(sd_path, 'resources'))
        var.update(kw)
        hostname_prefix = '{}node'.format(var.get('APP_NAME'))
        var.prompt('UUID', 'Do you want to set a deployment UUID? This can be used to tie status messages to specific hardware.', '', uuid)
        var.prompt('hostname', 'Do you want to set the device hostname? (default: {}-$MAC_ADDR)'.format(hostname_prefix), '', hostname)
        if hostname is False or not var.get('hostname'):
            var.prompt('hostname_prefix', 'Do you want to change the device hostname prefix? (default: {})'.format(hostname_prefix), '')
        var.prompt_any()

        print('Please eject the SD card, insert it into your Pi, and start up!')
    except KeyboardInterrupt:
        print('Interrupted.')


# @functools.wraps(varsfile.Vars)
def vars(path=os.path.join(DEFAULT_SD_PATH, 'resources'), *a, **kw):
    return varsfile.Vars(path, *a, **kw)


def check(sd_path=DEFAULT_SD_PATH, uuid=None):
    var = varsfile.Vars(os.path.join(sd_path, 'resources'))
    if uuid:
        assert 'uuid' in var.config, 'missing UUID. Set using rpiup sd vars set --UUID=something-asdfasdf'
