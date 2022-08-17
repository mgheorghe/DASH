from sai_thrift.sai_headers import *
from sai_base_test import *

from ptf.testutils import *

from sai_helper_dash import SaiHelperDash


class TestSaiVnetInboundTest(SaiHelperDash):

    # Constants
    VIP = "10.10.1.1"
    SWITCH_ID = 1
    DIR_LOOKUP_ENI = 60
    ENI_MAC = "00:00:00:09:03:14"
    # ENI_MAC = '\x00\x00\x00\x09\x03\x0d'
    PA_VALIDATION_SIP = "10.10.2.10"
    PA_VALIDATION_DIP = "10.10.2.20"
    INBOUND_ROUTING_VNI = 2
    INNER_VM_IP = "172.19.1.100"
    INNER_REMOTE_IP = "172.19.1.1"

    def setUp(self):
        super(TestSaiVnetInboundTest, self).setUp()

        # Variables
        self.pa_validation_entry = None
        self.inbound_routing_entry = None
        self.eni_ether_address_map_entry = None
        self.eni_id = None
        self.vnet_id = None
        self.out_acl_group_id = None
        self.in_acl_group_id = None
        self.dir_lookup_entry = None
        self.vip_entry = None

    def create_vnet_config(self):

        print("Create VIP")
        self.vip_entry = sai_thrift_vip_entry_t(switch_id = self.SWITCH_ID, vip=sai_ipaddress(self.VIP))
        sai_thrift_create_vip_entry(self.client, self.vip_entry, action=SAI_VIP_ENTRY_ACTION_ACCEPT)
        #assert(status == SAI_STATUS_SUCCESS)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        print("Create direction lookup")
        self.dir_lookup_entry = sai_thrift_direction_lookup_entry_t(switch_id=self.SWITCH_ID, vni=self.DIR_LOOKUP_ENI)
        sai_thrift_create_direction_lookup_entry(self.client, self.dir_lookup_entry,
                                                 action=SAI_DIRECTION_LOOKUP_ENTRY_ACTION_SET_OUTBOUND_DIRECTION)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        # assert(status == SAI_STATUS_SUCCESS)

        print("Create ACL groups")
        self.in_acl_group_id = sai_thrift_create_dash_acl_group(self.client,
                                                           ip_addr_family=SAI_IP_ADDR_FAMILY_IPV4)
        assert self.in_acl_group_id != SAI_NULL_OBJECT_ID
        self.out_acl_group_id = sai_thrift_create_dash_acl_group(self.client,
                                                            ip_addr_family=SAI_IP_ADDR_FAMILY_IPV4)
        assert self.out_acl_group_id != SAI_NULL_OBJECT_ID

        print("Create VNET")
        self.vnet_id = sai_thrift_create_vnet(self.client, vni=self.DIR_LOOKUP_ENI)
        assert (self.vnet_id != SAI_NULL_OBJECT_ID)

        print("Create ENI")
        # eni_id = sai_thrift_create_eni(self.client, vm_vni = 1)
        vm_underlay_dip = sai_thrift_ip_address_t(addr_family=SAI_IP_ADDR_FAMILY_IPV4,
                                                  addr=sai_thrift_ip_addr_t(ip4=self.PA_VALIDATION_DIP))
        self.eni_id = sai_thrift_create_eni(self.client, cps=10000,
                                        pps=100000, flows=100000,
                                        admin_state=True,
                                        vm_underlay_dip=vm_underlay_dip,
                                        vm_vni=9,
                                        vnet_id=self.vnet_id,
                                        inbound_v4_stage1_dash_acl_group_id = self.in_acl_group_id,
                                        inbound_v4_stage2_dash_acl_group_id = self.in_acl_group_id,
                                        inbound_v4_stage3_dash_acl_group_id = self.in_acl_group_id,
                                        inbound_v4_stage4_dash_acl_group_id = self.in_acl_group_id,
                                        inbound_v4_stage5_dash_acl_group_id = self.in_acl_group_id,
                                        outbound_v4_stage1_dash_acl_group_id = self.out_acl_group_id,
                                        outbound_v4_stage2_dash_acl_group_id = self.out_acl_group_id,
                                        outbound_v4_stage3_dash_acl_group_id = self.out_acl_group_id,
                                        outbound_v4_stage4_dash_acl_group_id = self.out_acl_group_id,
                                        outbound_v4_stage5_dash_acl_group_id = self.out_acl_group_id,
                                        inbound_v6_stage1_dash_acl_group_id = 0,
                                        inbound_v6_stage2_dash_acl_group_id = 0,
                                        inbound_v6_stage3_dash_acl_group_id = 0,
                                        inbound_v6_stage4_dash_acl_group_id = 0,
                                        inbound_v6_stage5_dash_acl_group_id = 0,
                                        outbound_v6_stage1_dash_acl_group_id = 0,
                                        outbound_v6_stage2_dash_acl_group_id = 0,
                                        outbound_v6_stage3_dash_acl_group_id = 0,
                                        outbound_v6_stage4_dash_acl_group_id = 0,
                                        outbound_v6_stage5_dash_acl_group_id = 0)
        #self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        self.assertNotEqual(self.eni_id, 0)

        print("Create Addres MAP entry")
        self.eni_ether_address_map_entry = sai_thrift_eni_ether_address_map_entry_t(switch_id=self.SWITCH_ID, address=self.ENI_MAC)
        status = sai_thrift_create_eni_ether_address_map_entry(self.client,
                                                               eni_ether_address_map_entry=self.eni_ether_address_map_entry,
                                                               eni_id=self.eni_id)
        #self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        assert status == SAI_STATUS_SUCCESS

        print("Create inbound routing entry")
        self.inbound_routing_entry = sai_thrift_inbound_routing_entry_t(switch_id=self.SWITCH_ID, vni=self.INBOUND_ROUTING_VNI)
        sai_thrift_create_inbound_routing_entry(self.client, self.inbound_routing_entry,
                                                action=SAI_INBOUND_ROUTING_ENTRY_ACTION_VXLAN_DECAP_PA_VALIDATE)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

        print("Create PA validation entry")
        self.pa_validation_entry = sai_thrift_pa_validation_entry_t(switch_id=self.SWITCH_ID, eni_id=self.eni_id,
                                                               sip=sai_ipaddress(self.PA_VALIDATION_SIP), vni=self.INBOUND_ROUTING_VNI)
        sai_thrift_create_pa_validation_entry(self.client, self.pa_validation_entry,
                                              action=SAI_PA_VALIDATION_ENTRY_ACTION_PERMIT)
        self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

    def remove_vnet_config(self):
        # Delete VNET
        if self.pa_validation_entry:
            print("Delete PA validation entry")
            sai_thrift_remove_pa_validation_entry(self.client, self.pa_validation_entry)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        if self.inbound_routing_entry:
            print("Delete inbound routing entry")
            sai_thrift_remove_inbound_routing_entry(self.client, self.inbound_routing_entry)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        if self.eni_ether_address_map_entry:
            print("Delete Addres MAP entry")
            sai_thrift_remove_eni_ether_address_map_entry(self.client, self.eni_ether_address_map_entry)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        if self. eni_id:
            print("Delete ENI")
            sai_thrift_remove_eni(self.client, self.eni_id)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        if self.vnet_id:
            print("Delete VNET")
            sai_thrift_remove_vnet(self.client, self.vnet_id)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        if self.out_acl_group_id:
            print("Delete Out ACL groups")
            sai_thrift_remove_dash_acl_group(self.client, self.out_acl_group_id)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        if self.in_acl_group_id:
            print("Delete In ACL groups")
            sai_thrift_remove_dash_acl_group(self.client, self.in_acl_group_id)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        if self.dir_lookup_entry:
            print("Delete direction lookup")
            sai_thrift_remove_direction_lookup_entry(self.client, self.dir_lookup_entry)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)
        if self.vip_entry:
            print("Delete VIP")
            sai_thrift_remove_vip_entry(self.client, self.vip_entry)
            self.assertEqual(self.status(), SAI_STATUS_SUCCESS)

    def run_traffic_check(self):
        # Check forwarding

        outer_smac = "00:0a:05:06:06:06"
        outer_dmac = "00:0b:05:06:06:06"
        inner_smac = "00:0a:04:06:06:06"
        inner_dmac = "00:0b:04:06:06:06"

        # PAcket to send
        inner_pkt = simple_udp_packet(eth_dst=self.ENI_MAC,
                                        eth_src=inner_smac,
                                        ip_dst=self.INNER_VM_IP,
                                        ip_src=self.INNER_REMOTE_IP)
        vxlan_pkt = simple_vxlan_packet(eth_dst=outer_dmac,
                                        eth_src=outer_smac,
                                        ip_dst=self.PA_VALIDATION_DIP,
                                        ip_src=self.PA_VALIDATION_SIP,
                                        udp_sport=11638,
                                        with_udp_chksum=False,
                                        vxlan_vni=self.DIR_LOOKUP_ENI,
                                        inner_frame=inner_pkt)

        # Expected Packet to check
        inner_exp_pkt = simple_udp_packet(eth_dst=inner_dmac,
                                            eth_src=self.ENI_MAC,
                                            ip_dst=self.INNER_VM_IP,
                                            ip_src=self.INNER_REMOTE_IP)
        vxlan_exp_pkt = simple_vxlan_packet(eth_dst="00:00:00:00:00:00",
                                        eth_src="00:00:00:00:00:00",
                                        ip_dst=self.PA_VALIDATION_DIP,
                                        ip_src=self.PA_VALIDATION_SIP,
                                        udp_sport=0,
                                        with_udp_chksum=False,
                                        vxlan_vni=self.INBOUND_ROUTING_VNI,
                                        inner_frame=inner_exp_pkt)
        # TODO: Fix IP chksum
        vxlan_exp_pkt[IP].chksum = 0
        # TODO: Fix UDP length
        vxlan_exp_pkt[IP][UDP][VXLAN].flags = 0

        print("\nSending outbound packet...\n\n", vxlan_pkt.__repr__())
        send_packet(self, 0, vxlan_pkt)

        print("\nVerifying packet...\n", vxlan_exp_pkt.__repr__())
        verify_packet(self, vxlan_exp_pkt, 0)

        print ("run_traffic_check OK")

    def runTest(self):
        self.create_vnet_config()
        # self.run_traffic_check()
        self.remove_vnet_config()

    def tearDown(self):
        super(TestSaiVnetInboundTest, self).tearDown()
