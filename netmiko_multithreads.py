# This example show how to execute a command concurrently in the devices
# Using multithreads

# Change import settings
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from functions import get_devices, send_command


if __name__ == "__main__":
    # Type device filter by IP or hostname. Partial values or full. Optionally 'all'
    device_filter = input('\nSpecify device filter or all: ')

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
        # loop to run command in context manager. Using 6 as max Threads to start and wait
        with ThreadPoolExecutor(max_workers=6) as executor:
            future_list = []
            for device in inventory['hosts']:
                # update the device dictionary with the credentials and send command
                device.update(credentials)
                # Add the task to the pool of threads and run
                future = executor.submit(send_command, device, command)
                future_list.append(future)

            # force to wait until the future_list has been executed
            for f in as_completed(future_list):
                print(f.result())

        # Get and print finishing time
        elapsed_time = time.perf_counter() - execution_start_timer
        print(f"\n\"{command}\" executed in {devices_counter} devices in {elapsed_time:0.2f} seconds.\n")

        # Enter new command
        command = input('Command to run or \'exit\': ')
