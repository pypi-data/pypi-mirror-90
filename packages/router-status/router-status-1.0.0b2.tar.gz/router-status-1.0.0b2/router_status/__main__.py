import json
from ipaddress import IPv4Address

from . import RouterFactory
from .models.errors import RouterNotContactableError

DEFAULT_ROUTER_IP = '192.168.1.254'


def read_config() -> dict:
    with open('config.json', 'r') as fp:
        conf = json.load(fp)
    return conf


def main():
    try:
        config = read_config()
    except Exception as e:
        exit(f'Could not read config error ({e})')
    router_ip = config.get('routerIp', DEFAULT_ROUTER_IP)
    try:
        router_ip = IPv4Address(router_ip)
    except Exception:
        exit(f"Invalid IPv4 address for routerIp '{router_ip}'")
    try:
        router_type = config['routerType']
    except KeyError:
        exit('routerType is not defined in config.json')
    try:
        device_class = RouterFactory(router_type)
    except Exception as e:
        exit(e)
    device = device_class(router_ip)

    try:
        print(device.get_status())
    except RouterNotContactableError as e:
        exit(e)


if __name__ == '__main__':
    main()
