import ktl

from ddoitranslatormodule.KPFTranslatorFunction import KPFTranslatorFunction


class ExecuteObservation(KPFTranslatorFunction):
    '''
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        
        # Check guiding
        guidingkw = ktl.cache(keyword='mqstartg', service='magiq')
        guiding = bool(guidingkw.read())
        if guiding is True:
            logger.warn(f'MAGIQ is guiding')
            return False

        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        
        # Set the exposure time
        TTIMEkw = ktl.cache(service='magiq', keyword='TTIME')
        new_exptime = float(args.exptime)*1000
        logger.debug(f'Setting exposure time to {new_exptime:.1f} ms')
        ITIMEkw.write(new_exptime)

        # Expose!
        GOkw = ktl.cache(service='magiq', keyword='camcmd')
        logger.info('Starting exposure')
        GOkw.write(start)
        
        return
#        raise NotImplementedError()

    @classmethod
    def post_condition(cls, args, logger, cfg):
        logger.debug("No post-condition for expose defined")
        return True
