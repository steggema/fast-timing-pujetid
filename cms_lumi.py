from ROOT import TPad
from ROOT import TLatex
from ROOT import TLine
from ROOT import TBox
from ROOT import TASImage
from ROOT import TString
from ROOT import TStyle

#
# Global variables
#

cmsText     = TString("CMS Phase I Simulation")
cmsTextFont   = 61  # default is helvetic-bold

writeExtraText = False
extraText   = TString("Preliminary")
extraTextFont = 52  # default is helvetica-italics

# text sizes and text offsets with respect to the top frame
# in unit of the top margin size
lumiTextSize     = 0.6
lumiTextOffset   = 0.2
cmsTextSize      = 0.75
cmsTextOffset    = 0.1  # only used in outOfFrame version

relPosX    = 0.045
relPosY    = 0.035
relExtraDY = 1.2

# ratio of "CMS" and extra text size
extraOverCmsTextSize  = 0.76

lumi_13TeV = TString("20.1 fb^{-1}")
lumi_8TeV  = TString("19.7 fb^{-1}")
lumi_7TeV  = TString("5.1 fb^{-1}")
lumi_14TeV = TString("PU = 140")
lumi_1420TeV = TString("PU = 20")

drawLogo      = False

def cms_lumi(pad, iPeriod, iPosX):
    outOfFrame    = False
    if iPosX/10==0:
        outOfFrame = True
    alignY_=3
    alignX_=2
    if iPosX/10==0: alignX_=1
    if iPosX==0   : alignY_=1
    if iPosX/10==1: alignX_=1
    if iPosX/10==2: alignX_=2
    if iPosX/10==3: alignX_=3
    align_ = 10*alignX_ + alignY_

    H = pad.GetWh()
    W = pad.GetWw()
    l = pad.GetLeftMargin()
    t = pad.GetTopMargin()
    r = pad.GetRightMargin()
    b = pad.GetBottomMargin()
    # e = 0.025

    pad.cd()

    lumiText = TString('')
    if iPeriod==1:
        lumiText += lumi_7TeV
        lumiText += " (7 TeV)"

    elif  iPeriod==2:
        lumiText += lumi_8TeV
        lumiText += " (8 TeV)"

    elif iPeriod==3: 
        lumiText = lumi_8TeV 
        lumiText += " (8 TeV)"
        lumiText += " + "
        lumiText += lumi_7TeV
        lumiText += " (7 TeV)"

    elif  iPeriod==4:
        lumiText += lumi_13TeV
        lumiText += " (13 TeV)"

    elif iPeriod==7:
        if outOfFrame:
            lumiText += "#scale[0.85]{"
        lumiText += lumi_13TeV 
        lumiText += " (13 TeV)"
        lumiText += " + "
        lumiText += lumi_8TeV 
        lumiText += " (8 TeV)"
        lumiText += " + "
        lumiText += lumi_7TeV
        lumiText += " (7 TeV)"
        if outOfFrame:
            lumiText += "}"

    elif iPeriod==12:
        lumiText += "8 TeV"

    elif iPeriod==14:
        lumiText += lumi_14TeV
        lumiText += ", 14 TeV"
    elif iPeriod==1420:
        lumiText += lumi_1420TeV
        lumiText += ", 14 TeV"

    print lumiText

    latex = TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(TStyle.kBlack)    

    extraTextSize = extraOverCmsTextSize*cmsTextSize

    latex.SetTextFont(42)
    latex.SetTextAlign(31) 
    latex.SetTextSize(lumiTextSize*t)    
    latex.DrawLatex(1-r, 1-t+lumiTextOffset*t, lumiText.Data())

    if outOfFrame:
        latex.SetTextFont(cmsTextFont)
        latex.SetTextAlign(11) 
        latex.SetTextSize(cmsTextSize*t)    
        latex.DrawLatex(l,1-t+lumiTextOffset*t,cmsText)


    pad.cd()

    posX_ = 0
    if iPosX%10<=1:
        posX_ = l + relPosX*(1-l-r)
    elif iPosX%10==2:
      posX_ = l + 0.5*(1-l-r)
    elif iPosX%10==3:
        posX_ =  1-r - relPosX*(1-l-r)
    posY_ = 1-t - relPosY*(1-t-b)
    if not outOfFrame:
        if drawLogo:
            posX_ =   l + 0.045*(1-l-r)*W/H
            posY_ = 1-t - 0.045*(1-t-b)
            xl_0 = posX_
            yl_0 = posY_ - 0.15
            xl_1 = posX_ + 0.15*H/W
            yl_1 = posY_
            CMS_logo = TASImage("CMS-BW-label.png")
            pad_logo = TPad("logo","logo", xl_0, yl_0, xl_1, yl_1 )
            pad_logo.Draw()
            pad_logo.cd()
            CMS_logo.Draw("X")
            pad_logo.Modified()
            pad.cd()
    
        else:
            latex.SetTextFont(cmsTextFont)
            latex.SetTextSize(cmsTextSize*t)
            latex.SetTextAlign(align_)
            latex.DrawLatex(posX_, posY_, cmsText.Data())
            if writeExtraText:
                latex.SetTextFont(extraTextFont)
                latex.SetTextAlign(align_)
                latex.SetTextSize(extraTextSize*t)
                latex.DrawLatex(posX_, posY_- relExtraDY*cmsTextSize*t, extraText)

    elif writeExtraText:
        if iPosX==0:
            posX_ =   l +  relPosX*(1-l-r)
            posY_ =   1-t+lumiTextOffset*t
        latex.SetTextFont(extraTextFont)
        latex.SetTextSize(extraTextSize*t)
        latex.SetTextAlign(align_)
        latex.DrawLatex(posX_, posY_, extraText)      

