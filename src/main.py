import analyzer
    
if (__name__ == "__main__"):

    sim = analyzer.HSS001Analyzer()
    sim.calcMandExp(False)
    sim.calcMandExp(True)

    #sim.calcExpEffOnCampus(False)
    #sim.calcExpEffOnCampus(True)

    #sim.printStatus()
