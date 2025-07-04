"""
proj2.py

pyATS test script to:
1. Connect to all devices in a testbed
2. Verify connectivity
3. Check device OS versions
"""

import logging
from pyats import aetest
from genie.utils import Dq
from genie.conf import Genie
from ats.log.utils import banner
from unicon.core.errors import ConnectionError, StateMachineError

# Configure logger
logger = logging.getLogger(__name__)

class CommonSetup(aetest.CommonSetup):
    """Common setup for connecting to devices and storing references."""

    @aetest.subsection
    def connect(self, testbed):
        """Connect to all devices in the provided testbed."""
        assert testbed, 'Testbed is not provided!'
        logger.info("Initializing Genie testbed...")

        genie_testbed = Genie.init(testbed)
        self.parent.parameters['testbed'] = genie_testbed
        device_list = []

        for device in genie_testbed.devices.values():
            logger.info(banner(f"Connecting to device '{device.name}'"))
            try:
                device.connect(
                    init_exec_commands=[],
                    init_config_commands=[],
                    log_stdout=False
                )
                logger.info(f"Connected to {device.name}")
                device_list.append(device)
            except Exception as e:
                logger.error(f"Failed to connect to {device.name}: {e}")
                self.failed(f"Connection to '{device.name}' failed.")

        self.parent.parameters.update(dev=device_list)

    @aetest.subsection
    def print_parameters(self):
        """Print shared testbed parameters for debug."""
        logger.debug("Printing test parameters:")
        logger.debug(f"{self.parent.parameters}")

class VerifyConnected(aetest.Testcase):
    """Verify all devices are connected."""

    @aetest.test
    def test_connection(self, testbed, steps):
        """Ensure each device has an active connection."""
        for device_name, device in testbed.devices.items():
            with steps.start(f"Check connection for {device_name}", continue_=True) as step:
                if device.connected:
                    logger.info(f"{device_name} is connected.")
                else:
                    logger.error(f"{device_name} is NOT connected.")
                    step.failed()

class CheckVersion(aetest.Testcase):
    """Check that each device is running the expected OS version."""

    @aetest.setup
    def loop_over_devices(self):
        """Loop this test over each device."""
        devices = self.parent.parameters.get('dev', [])
        aetest.loop.mark(self.check_version, device=devices)

    @aetest.test
    def check_version(self, device):
        """Compare parsed version with expected version."""
        try:
            parsed_output = device.parse("show version")
            actual_version = Dq(parsed_output).get_values("version_short")[0]
            expected_version = device.custom.version

            if actual_version != expected_version:
                self.failed(f"{device.name} is running {actual_version}, expected {expected_version}")
            else:
                self.passed(f"{device.name} is running expected version {actual_version}")

        except Exception as e:
            self.failed(f"Version check failed for {device.name}: {e}")

class PlaceholderTest(aetest.Testcase):
    """Testcase scaffold for future logic."""

    @aetest.test
    def placeholder(self):
        logger.info("Placeholder for additional logic.")

class CommonCleanup(aetest.CommonCleanup):
    """Common cleanup section for disconnecting devices, if needed."""
    @aetest.subsection
    def disconnect_all(self):
        devices = self.parent.parameters.get('dev', [])
        for device in devices:
            if device.connected:
                logger.info(f"Disconnecting from {device.name}")
                device.disconnect()

if __name__ == '__main__':
    import argparse
    from pyats import topology

    parser = argparse.ArgumentParser(description="Standalone pyATS script")
    parser.add_argument('--testbed', dest='testbed',
                        help='Path to testbed YAML file',
                        type=topology.loader.load,
                        default=None)
    args = parser.parse_known_args()[0]
    aetest.main(testbed=args.testbed)
