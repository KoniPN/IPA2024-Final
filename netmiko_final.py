from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException
from pprint import pprint

device_ip = "10.0.15.61"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
    "conn_timeout": 20,  # Connection timeout (default: 10)
    "timeout": 20,       # Command timeout (default: 100, but be conservative)
}


def gigabit_status():
    """Get the status of all GigabitEthernet interfaces"""
    try:
        ans = ""
        with ConnectHandler(**device_params) as ssh:
            up = 0
            down = 0
            admin_down = 0
            result = ssh.send_command("show ip interface brief", use_textfsm=True)
            
            # Check if result is valid
            if not result or not isinstance(result, list):
                return "Error: Unable to retrieve interface information"
            
            for interface in result:
                # TextFSM returns 'interface' key (lowercase), not 'intf'
                if interface.get('interface', '').startswith('GigabitEthernet'):
                    interface_name = interface['interface']
                    status = interface.get('status', 'unknown')
                    
                    if status == "up":
                        up += 1
                        ans += f"{interface_name} up, "
                    elif status == "down":
                        down += 1
                        ans += f"{interface_name} down, "
                    elif status == "administratively down":
                        admin_down += 1
                        ans += f"{interface_name} administratively down, "
            
            # Remove trailing comma and space
            ans = ans.rstrip(', ')
            
            # Add summary
            summary = f" -> {up} up, {down} down, {admin_down} administratively down"
            ans += summary
            
            pprint(ans)
            return ans
            
    except NetmikoTimeoutException as e:
        error_msg = f"Error: Connection timeout to router {device_ip}. Please check network connectivity."
        print(error_msg)
        return error_msg
    except NetmikoAuthenticationException as e:
        error_msg = f"Error: Authentication failed to router {device_ip}."
        print(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"Error: Unable to get interface status - {str(e)}"
        print(error_msg)
        return error_msg
