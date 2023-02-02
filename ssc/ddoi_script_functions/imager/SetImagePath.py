import time
import ktl

from ddoitranslatormodule.SSCTranslatorFunction import SSCTranslatorFunction
from .. import (log, SSCException, FailedPreCondition, FailedPostCondition,
                FailedToReachDestination, check_input)


class SetImagePath(SSCTranslatorFunction):
    '''Sets the image save path for the SSC in the magiq keyword service.
    
    Args:
    Image Path - The path for saving images
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        check_input(args, 'path', allowed_types=[str])
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        magiq = ktl.cache('magiq')
        path = args.get('path')
        log.debug("Setting exposure time to "+path)
        magiq['IMGDIR'].write(path)
        magiq['IMGCMD'].write('set')

    @classmethod
    def post_condition(cls, args, logger, cfg):
        log.debug("Checking for success")
        path = args.get('path')
        magiq = ktl.cache('magiq')
        magiqpath=magiq.read('IMGDIR')
        if magiqpath!=path:
            raise FailedToReachDestination(magiqpath, path)
        else:
            return True

    @classmethod
    def add_cmdline_args(cls, parser, cfg=None):
        '''The arguments to add to the command line interface.
        '''
        from collections import OrderedDict
        args_to_add = OrderedDict()
        args_to_add['path'] = {'type': str,
                                  'help': 'The path for saving images.'}
        parser = cls._add_args(parser, args_to_add, print_only=False)
        return super().add_cmdline_args(parser, cfg)
