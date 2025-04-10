"""
Script to parse and extract data from the DataCite XML dataset.
"""
import xml.etree.ElementTree as ET
import pandas as pd
from pathlib import Path
import json

# Define paths
ROOT_DIR = Path(__file__).parent.parent
RAW_DATA_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DATA_DIR = ROOT_DIR / "data" / "processed"
XML_FILE = RAW_DATA_DIR / "24853467 (3).xml"

# Define namespace
NAMESPACE = {'datacite': 'http://datacite.org/schema/kernel-4'}

def clean_tag(tag):
    """Remove namespace from tag."""
    return tag.split('}')[-1] if '}' in tag else tag

def parse_xml():
    """Parse the XML file and extract all data."""
    print(f"Parsing {XML_FILE}...")
    
    # Parse XML
    tree = ET.parse(XML_FILE)
    root = tree.getroot()
    
    # Print structure information
    print("\nXML Structure:")
    print(f"Root tag: {clean_tag(root.tag)}")
    
    # Extract metadata
    metadata = {
        'identifier': None,
        'creators': [],
        'titles': [],
        'publisher': None,
        'publicationYear': None,
        'subjects': [],
        'dates': [],
        'descriptions': [],
        'alternateIdentifiers': []
    }
    
    # Get identifier
    identifier = root.find('.//datacite:identifier', NAMESPACE)
    if identifier is not None:
        metadata['identifier'] = {
            'value': identifier.text,
            'type': identifier.get('identifierType')
        }
    
    # Get creators
    for creator in root.findall('.//datacite:creator', NAMESPACE):
        creator_data = {}
        name = creator.find('datacite:creatorName', NAMESPACE)
        if name is not None:
            creator_data['name'] = name.text
        given_name = creator.find('datacite:givenName', NAMESPACE)
        if given_name is not None:
            creator_data['givenName'] = given_name.text
        family_name = creator.find('datacite:familyName', NAMESPACE)
        if family_name is not None:
            creator_data['familyName'] = family_name.text
        metadata['creators'].append(creator_data)
    
    # Get titles
    for title in root.findall('.//datacite:title', NAMESPACE):
        metadata['titles'].append(title.text)
    
    # Get publisher
    publisher = root.find('.//datacite:publisher', NAMESPACE)
    if publisher is not None:
        metadata['publisher'] = publisher.text
    
    # Get publication year
    pub_year = root.find('.//datacite:publicationYear', NAMESPACE)
    if pub_year is not None:
        metadata['publicationYear'] = pub_year.text
    
    # Get subjects
    for subject in root.findall('.//datacite:subject', NAMESPACE):
        if subject.text:
            metadata['subjects'].append(subject.text)
    
    # Get dates
    for date in root.findall('.//datacite:date', NAMESPACE):
        if date.text:
            metadata['dates'].append({
                'value': date.text,
                'type': date.get('dateType')
            })
    
    # Get descriptions
    for desc in root.findall('.//datacite:description', NAMESPACE):
        if desc.text:
            metadata['descriptions'].append({
                'value': desc.text,
                'type': desc.get('descriptionType')
            })
    
    # Get alternate identifiers
    for alt_id in root.findall('.//datacite:alternateIdentifier', NAMESPACE):
        if alt_id.text:
            metadata['alternateIdentifiers'].append({
                'value': alt_id.text,
                'type': alt_id.get('alternateIdentifierType')
            })
    
    # Save metadata as JSON
    output_path = PROCESSED_DATA_DIR / 'metadata.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    print(f"\nMetadata saved to {output_path}")
    
    return metadata

def analyze_metadata(metadata):
    """Analyze and print summary of the metadata."""
    print("\nMetadata Analysis:")
    
    if metadata['identifier']:
        print(f"\nIdentifier ({metadata['identifier']['type']}):")
        print(metadata['identifier']['value'])
    
    print(f"\nTitle: {metadata['titles'][0] if metadata['titles'] else 'N/A'}")
    
    print(f"\nCreators ({len(metadata['creators'])}):")
    for creator in metadata['creators']:
        print(f"- {creator.get('name', '')} ({creator.get('givenName', '')} {creator.get('familyName', '')})")
    
    print(f"\nPublisher: {metadata['publisher']}")
    print(f"Publication Year: {metadata['publicationYear']}")
    
    print(f"\nSubjects ({len(metadata['subjects'])}):")
    for subject in metadata['subjects']:
        print(f"- {subject}")
    
    print("\nDescriptions:")
    for desc in metadata['descriptions']:
        print(f"\n[{desc['type']}]")
        print(desc['value'][:200] + "..." if len(desc['value']) > 200 else desc['value'])

def main():
    """Main function to parse and analyze the XML data."""
    # Create processed directory if it doesn't exist
    PROCESSED_DATA_DIR.mkdir(exist_ok=True)
    
    # Parse XML and get metadata
    metadata = parse_xml()
    
    # Analyze metadata
    analyze_metadata(metadata)
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    main() 