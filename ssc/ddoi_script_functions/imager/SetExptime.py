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
        check_input(args, 'Exptime', allowed_types=[int, float])
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        magiq = ktl.cache('magiq')
        ttime = args.get('TTIME')
        log.debug(f"Setting exposure time to {ttime:.3f}")
        magiq['TTIME'].write(ttime)
        magiq['camcmd'].write('start')

    @classmethod
    def post_condition(cls, args, logger, cfg):
        log.debug("Checking for success")
        ttime = args.get('TTIME')
        tol = cfg.get('tolerances', 'sscexpose_exptime_tolerance', fallback=0.01)
        timeout = cfg.get('times', 'sscexpose_response_time', fallback=1)
#?       expr = (f"($ssc.EXPOSURE >= {ttime-tol}) and "
#?                f"($ssc.EXPOSURE <= {ttime+tol})")
        log.debug(expr)
        success = ktl.waitFor(expr, timeout=timeout)
#?        if success is not True:
#?            exposure = ktl.cache('kpfexpose', 'EXPOSURE')
#?            raise FailedToReachDestination(exposure.read(), exptime)

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
