import ktl

from ssc.SSCTranslatorFunction import SSCTranslatorFunction
from ddoitranslatormodule.ddoiexceptions import DDOIExceptions



class ToggleCamera(SSCTranslatorFunction):
    '''Sets the exposure time for the SSC in the magiq keyword service.
    
    Args:
    Exptime - The exposure time in seconds
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        cls.check_inputs(args, 'status', allowed_types=[str])
        if args.get('status') not in ['start', 'stop']:
            raise DDOIExceptions.DDOIMissingArgumentException(f"Expected (start) or (stop), but got {args.get('status')}")
        
        service = cfg['magiq']['service_name']
        magiq = ktl.cache(service)

        if magiq.read('CAMCMD') == args.get('status'):
            logger.warning(f"Requested to set f{service} to {args.get('status')}, but it is already there! Continuing...")

        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        service = cfg['magiq']['service_name']
        magiq = ktl.cache(service)
        status = args.get('status')
        logger.debug(f"Setting camera command to {status} for service {service}")
        magiq['camcmd'].write(status)

    @classmethod
    def post_condition(cls, args, logger, cfg):
        service = cfg['magiq']['service_name']
        logger.debug(f"Checking for success for service {service}")
        status = args.get('status')
        magiq = ktl.cache(service)
        camcmd = magiq.read('CAMCMD')
        if camcmd!=status:
            raise DDOIExceptions.FailedToReachDestination(camcmd, status)
        else:
            return True


    @classmethod
    def add_cmdline_args(cls, parser, cfg=None):
        '''The arguments to add to the command line interface.
        '''
        from collections import OrderedDict
        args_to_add = OrderedDict()
        args_to_add['status'] = {'type': str,
                                  'help': 'Command for the camera server (start, stop)'}
        parser = cls._add_args(parser, args_to_add, print_only=False)
        return super().add_cmdline_args(parser, cfg)
