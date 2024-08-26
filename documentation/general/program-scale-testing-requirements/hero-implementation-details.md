# Hero test from theory to practice

## Introduction

Hero test is a synthetic test ment to stress the device under the worst case scenario. Reality is that worst case for device A is not necesary worst case for device B also any vendor desire is not to showcase only the worst case but they want also to showcase the best case. Knowing both the best and worst case is valuable because in production the expected performance will be somwhere between best and worst case case, knowing the lower and upperl limit will provide a good understanding of the device performance.

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

testbed1 

![testbed1](./testbed1.svg)

testbed2 

![testbed2](./testbed2.svg)

testbed3 

![testbed3](./testbed3.svg)


>**NOTE**: At this point all hardware should be in the lab powered on, accesible via IP and have link up on all the interfaces.


### "1 IP" test

Minimum config posible to run traffic through. 

#### Objectives

##### validate the hardware and software. 

It ensures we can program the DPU via private API, SAI or DASH and that we can pass 1 packets end to end from traffic generator through the device under test and back.

##### can also provide best case scenario performance numbers

its a maybe because 1 packets replicated milions of times may not necesarly work best for all hardware implementations.


### Baby Hero test

It is ment to be an intermediary step between 1 IP test and Hero test. 

We try to keep the scale at ~1% of hero test by using only one prefix per ACL instead of 100

| Metric                       | Baby Hero | % of HERO  |
|------------------------------|-----------|------------|
| VNIs                         | 32        | 3%         |
| ENIs                         | 32        | 100%       |
| NSGs per ENI                 | 10        | 100%       |
| NSGs                         | 320       | 100%       |
| ACL rules per NSG            |  1,000    | 100%       |
| ACL rules                    |  320,000  | 100%       |
| ACL prefixes per ACL rule    | 1         | 1%         |
| ACL prefixes                 |  320,000  | 1%         |
| ACL ports                    | NA        | 0%         |
| VNETs (Outbound)             | 32        | 100%       |
| Outbound routes per ENI      | 5K        |            |
| Outbound routes              | 160K      | 5%         |
| CA-to-PA mapping (Outbound)  | 80320     | 1%         |
| Inbound Routes per ENI       | 1         | 0%         |
| Inbound Routes               | 32        | 100%       |
| PAs (Inbound PA Validation)  | 32        | 100%       |


### In between scale

If Hero test scale numbers cannot be met we can add another checkpoint to gather aditional data before final implementation is ready

### Hero test

The test exactly as specified in the DASH requirements.

### Best case scenario

If we can find a scenario where we obtain better performance numbers then the numbers previously obtained during (1ip, baby hero, hero test ...) this will be added as a new data point to the results.

### Worst case scenario

If we can find a scenario where we obtain lower performance numbers then the numbers previously obtained during (1ip, baby hero, hero test ...) this will be added as a new data point to the results.


## Metrics

Besides CPS we actualy colect for all those dieferent scale points multiple metrics.

### PPS

PPS (packets per second) is the first metric we colect. Usualy it is UDP packets are used
Packets must be as small as posible so we do not to hit link speed constranints.
This test shows the fast path perfromance.

### Latency

Latency is the time it takes for a packet to go through the device under test.

Latency value is most acurate when we have highest PPS, smallest packet, and zero packet loss. and is measured using Ixnetwork and Novus card.

When testing the smart switch we have to run a test to get the switch latency without running the traffic through the DPU and then get the total system latency with the understanding that each packets travel once through the NPU to reach the DPU, than it travel through teh DPU and once more it will travel through teh NPU after it leave the DPU. 

smart switch latency = 2 x NPU latency + DPU latency

Latency is mostly a metric for fast path performance. Since we colect min/avg/max, max value in most cases will be impacted by the slow path. that first packet that arives may have the highest latency.

If slow path latency is desired configure random source/dest ports this way each packet will be a new flow and will hit the slow path only. care must be taken to send a fixed amount of packets not exceeding the flow table size.

### Throughput

Throughput is the amount of data that can be sent through the device under test.

Set PPS to a value lower than max PPS we measured in previous test and increase the packet size until we reach the max throughput.

PPM may need to be adjusted between test gear and device under test to get that 100G or 200G or 400G perfect number.

Consider looking at UHD400C stats and when looking at IxNetwork/Ixload stats will show less because the vxlan header is added later by UHD so we are interested in packet size as it enters the DPU x pps to get the throughput.


### CPS

CPS (connection per second) this is a metric that shows the slow path performance and we can get both TCP and UDP values.

For TCP we use IxLoad since it has full TCP stack that is very configurable and can simulate a lot of diferent scenarios.

While the hero test calls for 6 TCP packets SYN/SYNACK/ACK/FIN/FINACK/ACK, we make use of HTTP as aplication tha runs over TCP and on the wire we will end up with 7 packets for every conection. 

PPS used for CPS test can be sen the the L23 stats in IxLoad.

Keep an eye on TCP failures on client and server a retransmit is bad it simbolizes packet drop that was detected and TCP stack had to rentransmit. a conection drop is super extra bad it means even after 3-5 retries packet did not made it. 

We also look at number of concurent conection while the test is running. traffic generator puts on the wire equaly time spaced SYN packets to match the desired CPS but rest of comunication happens as fast as posible. impacted by line rate and latency. in theory if line rate is high and latency low the whole exchange of 7 packets could finish before the next SYN is sent resulting in 0 concurent conection. (flow table will be 1), while a slow travel time for packets will results in conections that have not been terminated yet as new connections get initiated and this will result in a certain number concurent connection. Idealy we want to see the concurent conection number as low as posible.

test trys to cycle through all the milions of IPs, source port is chosen at random in a specified range and destination port is fixed to 80

we can do variations like witch side initiates the fin and see if we observe and diferences in perfromance

for UDP CPS slow path test use random source/dest ports and send a fixed amount of packets not exceeding the flow table size.

Note down the bandwith utilized by the CPS test.

### Flow table size

Flow timer must be set to a very high value so flows do not expire during the test

For TCP we set the desired number of concurent conection and make sure we have a transaction rate that is a bit faster than the flow timer to make sure flows do not expire.

for UDP we use random source/destination ports and we set rate to 100K pps and for 32M flows it shoudl work fine for 320 seconds.

we look here that flow table can be filed to desired level.

one item to note here is to caracterize what happens when flow table is full. will it crash? will it drop anything after ? will it all extra packets be procesed as slow path?

### Baground  UDP flows


### Baground  UDP flows


### Hero test

Puting it all togather and running CPS test with backround traffic.

Start first the backround traffic and ensure the flow table is close to full but not full (need room for CPS), increase packet size to ensure bandwith is utilized at 100% - bandwitch needed by CPS test - a 5%-10% margin

Run the CPS

Provided each component of hero test was ran in isolation before it should all work when combined and provide performance numbers usualy lower than the standalone CPS numbers

### Loss

It must be 0 (zero) but this is a hard topic and requires caracterization that is vendor to vendor specific.

We gather few datapoint here:
- zero loss performance
- minimal loss performance (hundreds/thousdans packet lost)
- point after which everything gets lost

![loss](./loss.svg)


## The results

Results are presented as a graph trying to show a performance band, if the tests are done corectly the real performance in production should be somewhere in that band.

Idealy the diference between highest point and lowets point should be as small as posible and lowest point is above the minimum DASH requirment.

![results](./results.svg)

best case scenario: is the scale and traffic profile where the hardware obtains the best performance numbers, highest point in the graph
worst case scanrio: is the scale and traffic profile where the hardware obtains the worst performance numbers, lowest point in the graph












