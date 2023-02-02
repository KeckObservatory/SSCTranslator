import time
import ktl

from ddoitranslatormodule.SSCTranslatorFunction import SSCTranslatorFunction
from .. import (log, SSCException, FailedPreCondition, FailedPostCondition,
                FailedToReachDestination, check_input)


class SetExptime(SSCTranslatorFunction):
    '''Sets the exposure time for the SSC in the magiq keyword service.
    
    Args:
    Exptime - The exposure time in seconds
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        magiq = ktl.cache('magiq')
        log.debug("Taking Exposure")
        magiq['camcmd'].write('start')

    @classmethod
    def post_condition(cls, args, logger, cfg):
        return True

    @classmethod
    def add_cmdline_args(cls, parser, cfg=None):
        '''The arguments to add to the command line interface.
        '''
        from collections import OrderedDict
        args_to_add = OrderedDict()
        args_to_add['Exptime'] = {'type': float,
                                  'help': 'The exposure time in seconds.'}
        parser = cls._add_args(parser, args_to_add, print_only=False)
        return super().add_cmdline_args(parser, cfg)
