Following the previous labs at: https://github.com/aegiacometti/netmiko_5m_to_all

In order to speed up thing, in this one we are going to update de scripts to use **multiprocessing**, ***normal* multithreading** and **asyncio multithreading**

Install dependencies with `pip3 install -r requirements.txt`

Just update the **inventory.yml** with your devices info.

All the scripts do the same:
* select devices from inventory
* confirm
* enter command to run
* loop to keep throwing commands to the selected inventory

But each script use a different concurrency methodology:
* **netmiko_multiprocessing.py:** multi process
* **netmiko_multithreading.py:** multi threads sync
* **netdev_asyncio.py:** multi threads async (netdev is a library with roots on netmiko but adding async support)
