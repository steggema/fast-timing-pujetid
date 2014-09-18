import numpy
import ROOT

from tdrstyle_2014 import setTDRStyle, createCanvasUpgrade

from cms_lumi import cms_lumi

setTDRStyle()

tree = ROOT.TChain('Jets04')

tree.Add('data/CHS_jet_out_140PU_600ps.root')
# tree.Add('data/Default_jet_out.root')

treeNoPU = ROOT.TChain('Jets04')

treeNoPU.Add('data/NoPU_jet_out.root')


variables = {
    'pt':{
        'nbins':10,
        'xmin':0.,
        'xmax':100.,
        'xtitle':'p_{T} (GeV)',
        'tex':'jet \\pt'
    },
    'eta':{
        'nbins':30,
        'xmin':-3.0,
        'xmax':3.0,
        'xtitle':'#eta',
        'tex':'jet \\eta'
    },
    'dR2Mean':{
        'nbins':10,
        'xmin':0.,
        'xmax':0.125,
        'xtitle':'Average #Delta R^{2}',
        'tex':'average $\\Delta R^2$'

    },
    'nParticles':{
        'nbins':120,
        'xmin':-0.5,
        'xmax':119.5,
        'xtitle':'N(particles)',
        'tex':'number of particles'
    },
    'time':{
        'nbins':30,
        'xmin':-2.,
        'xmax':4.,
        'xtitle':'Time (leading cell) (ns)',
        'tex':'time of the highest-energy cell'
    },
    'ptD':{
        'nbins':30,
        'xmin':0.,
        'xmax':1.,
        'xtitle':'p_{T}^{D}',
        'tex':'$p_T^D$ variable'
    },
    'time0':{
        'nbins':30,
        'xmin':-2.,
        'xmax':4.,
        'xtitle':'Time (leading photon) (ns)',
        'tex':'time of the leading PF photon'
    },
    'time1':{
        'nbins':30,
        'xmin':-2.,
        'xmax':4.,
        'xtitle':'Time (2nd leading photon) (ns)',
        'tex':'time of the second leading PF photon'
    },
    'time2':{
        'nbins':30,
        'xmin':-2.,
        'xmax':4.,
        'xtitle':'Time (3rd leading photon) (ns)',
        'tex':'time of the third leading PF photon'
    },
    'time3':{
        'nbins':30,
        'xmin':-2.,
        'xmax':4.,
        'xtitle':'Time (4th leading photon) (ns)',
        'tex':'time of the fourth leading PF photon'
    },
    'logtime0':{
        'nbins':60,
        'xmin':-4.,
        'xmax':8.,
        'xtitle':'log(time leading photon (ns))',
        'tex':'logarithm of the time of the leading PF photon'
    },
    'logtime1':{
        'nbins':60,
        'xmin':-4.,
        'xmax':8.,
        'xtitle':'log(time 2nd leading photon (ns))',
        'tex':'logarithm of the time of the second leading PF photon'
    },
    'logtime2':{
        'nbins':60,
        'xmin':-4.,
        'xmax':8.,
        'xtitle':'log(time 3rd leading photon (ns))',
        'tex':'logarithm of the time of the third leading PF photon'
    },
    'logtime3':{
        'nbins':60,
        'xmin':-4.,
        'xmax':8.,
        'xtitle':'log(time 4th leading photon (ns))',
        'tex':'logarithm of the time of the fourth leading PF photon'
    },
    'pt0':{
        'nbins':30,
        'xmin':0.,
        'xmax':50.,
        'xtitle':'p_{T} (leading photon) (GeV)',
        'tex':'\\pt of the leading PF photon'
    },
    'pt1':{
        'nbins':30,
        'xmin':0.,
        'xmax':50.,
        'xtitle':'p_{T} (2nd leading photon) (GeV)',
        'tex':'\\pt of the second leading PF photon'
    },
    'pt2':{
        'nbins':30,
        'xmin':0.,
        'xmax':50.,
        'xtitle':'p_{T} (3rd leading photon) (GeV)',
        'tex':'\\pt of the third leading PF photon'
    },
    'avetime':{
        'nbins':30,
        'xmin':-6.,
        'xmax':10.,
        'xtitle':'Average time (ns)',
        'tex':'average time of all PF photons'
    },
    'sigmatime':{
        'nbins':30,
        'xmin':0.,
        'xmax':15.,
        'xtitle':'#sigma(time) (ns)',
        'tex':'width of the time distribution of all PF photons'
    },
    'betaStar':{
        'nbins':30,
        'xmin':0.,
        'xmax':1.0001,
        'xtitle':'#beta^{*}',
        'tex':'$\\beta^*$ variable'
    },
    'beta':{
        'nbins':30,
        'xmin':0.,
        'xmax':1.0001,
        'xtitle':'#beta',
        'tex':'$\\beta$ variable'
    },
    'log10_abs_dz__':{
        'nbins':30,
        'xmin':-5.,
        'xmax':2.,
        'xtitle':'log_{10}(|#Delta z| (cm))',
        'tex':'distance of closest approach of the leading PF charged hadron to the primary vertex in z direction'
    },
    'nCharged':{
        'nbins':70,
        'xmin':-0.5,
        'xmax':69.5,
        'xtitle':'N(charged particles)',
        'tex':'number of charged particles'
    },
    'nNeutrals':{
        'nbins':51,
        'xmin':-0.5,
        'xmax':50.5,
        'xtitle':'N(neutral particles)',
        'tex':'number of neutral particles'
    },
}

selections =  {
    'barrel':{
        'sel':'&& abs(eta)<1.5'
    },
    'endcap':{
        'sel':'&& abs(eta)>1.5 && abs(eta)<2.5'
    },
    'forward':{
        'sel':'&& abs(eta)>2.5 && abs(eta)<3.0'
    },
    'barrel_1_15':{
        'sel':'&& abs(eta)>1.0 && abs(eta)<1.5'
    },
    'endcap_15_20':{
        'sel':'&& abs(eta)>1.5 && abs(eta)<2.0'
    }
}

texText = '''
\\begin{{figure}}[hbtp]
  \\begin{{center}}
    \includegraphics[width=0.32\\textwidth]{{figures/pujetid/{var}_barrel.pdf}}
    \includegraphics[width=0.32\\textwidth]{{figures/pujetid/{var}_endcap.pdf}}
    \includegraphics[width=0.32\\textwidth]{{figures/pujetid/{var}_forward.pdf}}

    \caption{{Distribution of the {var_desc} for $0 <
      |\eta| < 1.5$ (left), $1.5 < |\eta| < 2.5$ (middle), and $2.5 < |\eta| < 3.0$
      (right).}}
    \label{{fig:pujetid_input_{var}}}
  \end{{center}}
\end{{figure}}
'''

cv = createCanvasUpgrade()

header = 'CHS, p_{T} > 20 GeV'

texOut = ''

for selection in selections:
    extraCut = selections[selection]['sel'] + '&& (abs(eta)>2.5 || nCharged>0) && pt>20'
    varCounter = 0
    for var in variables:
        varCounter += 1
        legend = ROOT.TLegend(0.65, 0.55, 0.95, 0.75)
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
        vd = variables[var]
        nbins = vd['nbins']
        xmin = vd['xmin']
        xmax = vd['xmax']
        title = vd['xtitle']

        histS = ROOT.TH1F(var+'s', '', nbins, xmin, xmax)
        histB = ROOT.TH1F(var+'b', '', nbins, xmin, xmax)
        histNoPU = ROOT.TH1F(var+'nopu', '', nbins, xmin, xmax)

        histB.SetLineColor(2)
        histB.SetLineWidth(3)
        histS.SetLineWidth(3)
        histB.SetLineStyle(2)

        histNoPU.SetLineColor(4)
        histNoPU.SetLineWidth(3)
        histNoPU.SetLineStyle(3)

        xvar = var
        if var == 'log10_abs_dz__':
            xvar = 'log10(abs(dz))'

        print tree.Project(histS.GetName(), xvar, '(genpt>8)'+extraCut)
        print tree.Project(histB.GetName(), xvar, '(genpt<0.1)'+extraCut)
        print treeNoPU.Project(histNoPU.GetName(), xvar, '(genpt>8)'+extraCut)

        histS.Scale(1./histS.Integral())
        histB.Scale(1./histB.Integral())
        histNoPU.Scale(1./histNoPU.Integral())

        maxY = max(histS.GetMaximum(), histB.GetMaximum(), histNoPU.GetMaximum())

        histS.GetYaxis().SetTitle('Normalised event rate')
        histS.GetXaxis().SetTitle(title)

        histS.Draw()
        histS.GetYaxis().SetRangeUser(0., maxY*1.2)
        histB.Draw('SAME')
        histNoPU.Draw('SAME')
        histS.Draw('SAME')
        histB.GetYaxis().SetRangeUser(0., maxY*1.2)

        legend.AddEntry(histS, 'Good jet', 'L')
        legend.AddEntry(histB, 'Pileup jet', 'L')
        legend.AddEntry(histNoPU, 'No pileup', 'L')

        legend.Draw()
        cv.SetLogy(False)
        cms_lumi(cv, iPeriod=14, iPosX=11)
        cv.Print('varplots600ps/{var}_{sel}.pdf'.format(sel=selection,var=var))
        if selection == 'barrel':
            texOut += texText.format(var=var, var_desc=vd['tex'])
            if varCounter%4 == 0:
                texOut += '\n\\pagebreak\\n'
    # cv.Print('reco_vertex.pdf')
    # cv.Print('reco_plus_no_vertex.pdf')

outText = open('pujetid_inputs.tex', 'w')
outText.write(texOut)
outText.close()
