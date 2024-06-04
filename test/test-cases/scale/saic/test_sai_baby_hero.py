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

    def create_baby_hero_config(self):
    #     """ Generate a configuration
    #         returns iterator (generator) of SAI records
    #     """
    #     conf = dpugen.sai.SaiConfig()
    #     # sets config size to 1% of the hero test size
    #     conf.mergeParams()
    #     conf.generate()
    #     ret = conf.items()
    #     return ret


        # confgen = sai.SaiConfig()
        # # confgen = sai.SaiConfig(baby_hero_params)
        # confgen.merge_params(baby_hero_params)
        # confgen.generate()

        current_file_dir = Path(__file__).parent
        with (current_file_dir / 'config_baby_hero.json').open(mode='r') as config_file:
            baby_hero_commands = json.load(config_file)
        return baby_hero_commands


    @pytest.mark.snappi
    def test_create_vnet_config(self, dpu):
        """Generate and apply configuration"""
        results = [*dpu.process_commands( (self.create_baby_hero_config()) )]
        print("\n======= SAI commands RETURN values =======")
        pprint(results)





    @pytest.mark.snappi
    def test_remove_vnet_config(self, dpu, dataplane):
        """
        Generate and remove configuration
        We generate configuration on remove stage as well to avoid storing giant objects in memory.
        """
        import pdb; pdb.set_trace()
        cleanup_commands = []
        for cmd in reversed(self.create_baby_hero_config()):
            cleanup_commands.append({'name': cmd['name'], 'op': 'remove'})

        for cleanup_command in cleanup_commands:
            try:
                result = [*dpu.process_commands([cleanup_command])]
                #print("\n======= SAI commands RETURN values =======")
                #pprint(result)
            except Exception as e:
                pass
                #print(f"Error during cleanup: {e}")


    # def make_remove_vnet_config(self):
    #     """ Generate a configuration to remove entries
    #         returns iterator (generator) of SAI records
    #     """
    #     cleanup_commands = reversed(self.make_create_vnet_config())
    #     for cmd in cleanup_commands:
    #         cmd['op'] = 'remove'
    #         yield cmd
    #     return