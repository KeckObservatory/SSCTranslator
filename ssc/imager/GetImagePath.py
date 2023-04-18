import time
import ktl

from ssc.SSCTranslatorFunction import SSCTranslatorFunction
from ddoitranslatormodule.ddoiexceptions import DDOIExceptions



class GetImagePath(SSCTranslatorFunction):
    '''Gets the image save path for the SSC in the magiq keyword service.
    
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        service = cfg['magiq']['service_name']
        magiq = ktl.cache(service)
        magiqpath=magiq.read('IMGDIR')
        logger.info(f"Exposure path is: {magiqpath} for service {service}")
        print(magiqpath)
        return magiqpath


    @classmethod
    def post_condition(cls, args, logger, cfg):
        return True
