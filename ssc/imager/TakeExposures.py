import time
import ktl

from ssc.SSCTranslatorFunction import SSCTranslatorFunction
from ssc.imager.TakeSnapshot import TakeSnapshot


# from ssc.imager import SetImagePath, SetGuiding, SetBinning, SetExptime, SetImageSave
from ddoitranslatormodule.ddoiexceptions import DDOIExceptions



class TakeExposures(SSCTranslatorFunction):
    '''Take an exposure with the SSC
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        cls.check_inputs(args, 'num_frames', [int])
        service = cfg['magiq']['service_name']
        magiq = ktl.cache(service)
        if magiq.read('CAMCMD') != 'OK':
            raise DDOIExceptions.DDOISubsystemDisabledException(f'MAGIQ CAMCMD not OK')
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        # service = cfg['magiq']['service_name']
        # magiq = ktl.cache(service)

        for i in range(int(args.get('num_frames'))):
            logger.info(f"Taking exposure #{i}...")
            TakeSnapshot({}, logger=logger)

        # lastframe=int(float(magiq.read('IMGFRNR')))
        # logger.info(f'taking {lastframe}th frame')
        # target_file_number = lastframe + args.get('num_frames')
        # expression = f"${service}.IMGFRNR < '{target_file_number}'"

        # # Exposure time x Number of frames x 2 (safety factor)
        # timeout = float(magiq.read('TTIME')) * args.get('num_frames') * 2

        # success = ktl.waitFor(expression, timeout=timeout)

        # if not success:
        #     raise DDOIExceptions.DDOIKTLTimeOut(f"Timed out while trying to expose with MAGIQ")
        
        # return success


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


