from ddoitranslatormodule.BaseFunction import TranslatorModuleFunction
import os
import ktl


class SSCTranslatorFunction(TranslatorModuleFunction):

    def _cfg_location(cls, args):
        """
        Return the fullpath + filename of default configuration file.
        :param args: <dict> The OB (or portion of OB) in dictionary form
        :return: <list> fullpath + filename of default configuration
        """
        cfg_path_base = os.path.dirname(os.path.abspath(__file__))

        inst = 'ssc'
        cfg = f"{cfg_path_base}/ddoi_configurations/{inst}_inst_config.ini"
        config_files = [cfg]

        return config_files
    
    @classmethod
    def check_inputs(cls, args, key, allowed_types):
        if args[key]:
            if type(args[key]) in allowed_types:
                return True
        return False
    
    @classmethod
    def set_magiq_cmd(cls, logger):
        magiq = ktl.cache('magiq')
        logger.debug(f"Setting magiqcmd")
        magiq['camcmd'].write('set')

