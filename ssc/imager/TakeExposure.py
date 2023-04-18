import time
import ktl

from ssc.SSCTranslatorFunction import SSCTranslatorFunction
from ssc.imager import SetImagePath, SetGuiding, SetBinning, SetExptime, SetImageSave
from ddoitranslatormodule.ddoiexceptions import DDOIExceptions



class TakeExposure(SSCTranslatorFunction):
    '''Take an exposure with the SSC
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        service = cfg['magiq']['service_name']
        magiq = ktl.cache(service)
        lastframe=int(float(magiq.read('IMGFRNR')))
        logger.info(f'taking {lastframe}th frame')

        SetImagePath(path='/s/nightly1/tonight')
        SetGuiding(guiding=False)
        SetBinning(binning=args.binning)
        SetExptime(Exptime=args.exptime)
        SetImageSave(save=True)


    @classmethod
    def post_condition(cls, args, logger, cfg):
        service = cfg['magiq']['service_name']
        magiq = ktl.cache(service)
        newframe=magiq.read('IMGFRNR')
        if newframe<=args.lastframe:
            raise DDOIExceptions.FailedToReachDestination(newframe, args.lastframe)
        else:
            return True


