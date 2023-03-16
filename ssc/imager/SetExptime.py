import time
import ktl

from ssc.SSCTranslatorFunction import SSCTranslatorFunction
from ddoitranslatormodule.ddoiexceptions import DDOIExceptions



class SetExptime(SSCTranslatorFunction):
    '''Sets the exposure time for the SSC in the magiq keyword service.
    
    Args:
    Exptime - The exposure time in seconds
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        SetExptime.check_input(args, 'Exptime', allowed_types=[int, float])
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        magiq = ktl.cache('magiq')
        ttime = args.get('TTIME')
        logger.debug(f"Setting exposure time to {ttime:.3f}")
        magiq['TTIME'].write(ttime)
        magiq['camcmd'].write('start')

    @classmethod
    def post_condition(cls, args, logger, cfg):
        logger.debug("Checking for success")
        ttime = args.get('TTIME')
        magiq = ktl.cache('magiq')
        magiqttime = magiq.read('TTIME')
        if magiqttime!=ttime:
            raise DDOIExceptions.FailedToReachDestination(magiqttime, ttime)
        else:
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
