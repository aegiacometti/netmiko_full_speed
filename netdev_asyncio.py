# This example show how to execute a command concurrently in the devices
# Using asyncio and netdev

# Change import settings
import time
from functions import get_devices
import asyncio
import netdev


async def task(dev, cmd):
    """
    Task executor
    :param dev: device info
    :param cmd: command to execute
    :return: -
    """
    # Remove key not supported by netdev
    hostname = dev['hostname']
    del dev['hostname']

    # Use context manager to open and close the SSH session
    async with netdev.create(**dev) as ios:
        # Send command
        output = await ios.send_command(cmd)

    # Re add variable and generate output
    dev['hostname'] = hostname
    print('*** host: {} - ip: {}\n{}\n'.format(hostname, dev['host'], output.strip()))


async def run(hosts, cred, cmd):
    """
    Generate list of tasks
    :param hosts: device list
    :param cred: credentials
    :param cmd: command to execute
    :return: -
    """
    tasks = []
    for host in hosts:
        host.update(cred)
        tasks.append(task(host, cmd))
    await asyncio.wait(tasks)


if __name__ == "__main__":
    # Type device filter by IP or hostname. Partial values or full. Optionally 'all'
    device_filter = input('\nSpecify device filter: ')

    # Load devices from file with the filter and display matching device
    inventory = get_devices(device_filter)
    devices_counter = len(inventory['hosts'])

    # get the common variables for all devices
    credentials = inventory['common_vars']

    # get command to execute from CLI
    command = input('\nCommand to run: ')

    # loop to keep throwing commands to the same selected inventory
    while command.lower() != 'exit':
        print(f'\nExecuting command: {command}\n')
        # Start timer variable
        execution_start_timer = time.perf_counter()

        # get event loop and run it
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run(inventory['hosts'], credentials, command))

        # Get and print finishing time
        elapsed_time = time.perf_counter() - execution_start_timer
        print(f"\n\"{command}\" executed in {devices_counter} devices in {elapsed_time:0.2f} seconds.\n")

        # Enter new command
        command = input('Command to run or \'exit\': ')
