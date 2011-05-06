#!/usr/bin/env python
"""Display APOGEE instrument status

History:
2011-05-06 ROwen
"""
import Tkinter
import RO.Constants
import RO.StringUtil
import RO.Wdg
import TUI.Models

class ReadStatusWdg(Tkinter.Frame):
    def __init__(self, master, helpURL=None):
        """Create a status widget
        """
        Tkinter.Frame.__init__(self, master)
        
        gridder = RO.Wdg.Gridder(master=self, sticky="w")
        self.gridder = gridder
        
        self.model = TUI.Models.getModel("apogeeql")
        self.apogeeModel = TUI.Models.getModel("apogee")
        
        self.expNameWdg = RO.Wdg.StrLabel(
            master = self,
            anchor = "w",
            helpText = "Name of current exposure",
            helpURL = helpURL,
        )
        gridder.gridWdg("Exposure", self.expNameWdg, colSpan=2)
        
        self.readNumWdg = RO.Wdg.StrLabel(
            master = self,
            anchor = "w",
            helpText = "Current and total read number",
            helpURL = helpURL,
        )
        gridder.gridWdg("Read Num", self.readNumWdg, colSpan=2)

#         self.predReadsWdg = RO.Wdg.StrLabel(
#             master = self,
#             anchor = "w",
#             helpText = "Predicted total number of reads",
#             helpURL = helpURL,
#         )
#         gridder.gridWdg("Predicted Reads", self.predReadsWdg)
        
        self.expTimeWdg = RO.Wdg.StrLabel(
            master = self,
            anchor = "w",
            width = 20, # room for "xxx of xxx; pred xxx"
            helpText = "Current and total exposure time",
            helpURL = helpURL,
        )
#        gridder.gridWdg("Exp Time", self.expTimeWdg, "sec")

#         self.predExpTimeWdg = RO.Wdg.StrLabel(
#             master = self,
#             anchor = "w",
#             helpText = "Predicted total exposure time",
#             helpURL = helpURL,
#         )
#         gridder.gridWdg("Pred. Exp. Time", self.predExpTimeWdg, "sec")

        self.snrWdg = RO.Wdg.StrLabel(
            master = self,
            anchor = "w",
            helpText = "Current and target S/N",
            helpURL = helpURL,
        )
        gridder.gridWdg("S/N", self.snrWdg, colSpan=2)
        
        self.ditherWdg = RO.Wdg.StrLabel(
            master = self,
            anchor = "w",
            width = 13, # room for "Bad x.xx/x.xx"
            helpText = "Measured/commanded dither position",
            helpURL = helpURL,
        )
        gridder.gridWdg("Dither", self.ditherWdg, "pixels")

        self.wavelenWdg = RO.Wdg.StrLabel(
            master = self,
            anchor = "w",
            helpText = "Measured wavelength offset",
            helpURL = helpURL,
        )
        gridder.gridWdg("Wave Offset", self.wavelenWdg, RO.StringUtil.AngstromStr)

        self.statusWdg = RO.Wdg.StrLabel(
            master = self,
            anchor = "w",
            helpText = "Are sky and FITS headers OK?",
            helpURL = helpURL,
        )
        gridder.gridWdg("Status", self.statusWdg, colSpan=2)
        
        self.model.utrData.addCallback(self._utrDataCallback)

        gridder.allGridded()
    
    def _utrDataCallback(self, keyVar):
        """utrData keyword callback
    Key('utrData',
    0    Int(name='expNum', help='Exposure number'),
    1    Int(name='readNum', help='Read number counter'),
    2    Float(name='snrH12', help='SNR value for this read'),
    3,4  Float(name='snrTotalLinFit', help='SNR^2 to readNum Linear fit to all the reads so far: y intercept, slope')*2,
    5,6  Float(name='snrRecentLinFit', help='SNR^2 to readNum Linear fit of most recent reads: y intercept, slope')*2,
    7    Bits('fitsBad', 'ditherBad', 'skyBad', 'waveBad', help='bitwise status (1=bad, 0=OK)'),
    8    Float(name='measDitherPos', help='Measured dither position'),
    9    Float(name='cmdDitherPos', help='Commanded dither position'),
    10   Float(name='waveOffset', help='Average wavelength solution offset between measured and expected for 3 chips'),
    11   Float(name='exptimeEst', help='Estimated exposure time to reach snrGoal'),
    12   Float(name='numReadsToTarget', help='Estimated number of UTR reads to reach snrGoal'),
    13   Int(name='nReads', help='Total number of UTR reads requested'),
    14   Float(name='deltaSNRH12', help="Change in SNR from previous read"),
        help='Data about the most recent up-the-ramp read'),
        """
        def fmt(val, fmtStr="%s"):
            if val == None:
                return "?"
            else:
                return fmtStr % (val,)
        
        def fmt2(val1, val2, sep=" of ", fmtStr="%s"):
            return "%s%s%s" % (fmt(val1, fmtStr=fmtStr), sep, fmt(val2, fmtStr=fmtStr))
        
        def r2t(reads):
            timePerRead = self.apogeeModel.utrReadTime[0]
            if None in (reads, timePerRead):
                return None
            return reads * timePerRead
        
        def btest(bitField, bitInd):
            if bitField == None:
                return None
            return bitField & 1 << bitInd

        isCurrent = keyVar.isCurrent

        self.expNameWdg.set(keyVar[0], isCurrent=isCurrent)

        readNum = keyVar[1]
        totReads = keyVar[13]
        predReads = keyVar[12]
        readNumStr = "%s; pred %s" % (fmt2(readNum, totReads), fmt(predReads))
        self.readNumWdg.set(readNumStr, isCurrent=isCurrent)
#        self.predReadsWdg.set(fmt(predReads, fmtStr="%0.1f"), isCurrent=isCurrent)

        expTimeStr = "%s; pred %s" % (fmt2(r2t(readNum), r2t(totReads), fmtStr="%0.0f"), fmt(r2t(predReads), fmtStr="%0.0f"))
        self.expTimeWdg.set(expTimeStr, isCurrent=isCurrent)
#         self.predExpTimeWdg.set(fmt(r2t(predReads), fmtStr="%0.0f"), isCurrent=isCurrent)

        snr = keyVar[2]
        snrGoal = self.model.snrGoal[0]
        snrStr = fmt2(snr, snrGoal, fmtStr="%0.1f", sep="; want ")
        self.snrWdg.set(snrStr, isCurrent=isCurrent)

        ditherStrList = []
        ditherSev = RO.Constants.sevNormal
        if btest(keyVar[7], 1):
            ditherStrList.append("Bad")
            ditherSev = RO.Constants.sevError
        ditherStrList.append(fmt2(keyVar[8], keyVar[9], sep="/", fmtStr="%0.2f"))
        ditherStr = " ".join(ditherStrList)
        self.ditherWdg.set(ditherStr, isCurrent=isCurrent, severity=ditherSev)
        
        waveStrList = []
        waveSev = RO.Constants.sevNormal
        if btest(keyVar[7], 3):
            waveStrList.append("Bad")
            waveSev = RO.Constants.sevError
        waveStrList.append(fmt(keyVar[10], fmtStr="%0.2f"))
        waveStr = " ".join(waveStrList)
        self.wavelenWdg.set(waveStr, isCurrent=isCurrent, severity=waveSev)

        statusStrList = []
        statusSev = RO.Constants.sevNormal
        for name, ind in (("FITS Hdr", 0), ("Sky", 2)):
            if btest(keyVar[7], ind):
                statusStrList.append(name)
        if statusStrList:
            statusStr = "Bad %s" % (", ".join(statusStrList))
            statusSev = RO.Constants.sevError
        else:
            statusStr = "OK"
        self.statusWdg.set(statusStr, isCurrent=isCurrent, severity=statusSev)
        


if __name__ == '__main__':
    import TUI.Base.Wdg
    root = RO.Wdg.PythonTk()

    import TestData
    tuiModel = TestData.tuiModel

    testFrame = ReadStatusWdg(tuiModel.tkRoot)
    testFrame.pack(side="top", expand=True)
    
    statusBar = TUI.Base.Wdg.StatusBar(root)
    statusBar.pack(side="top", expand=True, fill="x")

    Tkinter.Button(text="Demo", command=TestData.animate).pack(side="top")

    TestData.start()

    tuiModel.reactor.run()
