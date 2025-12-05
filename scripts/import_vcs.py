"""
Script to import VCs from OpenVC CSV.
Filters for VCs/groups (not solo angels) that would plausibly file Form D.

Min check sizes noted for reference only - we calculate from Form D data per cookbook.
"""

import csv
import json
import sys

# Investor types to include (would plausibly have Form D)
INCLUDE_TYPES = {
    "vc",
    "angel network", 
    "family office",
    "pe fund",
    "startup studio",
    "accelerator",
    "cvc",  # corporate VC
    "micro vc",
}

# Types to exclude
EXCLUDE_TYPES = {
    "angel",
    "solo angel",
    "individual",
}


def parse_money(val: str) -> int:
    """Parse $100000 to 100000"""
    if not val:
        return 0
    val = val.replace("$", "").replace(",", "").strip()
    try:
        return int(val)
    except:
        return 0


def process_csv(filepath: str) -> list[dict]:
    """Process OpenVC CSV and return list of VCs."""
    vcs = []
    
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        
        for row in reader:
            if len(row) < 7:
                continue
            
            name = row[0].strip()
            website = row[1].strip()
            investor_type = row[6].strip().lower() if len(row) > 6 else ""
            min_check = parse_money(row[7]) if len(row) > 7 else 0
            
            # Skip if no name
            if not name:
                continue
            
            # Filter by investor type
            type_ok = any(t in investor_type for t in INCLUDE_TYPES)
            type_bad = any(t in investor_type for t in EXCLUDE_TYPES)
            
            if type_bad and not type_ok:
                continue
            
            if not type_ok:
                continue
            
            vcs.append({
                "name": name,
                "website": website if website.startswith("http") else "",
                "_min_check": min_check,  # Reference only
            })
    
    return vcs


def generate_python_file(vcs: list[dict], output_path: str):
    """Generate the vc_firms.py file."""
    
    # Sort by name
    vcs.sort(key=lambda x: x["name"].lower())
    
    output = '''"""
Curated database of VC firms from OpenVC.
Note: min_check is for reference only - we calculate check size from Form D data.
"""

VC_FIRMS = [
'''
    
    for vc in vcs:
        name_escaped = vc["name"].replace('"', '\\"')
        website = vc["website"]
        
        # Generate simple aliases from name
        aliases = []
        name_lower = vc["name"].lower()
        
        # Common abbreviations
        if "ventures" in name_lower:
            aliases.append(name_lower.replace(" ventures", "").strip())
        if "capital" in name_lower:
            aliases.append(name_lower.replace(" capital", "").strip())
        if "partners" in name_lower:
            aliases.append(name_lower.replace(" partners", "").strip())
        
        aliases_str = json.dumps(aliases[:3]) if aliases else "[]"
        
        output += f'''    {{
        "name": "{name_escaped}",
        "aliases": {aliases_str},
        "website": "{website}",
        "cik": "",  # To be populated from SEC EDGAR
    }},
'''
    
    output += ''']


def search_curated_vcs(query: str, limit: int = 10) -> list[dict]:
    """Search the curated VC database."""
    query_lower = query.lower().strip()
    if len(query_lower) < 2:
        return []
    
    results = []
    for firm in VC_FIRMS:
        # Check main name
        if query_lower in firm["name"].lower():
            results.append(firm)
            continue
        
        # Check aliases
        for alias in firm.get("aliases", []):
            if query_lower in alias.lower():
                results.append(firm)
                break
    
    results.sort(key=lambda x: (len(x["name"]), x["name"]))
    return results[:limit]


def get_curated_vc_by_cik(cik: str) -> dict | None:
    """Get a curated VC by CIK."""
    cik_clean = cik.lstrip("0")
    for firm in VC_FIRMS:
        if firm.get("cik", "").lstrip("0") == cik_clean and cik_clean:
            return firm
    return None


def get_curated_vc_by_name(name: str) -> dict | None:
    """Get a curated VC by exact name match."""
    name_lower = name.lower()
    for firm in VC_FIRMS:
        if firm["name"].lower() == name_lower:
            return firm
    return None
'''
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output)
    
    print(f"Generated {output_path} with {len(vcs)} VCs")


if __name__ == "__main__":
    csv_path = "/mnt/c/Users/sudoredJ/Downloads/Oct 2025 - OpenVC.csv"
    output_path = "/home/sudoredj/projects/formD/data/vc_firms.py"
    
    vcs = process_csv(csv_path)
    print(f"Found {len(vcs)} VCs after filtering")
    
    generate_python_file(vcs, output_path)

