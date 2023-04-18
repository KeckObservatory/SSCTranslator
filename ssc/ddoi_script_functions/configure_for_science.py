import ktl
from ssc.SSCTranslatorFunction import SSCTranslatorFunction

from ssc.imager.SetBinning import SetBinning
from ssc.imager.SetExptime import SetExptime
from ssc.imager.ToggleCamera import ToggleCamera

class configure_for_science(SSCTranslatorFunction):
    '''
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        return True

    @classmethod
    def perform(cls, args, logger, cfg):

        # Extract our needed arguments (exptime and binning)
        sequence = args.get('sequence')
        parameters = sequence.get('paramters')
        exptime = parameters.get('det1_exp_time')
        binning = parameters.get('det1_binning')

        # Set the values
        SetBinning.execute({'exptime' : binning})
        SetExptime.execute({'binning' : exptime})
        
        # Tell MAGIQ to load those values
        cls.set_magiq_cmd(logger)

        # Start the camera
        ToggleCamera.execute({'status' : 'start'})


    @classmethod
    def post_condition(cls, args, logger, cfg):
        return True
