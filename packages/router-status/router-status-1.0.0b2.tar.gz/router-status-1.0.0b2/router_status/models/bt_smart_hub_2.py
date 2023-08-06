import logging
import time
from ipaddress import IPv4Address, IPv4Interface
from typing import Optional, Tuple
from urllib import request
from urllib.error import URLError
from urllib.parse import unquote
from xml.etree import ElementTree as ET

from .common import (BroadbandStatus, DSLLinkStatus, DSLStatus, DSLType,
                     Duration, Router, Usage, WANIpInfo)
from .errors import RouterNotContactableError

logger = logging.getLogger(__name__)


class BTSmartHub2(Router):

    def __init__(self, hub_ip: IPv4Address) -> None:
        self.url = f'http://{hub_ip}/nonAuth/wan_conn.xml'
        self.root: Optional[ET.Element] = None

    def _parse_xml(self, body: str) -> None:
        self.root = ET.fromstring(body)

    def _tag_value(self, tag_name: str) -> Optional[str]:
        if self.root is not None:
            st = self.root.find(tag_name)
            val = st.attrib['value']
            if val:
                return unquote(val)

    def _link_status(self) -> Tuple[str, str, int]:
        if (val := self._tag_value('link_status')):
            link_state, link_type, since = val.split(';')
            return link_state, link_type, int(since)
        return '', '', 0

    @property
    def _wan_active_idx(self) -> Optional[int]:
        if (val := self._tag_value('wan_active_idx')):
            return eval(val)

    @property
    def is_connected(self) -> bool:
        return self._link_status()[0].lower() == 'connected'

    @property
    def wan_ipv4(self) -> Optional[WANIpInfo]:
        if (idx := self._wan_active_idx) is not None:
            if val := self._tag_value('ip4_info_list'):
                val = val.replace('null', 'None')
                ssv = eval(val)[idx][0]
                info = ssv.split(';')
                return WANIpInfo(
                    IPv4Interface(info[0]),
                    IPv4Address(info[2]),
                    [IPv4Address(a) for a in info[3:]]
                )

    @property
    def sysuptime(self) -> int:
        if (val := self._tag_value('sysuptime')):
            return int(val)
        return 0

    @property
    def wan_uptime(self) -> int:
        link_status, _, since = self._link_status()
        return self.sysuptime - since if link_status.lower() == 'connected' else 0

    @property
    def wan_conn_volume(self) -> Usage:
        down, up = 0, 0
        if (idx := self._wan_active_idx) is not None:
            if val := self._tag_value('wan_conn_volume_list'):
                val = val.replace('null', 'None')
                ssv = eval(val)[idx][0]
                _, down, up = [int(i) for i in ssv.split(';')]
        return Usage(down, up)

    def wan_linestatuses(self) -> Optional[DSLStatus]:
        if val := self._tag_value('wan_linestatus_rate_list'):
            val = val.replace('null', 'None')
            ls = eval(val)[0]
            unknown = [int(i) for i in ls[5:11]]
            return DSLStatus(
                DSLLinkStatus(ls[0]),
                DSLType(ls[1]),
                ls[2],
                int(ls[3]),
                int(ls[4]),
                int(ls[11]) * 1000,
                int(ls[12]) * 1000,
                int(ls[13]),
                int(ls[14]),
                ls[15],
                unknown
            )

    def get_status(self) -> BroadbandStatus:
        try:
            fp = request.urlopen(self.url, timeout=1.0)
        except URLError:
            raise RouterNotContactableError(f"Connection Error: {self.url}")
        content = fp.read()
        try:
            self._parse_xml(content)
            return BroadbandStatus(
                self.is_connected,
                Duration(self.sysuptime),
                Duration(self.wan_uptime),
                self.wan_ipv4,
                self.wan_conn_volume,
                self.wan_linestatuses(),
            )
        except Exception as e:
            # something went wrong parsing the content, save copy for diagnostics
            fname = f'sh2_dump_{int(time.time())}.xml'
            with open(fname, 'wb') as fp:
                fp.write(content)
            logger.exception(e)
            raise
