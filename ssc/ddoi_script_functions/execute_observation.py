import ktl
from ssc.SSCTranslatorFunction import SSCTranslatorFunction
from ssc.imager.TakeSnapshot import TakeSnapshot
from ssc.imager.TakeExposures import TakeExposures
class execute_observation(SSCTranslatorFunction):
    '''
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        # Call TakeExposure
        sequence = args.get('sequence')
        metadata = sequence.get('metadata')
        seq_num = metadata.get('sequence_number')
        logger.info(f'excuting observation for seq {seq_num}')
        params = sequence.get('parameters')
        num_frames = params.get('det1_exp_number')
        
        if num_frames > 1:
            TakeExposures.execute({'num_frames' : num_frames})
        else:
            TakeSnapshot.execute()


        

    @classmethod
    def post_condition(cls, args, logger, cfg):
        return True
