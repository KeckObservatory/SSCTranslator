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
        cls.check_inputs(args, 'exptime', allowed_types=[int, float])
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        service = cfg['magiq']['service_name']
        magiq = ktl.cache(service)
        ttime = args.get('exptime')
        logger.debug(f"Setting exposure time to {ttime:.3f} for service {service}")
        magiq['TTIME'].write(ttime)
        magiq['camcmd'].write('start')

    @classmethod
    def post_condition(cls, args, logger, cfg):
        service = cfg['magiq']['service_name']
        logger.debug(f"Checking for success for service {service}")
        ttime = args.get('Exptime')
        magiq = ktl.cache(service)
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
        args_to_add['exptime'] = {'type': float,
                                  'help': 'The exposure time in seconds.'}
        parser = cls._add_args(parser, args_to_add, print_only=False)
        return super().add_cmdline_args(parser, cfg)
