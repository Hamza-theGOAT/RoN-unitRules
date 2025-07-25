import xml.etree.ElementTree as ET
import pandas as pd
import os
import shutil


def unitData(xml):
    # Parse the unitrules.xml file
    tree = ET.parse(xml)
    root = tree.getroot()

    unitSpecs = []
    aspects = [
        'NAME', 'GRAPH', 'OBJ_MASK', 'FLAGS', 'WHERE', 'ATTACK',
        'HITS', 'MOVES', 'SUPPORT', 'COST', 'JOB_TIME', 'PREQ0',
        'FROM', 'JUMP', 'RANGE', 'LOS', 'RECHARGE', 'ARMOR', 'DOMAIN'
    ]

    for unit in root.findall('.//UNIT'):
        unitSpec = {}
        for aspect in aspects:
            elmt = unit.find(aspect)
            unitSpec[aspect] = elmt.text if elmt is not None else None

        if unitSpec['NAME']:
            unitSpecs.append(unitSpec)

    return pd.DataFrame(unitSpecs)
