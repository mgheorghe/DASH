#!/usr/bin/env python3
"""
Test SAI Baby Hero.
Baby Hero test scale is 1% of the Hero test scale.
This is achieved by having only one prefix per ACL instead of 100 prefixes per ACL.
"""


import pytest
import saichallenger.common.sai_dataplane.snappi.snappi_traffic_utils as stu
import dpugen
import json
from pathlib import Path
from pprint import pprint
import ipaddress
import socket
import struct
import macaddress
import ipaddress
from copy import deepcopy
from munch import DefaultMunch
# utils
socket_inet_ntoa = socket.inet_ntoa
struct_pack = struct.pack
class MAC(macaddress.MAC):
    formats = ('xx:xx:xx:xx:xx:xx',) + macaddress.MAC.formats
maca = MAC       # optimization so the . does not get executed multiple times

baby_hero_params = {                    # CONFIG VALUE             # DEFAULT VALUE
    'DPUS':                             1,                         # 8
    'ENI_COUNT':                        32,                        # 256
    'ENI_L2R_STEP':                     1000,                      # 1000
    'IP_PER_ACL_RULE':                  1,                         # 100
}

# current_file_dir = Path(__file__).parent





class TestSaiBabyHero:

    #def create_baby_hero_config(self):
    #     """ Generate a configuration
    #         returns iterator (generator) of SAI records
    #     """
    #     conf = dpugen.sai.SaiConfig()
    #     # sets config size to 1% of the hero test size
    #     conf.mergeParams(baby_hero_params)
    #     conf.generate()
    #     ret = conf.items()
    #     return ret


        # confgen = sai.SaiConfig()
        # # confgen = sai.SaiConfig(baby_hero_params)
        # confgen.merge_params(baby_hero_params)
        # confgen.generate()

        # current_file_dir = Path(__file__).parent
        # with (current_file_dir / 'config_baby_hero.json').open(mode='r') as config_file:
        #     baby_hero_commands = json.load(config_file)
        # return baby_hero_commands


    # @pytest.mark.snappi
    # def test_create_vnet_config(self, dpu):
    #     """Generate and apply configuration"""
    #     results = [*dpu.process_commands( (self.create_baby_hero_config()) )]
    #     print("\n======= SAI commands RETURN values =======")
    #     pprint(results)

    @pytest.mark.snappi
    def test_baby_hero_traffic(self, dataplane):

        conf = dpugen.sai.SaiConfig()
        conf.mergeParams(baby_hero_params)

        dflt_params = {                        # CONFIG VALUE             # DEFAULT VALUE
            'SCHEMA_VER':                      '0.0.4',

            'DC_START':                        '220.0.1.1',                # '220.0.1.2'
            'DC_STEP':                         '0.0.1.0',                  # '0.0.1.0'

            'LOOPBACK':                        '221.0.0.1',                # '221.0.0.1'
            'PAL':                             '221.1.0.0',                # '221.1.0.1'
            'PAR':                             '221.2.0.0',                # '221.2.0.1'
            'GATEWAY':                         '222.0.0.1',                # '222.0.0.1'

            'DPUS':                             8,                         # 1

            'ENI_START':                        1,                         # 1
            'ENI_COUNT':                        256,                       # 32
            'ENI_STEP':                         1,                         # 1
            'ENI_L2R_STEP':                     0,                      # 1000

            'VNET_PER_ENI':                     1,                         # 16 TODO: partialy implemented

            'ACL_NSG_COUNT':                    5,                         # 5 (per direction per ENI)
            'ACL_RULES_NSG':                    1000,                    # 1000
            'IP_PER_ACL_RULE':                  1,                       # 100
            'ACL_MAPPED_PER_NSG':               500,                     # 500, efective is 250 because denny are skiped

            'MAC_L_START':                      '00:1A:C5:00:00:01',
            'MAC_R_START':                      '00:1B:6E:00:00:01',

            'MAC_STEP_ENI':                     '00:00:00:18:00:00',       # '00:00:00:18:00:00'
            'MAC_STEP_NSG':                     '00:00:00:02:00:00',
            'MAC_STEP_ACL':                     '00:00:00:00:01:00',

            'IP_L_START':                       '1.1.0.1',                 # local, eni
            'IP_R_START':                       '1.4.0.1',                 # remote, the world

            'IP_STEP1':                         '0.0.0.1',
            'IP_STEP_ENI':                      '0.64.0.0',
            'IP_STEP_NSG':                      '0.2.0.0',
            'IP_STEP_ACL':                      '0.0.1.0',
            'IP_STEPE':                         '0.0.0.2',

            'TOTAL_OUTBOUND_ROUTES':            25600000                  # ENI_COUNT * 100K
        }

        params_dict = deepcopy(dflt_params)

        cooked_params_dict = {}
        for ip in [
            'IP_STEP1',
            'IP_STEP_ENI',
            'IP_STEP_NSG',
            'IP_STEP_ACL',
            'IP_STEPE',
            'IP_L_START',
            'IP_R_START',
            'PAL',
            'PAR',
            'GATEWAY'
        ]:
            cooked_params_dict[ip] = int(ipaddress.ip_address((params_dict[ip])))
        for mac in [
            'MAC_L_START',
            'MAC_R_START',
            'MAC_STEP_ENI',
            'MAC_STEP_NSG',
            'MAC_STEP_ACL'
        ]:
            cooked_params_dict[mac] = int(maca(params_dict[mac]))

        params = DefaultMunch.fromDict(params_dict)
        cooked_params = DefaultMunch.fromDict(cooked_params_dict)

        p = params
        ip_int = cooked_params

        flows = []

        for eni_index, eni in enumerate(range(1, 33, 1)):

            f1 = dataplane.configuration.flows.flow(name="ENI%d_TO_NETWORK" % eni)[-1]
            f1.tx_rx.port.tx_name = dataplane.configuration.ports[0].name
            f1.tx_rx.port.rx_name = dataplane.configuration.ports[1].name
            f1.size.fixed = 256
            f1.duration.fixed_packets.packets = 250
            f1.rate.pps = 2 # unable to send more than 400 pps
            f1.metrics.enable = True

            outer_eth1, ip1, udp1, vxlan1, inner_eth1, inner_ip1, inner_udp1= (
                    f1.packet.ethernet().ipv4().udp().vxlan().ethernet().ipv4().udp()
            )

            remote_ip_a_eni = ip_int.IP_R_START + eni_index * ip_int.IP_STEP_ENI
            remote_mac_a_eni = ip_int.MAC_R_START + eni_index * ip_int.MAC_STEP_ENI

            eni_ip = socket_inet_ntoa(struct_pack('>L', ip_int.IP_L_START + eni_index * ip_int.IP_STEP_ENI))
            eni_mac = str(maca(ip_int.MAC_L_START + eni_index * ip_int.MAC_STEP_ENI))


            underlay_ip_eni = socket_inet_ntoa(struct_pack('>L', ip_int.PAL + eni_index * ip_int.IP_STEP1))


            outer_eth1.src.value = '00:00:00:00:00:00'
            outer_eth1.dst.value = '00:00:00:00:00:00'
            outer_eth1.ether_type.value = 2048


            ip1.src.value = underlay_ip_eni #ENI_VTEP_IP #ENI - VTEP

            ip1.dst.value = '221.0.0.1' #DPU_VTEP_IP #DPU - VTEP

            udp1.src_port.value = 11638
            udp1.dst_port.value = 4789

            vxlan1.vni.value = eni
            vxlan1.reserved0.value = 0
            vxlan1.reserved1.value = 0

            inner_eth1.src.value = eni_mac #INNER_SRC_MAC
            #inner_eth1.dst.value = '00:1B:6E:00:00:01' #INNER_DST_MAC
            inner_eth1.dst.increment.start = str(maca(remote_mac_a_eni))
            inner_eth1.dst.increment.count = 250
            inner_eth1.dst.increment.step  = '00:00:00:00:00:02'


            inner_ip1.src.value = eni_ip #ENI_IP   #ENI

            #import pdb; pdb.set_trace()
            inner_ip1.dst.increment.start = socket_inet_ntoa(struct_pack('>L', remote_ip_a_eni)) #NETWORK_IP1  #world
            inner_ip1.dst.increment.count = 250
            inner_ip1.dst.increment.step  = '0.0.0.2'


            inner_udp1.src_port.value = 10000
            inner_udp1.dst_port.value = 20000

            flows.append(f1)

        dataplane.set_config()

        flow_names = [f.name for f in flows]    

        ts = dataplane.api.transmit_state()
        ts.state = ts.START
        if len(flow_names) > 0:
            ts.flow_names = flow_names
        dataplane.api.set_transmit_state(ts)


        print('Checking metrics on all configured ports ...')
        print('Expected\tTotal Tx\tTotal Rx')
        assert self.wait_for(lambda: self.metrics_ok(dataplane.api)), 'Metrics validation failed!'


        while(True):
            if (dataplane.is_traffic_stopped(flow_names)):
                break 
        dataplane.stop_traffic()



        dataplane.teardown()

    # @pytest.mark.snappi
    # def test_remove_vnet_config(self, dpu, dataplane):
    #     """
    #     Generate and remove configuration
    #     We generate configuration on remove stage as well to avoid storing giant objects in memory.
    #     """
    #     import pdb; pdb.set_trace()
    #     cleanup_commands = []
    #     for cmd in reversed(self.create_baby_hero_config()):
    #         cleanup_commands.append({'name': cmd['name'], 'op': 'remove'})

    #     for cleanup_command in cleanup_commands:
    #         try:
    #             result = [*dpu.process_commands([cleanup_command])]
    #             #print("\n======= SAI commands RETURN values =======")
    #             #pprint(result)
    #         except Exception as e:
    #             pass
    #             #print(f"Error during cleanup: {e}")


    # def make_remove_vnet_config(self):
    #     """ Generate a configuration to remove entries
    #         returns iterator (generator) of SAI records
    #     """
    #     cleanup_commands = reversed(self.make_create_vnet_config())
    #     for cmd in cleanup_commands:
    #         cmd['op'] = 'remove'
    #         yield cmd
    #     return



    def metrics_ok(self, api):
        # create a port metrics request and filter based on port names
        cfg = api.get_config()

        req = api.metrics_request()
        req.port.port_names = [p.name for p in cfg.ports]
        # include only sent and received packet counts
        req.port.column_names = [req.port.FRAMES_TX, req.port.FRAMES_RX]
        # fetch port metrics
        res = api.get_metrics(req)
        # calculate total frames sent and received across all configured ports
        total_tx = sum([m.frames_tx for m in res.port_metrics])
        total_rx = sum([m.frames_rx for m in res.port_metrics])
        expected = sum([f.duration.fixed_packets.packets for f in cfg.flows])

        print('%d\t\t%d\t\t%d' % (expected, total_tx, total_rx))

        return expected == total_tx and total_rx >= expected

    def wait_for(self, func, timeout=1000, interval=0.2):
        '''
        Keeps calling the `func` until it returns true or `timeout` occurs
        every `interval` seconds.
        '''
        import time

        start = time.time()

        while time.time() - start <= timeout:
            if func():
                return True
            time.sleep(interval)

        print('Timeout occurred !')
        return False