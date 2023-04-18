import time
import ktl

from ssc.SSCTranslatorFunction import SSCTranslatorFunction
from ssc.imager.SetImagePath import SetImagePath
from ssc.imager.SetGuiding import SetGuiding
from ssc.imager.SetBinning import SetBinning
from ssc.imager.SetExptime import SetExptime
from ssc.imager.SetImageSave import SetImageSave
from ssc.imager.ToggleCamera import ToggleCamera


# from ssc.imager import SetImagePath, SetGuiding, SetBinning, SetExptime, SetImageSave
from ddoitranslatormodule.ddoiexceptions import DDOIExceptions



class TakeSnapshot(SSCTranslatorFunction):
    '''Take an exposure with the SSC
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        service = cfg['magiq']['service_name']
        magiq = ktl.cache(service)
        if magiq.read('CAMCMD') != 'OK':
            raise DDOIExceptions.DDOISubsystemDisabledException(f'MAGIQ CAMCMD not OK')
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        service = cfg['magiq']['service_name']
        magiq = ktl.cache(service)

        magiq['MQSNPGF'].write(1)

        # lastframe=int(float(magiq.read('IMGFRNR')))
        # logger.info(f'taking {lastframe}th frame')

        # ToggleCamera.execute({'status' : 'start'})
        # SetImagePath.execute({'path' : '/s/nightly1/tonight'})
        # SetGuiding.execute({'guiding' : False})
        # SetBinning.execute({'binning' : args.binning})
        # SetExptime.execute({'Exptime' : args.exptime})
        # SetImageSave.execute({'save' : True})
        # # Use MQSNPGF to save a frame
        # ToggleCamera.execute({'status' : 'stop'})


    @classmethod
    def post_condition(cls, args, logger, cfg):
        return True
        # service = cfg['magiq']['service_name']
        # magiq = ktl.cache(service)
        # newframe=magiq.read('IMGFRNR')
        # if newframe<=args.lastframe:
        #     raise DDOIExceptions.FailedToReachDestination(newframe, args.lastframe)
        # else:
        #     return True


