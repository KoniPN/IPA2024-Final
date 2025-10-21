from netmiko import ConnectHandler
from pprint import pprint

device_ip = "10.0.15.61"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}


def gigabit_status():
    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        result = ssh.send_command("show ip interface brief", use_textfsm=True)
        
        for interface in result:
            if interface['intf'].startswith('GigabitEthernet'):
                interface_name = interface['intf']
                status = interface['status']
                
                if status == "up":
                    up += 1
                    ans += f"{interface_name} up, "
                elif status == "down":
                    down += 1
                    ans += f"{interface_name} down, "
                elif status == "administratively down":
                    admin_down += 1
                    ans += f"{interface_name} administratively down, "
        
        ans = ans.rstrip(', ')
        
        summary = f" -> {up} up, {down} down, {admin_down} administratively down"
        ans += summary
        
        pprint(ans)
        return ans
