import numpy
import ROOT

from tdrstyle_2014 import setTDRStyle, createCanvasUpgrade

from cms_lumi import cms_lumi

setTDRStyle()


modes = ['barrel', 'endcap', 'forward']

# fileNames = ['TMVA_classification_BE_notime.root', 'TMVA_classification_BE_time.root']

def rocCurve(hS, hB):
    ''' Create a ROC TGraph from two input histograms.
    '''
    maxBin = hS.GetNbinsX()

    #rocPoints = [(hS.Integral(nBin, maxBin)/hS.Integral(), hB.Integral(nBin, maxBin)/hB.Integral()) for nBin in range(1, maxBin + 1) ]
    effsS = [hS.Integral(nBin, maxBin+1)/hS.Integral(0, maxBin+1) for nBin in range(0, maxBin + 1) ]
    effB = [hB.Integral(nBin, maxBin+1)/hB.Integral(0, maxBin+1) for nBin in range(0, maxBin + 1) ]

    rocCurve = ROOT.TGraph(maxBin, numpy.asarray(effsS), numpy.asarray(effB))
    return rocCurve

titles = {
    'barrel':'|#eta| < 1.5',
    'endcap':'1.5 < |#eta| < 2.5',
    'forward':'2.5 < |#eta| < 3.0',
}

cv = createCanvasUpgrade()

lineColours = [1, 2, 4, 7, 8]
lineStyles = [3, 2, 1, 4, 5]

for mode in modes:
    # fileNames = ['TMVA_classification_{mode}_2ps.root'.format(mode=mode), 'TMVA_classification_{mode}_time_2ps.root'.format(mode=mode), 'TMVA_classification_{mode}_time_15ps.root'.format(mode=mode),  'TMVA_classification_{mode}_time_50ps.root'.format(mode=mode), 'TMVA_classification_{mode}_time_600ps.root'.format(mode=mode)]
    fileNames = ['TMVA_classification_{mode}_2ps.root'.format(mode=mode), 'TMVA_classification_{mode}_time_15ps.root'.format(mode=mode),  'TMVA_classification_{mode}_time_50ps.root'.format(mode=mode)]
    graphs = []
    # header = '#splitline{Pileup jet ID (2 ps)}{CHS jet p_{T} > 20 GeV, '+titles[mode]+'}'
    header = 'CHS jet p_{T} > 20 GeV, '+titles[mode]
    legend = ROOT.TLegend(0.15, 0.45, 0.55, 0.75)
    # legend.SetFillStyle(cv.GetFillStyle())
    # legend.SetLineStyle(cv.GetLineStyle())
    legend.SetShadowColor(0)
    legend.SetFillColor(0)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextAngle(0)
    legend.SetTextColor(ROOT.TStyle.kBlack) 
    legend.SetTextSize(0.05)
    legend.SetTextAlign(12)
    legend.SetHeader(header)

    for i, f in enumerate(fileNames):

        histS = ROOT.TH1F('s'+f, '', 1000, -1., 1.001)
        histB = ROOT.TH1F('b'+f, '', 1000, -1., 1.001)

        chain = ROOT.TChain('TestTree')
        chain.Add(f)

        extraCut = ''

        chain.Project('s'+f, 'BDTG', '(classID==0)'+extraCut)
        chain.Project('b'+f, 'BDTG', '(classID==1)'+extraCut)

        
        graph = rocCurve(histS, histB)
        graphs.append(graph)
        graph.SetLineWidth(4)
        graph.SetLineColor(lineColours[i])
        graph.SetLineStyle(lineStyles[i])
        graph.SetTitle('PU jet ID')
        # graph.GetYaxis().SetTitle('#varepsilon_{B}')
        # graph.GetXaxis().SetTitle('#varepsilon_{S}')
        graph.GetYaxis().SetTitle('#varepsilon(pileup jet)')
        graph.GetXaxis().SetTitle('#varepsilon(good jet)')
        graph.GetXaxis().SetRangeUser(0.65, 1.)
        # graph.GetXaxis().SetRangeUser(0.8, 1.)
        graph.Draw('AL' if i == 0 else 'L')

        title = 'Default'
        if 'only_time_2' in f:
            title = 'Only timing (2 ps)'
        elif 'time_2' in f:
            title = 'With timing (2 ps)'
        elif 'time_15' in f:
            title = 'With timing (15 ps)'
        elif 'time_50' in f:
            title = 'With timing (50 ps)'
        elif 'time_pt_50' in f:
            title = 'With timing & p_{T} (50 ps)'
        elif '600' in f:
            title = 'With timing (600 ps)'

        legend.AddEntry(graph, title, 'L')

    legend.Draw()
    cv.SetLogy(False)
    cms_lumi(cv, iPeriod=14, iPosX=11)
    cv.Print('pujetid_{mode}.pdf'.format(mode=mode))
    cv.Print('pujetid_{mode}.C'.format(mode=mode))
    cv.Print('pujetid_{mode}.root'.format(mode=mode))
    # cv.Print('reco_vertex.pdf')
    # cv.Print('reco_plus_no_vertex.pdf')

