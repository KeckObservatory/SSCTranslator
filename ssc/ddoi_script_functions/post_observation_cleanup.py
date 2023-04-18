import ktl
from ssc.SSCTranslatorFunction import SSCTranslatorFunction
from ssc.imager.ToggleCamera import ToggleCamera

class post_observation_cleanup(SSCTranslatorFunction):
    '''
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        ToggleCamera.execute({'status' : 'stop'})

    @classmethod
    def post_condition(cls, args, logger, cfg):
        return True
