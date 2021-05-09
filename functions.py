import yaml
import sys
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException


def get_devices(device_filter: str) -> dict:
    """
    Get match devices from inventory bases on name or IP
    :param device_filter: string to look for
    :return: matching inventory
    """
    with open('inventory.yml') as f:
        inventory = yaml.safe_load(f.read())
    matched_devices = []
    if device_filter != 'all':
        for device in inventory['hosts']:
            if device_filter in device['hostname'] or device_filter in device['host']:
                matched_devices.append(device)
        inventory['hosts'] = matched_devices

    # Show matched inventory and confirm
    text = '\nMatched inventory'
    print('{}\n{}'.format(text, '*' * len(text)))
    for device in inventory['hosts']:
        print('* host: {} - ip: {}'.format(device['hostname'], device['host']))
    confirm = input('\nPlease confirm (y/n): ')

    if confirm.lower() != 'y':
        sys.exit()

    return inventory


def send_command(dev: dict, cmd: str) -> str:
    """
    Send command to device using Netmiko
    :param dev: device info
    :param cmd: command to execute
    :return: Command output from device
    """
    hostname = dev['hostname']
    # remove key hostname from dictionary since it is not expected/valid for netmiko
    del dev['hostname']

    try:
        # Use context manager to open and close the SSH session
        with ConnectHandler(**dev) as ssh:
            ssh.enable()
            output = ssh.send_command(cmd)

    except (NetmikoTimeoutException, NetmikoAuthenticationException):
        output = 'Connection to device failed'

    output = '*** host: {} - ip: {}\n{}\n'.format(hostname, dev['host'], output.strip())
    dev['hostname'] = hostname

    return output
