import time
import ktl

from SSCTranslatorFunction import SSCTranslatorFunction
from imager import SetImagePath, SetGuiding, SetBinning, SetExptime, SetImageSave
from .. import (log, SSCException, FailedPreCondition, FailedPostCondition,
                FailedToReachDestination, check_input)


class TakeExposure(SSCTranslatorFunction):
    '''Take an exposure with the SSC
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        return True

    @classmethod
    def perform(cls, args, logger, cfg):

        magiq = ktl.cache('magiq')
        lastframe=magiq.read('IMGFRNR')

        SetImagePath(path='/s/nightly1/tonight')
        SetGuiding(guiding=False)
        SetBinning(binning=args.binning)
        SetExptime(Exptime=args.exptime)
        SetImageSave(save=True)


    @classmethod
    def post_condition(cls, args, logger, cfg):

        magiq = ktl.cache('magiq')
        newframe=magiq.read('IMGFRNR')
        if newframe<=args.lastframe:
            raise FailedToReachDestination(newframe, args.lastframe)
        else:
            return True

