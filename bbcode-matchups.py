import re

def clean_matchup_sections(input_file, output_file):
    """
    Clean up BBCode matchup sections by:
    1. Consolidating duplicate champion title lines
    2. Adding separators between matchups
    """
    
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Pattern to match the duplicate champion title structure
    # This looks for the pattern where champion name appears twice with anchor in between
    pattern = r'\[size=5\]\[color=#FFD700\]\[b\]([^]]+)\[/b\]\[/color\]\[/size\]\s*\[size=1\]\[color=#FFFF99\]\s*\[/color\]\[/size\]\s*\[anchor=([^\]]+)\]\s*\[size=5\]\[color=#FFD700\]\[b\]\1\[/b\]\[/color\]\[/size\]\s*\[size=1\]\[color=#FFFF99\]\s*\[/color\]\[/size\]'
    
    def replace_champion_title(match):
        champion_name = match.group(1)
        anchor_name = match.group(2)
        # Return the consolidated version
        return f'[size=5][color=#FFD700][b]{champion_name}[/b][/color][/size] [size=1][color=#FFFF99] [/color][/size] [anchor={anchor_name}]'
    
    # Replace the duplicate champion titles
    content = re.sub(pattern, replace_champion_title, content, flags=re.MULTILINE | re.DOTALL)
    
    # Find all matchup sections (each responsive block containing a champion matchup)
    # Look for the pattern that ends each matchup section
    matchup_end_pattern = r'(\[/table\]\s*\[/col\]\s*\[/row\]\s*\[/responsive\])'
    
    def add_separator(match):
        original_ending = match.group(1)
        separator = '\n\n[center][size=5][color=#FF8C00][b]═══════════════════════════════════════════════════[/b][/color][/size][/center]\n'
        return original_ending + separator
    
    # Add separators after each matchup section
    content = re.sub(matchup_end_pattern, add_separator, content, flags=re.MULTILINE)
    
    # Clean up any extra whitespace that might have been created
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Write the cleaned content to output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(content)
    
    print(f"Successfully processed {input_file} and saved to {output_file}")

def main():
    input_filename = "matchups_input.txt"
    output_filename = "matchups_output.txt"
    
    try:
        clean_matchup_sections(input_filename, output_filename)
        print("Processing complete!")
        
        # Optional: Show a preview of changes
        print("\nPreview of changes made:")
        print("- Consolidated duplicate champion title lines")
        print("- Added separators between matchup sections")
        
    except FileNotFoundError:
        print(f"Error: Could not find {input_filename}")
        print("Please make sure the input file exists in the same directory as this script.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()