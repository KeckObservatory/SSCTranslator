import time
import ktl

from SSCTranslatorFunction import SSCTranslatorFunction
from ddoitranslatormodule.ddoiexceptions import DDOIExceptions



class SetImageSave(SSCTranslatorFunction):
    '''Sets the image saving parameter for the SSC in the magiq keyword service.
    
    Args:
    Image Save - Turns image saving on/off
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        cls.check_input(args, 'save', allowed_types=[bool])
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        magiq = ktl.cache('magiq')
        save = args.get('save')
        logger.debug("Setting image saving to "+str(save))
        if save==True:
            magiq['mqsnpff'].write(1)
        else:
            magiq['mqsnpff'].write(0)


    @classmethod
    def post_condition(cls, args, logger, cfg):
        logger.debug("Checking for success")
        save = args.get('save')
        magiq = ktl.cache('magiq')
        magiqsave=magiq.read('mqsnpff')
        if save!=bool(magiqsave):
            raise DDOIExceptions.FailedToReachDestination(magiqsave, save)
        else:
            return True

    @classmethod
    def add_cmdline_args(cls, parser, cfg=None):
        '''The arguments to add to the command line interface.
        '''
        from collections import OrderedDict
        args_to_add = OrderedDict()
        args_to_add['save'] = {'type': bool,
                                  'help': 'Set image saving to True/False.'}
        parser = cls._add_args(parser, args_to_add, print_only=False)
        return super().add_cmdline_args(parser, cfg)
