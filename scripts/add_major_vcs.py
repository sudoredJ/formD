"""Add major VCs with known CIKs to the database."""

import re

# Major VCs with known SEC CIKs
MAJOR_VCS = [
    {"name": "Andreessen Horowitz", "aliases": ["a16z", "andreessen", "ah"], "website": "https://a16z.com", "cik": "1578090"},
    {"name": "Sequoia Capital", "aliases": ["sequoia"], "website": "https://www.sequoiacap.com", "cik": "1603454"},
    {"name": "Accel", "aliases": ["accel partners"], "website": "https://www.accel.com", "cik": "1437283"},
    {"name": "Kleiner Perkins", "aliases": ["kleiner", "kpcb"], "website": "https://www.kleinerperkins.com", "cik": "1385818"},
    {"name": "Lightspeed Venture Partners", "aliases": ["lightspeed", "lsvp"], "website": "https://lsvp.com", "cik": "1458961"},
    {"name": "Benchmark", "aliases": ["benchmark capital"], "website": "https://www.benchmark.com", "cik": "1357349"},
    {"name": "Greylock Partners", "aliases": ["greylock"], "website": "https://greylock.com", "cik": "1486159"},
    {"name": "Index Ventures", "aliases": ["index"], "website": "https://www.indexventures.com", "cik": "1609989"},
    {"name": "General Catalyst", "aliases": ["gc", "general catalyst partners"], "website": "https://www.generalcatalyst.com", "cik": "1493293"},
    {"name": "NEA", "aliases": ["new enterprise associates"], "website": "https://www.nea.com", "cik": "1456313"},
    {"name": "Lux Capital", "aliases": ["lux", "lux ventures"], "website": "https://www.luxcapital.com", "cik": "1534238"},
    {"name": "Founders Fund", "aliases": ["ff"], "website": "https://foundersfund.com", "cik": "1460270"},
    {"name": "Bessemer Venture Partners", "aliases": ["bessemer", "bvp"], "website": "https://www.bvp.com", "cik": "1391131"},
    {"name": "Tiger Global", "aliases": ["tiger", "tiger global management"], "website": "https://www.tigerglobal.com", "cik": "1167483"},
    {"name": "Insight Partners", "aliases": ["insight", "insight venture partners"], "website": "https://www.insightpartners.com", "cik": "1452860"},
    {"name": "Khosla Ventures", "aliases": ["khosla", "kv"], "website": "https://www.khoslaventures.com", "cik": "1539620"},
    {"name": "GGV Capital", "aliases": ["ggv"], "website": "https://www.ggvc.com", "cik": "1419862"},
    {"name": "Battery Ventures", "aliases": ["battery"], "website": "https://www.battery.com", "cik": "1280570"},
    {"name": "Redpoint Ventures", "aliases": ["redpoint"], "website": "https://www.redpoint.com", "cik": "1482188"},
    {"name": "First Round Capital", "aliases": ["first round", "frc"], "website": "https://firstround.com", "cik": "1432189"},
    {"name": "Union Square Ventures", "aliases": ["usv", "union square"], "website": "https://www.usv.com", "cik": "1408287"},
    {"name": "Spark Capital", "aliases": ["spark"], "website": "https://www.sparkcapital.com", "cik": "1409461"},
    {"name": "8VC", "aliases": ["8 vc", "eight vc"], "website": "https://8vc.com", "cik": "1654612"},
    {"name": "Emergence Capital", "aliases": ["emergence"], "website": "https://www.emcap.com", "cik": "1481506"},
    {"name": "Ribbit Capital", "aliases": ["ribbit"], "website": "https://ribbitcap.com", "cik": "1599053"},
    {"name": "IVP", "aliases": ["institutional venture partners"], "website": "https://www.ivp.com", "cik": "1293166"},
    {"name": "Mayfield", "aliases": ["mayfield fund"], "website": "https://www.mayfield.com", "cik": "1494163"},
    {"name": "Norwest Venture Partners", "aliases": ["norwest", "nvp"], "website": "https://www.nvp.com", "cik": "1396155"},
    {"name": "Coatue Management", "aliases": ["coatue"], "website": "https://www.coatue.com", "cik": "1536486"},
    {"name": "Thrive Capital", "aliases": ["thrive"], "website": "https://thrivecap.com", "cik": "1550627"},
    {"name": "Y Combinator", "aliases": ["yc", "ycombinator"], "website": "https://www.ycombinator.com", "cik": "1541761"},
    {"name": "Softbank Vision Fund", "aliases": ["softbank", "vision fund", "svf"], "website": "https://visionfund.com", "cik": "1793128"},
    {"name": "Paradigm", "aliases": ["paradigm crypto"], "website": "https://www.paradigm.xyz", "cik": "1849569"},
    {"name": "Dragoneer Investment Group", "aliases": ["dragoneer"], "website": "https://www.dragoneer.com", "cik": "1524880"},
    {"name": "Addition", "aliases": ["addition vc"], "website": "https://www.addition.com", "cik": "1833543"},
    {"name": "DST Global", "aliases": ["dst"], "website": "https://dst.global", "cik": "1529766"},
    {"name": "CRV", "aliases": ["charles river ventures"], "website": "https://www.crv.com", "cik": "1421855"},
    {"name": "Forerunner Ventures", "aliases": ["forerunner"], "website": "https://www.forerunnerventures.com", "cik": "1580587"},
    {"name": "Felicis Ventures", "aliases": ["felicis"], "website": "https://www.felicis.com", "cik": "1547481"},
    {"name": "Greenoaks Capital", "aliases": ["greenoaks"], "website": "https://www.greenoakscap.com", "cik": "1615844"},
    {"name": "Founders Circle Capital", "aliases": ["founders circle"], "website": "https://www.founderscircle.com", "cik": "1681777"},
    {"name": "Initialized Capital", "aliases": ["initialized"], "website": "https://initialized.com", "cik": "1667137"},
    {"name": "Social Capital", "aliases": [], "website": "https://www.socialcapital.com", "cik": "1651209"},
    {"name": "Lowercase Capital", "aliases": ["lowercase"], "website": "https://lowercasecapital.com", "cik": "1547011"},
    {"name": "SV Angel", "aliases": ["sv"], "website": "https://svangel.com", "cik": "1534237"},
    {"name": "True Ventures", "aliases": ["true"], "website": "https://trueventures.com", "cik": "1448217"},
    {"name": "Menlo Ventures", "aliases": ["menlo"], "website": "https://www.menlovc.com", "cik": "1427821"},
    {"name": "Shasta Ventures", "aliases": ["shasta"], "website": "https://shastaventures.com", "cik": "1406611"},
    {"name": "Scale Venture Partners", "aliases": ["scale", "scale ventures"], "website": "https://www.scalevp.com", "cik": "1414589"},
    {"name": "Foundation Capital", "aliases": ["foundation"], "website": "https://foundationcap.com", "cik": "1328330"},
]

def main():
    # Read existing file
    with open("/home/sudoredj/projects/formD/data/vc_firms.py", "r") as f:
        content = f.read()
    
    # Find where VC_FIRMS list starts
    match = re.search(r"VC_FIRMS = \[\n", content)
    if not match:
        print("Could not find VC_FIRMS list!")
        return
    
    # Build the major VCs entries
    major_entries = ""
    for vc in MAJOR_VCS:
        aliases_str = str(vc["aliases"])
        major_entries += f'''    {{
        "name": "{vc["name"]}",
        "aliases": {aliases_str},
        "website": "{vc["website"]}",
        "cik": "{vc["cik"]}",
    }},
'''
    
    major_entries += "    # --- CSV imported VCs below (no CIKs) ---\n"
    
    # Insert after VC_FIRMS = [
    insert_pos = match.end()
    new_content = content[:insert_pos] + major_entries + content[insert_pos:]
    
    # Write back
    with open("/home/sudoredj/projects/formD/data/vc_firms.py", "w") as f:
        f.write(new_content)
    
    print(f"Added {len(MAJOR_VCS)} major VCs with CIKs")

if __name__ == "__main__":
    main()

