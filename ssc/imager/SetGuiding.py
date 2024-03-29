import time
import ktl

from ssc.SSCTranslatorFunction import SSCTranslatorFunction


class SetGuiding(SSCTranslatorFunction):
    '''Sets the guiding for the SSC in the magiq keyword service.
    
    Args:
    Guiding - Turns guiding on or off
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        cls.check_inputs(args, 'guiding', allowed_types=[bool])
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        service = cfg['magiq']['service_name']
        magiq = ktl.cache(service)
        guiding = args.get('guiding')
        logger.debug("Setting guiding to "+guiding)
        if guiding==True:
            magiq['mqstopg'].write(1)
        else:
            magiq['mqstopg'].write(0)
        magiq['camcmd'].write('set')

    @classmethod
    def post_condition(cls, args, logger, cfg):
        return True

    @classmethod
    def add_cmdline_args(cls, parser, cfg=None):
        '''The arguments to add to the command line interface.
        '''
        from collections import OrderedDict
        args_to_add = OrderedDict()
        args_to_add['guiding'] = {'type': bool,
                                  'help': 'Set Guiding on or off (True or False).'}
        parser = cls._add_args(parser, args_to_add, print_only=False)
        return super().add_cmdline_args(parser, cfg)
