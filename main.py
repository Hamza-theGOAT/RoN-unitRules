import xml.etree.ElementTree as ET
import pandas as pd
from openpyxl import load_workbook
import os
import shutil
from dotenv import load_dotenv
from formatz import formatWB


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


def toExcel(pathz: dict, df: pd.DataFrame):
    wbN = pathz['wbNin']
    with pd.ExcelWriter(wbN) as xlwriter:
        df.to_excel(xlwriter, sheet_name='Main', index=False)
        domains = df['DOMAIN'].unique()
        for domain in domains:
            domDF = df[df['DOMAIN'] == domain].copy()
            sh = f'{domain}_Units'
            domDF.to_excel(xlwriter, sheet_name=sh, index=False)

    formatWB(wbN, wbN)


def updateRules(pathz: dict):
    # DataFrame for updated unit specs
    df = pd.read_excel(pathz['wbNout'], sheet_name='Upd')
    df.columns = df.columns.str.strip()
    df['NAME'] = df['NAME'].astype(str).str.strip()

    # Reset the updated unitrules.xml instance
    shutil.copy2(pathz['unitRules'], pathz['updStats'])

    # Get XML root
    tree = ET.parse(pathz['updStats'])
    root = tree.getroot()

    # Iterate over each row (each unit)
    for _, row in df.iterrows():
        unitName = row['NAME']

        for unit in root.findall('UNIT'):
            nameTag = unit.find('NAME')
            if nameTag is not None and nameTag.text.strip() == unitName:
                print(f"\nUpdating unit: {unitName}")
                for col in df.columns:
                    if col == 'NAME':
                        continue
                    if pd.notna(row[col]):
                        fieldTag = unit.find(col)
                        if fieldTag is not None:
                            print(f" - {col}: {fieldTag.text} → {row[col]}")
                            fieldTag.text = str(row[col])
                        else:
                            print(
                                f" - Field <{col}> not found in XML for {unitName}")
                break
        else:
            print(f"Unit <{unitName}> not found in XML")

    # Save updated XML
    tree.write(pathz['updStats'], encoding='utf-8', xml_declaration=True)


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

    # Save data to excel
    toExcel(pathz, unitSpecs)

    # Update unitrules.xml file in working_dir
    updateRules(pathz)


if __name__ == '__main__':
    main()
