import xml.etree.ElementTree as ET
import pandas as pd
import os
import shutil
from dotenv import load_dotenv


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


def getPathz():
    # Project directories
    sdir = 'source_dir'
    wdir = 'working_dir'
    stdir = 'storage_dir'

    # Project file paths
    unitRules = os.path.join(sdir, 'unitrules.xml')
    updStats = os.path.join(wdir, 'unitrules.xml')
    wbNin = os.path.join(wdir, 'unitStats.xlsx')
    wbNout = os.path.join(wdir, 'unitStats_Alt.xlsx')

    # unitrules.xml file path in game directory
    load_dotenv()
    gameRules = os.getenv('gameRules')

    return {
        'sdir': sdir,
        'wdir': wdir,
        'stdir': stdir,
        'unitRules': unitRules,
        'updStats': updStats,
        'wbNin': wbNin,
        'wbNout': wbNout,
        'gameRules': gameRules
    }


def main():
    # Get project paths dictionary
    pathz = getPathz()

    # Get unit specs as pd.DataFrame after parsing xml data
    unitSpecs = unitData(pathz['unitRules'])


if __name__ == '__main__':
    main()
