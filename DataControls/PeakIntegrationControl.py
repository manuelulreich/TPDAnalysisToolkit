import tkinter as tk
import tkinter.ttk as ttk
from PlotsFrame import MPLContainer # pylint: disable=import-error
from DataControls.ControlElements import Chord, ScrolledListBox, EnhancedCheckButton, ProcessingStepControlBase, EnhancedEntry, DisplayOptionsFrame, SingleInputFileSelectionControl #ui element # pylint: disable=import-error
from DataModels.ProcessedDataWrapper import ProcessedDataWrapper # pylint: disable=import-error
from tkinter.filedialog import askopenfilename

class PeakIntegrationControl(ProcessingStepControlBase):
    def __init__(self, controller, root, accordion):
        super().__init__("Peak Integration (WIP)", controller, accordion)
        self.m_parsedData = None
        self.m_plots["Processed Data"] = MPLContainer(self.m_chord.m_notebookRef, "Processed Data", "Desorption Rate (arb. U.)", "Temperature (K)", root)

    def onFileSelected(self):
        self.m_parsedData = ProcessedDataWrapper(self.m_fileSelectionControl.m_inputFilePath)
        self.m_parsedData.parseProcessedDataFile()
        self.m_spectrumCB["values"] = self.m_parsedData.m_includedFiles
        # self.m_spectrumCB.current(0)

    def plotSelectedSpectrum(self):
        targetData = self.m_parsedData.fileNameToExpDesorptionRateVSTemp(self.m_spectrumCB.get())
        targetLabel = self.m_parsedData.fileNameToCoverageLabel(self.m_spectrumCB.get())
        self.m_plots["Processed Data"].clearPlots()
        self.m_plots["Processed Data"].addPrimaryLinePlots(targetData,targetLabel)
        # self.m_plots["Processed Data"].addVerticalLine(self.m_tCutEndEntry.get())
        # self.m_plots["Processed Data"].addVerticalLine(self.m_tCutStartEntry.get())

    def onSpectrumSelected(self, *args, **kwargs):
        if(self.m_parsedData != None):
            self.checkIntegrationBounds()
            self.plotSelectedSpectrum()


    def tryReadStartCutEntry(self):
        if(self.m_tCutStartEntry.get() == ''):
            return False
        try:
            int(self.m_tCutStartEntry.get())
        except ValueError:
            tk.messagebox.showerror("Initial Temperature", "Please enter an integer for the temperature at which to start integration.")
            return False
        return True

    def tryReadStopCutEntry(self):
        if(self.m_tCutEndEntry.get() == ''):
            return False
        try:
            int(self.m_tCutEndEntry.get())
        except ValueError:
            tk.messagebox.showerror("Final Temperature", "Please enter an integer for the temperature at which to end integration.")
            return False
        return True

    def checkIntegrationBounds(self):
        minStartCut = int(self.m_parsedData.getMinTemp())
        maxStopCut = int(self.m_parsedData.getMaxTemp())
        if(self.tryReadStartCutEntry()):
            if(minStartCut > int(self.m_tCutStartEntry.get())):
                self.m_tCutStartEntry.set(str(minStartCut))
        else:
            self.m_tCutStartEntry.set(str(minStartCut))
        if(self.tryReadStopCutEntry()):
            if(maxStopCut < int(self.m_tCutEndEntry.get())):
                self.m_tCutEndEntry.set(str(maxStopCut))
        else:
                self.m_tCutEndEntry.set(str(maxStopCut))

    def onBoundsChanged(self):
        self.checkIntegrationBounds()

    def initChordUI(self):
        self.m_chordFrame = self.m_chord.m_scrollable_frame

        # File selection

        self.m_fileSelectionControl = SingleInputFileSelectionControl(self.m_chordFrame, onSelect=self.onFileSelected)
        self.m_fileSelectionControl.grid(row=0, column = 0, columnspan = 4, sticky = "nsew")

        # Spectrum selection

        self.m_spectrumSelectionLabel = ttk.Label(self.m_chordFrame, text='Select TPD Spectrum for Integration:')
        self.m_spectrumSelectionLabel.grid(row = 1, column = 0, columnspan = 2, sticky="nsw")

        self.m_spectrumCB = ttk.Combobox(self.m_chordFrame)
        self.m_spectrumCB.configure(state = 'readonly')
        self.m_spectrumCB.bind("<<ComboboxSelected>>", self.onSpectrumSelected) #binding to event because CB does not have 'command' param
        self.m_spectrumCB.grid(row = 2, column = 0, columnspan = 3, sticky = "nsew")
        
        # self.m_spectrumSelectionLabel = ttk.Label(self.m_chordFrame, text='Select Mass Spectrum for Integration:')
        # self.m_spectrumSelectionLabel.grid(row = 3, column = 0, columnspan = 2, sticky="nsw")

        # self.m_spectrumCB = ttk.Combobox(self.m_chordFrame)
        # # self.m_prefactorCB.bind("<<ComboboxSelected>>", self.plotDataForSelectedPrefactor) #binding to event because CB does not have 'command' param
        # self.m_spectrumCB.grid(row = 4, column = 0, columnspan = 3, sticky = "nsew")

        # Integration Options

        self.m_optionsLabel = ttk.Label(self.m_chordFrame, text="Integration Options:")#, compound = tk.CENTER)
        self.m_optionsLabel.grid(row=5, column = 0, sticky = "nsw")
        
        self.m_tCutStartLabel = ttk.Label(self.m_chordFrame, text="Initial Temperature:")
        self.m_tCutStartLabel.grid(row=6, column = 1, sticky = "nse")

        self.m_tCutStartEntry = EnhancedEntry(self.m_chordFrame)
        self.m_tCutStartEntry.grid(row=6, column = 2, sticky = "nsw")

        self.m_tCutEndLabel = ttk.Label(self.m_chordFrame, text="Final Temperature:")
        self.m_tCutEndLabel.grid(row=7, column = 1, sticky = "nse")

        self.m_tCutEndEntry = EnhancedEntry(self.m_chordFrame)
        self.m_tCutEndEntry.grid(row=7, column = 2, sticky = "nsw")

        # Display Options

        self.m_showBoundsCB = EnhancedCheckButton(self.m_chordFrame, text="Show Temp. Bounds")




