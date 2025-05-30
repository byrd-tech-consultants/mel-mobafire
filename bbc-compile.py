#!/usr/bin/env python3
"""
BBCode Preprocessor
Removes comments from BBCode files for forum posting
Supports // line comments and /* block comments */
"""

import re
import sys
import argparse
from pathlib import Path

class BBCodePreprocessor:
    def __init__(self):
        self.stats = {
            'lines_removed': 0,
            'blocks_removed': 0,
            'original_lines': 0,
            'final_lines': 0
        }
    
    def remove_line_comments(self, content):
        """Remove // style comments (entire line)"""
        lines = content.split('\n')
        self.stats['original_lines'] = len(lines)
        
        filtered_lines = []
        for line in lines:
            # Skip lines that are only whitespace + // comment
            if re.match(r'^\s*//.*$', line):
                self.stats['lines_removed'] += 1
                continue
            filtered_lines.append(line)
        
        return '\n'.join(filtered_lines)
    
    def remove_block_comments(self, content):
        """Remove /* */ style block comments"""
        # Count block comments before removal
        blocks = re.findall(r'/\*[\s\S]*?\*/', content)
        self.stats['blocks_removed'] = len(blocks)
        
        # Remove block comments
        return re.sub(r'/\*[\s\S]*?\*/', '', content)
    
    def clean_whitespace(self, content):
        """Optional: remove excessive empty lines"""
        # Replace multiple consecutive newlines with max 2
        content = re.sub(r'\n\s*\n\s*\n+', '\n\n', content)
        
        # Count final lines
        self.stats['final_lines'] = len(content.split('\n'))
        
        return content.strip()
    
    def process_file(self, input_path, output_path, clean_whitespace=True):
        """Process a BBCode file and remove comments"""
        try:
            # Read input file
            with open(input_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Reset stats
            self.stats = {
                'lines_removed': 0,
                'blocks_removed': 0,
                'original_lines': 0,
                'final_lines': 0
            }
            
            # Process content
            content = self.remove_line_comments(content)
            content = self.remove_block_comments(content)
            
            if clean_whitespace:
                content = self.clean_whitespace(content)
            else:
                self.stats['final_lines'] = len(content.split('\n'))
            
            # Write output file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True, "Success"
            
        except FileNotFoundError:
            return False, f"Error: Input file '{input_path}' not found"
        except PermissionError:
            return False, f"Error: Permission denied writing to '{output_path}'"
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def print_stats(self):
        """Print processing statistics"""
        print(f"\nProcessing Statistics:")
        print(f"  Line comments removed: {self.stats['lines_removed']}")
        print(f"  Block comments removed: {self.stats['blocks_removed']}")
        print(f"  Original lines: {self.stats['original_lines']}")
        print(f"  Final lines: {self.stats['final_lines']}")
        print(f"  Lines saved: {self.stats['original_lines'] - self.stats['final_lines']}")

def main():
    parser = argparse.ArgumentParser(
        description='Remove comments from BBCode files',
        epilog='''
Examples:
  python bbcode_preprocessor.py input.bbcode output.bbcode
  python bbcode_preprocessor.py -k input.bbcode output.bbcode  # keep whitespace
  python bbcode_preprocessor.py --stats input.bbcode output.bbcode  # show stats
        ''',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('input_file', help='Input BBCode file with comments')
    parser.add_argument('output_file', help='Output BBCode file (clean)')
    parser.add_argument('-k', '--keep-whitespace', action='store_true',
                       help='Keep original whitespace (don\'t clean excessive newlines)')
    parser.add_argument('-s', '--stats', action='store_true',
                       help='Show processing statistics')
    
    args = parser.parse_args()
    
    # Validate input file exists
    input_path = Path(args.input_file)
    if not input_path.exists():
        print(f"Error: Input file '{args.input_file}' does not exist")
        return 1
    
    # Process file
    processor = BBCodePreprocessor()
    success, message = processor.process_file(
        args.input_file, 
        args.output_file, 
        clean_whitespace=not args.keep_whitespace
    )
    
    if success:
        print(f"✓ Successfully processed '{args.input_file}' -> '{args.output_file}'")
        if args.stats:
            processor.print_stats()
    else:
        print(f"✗ {message}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())