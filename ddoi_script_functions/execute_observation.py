import ktl

from ddoitranslatormodule.KPFTranslatorFunction import KPFTranslatorFunction


class ExecuteObservation(KPFTranslatorFunction):
    '''
    '''
    @classmethod
    def pre_condition(cls, args, logger, cfg):
        
        # Check guiding
        guidingkw = ktl.cache(keyword='mqstartg', service='magiq')
        guiding = bool(guidingkw.read())
        if guiding is True:
            logger.warn(f'MAGIQ is guiding')
            return False

        return True

    @classmethod
    def perform(cls, args, logger, cfg):
        
        # Set the exposure time
        TTIMEkw = ktl.cache(service='magiq', keyword='TTIME')
        new_exptime = float(args.exptime)*1000
        logger.debug(f'Setting exposure time to {new_exptime:.1f} ms')
        ITIMEkw.write(new_exptime)

        # Set coadds
        COADDSkw = ktl.cache(service='mds', keyword='COADDS')
        logger.debug(f'Setting coadds to {int(args.coadds)}')
        COADDSkw.write(int(input))
    
        # Set sampling
        
        namematch = re.match('(M?CDS)(\d*)', input.strip())
        if namematch is None:
            raise DDOIMissingArgumentException(f'Unable to parse "{args.sampmode}"')
        mode = {'CDS': 2, 'MCDS': 3}.get(namematch.group(1))

        SAMPMODEkw = ktl.cache(service='mds', keyword='SAMPMODE')
        NUMREADSkw = ktl.cache(service='mds', keyword='NUMREADS')
        SAMPMODEkw.write(mode)
        if mode == 3:
            nreads = int(namematch.group(2))
            NUMREADSkw.write(nreads)
        
        # Set Object
        objectkw = ktl.cache(service='mds', keyword='OBJECT')
        objectkw.write(args.object)

        # Update FCS

        ROTPPOSNkw = ktl.cache(keyword='ROTPPOSN', service='dcs')
        ROTPPOSN = float(ROTPPOSNkw.read())
        ELkw = ktl.cache(keyword='EL', service='dcs')
        EL = float(ELkw.read())

        FCPA_ELkw = ktl.cache(keyword='PA_EL', service='mfcs')
        FCPA_ELkw.write(f"{ROTPPOSN:.2f} {EL:.2f}")

        FCPA_ELkw = ktl.cache(keyword='PA_EL', service='mfcs')
        FCPA_EL = FCPA_ELkw.read()
        FCSPA = float(FCPA_EL.split()[0])
        FCSEL = float(FCPA_EL.split()[1])
        
        ROTPPOSNkw = ktl.cache(keyword='ROTPPOSN', service='dcs')
        ROTPPOSN = float(ROTPPOSNkw.read())
        ELkw = ktl.cache(keyword='EL', service='dcs')
        EL = float(ELkw.read())
        done = np.isclose(FCSPA, ROTPPOSN, atol=args.PAthreshold)\
            and np.isclose(FCSEL, EL, atol=args.ELthreshold)
        
        if not done:
            logger.warn("Unable to update FCS. Exiting")
            return
        
        # Pad time to ensure proper execution
        sleep(1)

        # Expose!
        GOkw = ktl.cache(service='magiq', keyword='camcmd=start')
        logger.info('Starting exposure')
        GOkw.write(True)
        
        return
#        raise NotImplementedError()

    @classmethod
    def post_condition(cls, args, logger, cfg):
        logger.debug("No post-condition for expose defined")
        return True
