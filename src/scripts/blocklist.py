physical_blocktypes = ["DIG","ANA","SENS","OTSC","ECU","CAN","NCU","BAT","FCON","MCON","ACT","HMI","PCU"]
functional_blocktypes = ["ENVIN","ENVOUT","FE","FS"]

ignore_blocktype = [ "FRAME", "IGNORE"]

physical_signals = ["DIG", "ANA", "CAN"]
functional_signals = ["FS"]

physical_blocks = ["SENS","OTSC","ECU","NCU","BAT","FCON","MCON","ACT","HMI","PCU"]
functional_blocks = ["ENVIN","ENVOUT","FE"]

defaultpowerlist = ["+24V", "+5V"]

mergefields_ignore = ["id", "Filename", "PageName", "PageId", "MetaParent", "Allocation", \
    "x", "y", "label", "placeholders", "edge", "MetaParent", "width", "relative", "as", "source_x", "source_y",\
       "target_x", "target_y" ]
mergefields_concat = ["id", "Function", "target"]
