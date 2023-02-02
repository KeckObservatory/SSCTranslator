import time
import ktl

from ddoitranslatormodule.SSCTranslatorFunction import SSCTranslatorFunction
from .. import (log, SSCException, FailedPreCondition, FailedPostCondition,
                FailedToReachDestination, check_input)


class SetFrameNumber(SSCTranslatorFunction):
    '''Sets the image frame number for the SSC in the magiq keyword service.
    
    Args:
    frame - The frame number for saving images
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        check_input(args, 'frame', allowed_types=[int])
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        magiq = ktl.cache('magiq')
        frame = args.get('frame')
        log.debug("Setting frame number to "+frame)
        magiq['IMGFRNR'].write(frame)
        magiq['IMGCMD'].write('set')

    @classmethod
    def post_condition(cls, args, logger, cfg):
        log.debug("Checking for success")
        frame = args.get('frame')
        magiq = ktl.cache('magiq')
        magiqframe=magiq.read('IMGFRNR')
        if magiqframe!=frame:
            raise FailedToReachDestination(magiqframe, frame)
        else:
            return True

    @classmethod
    def add_cmdline_args(cls, parser, cfg=None):
        '''The arguments to add to the command line interface.
        '''
        from collections import OrderedDict
        args_to_add = OrderedDict()
        args_to_add['frame'] = {'type': int,
                                  'help': 'The frame number for saving images.'}
        parser = cls._add_args(parser, args_to_add, print_only=False)
        return super().add_cmdline_args(parser, cfg)
