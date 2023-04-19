import ktl
from ssc.SSCTranslatorFunction import SSCTranslatorFunction

from ssc.imager.SetBinning import SetBinning
from ssc.imager.SetExptime import SetExptime
from ssc.imager.SetImagePath import SetImagePath
from ssc.imager.SetImageSave import SetImageSave
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
        parameters = sequence.get('parameters')
        exptime = parameters.get('det1_exp_time')
        binning = parameters.get('det1_binning')

        # Set the values
        # SetBinning.execute({'exptime' : binning}, logger=logger)
        SetExptime.execute({'binning' : exptime}, logger=logger)

        # Where to save these images
        SetImagePath.execute({'path' : '/s/nightly1/tonight'}, logger=logger)
        # Tell MAGIQ to save these images
        SetImageSave.execute({'save' : True}, logger=logger)

        # I AM NOT SETTING BINNING OR GUIDING HERE
        
        # Tell MAGIQ to load our values
        cls.set_magiq_cmd(logger)

        # Start the camera
        ToggleCamera.execute({'status' : 'start'})


    @classmethod
    def post_condition(cls, args, logger, cfg):
        return True
