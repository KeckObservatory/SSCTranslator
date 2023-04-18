import ktl
from ssc.SSCTranslatorFunction import SSCTranslatorFunction
from ..imager.SetExptime import SetExptime
from ..imager.GetImagePath import GetImagePath 

class execute_observation(SSCTranslatorFunction):
    '''
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        sequence = args.get('sequence')
        metadata = sequence.get('metadata')
        seq_num = metadata.get('sequence_number')
        logger.info(f'excuting observation for seq {seq_num}')
        params = sequence.get('parameters')
        exptime = params.get('det1_exp_time')
        seArgs = {'exptime': exptime}

        SetExptime.execute(seArgs, logger, cfg)
        GetImagePath.execute({}, logger, cfg)

        

    @classmethod
    def post_condition(cls, args, logger, cfg):
        return True
