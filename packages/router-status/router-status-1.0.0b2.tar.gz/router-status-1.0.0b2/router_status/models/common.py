from abc import ABC, abstractclassmethod
from dataclasses import dataclass
from enum import Enum
from ipaddress import IPv4Address, IPv4Interface
from typing import List, Optional


class Duration:
    def __init__(self, seconds: int) -> None:
        self._secs = seconds

    def __repr__(self):
        return f'Duration({self._secs})'

    def __str__(self):
        mins, secs = divmod(self._secs, 60)
        hours, mins = divmod(mins, 60)
        days, hours = divmod(hours, 24)
        return f'{days}d{hours}h{mins}m{secs}s'


class DSLLinkStatus(Enum):
    UP = 'UP'
    DOWN = 'DOWN'


class DSLType(Enum):
    ADSL = 'ADSL'
    ADSL2 = 'ADSL2'
    VDSL = 'VDSL'
    VDSL2 = 'VDSL2'


@dataclass
class Usage:
    bytes_down: int
    bytes_up: int


@dataclass
class WANIpInfo:
    wan_ip: IPv4Interface
    gateway: IPv4Address
    dns: List[IPv4Address]


@dataclass
class DSLStatus:
    status: DSLLinkStatus
    type: DSLType
    line_profile: str
    down_margin: int
    up_margin: int
    rate_down: int
    rate_up: int
    attain_down: int
    attain_up: int
    interleave: str
    other: List[int]


@dataclass
class BroadbandStatus:
    dsl_connected: bool
    sys_up_time: Duration
    wan_uptime: Duration
    wan_ipv4: Optional[WANIpInfo]
    usage: Usage
    dsl: Optional[DSLStatus]

    def __str__(self) -> str:
        r = []
        if self.dsl_connected:
            r.append('MODEM-ROUTER SYSTEM')
            r.append(f'  Up-time:                      {self.sys_up_time}')
            r.append(f'  Bytes down/up:                {self.usage.bytes_down} / {self.usage.bytes_up}')
            r.append('\nWAN CONNECTION (LAYER 3)')
            r.append(f'  Up-time:                      {self.wan_uptime}')
            r.append(f'  IP Address:                   {self.wan_ipv4.wan_ip}')
            r.append(f'  Gateway:                      {self.wan_ipv4.gateway}')
            dns_list = ', '.join([str(d) for d in self.wan_ipv4.dns])
            r.append(f'  DNS:                          {dns_list}')
            r.append('\nDSL (LAYER 2)')
            r.append(f'  Line Profile:                 {self.dsl.type.value}, {self.dsl.line_profile}')
            r.append(f'  Interleave mode:              {self.dsl.interleave}')
            r.append(f'  Current bit rate down/up:    {self.dsl.rate_down:9} / {self.dsl.rate_up}')
            r.append(f'  Attainable bit rate down/up: {self.dsl.attain_down:9} / {self.dsl.attain_up}')
            r.append(f'  SNR Margin (dB) down/up:     {self.dsl.down_margin / 10:9} / {self.dsl.up_margin / 10}')
            # r.append(f' Other values                 {self.dsl.other}')
        else:
            r = ['Not connected']
        return '\n'.join(r)


class Router(ABC):

    @abstractclassmethod
    def __init__(self, hub_ip: IPv4Address) -> None:
        pass

    @abstractclassmethod
    def get_status(self) -> BroadbandStatus:        # type: ignore
        pass
