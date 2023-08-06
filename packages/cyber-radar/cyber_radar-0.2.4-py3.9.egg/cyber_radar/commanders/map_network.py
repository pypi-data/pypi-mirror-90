#  This file is part of RADAR.
#  Copyright (C) 2019 Cole Daubenspeck
#
#  RADAR is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  RADAR is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with RADAR.  If not, see <https://www.gnu.org/licenses/>.

import netaddr
import re
import sys

from cyber_radar.client_uplink_connection import UplinkConnection
from cyber_radar.system_command import SystemCommand
from cyber_radar.automation_managers import CommandParserManager, PlaybookManager


def run(uplink: UplinkConnection, args: list):
    # get stats to monitor this commander's performance
    print(f"args: {repr(args)}")

    # get list of hosts in scope
    raw_inputs = []

    user_input = ""
    while True:
        user_input = input(f"Enter a target IP address, IP range, CIDR, or host to include in scope or type 'END' to stop").strip()
        if user_input.lower() == "end":
            print("No more hosts will be included in scope. ")
            break
        raw_inputs.append(user_input)
        

    # IP Input patterns
    ipaddr_rex = '^([0-9]{1,3}\.){3}[0-9]{1,3}$'
    iprange_rex = '^([0-9]{1,3}\.){3}[0-9]{1,3} *\- *([0-9]{1,3}\.){3}[0-9]{1,3}$'
    ipcidr_rex = '^([0-9]{1,3}\.){3}[0-9]{1,3}/[0-9]{1,2}$'

    # tokenize each target in target_list
    print("###  Verifying targets")
    for target in raw_inputs:
        if re.match(ipaddr_rex, target):
            print(f"  {target} is an IP address")
        elif re.match(iprange_rex, target):
            print(f"  {target} is an IP range")
        elif re.match(ipcidr_rex, target):
            print(f"  {target} is an CIDR network")
        else:
            print(f"  {target} is a hostname, URL, or other non-IP address target")
    valid = input("Does this look correct? [Y/n]: ").strip().lower()
    if len(valid) > 0 and valid[0] != 'y':
        print('!!!  You said targets are invalid... stopping now')
        exit(2)

    all_targets = []
    for target in raw_inputs:
        try:
            if re.match(ipaddr_rex, target):
                host_ip = netaddr.IPAddress(target)
                all_targets.append(str(host_ip))
            elif re.match(iprange_rex, target):
                range_start_end = [ip.strip() for ip in target.split('-')]
                range_start = range_start_end[0]
                range_end = range_start_end[1]
                # check if end range is relative and we need to figure out start
                if range_start.count(".") > range_end.count("."):
                    relative_range_start = range_start.rsplit(".", range_end.count(".")+1)[0]
                    range_end = f"{relative_range_start}.{range_end}"
                iprange = netaddr.IPRange(range_start, range_end)
                for host_ip in iprange:
                    all_targets.append(str(host_ip))
            elif re.match(ipcidr_rex, target):
                cidr = netaddr.IPNetwork(target)
                for host_ip in cidr.iter_hosts():
                    all_targets.append(str(host_ip))
            else:
                all_targets.append(target)
        except Exception as err:
            print(f"!!!  Invalid target '{target}': {err}")
    if len(all_targets) == 0:
        print("!!!  No valid targets... aborting")
        exit(1)

    # execute fast & wide scan to identify hosts


    # collect details about targets


    # perform intense scans

    # stream results and prioritize