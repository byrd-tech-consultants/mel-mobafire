import re

def extract_champion_sections(text):
    """Extract individual champion sections from BBCode text"""
    # Pattern to match each champion section including the responsive wrapper
    pattern = r'\[responsive\]\s*\[row\]\s*\[col width="100%"\]\s*\[spoiler=([^\]]+)\](.*?)\[/spoiler\]\s*\[/col\]\s*\[/row\]\s*\[/responsive\]'
    
    matches = re.findall(pattern, text, re.DOTALL)
    
    champions = []
    for match in matches:
        champion_name = match[0].strip()
        champion_content = match[1].strip()
        champions.append((champion_name, champion_content))
    
    return champions

def create_champion_section_without_spoiler(champion_name, content):
    """Create a champion section without the individual spoiler wrapper"""
    return f"""[responsive]
    [row]
        [col width="100%"]
            [anchor={champion_name}]
            [size=5][color=#FFD700][b]{champion_name}[/b][/color][/size]
            [size=1][color=#FFFF99] [/color][/size]
{content}
        [/col]
    [/row]
[/responsive]

"""

def split_champions_alphabetically(champions):
    """Split champions into A-L and M-Z groups"""
    a_to_l = []
    m_to_z = []
    
    for champion_name, content in champions:
        first_letter = champion_name[0].upper()
        if 'A' <= first_letter <= 'L':
            a_to_l.append((champion_name, content))
        else:
            m_to_z.append((champion_name, content))
    
    return a_to_l, m_to_z

def create_spoiler_section(champions, section_title):
    """Create a spoiler section containing multiple champions"""
    section_content = ""
    
    for champion_name, content in champions:
        section_content += create_champion_section_without_spoiler(champion_name, content)
    
    return f"""[spoiler={section_title}]
{section_content}[/spoiler]

"""

def process_matchups_file(input_file, output_file):
    """Main function to process the matchups file"""
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Extract champion sections
        champions = extract_champion_sections(text)
        
        if not champions:
            print("No champion sections found. Please check the input format.")
            return
        
        print(f"Found {len(champions)} champions:")
        for name, _ in champions:
            print(f"  - {name}")
        
        # Split alphabetically
        a_to_l, m_to_z = split_champions_alphabetically(champions)
        
        print(f"\nA-L group ({len(a_to_l)} champions):")
        for name, _ in a_to_l:
            print(f"  - {name}")
            
        print(f"\nM-Z group ({len(m_to_z)} champions):")
        for name, _ in m_to_z:
            print(f"  - {name}")
        
        # Create the new structure
        output_text = ""
        
        # Add A-L section
        if a_to_l:
            output_text += create_spoiler_section(a_to_l, "Champions A-L")
        
        # Add M-Z section  
        if m_to_z:
            output_text += create_spoiler_section(m_to_z, "Champions M-Z")
        
        # Write to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_text)
        
        print(f"\nSuccessfully processed matchups and saved to {output_file}")
        
    except FileNotFoundError:
        print(f"Error: Could not find input file '{input_file}'")
    except Exception as e:
        print(f"Error processing file: {e}")

def preview_output(input_text):
    """Preview the output without saving to file"""
    champions = extract_champion_sections(input_text)
    
    if not champions:
        print("No champion sections found in the provided text.")
        return ""
    
    a_to_l, m_to_z = split_champions_alphabetically(champions)
    
    output_text = ""
    if a_to_l:
        output_text += create_spoiler_section(a_to_l, "Champions A-L")
    if m_to_z:
        output_text += create_spoiler_section(m_to_z, "Champions M-Z")
    
    return output_text

# Example usage
if __name__ == "__main__":
    # Option 1: Process files
    input_filename = "matchups_input.txt"
    output_filename = "matchups_output.txt"
    
    print("BBCode Matchup Splitter")
    print("=" * 30)
    
    choice = input("Choose option:\n1. Process files\n2. Preview with sample text\nEnter choice (1 or 2): ")
    
    if choice == "1":
        # File processing mode
        process_matchups_file(input_filename, output_filename)
    elif choice == "2":
        # Preview mode with your sample text
        sample_text = """[responsive]
    [row]
        [col width="100%"]
            [spoiler=Ahri]
            [size=5][color=#FFD700][b]Ahri[/b][/color][/size]
            [size=1][color=#FFFF99] [/color][/size]
            <!-- Ahri content here -->
            [/spoiler]
        [/col]
    [/row]
[/responsive]

[responsive]
    [row]
        [col width="100%"]
            [spoiler=Akali]
            [anchor=Akali]
            [size=5][color=#FFD700][b]Akali[/b][/color][/size]
            [size=1][color=#FFFF99] [/color][/size]
            <!-- Akali content here -->
            [/spoiler]
        [/col]
    [/row]
[/responsive]"""
        
        result = preview_output(sample_text)
        print("\nPreview Output:")
        print("=" * 50)
        print(result)
    else:
        print("Invalid choice. Please run the program again.")