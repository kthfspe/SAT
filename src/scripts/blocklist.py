ignore_blocktype = [ "FRAME", "IGNORE"]

physical_signals = ["DIG", "ANA", "CAN"]
functional_signals = ["FS"]

physical_blocks = ["SENS","OTSC","ECU","NCU","BAT","FCON","MCON","ACT","HMI","PCU"]
functional_blocks = ["ENVIN","ENVOUT","FE"]

physical_blocktypes = physical_blocks + physical_signals
functional_blocktypes = functional_blocks + functional_signals

defaultpowerlist = ["+24V", "+5V"]

mergefields_ignore_physical = ["id", "Filename", "PageName", "PageId", "MetaParent",  \
    "x", "y", "label", "placeholders", "edge", "MetaParent", "width", "relative", "as", "source_x", "source_y",\
       "target_x", "target_y", "target", "source" ]
mergefields_ignore_functional = ["id", "Filename", "PageName", "PageId", "MetaParent", "Allocation", \
    "x", "y", "label", "placeholders", "edge", "MetaParent", "width", "relative", "as", "source_x", "source_y",\
       "target_x", "target_y", "Function", "target" ]
mergefields_concat = ["id", "Function", "target"]
