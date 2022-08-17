from sai_thrift.sai_headers import *
from sai_base_test import *


class SaiHelperDash(SaiHelperBase):

    def setUp(self):
        super(SaiHelperBase, self).setUp()

        self.getSwitchPorts()
        # initialize switch
        self.start_switch()

        self.switch_resources = self.saveNumberOfAvaiableResources(debug=True)

        # get default vlan
        attr = sai_thrift_get_switch_attribute(
            self.client, default_vlan_id=True)
        self.default_vlan_id = attr['default_vlan_id']
        # self.assertNotEqual(self.default_vlan_id, 0)
        print("> default_vlan_id", self.default_vlan_id)

        self.recreate_ports()

        # get number of active ports
        self.get_active_port_list()

        # get default vrf
        attr = sai_thrift_get_switch_attribute(
            self.client, default_virtual_router_id=True)
        self.default_vrf = attr['default_virtual_router_id']
        # self.assertNotEqual(self.default_vrf, 0)
        print("> default_vrf", self.default_vrf)

        self.turn_up_and_check_ports()

        # get default 1Q bridge OID
        self.get_default_1q_bridge_id()

        #remove all default 1Q bridge port
        self.reset_1q_bridge_ports()

        # get cpu port
        attr = sai_thrift_get_switch_attribute(self.client, cpu_port=True)
        self.cpu_port_hdl = attr['cpu_port']
        # self.assertNotEqual(self.cpu_port_hdl, 0)
        print("> cpu_port_hdl", self.cpu_port_hdl)

        # get cpu port queue handles
        # self.check_cpu_port_hdl()

        print("Finish SaiHelperBase setup")
