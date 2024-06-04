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
        DPU_VTEP_IP = conf.params_dict['LOOPBACK']
        ENI_VTEP_IP = conf.params_dict['PAL']

        ENI_IP = conf.params_dict['IP_L_START']
        NETWORK_IP1 = conf.params_dict['IP_R_START']

        INNER_SRC_MAC = conf.params_dict['MAC_L_START']
        INNER_DST_MAC = conf.params_dict['MAC_R_START']

        f1 = dataplane.configuration.flows.flow(name="ENI1_TO_NETWORK")[-1]
        f1.tx_rx.port.tx_name = dataplane.configuration.ports[0].name
        f1.tx_rx.port.rx_name = dataplane.configuration.ports[1].name
        f1.size.fixed = 256
        f1.duration.fixed_packets.packets = 1
        f1.rate.pps = 10
        f1.metrics.enable = True

        outer_eth1, ip1, udp1, vxlan1, inner_eth1, inner_ip1, inner_udp1= (
                f1.packet.ethernet().ipv4().udp().vxlan().ethernet().ipv4().udp()
        )

        outer_eth1.src.value = '00:00:00:00:00:00'
        outer_eth1.dst.value = '00:00:00:00:00:00'
        outer_eth1.ether_type.value = 2048

        print('221.1.0.0')
        print(ENI_VTEP_IP)
        ip1.src.value = '221.1.0.0' #ENI_VTEP_IP #ENI - VTEP

        print('221.0.0.1')
        print(DPU_VTEP_IP)
        ip1.dst.value = '221.0.0.1' #DPU_VTEP_IP #DPU - VTEP

        udp1.src_port.value = 11638
        udp1.dst_port.value = 4789

        vxlan1.vni.value = 1
        vxlan1.reserved0.value = 0
        vxlan1.reserved1.value = 0

        inner_eth1.src.value = '00:1A:C5:00:00:01' #INNER_SRC_MAC
        inner_eth1.dst.value = '00:1B:6E:00:00:01' #INNER_DST_MAC

        inner_ip1.src.value = '1.1.0.1' #ENI_IP   #ENI
        inner_ip1.dst.value = '1.4.0.1' #NETWORK_IP1  #world

        inner_udp1.src_port.value = 10000
        inner_udp1.dst_port.value = 20000

        dataplane.set_config()

        ts = dataplane.api.transmit_state()
        ts.state = ts.START
        if f1.name != None:
            ts.flow_names = [f1.name]
        dataplane.api.set_transmit_state(ts)


        print('Checking metrics on all configured ports ...')
        print('Expected\tTotal Tx\tTotal Rx')
        assert self.wait_for(lambda: self.metrics_ok(dataplane.api)), 'Metrics validation failed!'


        flow_names=[f1.name]

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

    def wait_for(self, func, timeout=10, interval=0.2):
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