#!/usr/bin/env python3
"""
Circuit CLI - Command-line tool for working with .circuit.json files

Usage:
    circuit validate <file>           - Validate a circuit file
    circuit render <file> [--3d]      - Render circuit visualization
    circuit export <file> --format    - Export to different formats
    circuit info <file>                - Display circuit information
    circuit --version                  - Show version
    circuit --help                     - Show help

Author: Circuit Project
License: MIT
"""

import sys
import argparse
import json
from pathlib import Path
from typing import Optional

# Import CLI modules
from .validator import validate_circuit_file
from .info import display_circuit_info
from .exporter import export_circuit


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="circuit",
        description="Circuit - CLI tool for electronic circuit files (.circuit.json)",
        epilog="For more information, visit: https://github.com/Blackmvmba88/circuit"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Validate command
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate a .circuit.json file against the schema"
    )
    validate_parser.add_argument(
        "file",
        type=str,
        help="Path to .circuit.json file"
    )
    validate_parser.add_argument(
        "--strict",
        action="store_true",
        help="Enable strict validation mode"
    )
    
    # Info command
    info_parser = subparsers.add_parser(
        "info",
        help="Display circuit information and statistics"
    )
    info_parser.add_argument(
        "file",
        type=str,
        help="Path to .circuit.json file"
    )
    info_parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Show detailed information"
    )
    
    # Export command
    export_parser = subparsers.add_parser(
        "export",
        help="Export circuit to different formats"
    )
    export_parser.add_argument(
        "file",
        type=str,
        help="Path to .circuit.json file"
    )
    export_parser.add_argument(
        "--format",
        type=str,
        required=True,
        choices=["altium", "kicad", "eagle", "spice", "netlist", "bom"],
        help="Export format"
    )
    export_parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output directory (default: current directory)"
    )
    
    # Render command (placeholder for future implementation)
    render_parser = subparsers.add_parser(
        "render",
        help="Render circuit visualization (requires dependencies)"
    )
    render_parser.add_argument(
        "file",
        type=str,
        help="Path to .circuit.json file"
    )
    render_parser.add_argument(
        "--3d",
        action="store_true",
        dest="three_d",
        help="Render in 3D mode (requires Blender)"
    )
    render_parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output file path"
    )
    
    # Parse arguments
    args = parser.parse_args()
    
    # Handle no command
    if not args.command:
        parser.print_help()
        return 0
    
    # Execute commands
    try:
        if args.command == "validate":
            return validate_command(args)
        elif args.command == "info":
            return info_command(args)
        elif args.command == "export":
            return export_command(args)
        elif args.command == "render":
            return render_command(args)
        else:
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        return 130
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        if "--debug" in sys.argv:
            import traceback
            traceback.print_exc()
        return 1


def validate_command(args) -> int:
    """Execute validate command."""
    file_path = Path(args.file)
    
    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}")
        return 1
    
    print(f"🔍 Validating: {file_path}")
    print()
    
    is_valid, errors, warnings = validate_circuit_file(str(file_path), strict=args.strict)
    
    if is_valid:
        print("✅ Validation passed!")
        if warnings:
            print(f"\n⚠️  {len(warnings)} warning(s):")
            for warning in warnings:
                print(f"   - {warning}")
        return 0
    else:
        print("❌ Validation failed!")
        print(f"\n{len(errors)} error(s) found:")
        for error in errors:
            print(f"   - {error}")
        if warnings:
            print(f"\n⚠️  {len(warnings)} warning(s):")
            for warning in warnings:
                print(f"   - {warning}")
        return 1


def info_command(args) -> int:
    """Execute info command."""
    file_path = Path(args.file)
    
    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}")
        return 1
    
    try:
        display_circuit_info(str(file_path), verbose=args.verbose)
        return 0
    except Exception as e:
        print(f"❌ Error displaying circuit info: {e}")
        return 1


def export_command(args) -> int:
    """Execute export command."""
    file_path = Path(args.file)
    
    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}")
        return 1
    
    output_dir = args.output if args.output else "."
    
    try:
        print(f"📤 Exporting {file_path.name} to {args.format} format...")
        export_circuit(str(file_path), args.format, output_dir)
        print(f"✅ Export complete! Files saved to: {output_dir}")
        return 0
    except NotImplementedError as e:
        print(f"⚠️  {e}")
        print(f"   The {args.format} exporter is not yet implemented.")
        print(f"   Available: altium")
        return 1
    except Exception as e:
        print(f"❌ Error exporting circuit: {e}")
        return 1


def render_command(args) -> int:
    """Execute render command."""
    file_path = Path(args.file)
    
    if not file_path.exists():
        print(f"❌ Error: File not found: {file_path}")
        return 1
    
    if args.three_d:
        print("🎨 3D rendering requires Blender to be installed.")
        print("   Please use the Blender scripts in blender_models/scripts/")
        print(f"   Example: blender --python blender_models/scripts/component_generator.py -- {file_path}")
        return 1
    else:
        print("🎨 2D rendering is not yet implemented.")
        print("   Future versions will support SVG/PNG export.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
