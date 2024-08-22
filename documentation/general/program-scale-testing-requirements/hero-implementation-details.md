# Hero test from theory to practice

## Introduction

Hero test is a syntetic test ment to stress the device under the worst case scenario. Reality is that worst case for device A is not necesary worst case for device B also any vendor desire is not to showcase only the worst case but they want also to showcase the best case. Knowing both the best and worst case is valuable because in production the expected performance will be somwhere between best and worst case case, knowing the lower and upperl limit will provide a good understanding of the device performance.

This is why the implemenentation of hero test is actualy a colection of tests that colect multiple metrics.

## Life cycle

### Hardware and setup bringup

#### Common topologies:

End objective is to test the smartswitch, but we can start testing much earlied by using a standalone DPU or by combinint a switch with an appliance. 

###### stand alone DPU

Comes in form on a PCIE card. Small in size, lower price, easy to ship, already available. Used for the initial testing and validation of a single ASIC.

###### appliance

An enclosure/server hosting multiple DPUs. Combined with a switch can provide a deployment with of the shelf components for an out of server solution.

###### smart switch

Fully integrated solution of a switching ASIC with multiple DPU ASICs. 


#### Test Tools packet generator (keysight version)

One solution to test the smart switch is makeing use of Keysight(Ixia) packet generator for TCP traffic we use CloudStorm & IxLoad and for UDP traffic we use Novus & IxNetwork and it is all mixed in by the UHD Connect.

https://github.com/sonic-net/sonic-mgmt/blob/master/docs/testbed/README.testbed.Keysight.md 
https://www.keysight.com/us/en/products/network-test/network-test-hardware/cloudstorm-100ge-2-port.html
https://www.keysight.com/us/en/products/network-test/network-test-hardware/novus-qsfp28-1005025ge.html
https://www.keysight.com/us/en/product/944-1188/uhd400t.html
https://www.keysight.com/us/en/products/network-test/network-test-hardware/xgs12-chassis-platform.html

Amount of hardware needed varies based on the device performance. Curent DASH requirment specifies 24M CPS as minimum requirment but each vendor wants to showcase how much more they can do so based on that plus adding a 10%-20% for the headroom we can calculate the amount of hardware needed. 

### Puting everything togather

#### Cables

Most cost efective is to use DAC cables, but if equipemnt is in diferent racks optical fibers will be required. We also make use of breakout cables 1x400G to 4x100G to connect UHD400C to CloudSTorm and Novus.

#### Layer 1 considerations

- DASH device port speeds are 100G or 200G or 400G, PAM4 or NRZ are UHD400C device port speeds are 100G or 200G or 400G, PAM4 or NRZ so far the 2 should interface with no issues.
- IEEE defaults autoneg is preferable but at a minimum if AN is disabled please ensure FEC is enabled. With FEC disabled we observed few packet drops in the DACs and that can create a lot of hasle hunting down a lost packet that has nothing to do with DASH performance.  

#### Testbed examples

Few examples bellow with 100G cables, with 400G cables with fanout cables, single DPU or applaince or smartswitch.
- testbed1 ![testbed1](./testbed1.svg)
- testbed2 ![testbed2](./testbed2.svg)
- testbed3 ![testbed3](./testbed3.svg)

### "1 IP" test

