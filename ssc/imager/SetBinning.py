import time
import ktl

from ssc.SSCTranslatorFunction import SSCTranslatorFunction
from ddoitranslatormodule.ddoiexceptions import DDOIExceptions

class SetBinning(SSCTranslatorFunction):
    '''Sets the binning for the SSC in the magiq keyword service.
    
    Args:
    Binning - The binning value 1, 2, 4, 8
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        if not cls.check_inputs(args, 'binning', allowed_types=[int]):
            logger.error("")
            raise DDOIExceptions.DDOIInvalidArguments(f"'Binning' argument not found")
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        service = cfg['magiq']['service_name']
        magiq = ktl.cache(service)
        binning = args.get('binning')
        logger.debug(f"Setting binning to {binning:.3f}")
        magiq['BINNING'].write(binning)
        magiq['camcmd'].write('set')

    @classmethod
    def post_condition(cls, args, logger, cfg):
        service = cfg['magiq']['service_name']
        magiq = ktl.cache(service)
        logger.debug("Checking for success")
        binning = args.get('binning')
        magiqbin = magiq['BINNING'].read()
        logger.debug(f"Checking binning: Requsted {binning:.3f}, Actual {binning:.3f} ")

        if magiqbin==binning:
            success=True
        else:
            success=False

    @classmethod
    def add_cmdline_args(cls, parser, cfg=None):
        '''The arguments to add to the command line interface.
        '''
        from collections import OrderedDict
        args_to_add = OrderedDict()
        args_to_add['binning'] = {'type': int,
                                  'help': 'The number of pixels to bin.'}
        parser = cls._add_args(parser, args_to_add, print_only=False)
        return super().add_cmdline_args(parser, cfg)
