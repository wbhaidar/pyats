'''
PROJ2.py

'''
# see https://pubhub.devnetcloud.com/media/pyats/docs/aetest/index.html
# for documentation on pyATS test scripts

# optional author information
# (update below with your contact information if needed)
__author__ = 'Cisco Systems Inc.'
__copyright__ = 'Copyright (c) 2019, Cisco Systems Inc.'
__contact__ = ['pyats-support-ext@cisco.com']
__credits__ = ['list', 'of', 'credit']
__version__ = 1.0

import logging

from pyats import aetest
from genie.utils import Dq
from genie.conf import Genie
from ats.log.utils import banner
#from genie.testbed import load

# create a logger for this module
logger = logging.getLogger(__name__)

param1 = "abc"

class CommonSetup(aetest.CommonSetup):

#    @aetest.subsection
#    def load_testbed(self, testbed):
#        # Convert pyATS testbed to Genie Testbed
#        logger.info(
#            "Converting pyATS testbed to Genie Testbed to support pyATS Library features"
#        )
#        testbed = load(testbed)
#        self.parent.parameters.update(testbed=testbed)



    @aetest.subsection
    def connect(self, testbed):
        '''
        establishes connection to all your testbed devices.
        '''
        # make sure testbed is provided
        assert testbed, 'Testbed is not provided!'

        try:
            testbed.connect()
        except (TimeoutError, StateMachineError, ConnectionError):
            logger.error("Unable to connect to all devices")


 # Get specified testbed

#        genie_testbed = Genie.init(testbed)
      # Save in environment variables
#        self.parent.parameters['testbed'] = genie_testbed
#        device_list = []
        # Try connect one by one and save device objects in a list
#        for device in genie_testbed.devices.values():
#            logger.info(banner( "Connect to device '{d}'".format(d=device.name)))
#            try:
#                    device.connect(init_exec_commands=[], init_config_commands=[], log_stdout=False)
#            except Exception as e:
#                   self.failed("Failed to establish connection to '{}'".format(device.name))
#            device_list.append(device)
#
#        self.parent.parameters.update(dev=device_list)
#        print('device list {}'.format(device_list))

    @aetest.subsection
    def print(self, testbed):
        print(self)
        print(type(self))
        print(self.parent.parameters)
        print('parameters.testbed %s' % self.parent.parameters['testbed'])


#        print(self.parent.parameters['dev'])

class verify_connected(aetest.Testcase):
    """verify_connected

    Ensure successful connection to all devices in testbed.

    """
    @aetest.test
    def test(self, testbed, steps):
        # Loop over every device in the testbed
        for device_name, device in testbed.devices.items():
            logger.warn(f"device_name is {device_name} and device is {device}")
            with steps.start(
                f"Test Connection Status of {device_name}", continue_=True
            ) as step:
                # Test "connected" status
                if device.connected:
                    logger.info(f"{device_name} connected status: {device.connected}")
                else:
                    logger.error(f"{device_name} connected status: {device.connected}")
                    step.failed()



class CHECK_VER(aetest.Testcase):
    '''testcase_one

    < docstring description of this testcase >

    '''

    # testcase groups (uncomment to use)
    # groups = []

    @aetest.setup
    def setup(self):
        logger.info('This is a sample message that has been logged using logger info')
        print('THIS iS A MESSAGE VIA PRINT')
        devices=self.parent.parameters['dev']
        aetest.loop.mark(self.check_ver, device=devices)

    @aetest.test
    def check_ver(self,device):
        parsed_v1 = device.parse("show version")
        parsed_v2 = Dq(parsed_v1).get_values('version_short')
        parsed_v3 = parsed_v2[0]

        logger.warning('param2: %s' % param2)
        if not parsed_v3 == device.custom.version:
            self.failed(f"{device.name} is not running {device.custom.version}, but {parsed_v3}",)
        else :
            self.passed(f"{device.name} is running the correct version: {parsed_v3}")

#        parsed_version = device.parse("show version")
#        v_installed=Dq(parsed_version).get_values('version_short')
#        v_installed=parsed_version['version_short']

#        logger.warning('param: %s' % param1)
        logger.warning('param2: %s' % param2)
#        logger.warning('ver_installed: %s' %parsed_version)
#        logger.warning('v_installed: %s' %v_installed)
#        logger.warning('ver_required: %s' %device.custom.ver)
        pass

    @aetest.cleanup
    def cleanup(self):
        pass
    

class testcase_two(aetest.Testcase):
    '''testcase_two

    < docstring description of this testcase >

    '''

    # testcase groups (uncomment to use)
    # groups = []

    @aetest.setup
    def setup(self):
        pass

    # you may have N tests within each testcase
    # as long as each bears a unique method name
    # this is just an example
    @aetest.test
    def test(self):
        pass

    @aetest.cleanup
    def cleanup(self):
        pass
    


class CommonCleanup(aetest.CommonCleanup):
    '''CommonCleanup Section

    < common cleanup docstring >

    '''

    # uncomment to add new subsections
    # @aetest.subsection
    # def subsection_cleanup_one(self):
    #     pass

if __name__ == '__main__':
    # for stand-alone execution
    import argparse
    from pyats import topology

    parser = argparse.ArgumentParser(description = "standalone parser")
    parser.add_argument('--testbed', dest = 'testbed',
                        help = 'testbed YAML file',
                        type = topology.loader.load,
                        default = None)

    # do the parsing
    args = parser.parse_known_args()[0]
    print(args.testbed)
    aetest.main(testbed = args.testbed)

