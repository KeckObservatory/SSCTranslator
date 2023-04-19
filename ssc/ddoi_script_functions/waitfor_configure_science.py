import ktl
from ssc.SSCTranslatorFunction import SSCTranslatorFunction
import time


class waitfor_configure_science(SSCTranslatorFunction):
    '''
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        time.sleep(1)

    @classmethod
    def post_condition(cls, args, logger, cfg):
        return True
