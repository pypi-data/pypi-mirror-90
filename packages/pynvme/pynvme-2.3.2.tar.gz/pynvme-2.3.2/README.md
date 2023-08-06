<img src="https://github.com/pynvme/pynvme/raw/master/doc/logo.jpg" width="256" align="right" />

# pynvme: builds your own tests.

Pynvme is an user-space NVMe test driver with Python API. It is an open, fast, and extensible solution for SSD developers and test engineers to build their own tests intuitively.

## Features

1. access PCI configuration space
1. access NVMe registers in BAR space
1. send any NVMe admin/IO commands
1. support callback functions for NVMe commands
1. support MSI/MSIx interrupts
1. transparent checksum verification on every LBA
1. generates IO workload of high performance and low latency
1. support multiple namespaces
1. support multiple tests on different controllers
1. integrate with pytest
1. integrate with VSCode to display cmdlog in GUI
1. support NVMe over TCP targets
1. HMB: Host Memory Buffer (PyNVMe3 only)
1. ZNS: Zoned Namespace (PyNVMe3 only)
1. TCG (PyNVMe3 only)

## Links

### Repositories
* GitHub: [https://github.com/pynvme/pynvme](https://github.com/pynvme/pynvme)
* Mirror: [https://gitee.com/pynvme/pynvme](https://gitee.com/pynvme/pynvme)

### Documents

* Web: [https://pynvme.readthedocs.io/](https://pynvme.readthedocs.io/)
* PDF: [https://buildmedia.readthedocs.org/media/pdf/pynvme/latest/pynvme.pdf](https://buildmedia.readthedocs.org/media/pdf/pynvme/latest/pynvme.pdf)

### Presentation

* Introduction: [pynvme builds your own tests.](https://raw.githubusercontent.com/cranechu/pynvme/master/doc/_static/pynvme_builds_your_own_tests.pdf)
* SPDK PRC Summit 2019, Beijing. Why SSD Developers Need Pynvme and Why Pynvme Needs SPDK. [pdf](https://raw.githubusercontent.com/cranechu/pynvme/master/doc/_static/02_Presentation_26_Why_SSD_Developers_Need_Pynvme_and_Why_Pynvme_Needs_SPDK_Crane.pdf), [video](https://www.youtube.com/watch?v=Zg-vliodKx0).
* SDC2020. Pynvme: an Open, Fast and Extensible NVMe SSD Test Tool. [pdf](https://raw.githubusercontent.com/cranechu/pynvme/master/doc/_static/pynvme_chu_sdc2020.pdf), [video](https://www.youtube.com/watch?v=Yoru7vzVyL8).
  
### Contact

* Email: sales@pynv.me
