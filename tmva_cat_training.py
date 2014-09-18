import numpy
import ROOT
import array
import optparse

training_vars = [
    'pt',
    'abs(eta)',
    'betaStar',
    'beta',
    'log10(abs(dz))',
    'ptD',
    'dR2Mean',
    'nCharged',
    'nNeutrals',
]

training_vars_only_time = [
    'time',
    'time0',
    'logtime0',
    'pt0',
    'time1',
    'logtime1',
    'pt1',
    'time2',
    'logtime2',
    'pt2',
    'logtime3',
    'avetime',
    'sigmatime'
]

training_vars_time = training_vars[:] + training_vars_only_time[:]

def parse_options():
    usage = '''
%prog [options]
'''
    parser = optparse.OptionParser(usage)
    parser.add_option('-i', '--input', dest='input_file', help='input file name', default='data/CHS_jet_out_140PU_600ps.root', type='string')
    parser.add_option('-o', '--out_postfix', dest='out_postfix', help='output file postfix', default='600ps', type='string')
    opts, args = parser.parse_args()
    return opts, args

def train(name='barrel', selection='(pt>20 && pt<100 && abs(eta) < 1.5)', vars=training_vars, out_name=''):

    signal_selection = selection + '&&(genpt>8)' # good jet
    background_selection = selection + '&&(genpt<8)' # PU jet

    num_pass = tree.GetEntries(signal_selection)
    num_fail = tree.GetEntries(background_selection)

    print 'N events signal', num_pass
    print 'N events background', num_fail
    outFile = ROOT.TFile('TMVA_classification_'+name+'_{out}.root'.format(out=out_name), 'RECREATE')

    factory    = ROOT.TMVA.Factory(
        "TMVAClassification", 
        outFile, 
        "!V:!Silent:Color:DrawProgressBar:Transformations=I" ) 

    for var in vars:
        factory.AddVariable(var, 'F') # add float variable

    # factory.SetWeightExpression('')

    factory.AddSignalTree(tree, 1.)
    factory.AddBackgroundTree(tree, 1.)

    # import pdb; pdb.set_trace()

    factory.PrepareTrainingAndTestTree( ROOT.TCut(signal_selection), ROOT.TCut(background_selection),
                                        "nTrain_Signal=0:nTest_Background=0:SplitMode=Random:NormMode=NumEvents:!V" )


    # factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDTG","!H:!V:NTrees=500::BoostType=Grad:Shrinkage=0.05:GradBaggingFraction=0.9:nCuts=500:MaxDepth=5" ) #UseBaggedBoost:MinNodeSize=0.1
    bdt = factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDTG","!H:!V:NTrees=1000:BoostType=Grad:Shrinkage=0.02:UseBaggedBoost=True:BaggedSampleFraction=0.5:nCuts=10000:MaxDepth=7:MinNodeSize=0.01:UseRandomisedTrees=True:NodePurityLimit=1." ) #UseBaggedBoost:MinNodeSize=0.1

    bdt.CheckForUnusedOptions()

    # factory.BookMethod(ROOT.TMVA.Types.kBDT, "BDT_ADA", "!H:!V:NTrees=400:BoostType=AdaBoost:SeparationType=GiniIndex:nCuts=50:AdaBoostBeta=0.2:MaxDepth=5:MinNodeSize=0.1")

    # factory.BookMethod( ROOT.TMVA.Types.kFisher, "Fisher", "H:!V:Fisher:CreateMVAPdfs:PDFInterpolMVAPdf=Spline2:NbinsMVAPdf=50:NsmoothMVAPdf=10" )


    factory.TrainAllMethods()

    # factory.OptimizeAllMethods()

    factory.TestAllMethods()

    factory.EvaluateAllMethods()

    outFile.Close()

# The following is example code that's not used at the moment
def read():
    reader = ROOT.TMVA.Reader('TMVAClassification_BDTG')

    varDict = {}
    for var in training_vars:
        varDict[var] = array.array('f',[0])
        reader.AddVariable(var, varDict[var])

    reader.BookMVA("BDTG","weights/TMVAClassification_BDTG.weights.xml")

    bdtOuts = []
    flavours = []

    for jentry in xrange(tree.GetEntries()):

        ientry = tree.LoadTree(jentry)
        nb = tree.GetEntry(jentry)

        for var in varDict:
            varDict[var][0] = getattr(tree, var)

        bdtOutput = reader.EvaluateMVA("BDTG")

        flavour = tree.flavour
        bdtOuts.append(bdtOutput)
        flavours.append(flavour)

        if jentry%1000 == 0:
            print jentry, varDict['f1'], bdtOutput, flavour

    writeSmallTree = False

    if writeSmallTree:

        BDTG = numpy.zeros(1, dtype=float)
        flav = numpy.zeros(1, dtype=float)

        fout = ROOT.TFile('trainPlusBDTG.root', 'RECREATE')
        treeout = ROOT.TTree()
        treeout.Branch('BDTG', BDTG, 'BDTG/D')
        treeout.Branch('flavour', flav, 'loss/D')


        for i, bdtOut in enumerate(bdtOuts):
            BDTG[0] = bdtOut
            flav[0] = flavours[i]
            if i%1000==0:
                print i, bdtOut, flavours[i]
            treeout.Fill()
        treeout.Write()
        fout.Write()
        fout.Close()


def gui(fname='TMVA_classification.root'):
    ROOT.gROOT.LoadMacro('$ROOTSYS/tmva/test/TMVAGui.C')
    ROOT.TMVAGui(fname)
    raw_input("Press Enter to continue...")

if __name__ == '__main__':
    opts, args = parse_options()

    input_file = opts.input_file
    out_postfix = opts.out_postfix
    
    TMVA_tools = ROOT.TMVA.Tools.Instance()

    tree = ROOT.TChain('Jets04')

    tree.Add(input_file)

    selection_forward = '(pt>20 && pt<100 && abs(eta) > 2.5 && abs(eta) < 3.0)'
    selection_endcap = '(pt>20 && pt<100 && abs(eta) > 1.5 && abs(eta) < 2.5)'
    selection_barrel = '(pt>20 && pt<100 && abs(eta) < 1.5)'

    # train('barrel', selection_barrel, training_vars, out_name=out_postfix)
    train('barrel_time_pt', selection_barrel, training_vars_time, out_name=out_postfix)
    # train('barrel_only_time', selection_barrel, training_vars_only_time, out_name=out_postfix)
    # train('endcap', selection_endcap, training_vars, out_name=out_postfix)
    # train('endcap_time', selection_endcap, training_vars_time, out_name=out_postfix)
    # train('endcap_only_time', selection_endcap, training_vars_only_time, out_name=out_postfix)
    # train('forward', selection_forward, training_vars, out_name=out_postfix)
    # train('forward_time', selection_forward, training_vars_time, out_name=out_postfix)
    # train('forward_only_time', selection_forward, training_vars_only_time, out_name=out_postfix)

    # gui('TMVA_classification_barrel_{out}.root'.format(out=out_postfix))
    

