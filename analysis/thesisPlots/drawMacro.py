import ROOT
from array import array

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetPadTickY(1)

marginL, marginR, marginT = 0.13, 0.07, 0.06

colors = {"RECO": "\033[1;36m", "GEN": "\033[1;34m", "BKG": "\033[1;31m", "NC": "\033[0m", "YELLOW": "\033[1;33m"}

defaultHistColors = [ROOT.kRed + 1, ROOT.kBlue, ROOT.kGreen + 2, ROOT.kYellow + 1, ROOT.kOrange + 8]

def savePlot(histograms, imageName, options=None):
    text = " Starting... ".center(70, "~")
    print(colors["YELLOW"] + "[savePlot]~~~{}".format(text) + colors["NC"])

    imagePath = "/home/submit/pdmonte/public_html/thesisPlots"
    cs = ROOT.TCanvas("canvas", "canvas", 900, 900)
    xlow, ylow, xup, yup = 0.60, 0.70, 0.87, 0.87
    legendFontSize = 0.035
    if "legendFontSize" in options:
        legendFontSize = options["legendFontSize"]
    if "moveLegend" in options:
        xlow, xup = options["moveLegend"], options["moveLegend"] + 0.27
    if options["data"] and not "fit" in options:
        ydiv = 0.20
        deltadiv = 0.05
        pad1 = ROOT.TPad("upper_pad", "", 0., ydiv, 1., 1.)#xlow, ylow, xup, yup
        pad1.SetTopMargin(0.125)
        pad1.Draw()
        pad2 = ROOT.TPad("lower_pad", "", 0., 0., 1., ydiv + deltadiv)
        pad2.Draw()
        pad2.SetLeftMargin(marginL)
        pad2.SetRightMargin(marginR)
        ylow, yup = 0.625, 0.8375
        #xlow, xup = 0.65, 0.92
    else:
        pad1 = ROOT.TPad("upper_pad", "", 0., 0., 1., 1.)#xlow, ylow, xup, yup
        pad1.Draw()
    if "HCandMass" in options:
        xlow, xup = 0.162, 0.162 + 0.27
    legend4 = ROOT.TLegend(xlow, ylow, xup, yup)
    pad1.SetLeftMargin(marginL)
    pad1.SetRightMargin(marginR)

    usedColors = options["colors"] if "colors" in options else defaultHistColors

    if "scatter" in options:
        stack4 = ROOT.TMultiGraph()
        for i, h in enumerate(histograms):
            gr = ROOT.TGraph(len(h[1][0]), array('d', h[1][0]), array('d', h[1][1]))
            gr.SetMarkerStyle(ROOT.kFullCircle)
            gr.SetMarkerSize(1 if i == 0 else 3)
            gr.SetMarkerColor(usedColors[i])
            legend4.AddEntry(gr, h[0], "p")
            stack4.Add(gr)
            #    mgr.Draw("ap")
    elif "fit" in options:
        stack4 = histograms[0][1]
        stack4.SetTitle("")
    else:
        stack4 = ROOT.THStack()
        markers = []
        maxHeight = 0
        for i, h in enumerate(histograms):
            maxHeight = max(maxHeight, h[1].GetMaximum())
            if "style" in options:
                if options["style"][i] == "l":
                    stack4.Add(h[1])
                    legend4.AddEntry(h[1], h[0], "l")
                    h[1].SetLineWidth(3)
                    h[1].SetLineColor(usedColors[i])
                elif options["style"][i] == "f":
                    legend4.AddEntry(h[1], h[0], "f")
                    stack4.Add(h[1])
                    h[1].SetLineWidth(0)
                    h[1].SetFillColor(usedColors[i])
                elif options["style"][i] == "p":
                    legend4.AddEntry(h[1], h[0], "lep")
                    markers.append((h[1], usedColors[i]))
            else:
                stack4.Add(h[1])
                legend4.AddEntry(h[1], h[0], "l")
                h[1].SetLineWidth(3)
                h[1].SetLineColor(usedColors[i])

    pad1.cd()# Draw onto main plot
    if "scatter" in options:
        stack4.Draw("ap")
    elif "fit" in options:
        for i, h in enumerate(histograms):
            if i == 0:#sgn/bkg
                legend4.AddEntry(h[1], h[0], "lep")
                h[1].SetMarkerStyle(20)
                h[1].SetMarkerSize(1.3)
                h[1].SetLineWidth(3)
                h[1].SetMarkerColor(usedColors[i])
                h[1].SetLineColor(usedColors[i])
                maxHeight = h[1].GetMaximum()
                h[1].GetYaxis().SetRangeUser(0, maxHeight*1.2)
                h[1].Draw("EP SAME")
                #blind
                if "blind" in options:
                    box=ROOT.TBox(115., 0., 135., maxHeight*1.2)
                    box.SetFillColor(ROOT.kWhite)
                    box.Draw()

            else:#fits
                legend4.AddEntry(h[1], h[0], "l")
                h[1].SetLineWidth(3)
                h[1].SetLineStyle(0)
                h[1].SetMarkerColor(usedColors[i])
                h[1].SetLineColor(usedColors[i])
                h[1].Draw("c SAME")
    else:
        if "HCandMass" in options:
            hStack = histograms[0][1].Clone("allstack")
            hStack.Add(histograms[1][1])
            hStack.Add(histograms[2][1])
            maxHeight = max(maxHeight, hStack.GetMaximum())
            print(maxHeight)
            stack4.Draw("hist")
            line1 = ROOT.TLine(115., 0., 115., maxHeight*1)
            line1.SetLineColor(11)
            line1.Draw()
            line2 = ROOT.TLine(135., 0., 135., maxHeight*1)
            line2.SetLineColor(11)
            line2.Draw()
        else:
            stack4.Draw("hist nostack")

        for h, col in markers:
            h.SetMarkerStyle(20)
            h.SetMarkerSize(1.3)
            h.SetLineWidth(3)
            h.SetMarkerColor(col)
            h.SetLineColor(col)
            h.Draw("EP SAME")
            
        stack4.SetMaximum(1.2*maxHeight)

    if "labelXAxis" in options:
        stack4.GetXaxis().SetTitle(options["labelXAxis"])
        #stack4.GetYaxis().SetNdivisions(5, 2, 0)
    if "labelYAxis" in options:
        stack4.GetYaxis().SetTitle(options["labelYAxis"])
        stack4.GetYaxis().SetDecimals()
        stack4.GetYaxis().ChangeLabel(1, -1, 0)
        print("I am here")
    if "xRange" in options:
        if "scatter" in options:
            stack4.GetXaxis().SetLimits(options["xRange"][0], options["xRange"][1])
        else:
            stack4.GetXaxis().SetRangeUser(options["xRange"][0], options["xRange"][1])
    if "yRange" in options:
        stack4.GetYaxis().SetRangeUser(options["yRange"][0], options["yRange"][1])
    if "logScale" in options:
        if options["logScale"]:
            stack4.SetMaximum(7*maxHeight)
            stack4.SetMinimum(100)
            pad1.SetLogy(1)
            
    
    if not options["data"] or "fit" in options:
        legend4.SetTextFont(42)
        legend4.SetFillStyle(0)
        legend4.SetBorderSize(0)
        legend4.SetTextSize(legendFontSize)
        legend4.SetTextAlign(12)
        legend4.Draw("same")

        text = ROOT.TLatex()
        text.SetNDC()
        text.SetTextFont(72)
        text.SetTextSize(0.045)
        text.DrawLatex(0.135, 0.913, "CMS")
        text.SetTextFont(42)
        text.DrawLatex(0.135 + 0.12, 0.913, "Internal" if options["data"] else "Simulation")
        text.SetTextSize(0.035)
        text.DrawLatex(0.62, 0.913, "#sqrt{{s}} = 13 TeV, {lumi} fb#kern[{space}]{{^{{-1}}}}".format(lumi=39.54, space=-0.1))
        stack4.GetXaxis().SetTitleSize(0.040)
        stack4.GetXaxis().SetLabelSize(0.035)
        stack4.GetYaxis().SetTitleSize(0.040)
        stack4.GetYaxis().SetLabelSize(0.035)
        stack4.GetYaxis().SetTitleOffset(1.75)

    else:
        fact = 1.25
        legend4.SetTextFont(42)
        legend4.SetFillStyle(0)
        legend4.SetBorderSize(0)
        legend4.SetTextSize(legendFontSize*fact)
        legend4.SetTextAlign(12)
        legend4.Draw("same")

        text = ROOT.TLatex()
        text.SetNDC()
        text.SetTextFont(72)
        text.SetTextSize(0.045*fact)
        text.DrawLatex(0.135, 0.89125, "CMS")
        text.SetTextFont(42)
        text.DrawLatex(0.135 + 0.12, 0.89125, "Internal" if options["data"] else "Simulation")
        text.SetTextSize(0.035*fact)
        text.DrawLatex(0.62, 0.89125, "#sqrt{{s}} = 13 TeV, {lumi} fb#kern[{space}]{{^{{-1}}}}".format(lumi=39.54, space=-0.1))
        
        stack4.GetXaxis().SetLabelOffset(99)#0.005 default
        stack4.GetXaxis().SetTitleOffset(99)#1 is default
        stack4.GetXaxis().SetTitleSize(0.040*fact)
        stack4.GetXaxis().SetLabelSize(0.035*fact)
        stack4.GetYaxis().SetTitleSize(0.040*fact)
        stack4.GetYaxis().SetLabelSize(0.035*fact)
        stack4.GetYaxis().SetTitleOffset(1.45)
        #draw ratio
        pad2.cd()
        pad2.SetTopMargin(0.0)
        pad2.SetBottomMargin(0.4)
        
        hData = histograms[-1][1]
        mcBKG = histograms[0][1]
        ratio = hData.Clone("dataratio")
        print("ALL mcTOT integral(): ",mcBKG.Integral())
        print("ALL data integral(): ", hData.Integral())

        ratio.Divide(mcBKG)
        ratio.GetYaxis().SetTitle("data/MC")
        ratio.GetYaxis().SetRangeUser(0.5,1.5)
        ratio.GetYaxis().SetTitleOffset(0.3)
        ratio.GetYaxis().SetTitleSize(0.15)
        ratio.GetYaxis().SetLabelSize(0.12)
        ratio.GetYaxis().SetNdivisions(5, 2, 0)
        fact = 4.0
        ratio.GetXaxis().SetTitleSize(0.040*fact)
        ratio.GetXaxis().SetLabelSize(0.035*fact)
        ratio.GetXaxis().SetLabelOffset(0.005*fact)#0.005 default
        ratio.GetXaxis().SetTitleOffset(1)#1 is default
        ratio.GetXaxis().SetTitle(options["labelXAxis"])
        
        ratio.SetTitle("")

        ratio.Draw("pe")
        lineZero = ROOT.TLine(mcBKG.GetXaxis().GetXmin(), 1.,  mcBKG.GetXaxis().GetXmax(), 1.)
        lineZero.SetLineColor(11)
        lineZero.Draw("same")

    ROOT.gPad.RedrawAxis()
    
    cs.SaveAs("{}/{}".format(imagePath, imageName))

    text = " Done! ".center(70, "~")
    print(colors["YELLOW"] + "[savePlot]~~~{}".format(text) + colors["NC"] + "\n")


def readBSFFile(filename):
    names, errors, shape, loss = [], [], [], []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split()
            names.append(parts[0])
            errors.append(float(parts[1]))
            shape.append(float(parts[2]))
            loss.append(float(parts[3]))
    return names, errors, shape, loss


def saveBSFPythonPlot():
    fileName = "BSF_vs_RMSE_phi.png"
    options = {"labelXAxis": "RMSE (predicted - gen) [GeV]", "labelYAxis": "BSF", "scatter": True, "data": False, "xRange": (3.0, 5.5), "yRange": (0, 40)}
    graphs = []
    names, errors, shapes, bsf = readBSFFile("/home/submit/pdmonte/CMSSW_10_6_27/src/Hrare2023/analysis/TMVA_regression/evalPhi.out")
    bsf = [l/10. if l > 60 else l for l in bsf]
    bsfOther, bsfReco, bsfUsed, errorsOther, errorsReco, errorsUsed = [], [], [], [], [], []
    print(len(names))
    for i, n in enumerate(names):
        if n == "RECO":
            bsfReco.append(bsf[i])
            errorsReco.append(errors[i])
        elif n == "BDTG_df13_dl3620_v0_v1_opt50098":
            bsfUsed.append(bsf[i])
            errorsUsed.append(errors[i])
        else:
            bsfOther.append(bsf[i])
            errorsOther.append(errors[i])
    graphs.append(("Models", (errorsOther, bsfOther)))
    graphs.append(("Used Model", (errorsUsed, bsfUsed)))
    graphs.append(("No Model", (errorsReco, bsfReco)))
    savePlot(graphs, fileName, options=options)
