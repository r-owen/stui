import TUI.Base.TestDispatcher

testDispatcher = TUI.Base.TestDispatcher.TestDispatcher("apogeeql", delay=0.5)
tuiModel = testDispatcher.tuiModel

MainDataList = (
    "exposureData=1001, 1, 00000113, 600.0, 5, 30.0,  0.0, 28.2,  600, 28.2",
    "exposureData=1001, 2, 00000114, 600.0, 5, 30.0,  0.5, 28.2, 1200, 39.9",
    "exposureData=1001, 3, 00000115, 600.0, 5, 30.0, -0.5, 28.2, 1800, 48.8",
    "exposureData=1001, 4, 00000116, 600.0, 5, 30.0,  0.5, 28.2, 2400, 56.4",
    "exposureData=1001, 5, 00000117, 600.0, 5, 30.0, -0.5, 28.2, 3000, 63.1",
    "exposureData=1001, 6, 00000118, 600.0, 5, 30.0,  0.5, 28.2, 3600, 69.1",
    "snrH12Target=30",
    "utrData=6, 1, 10, -99.05, 174.10, -98.70, 171.90, 0, 0.51, 0.50, 1.0, 633.0, 6",
    "utrData=6, 2, 15, -99.05, 174.10, -98.70, 171.90, 0, 0.51, 0.50, 1.0, 633.0, 6",
    "utrData=6, 3, 20, -99.05, 174.10, -98.70, 171.90, 0, 0.51, 0.50, 1.0, 633.0, 6",
    "utrData=6, 4, 24, -99.05, 174.10, -98.70, 171.90, 0, 0.51, 0.50, 1.0, 633.0, 6",
    "utrData=6, 5, 28, -99.05, 174.10, -98.70, 171.90, 0, 0.51, 0.50, 1.0, 633.0, 6",
    "snrAxisRange=14, 32",
)

AnimDataSet = (
    (
    ),
)

def start():
    print "dispatch MainDataList"
    testDispatcher.dispatch(MainDataList)
    
def animate(dataIter=None):
    testDispatcher.runDataSet(AnimDataSet)
