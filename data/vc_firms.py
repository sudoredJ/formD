"""
Curated database of well-known VC firms.
This serves as a seed list for better search UX.
"""

VC_FIRMS = [
    # Tier 1 - Mega Funds
    {
        "name": "Andreessen Horowitz",
        "aliases": ["a16z", "andreessen"],
        "website": "https://a16z.com",
        "cik": "1578090",
        "location": "Menlo Park, CA",
        "focus": ["Software", "Crypto", "Bio", "Fintech", "Consumer"],
        "aum_estimate": "$35B+",
        "notable_partners": ["Marc Andreessen", "Ben Horowitz", "Chris Dixon", "Arianna Simpson"],
    },
    {
        "name": "Sequoia Capital",
        "aliases": ["sequoia"],
        "website": "https://www.sequoiacap.com",
        "cik": "1603454",
        "location": "Menlo Park, CA",
        "focus": ["Enterprise", "Consumer", "Fintech", "Healthcare"],
        "aum_estimate": "$85B+",
        "notable_partners": ["Roelof Botha", "Alfred Lin", "Shaun Maguire"],
    },
    {
        "name": "Accel",
        "aliases": ["accel partners"],
        "website": "https://www.accel.com",
        "cik": "1437283",
        "location": "Palo Alto, CA",
        "focus": ["Enterprise", "Consumer", "Fintech"],
        "aum_estimate": "$50B+",
        "notable_partners": ["Jim Breyer", "Sonali De Rycker", "Rich Wong"],
    },
    {
        "name": "Kleiner Perkins",
        "aliases": ["kleiner", "kpcb"],
        "website": "https://www.kleinerperkins.com",
        "cik": "1385818",
        "location": "Menlo Park, CA",
        "focus": ["Enterprise", "Consumer", "Hardtech", "Climate"],
        "aum_estimate": "$18B+",
        "notable_partners": ["Mamoon Hamid", "Bucky Moore", "Ilya Fushman"],
    },
    {
        "name": "Lightspeed Venture Partners",
        "aliases": ["lightspeed", "lsvp"],
        "website": "https://lsvp.com",
        "cik": "1458961",
        "location": "Menlo Park, CA",
        "focus": ["Enterprise", "Consumer", "Fintech", "Crypto"],
        "aum_estimate": "$25B+",
        "notable_partners": ["Ravi Mhatre", "Jeremy Liew", "Mercedes Bent"],
    },
    {
        "name": "Benchmark",
        "aliases": ["benchmark capital"],
        "website": "https://www.benchmark.com",
        "cik": "1357349",
        "location": "San Francisco, CA",
        "focus": ["Consumer", "Enterprise", "Marketplaces"],
        "aum_estimate": "$5B+",
        "notable_partners": ["Bill Gurley", "Peter Fenton", "Sarah Tavel"],
    },
    {
        "name": "Greylock Partners",
        "aliases": ["greylock"],
        "website": "https://greylock.com",
        "cik": "1486159",
        "location": "Menlo Park, CA",
        "focus": ["Enterprise", "Consumer", "AI"],
        "aum_estimate": "$20B+",
        "notable_partners": ["Reid Hoffman", "David Sze", "Sarah Guo"],
    },
    {
        "name": "Index Ventures",
        "aliases": ["index"],
        "website": "https://www.indexventures.com",
        "cik": "1609989",
        "location": "San Francisco, CA / London",
        "focus": ["Enterprise", "Consumer", "Fintech", "Gaming"],
        "aum_estimate": "$16B+",
        "notable_partners": ["Mike Volpi", "Danny Rimer", "Nina Achadjian"],
    },
    {
        "name": "General Catalyst",
        "aliases": ["gc", "general catalyst partners"],
        "website": "https://www.generalcatalyst.com",
        "cik": "1493293",
        "location": "Cambridge, MA",
        "focus": ["Enterprise", "Consumer", "Health", "Fintech"],
        "aum_estimate": "$25B+",
        "notable_partners": ["Hemant Taneja", "Deep Nishar", "Niko Bonatsos"],
    },
    {
        "name": "NEA",
        "aliases": ["new enterprise associates"],
        "website": "https://www.nea.com",
        "cik": "1456313",
        "location": "Menlo Park, CA",
        "focus": ["Enterprise", "Healthcare", "Consumer"],
        "aum_estimate": "$25B+",
        "notable_partners": ["Scott Sandell", "Liza Landsman", "Tony Florence"],
    },
    
    # Tier 2 - Major Funds
    {
        "name": "Lux Capital",
        "aliases": ["lux", "lux ventures"],
        "website": "https://www.luxcapital.com",
        "cik": "1534238",
    },
    {
        "name": "SV Angel",
        "aliases": ["sv angel", "svangel"],
        "website": "https://svangel.com",
        "cik": "1516655",
    },
    {
        "name": "Root Ventures",
        "aliases": ["root"],
        "website": "https://root.vc",
        "cik": "1626606",
    },
    {
        "name": "Walden Catalyst Ventures",
        "aliases": ["walden", "walden catalyst"],
        "website": "https://www.waldenvc.com",
        "cik": "1358711",
    },
    {
        "name": "First Round Capital",
        "aliases": ["first round", "frc"],
        "website": "https://firstround.com",
        "cik": "1415535",
    },
    {
        "name": "Bessemer Venture Partners",
        "aliases": ["bessemer", "bvp"],
        "website": "https://www.bvp.com",
        "cik": "1389941",
    },
    {
        "name": "Union Square Ventures",
        "aliases": ["usv", "union square"],
        "website": "https://www.usv.com",
        "cik": "1415163",
    },
    {
        "name": "Spark Capital",
        "aliases": ["spark"],
        "website": "https://www.sparkcapital.com",
        "cik": "1445970",
    },
    {
        "name": "Insight Partners",
        "aliases": ["insight"],
        "website": "https://www.insightpartners.com",
        "cik": "1370063",
    },
    {
        "name": "Tiger Global",
        "aliases": ["tiger", "tiger global management"],
        "website": "https://www.tigerglobal.com",
        "cik": "1167483",
    },
    {
        "name": "Coatue Management",
        "aliases": ["coatue"],
        "website": "https://www.coatue.com",
        "cik": "1343009",
    },
    {
        "name": "Khosla Ventures",
        "aliases": ["khosla", "kv"],
        "website": "https://www.khoslaventures.com",
        "cik": "1487526",
    },
    {
        "name": "Felicis Ventures",
        "aliases": ["felicis"],
        "website": "https://www.felicis.com",
        "cik": "1533426",
    },
    {
        "name": "Initialized Capital",
        "aliases": ["initialized"],
        "website": "https://initialized.com",
        "cik": "1630039",
    },
    {
        "name": "Forerunner Ventures",
        "aliases": ["forerunner"],
        "website": "https://forerunnerventures.com",
        "cik": "1548360",
    },
    {
        "name": "Craft Ventures",
        "aliases": ["craft"],
        "website": "https://www.craftventures.com",
        "cik": "1755953",
    },
    {
        "name": "Ribbit Capital",
        "aliases": ["ribbit"],
        "website": "https://ribbitcap.com",
        "cik": "1571246",
    },
    {
        "name": "Thrive Capital",
        "aliases": ["thrive"],
        "website": "https://www.thrivecap.com",
        "cik": "1557839",
    },
    {
        "name": "Slow Ventures",
        "aliases": ["slow"],
        "website": "https://slow.co",
        "cik": "1586413",
    },
    {
        "name": "Lowercase Capital",
        "aliases": ["lowercase"],
        "website": "https://lowercasecapital.com",
        "cik": "1543617",
    },
    {
        "name": "Collaborative Fund",
        "aliases": ["collaborative"],
        "website": "https://www.collaborativefund.com",
        "cik": "1561370",
    },
    {
        "name": "Menlo Ventures",
        "aliases": ["menlo"],
        "website": "https://www.menlovc.com",
        "cik": "1389936",
    },
    {
        "name": "IVP",
        "aliases": ["institutional venture partners"],
        "website": "https://www.ivp.com",
        "cik": "1402125",
    },
    {
        "name": "Battery Ventures",
        "aliases": ["battery"],
        "website": "https://www.battery.com",
        "cik": "1371981",
    },
    {
        "name": "Redpoint Ventures",
        "aliases": ["redpoint"],
        "website": "https://www.redpoint.com",
        "cik": "1406388",
    },
    {
        "name": "Norwest Venture Partners",
        "aliases": ["norwest", "nvp"],
        "website": "https://www.nvp.com",
        "cik": "1371127",
    },
    {
        "name": "GGV Capital",
        "aliases": ["ggv"],
        "website": "https://www.ggvc.com",
        "cik": "1431873",
    },
    {
        "name": "Mayfield Fund",
        "aliases": ["mayfield"],
        "website": "https://www.mayfield.com",
        "cik": "1389937",
    },
    {
        "name": "Shasta Ventures",
        "aliases": ["shasta"],
        "website": "https://shastaventures.com",
        "cik": "1447986",
    },
    {
        "name": "True Ventures",
        "aliases": ["true"],
        "website": "https://trueventures.com",
        "cik": "1447985",
    },
    {
        "name": "Upfront Ventures",
        "aliases": ["upfront"],
        "website": "https://upfront.com",
        "cik": "1422012",
    },
    {
        "name": "Foundry Group",
        "aliases": ["foundry"],
        "website": "https://foundrygroup.com",
        "cik": "1437614",
    },
    {
        "name": "Scale Venture Partners",
        "aliases": ["scale"],
        "website": "https://www.scalevp.com",
        "cik": "1449133",
    },
    {
        "name": "Matrix Partners",
        "aliases": ["matrix"],
        "website": "https://www.matrixpartners.com",
        "cik": "1389943",
    },
    {
        "name": "Sapphire Ventures",
        "aliases": ["sapphire"],
        "website": "https://sapphireventures.com",
        "cik": "1604484",
    },
    {
        "name": "8VC",
        "aliases": ["8vc", "eight vc"],
        "website": "https://8vc.com",
        "cik": "1651197",
    },
    {
        "name": "Social Capital",
        "aliases": ["social capital", "chamath"],
        "website": "https://www.socialcapital.com",
        "cik": "1603966",
    },
    {
        "name": "DST Global",
        "aliases": ["dst"],
        "website": "https://dst.global",
        "cik": "1536486",
    },
    {
        "name": "CRV",
        "aliases": ["charles river ventures"],
        "website": "https://www.crv.com",
        "cik": "1389942",
    },
    {
        "name": "Balderton Capital",
        "aliases": ["balderton"],
        "website": "https://www.balderton.com",
        "cik": "1518977",
    },
    {
        "name": "Atomico",
        "aliases": ["atomico"],
        "website": "https://www.atomico.com",
        "cik": "1642044",
    },
    {
        "name": "Founders Fund",
        "aliases": ["ff", "founders", "founders fund growth", "peter thiel"],
        "website": "https://foundersfund.com",
        "cik": "2059945",
        "location": "San Francisco, CA",
        "focus": ["Deep Tech", "Consumer", "Enterprise", "Crypto"],
        "aum_estimate": "$11B+",
        "notable_partners": ["Peter Thiel", "Keith Rabois", "Trae Stephens"],
    },
    {
        "name": "Bessemer Venture Partners",
        "aliases": ["bessemer", "bvp"],
        "website": "https://www.bvp.com",
        "cik": "1391131",
        "location": "San Francisco, CA",
        "focus": ["Enterprise", "Consumer", "Healthcare"],
        "aum_estimate": "$20B+",
        "notable_partners": ["Byron Deeter", "Ethan Kurzweil", "Mary D'Onofrio"],
    },
    {
        "name": "Tiger Global",
        "aliases": ["tiger", "tiger global management"],
        "website": "https://www.tigerglobal.com",
        "cik": "1167483",
        "location": "New York, NY",
        "focus": ["Growth", "Enterprise", "Consumer", "Fintech"],
        "aum_estimate": "$80B+",
        "notable_partners": ["Chase Coleman", "Scott Shleifer", "John Curtius"],
    },
    {
        "name": "Insight Partners",
        "aliases": ["insight", "insight venture partners"],
        "website": "https://www.insightpartners.com",
        "cik": "1452860",
        "location": "New York, NY",
        "focus": ["Growth", "Enterprise Software"],
        "aum_estimate": "$90B+",
        "notable_partners": ["Jeff Horing", "Deven Parekh", "Lonne Jaffe"],
    },
    {
        "name": "Khosla Ventures",
        "aliases": ["khosla", "kv"],
        "website": "https://www.khoslaventures.com",
        "cik": "1539620",
        "location": "Menlo Park, CA",
        "focus": ["Deep Tech", "Climate", "AI", "Healthcare"],
        "aum_estimate": "$15B+",
        "notable_partners": ["Vinod Khosla", "Samir Kaul", "Sven Strohband"],
    },
    {
        "name": "GGV Capital",
        "aliases": ["ggv"],
        "website": "https://www.ggvc.com",
        "cik": "1419862",
        "location": "Menlo Park, CA",
        "focus": ["Enterprise", "Consumer", "Fintech"],
        "aum_estimate": "$9B+",
        "notable_partners": ["Hans Tung", "Glenn Solomon", "Jeff Richards"],
    },
    {
        "name": "Battery Ventures",
        "aliases": ["battery"],
        "website": "https://www.battery.com",
        "cik": "1280570",
        "location": "Boston, MA",
        "focus": ["Enterprise", "Infrastructure", "Industrial Tech"],
        "aum_estimate": "$13B+",
        "notable_partners": ["Neeraj Agrawal", "Chelsea Stoner", "Dharmesh Thakker"],
    },
    {
        "name": "Redpoint Ventures",
        "aliases": ["redpoint"],
        "website": "https://www.redpoint.com",
        "cik": "1482188",
        "location": "Menlo Park, CA",
        "focus": ["Enterprise", "Consumer", "Infrastructure"],
        "aum_estimate": "$6B+",
        "notable_partners": ["Tomasz Tunguz", "Annie Kadavy", "Logan Bartlett"],
    },
    {
        "name": "First Round Capital",
        "aliases": ["first round", "frc"],
        "website": "https://firstround.com",
        "cik": "1432189",
        "location": "San Francisco, CA",
        "focus": ["Seed", "Enterprise", "Consumer"],
        "aum_estimate": "$1B+",
        "notable_partners": ["Josh Kopelman", "Phin Barnes", "Hayley Barna"],
    },
    
    # Tier 3 - Specialized / Regional
    {
        "name": "Union Square Ventures",
        "aliases": ["usv", "union square"],
        "website": "https://www.usv.com",
        "cik": "1408287",
        "location": "New York, NY",
        "focus": ["Networks", "Marketplaces", "Crypto"],
        "aum_estimate": "$2B+",
        "notable_partners": ["Fred Wilson", "Albert Wenger", "Rebecca Kaden"],
    },
    {
        "name": "Spark Capital",
        "aliases": ["spark"],
        "website": "https://www.sparkcapital.com",
        "cik": "1409461",
        "location": "San Francisco, CA",
        "focus": ["Consumer", "Enterprise"],
        "aum_estimate": "$3B+",
        "notable_partners": ["Bijan Sabet", "Megan Quinn", "Nabeel Hyatt"],
    },
    {
        "name": "8VC",
        "aliases": ["8 vc", "eight vc"],
        "website": "https://8vc.com",
        "cik": "1654612",
        "location": "Austin, TX",
        "focus": ["Enterprise", "Defense", "Healthcare", "Logistics"],
        "aum_estimate": "$5B+",
        "notable_partners": ["Joe Lonsdale", "Drew Oetting", "Kimmy Scotti"],
    },
    {
        "name": "Andreessen Horowitz Bio",
        "aliases": ["a16z bio"],
        "website": "https://a16z.com/bio-health",
        "cik": "1866973",
        "location": "Menlo Park, CA",
        "focus": ["Bio", "Healthcare", "Life Sciences"],
        "aum_estimate": "$3B+",
        "notable_partners": ["Vijay Pande", "Jorge Conde", "Julie Yoo"],
    },
    {
        "name": "Emergence Capital",
        "aliases": ["emergence"],
        "website": "https://www.emcap.com",
        "cik": "1481506",
        "location": "San Mateo, CA",
        "focus": ["Enterprise SaaS", "B2B"],
        "aum_estimate": "$3B+",
        "notable_partners": ["Jason Green", "Santi Subotovsky", "Jake Saper"],
    },
    {
        "name": "Ribbit Capital",
        "aliases": ["ribbit"],
        "website": "https://ribbitcap.com",
        "cik": "1599053",
        "location": "Palo Alto, CA",
        "focus": ["Fintech"],
        "aum_estimate": "$4B+",
        "notable_partners": ["Micky Malka", "Nick Shalek", "Sigal Mandelker"],
    },
    {
        "name": "IVP",
        "aliases": ["institutional venture partners"],
        "website": "https://www.ivp.com",
        "cik": "1293166",
        "location": "Menlo Park, CA",
        "focus": ["Growth", "Enterprise", "Consumer"],
        "aum_estimate": "$9B+",
        "notable_partners": ["Somesh Dash", "Eric Liaw", "Tom Loverro"],
    },
    {
        "name": "Mayfield",
        "aliases": ["mayfield fund"],
        "website": "https://www.mayfield.com",
        "cik": "1494163",
        "location": "Menlo Park, CA",
        "focus": ["Enterprise", "Consumer", "AI"],
        "aum_estimate": "$3B+",
        "notable_partners": ["Navin Chaddha", "Rajeev Batra", "Ursheet Parikh"],
    },
    {
        "name": "Norwest Venture Partners",
        "aliases": ["norwest", "nvp"],
        "website": "https://www.nvp.com",
        "cik": "1396155",
        "location": "Palo Alto, CA",
        "focus": ["Enterprise", "Healthcare", "Consumer"],
        "aum_estimate": "$12B+",
        "notable_partners": ["Jeff Crowe", "Sonya Brown", "Rama Sekhar"],
    },
    {
        "name": "Coatue Management",
        "aliases": ["coatue"],
        "website": "https://www.coatue.com",
        "cik": "1536486",
        "location": "New York, NY",
        "focus": ["Growth", "Technology"],
        "aum_estimate": "$75B+",
        "notable_partners": ["Philippe Laffont", "Thomas Laffont", "Caryn Marooney"],
    },
    {
        "name": "Thrive Capital",
        "aliases": ["thrive"],
        "website": "https://thrivecap.com",
        "cik": "1550627",
        "location": "New York, NY",
        "focus": ["Consumer", "Enterprise", "Fintech"],
        "aum_estimate": "$15B+",
        "notable_partners": ["Josh Kushner", "Kareem Zaki", "Miles Grimshaw"],
    },
    {
        "name": "Y Combinator",
        "aliases": ["yc", "ycombinator"],
        "website": "https://www.ycombinator.com",
        "cik": "1541761",
        "location": "Mountain View, CA",
        "focus": ["Seed", "All Sectors"],
        "aum_estimate": "$6B+",
        "notable_partners": ["Garry Tan", "Dalton Caldwell", "Michael Seibel"],
    },
    {
        "name": "a]fin Capital",
        "aliases": ["fin", "a]fin vc"],
        "website": "https://www.fin.vc",
        "cik": "",
        "location": "San Francisco, CA",
        "focus": ["Fintech", "B2B"],
        "aum_estimate": "$500M+",
        "notable_partners": ["Logan Allin", "Matthew Witheiler"],
    },
    {
        "name": "Softbank Vision Fund",
        "aliases": ["softbank", "vision fund", "svf"],
        "website": "https://visionfund.com",
        "cik": "1793128",
        "location": "London / San Carlos, CA",
        "focus": ["Growth", "AI", "Mobility", "Fintech"],
        "aum_estimate": "$100B+",
        "notable_partners": ["Masayoshi Son", "Rajeev Misra", "Marcelo Claure"],
    },
    {
        "name": "Paradigm",
        "aliases": ["paradigm crypto"],
        "website": "https://www.paradigm.xyz",
        "cik": "1849569",
        "location": "San Francisco, CA",
        "focus": ["Crypto", "Web3"],
        "aum_estimate": "$10B+",
        "notable_partners": ["Matt Huang", "Fred Ehrsam", "Dan Robinson"],
    },
    {
        "name": "Dragoneer Investment Group",
        "aliases": ["dragoneer"],
        "website": "https://www.dragoneer.com",
        "cik": "1524880",
        "location": "San Francisco, CA",
        "focus": ["Growth", "Technology"],
        "aum_estimate": "$25B+",
        "notable_partners": ["Marc Stad", "Chris Barter"],
    },
    {
        "name": "Addition",
        "aliases": ["addition vc"],
        "website": "https://www.addition.com",
        "cik": "1833543",
        "location": "New York, NY",
        "focus": ["Growth", "Consumer", "Enterprise"],
        "aum_estimate": "$4B+",
        "notable_partners": ["Lee Fixel"],
    },
    {
        "name": "DST Global",
        "aliases": ["dst"],
        "website": "https://dst.global",
        "cik": "1529766",
        "location": "Hong Kong",
        "focus": ["Growth", "Consumer Tech"],
        "aum_estimate": "$40B+",
        "notable_partners": ["Yuri Milner", "John Lindfors", "Tom Stafford"],
    },
    {
        "name": "CRV",
        "aliases": ["charles river ventures"],
        "website": "https://www.crv.com",
        "cik": "1421855",
        "location": "Palo Alto, CA",
        "focus": ["Enterprise", "Consumer", "Bio"],
        "aum_estimate": "$4B+",
        "notable_partners": ["Saar Gur", "Anna Khan", "Max Gazor"],
    },
]


def search_curated_vcs(query: str, limit: int = 10) -> list[dict]:
    """
    Search the curated VC database.
    Returns matches based on name and aliases. Deduplicates by normalized name.
    """
    query_lower = query.lower().strip()
    if len(query_lower) < 2:
        return []
    
    results = []
    seen_names = set()  # Track normalized names to avoid duplicates
    
    for firm in VC_FIRMS:
        # Normalize name for deduplication
        normalized = firm["name"].lower().strip()
        if normalized in seen_names:
            continue
        
        matched = False
        
        # Check main name
        if query_lower in firm["name"].lower():
            matched = True
        else:
            # Check aliases
            for alias in firm.get("aliases", []):
                if query_lower in alias.lower():
                    matched = True
                    break
        
        if matched:
            seen_names.add(normalized)
            results.append(firm)
    
    # Sort by name length (shorter = more relevant) then alphabetically
    results.sort(key=lambda x: (len(x["name"]), x["name"]))
    return results[:limit]


def get_curated_vc_by_cik(cik: str) -> dict | None:
    """Get a curated VC by CIK."""
    cik_clean = cik.lstrip("0")
    for firm in VC_FIRMS:
        if firm.get("cik", "").lstrip("0") == cik_clean:
            return firm
    return None


def get_curated_vc_by_name(name: str) -> dict | None:
    """Get a curated VC by exact name match."""
    name_lower = name.lower()
    for firm in VC_FIRMS:
        if firm["name"].lower() == name_lower:
            return firm
        for alias in firm.get("aliases", []):
            if alias.lower() == name_lower:
                return firm
    return None

