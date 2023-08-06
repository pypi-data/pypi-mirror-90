from shishito.runtime.platform.shishito_execution import ShishitoExecution


class ControlExecution(ShishitoExecution):
    """ ControlExecution for generic platform"""

    def get_test_result_prefix(self, config_section):
        """ Create string prefix for test results.

        :param str config_section: section in platform/environment.properties config
        :return: str with test result prefix
        """

        return 'generic'

    def run_tests(self):
        """ Trigger PyTest runner. Run PyTest for for generic tests. """

        return self.trigger_pytest('generic')
