# Router Status

A utility to extract status information from domestic Broadband routers, such as WAN IP address, downstream rate, uptime, noise margin etc.

## Executing directly

The packaged can be called directly to print the router status in human readable form.

```bash
python3 -m router_status

MODEM-ROUTER SYSTEM
  Up-time:                      4d4h54m49s
  Bytes down/up:                27539064092 / 1289704767

WAN CONNECTION (LAYER 3)
  Up-time:                      2d17h56m21s
  IP Address:                   86.176.52.245/32
  Gateway:                      172.16.12.54
  DNS:                          81.139.57.100, 81.139.56.100

DSL (LAYER 2)
  Line Profile:                 VDSL2, Profile 17a
  Interleave mode:              fast
  Current bit rate down/up:     39225000 / 10693000
  Attainable bit rate down/up:  37365000 / 10660980
  SNR Margin (dB) down/up:           5.3 / 6.0
```

## Development

### Additional modem types

To support more router types, developers would need access to those routers, or alternatively owners could extract files and pass them on to developers. Files can be extracted using wget. Use browser developer mode (F12) to find out what URLs carry the low level status information.  Take multiple samples for each stage of connection (DSL down, DSL training, WAN aquiring IP address, WAN connected).

```bash
wget -O $(date +%s).xml http://192.168.2.254/nonAuth/wan_conn.xml
```
