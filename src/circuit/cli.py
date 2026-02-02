#!/usr/bin/env python3
"""
Circuit CLI - Command Line Interface for Circuit Format

This module provides the main CLI interface for working with .circuit.json files.

Commands:
  - validate: Validate circuit files against schema
  - diff: Compare two circuit files
  - export: Export to other formats
  - render: Render circuit diagrams
"""

import sys
import json
import os
import tempfile
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich import print as rprint

from .validator import CircuitValidator
from .diff import CircuitDiff
from .persistence import CircuitPersistence, PersistenceError

console = Console()


@click.group()
@click.version_option(version="0.2.0", prog_name="circuit")
def main():
    """
    Circuit CLI - Universal Electronic Circuit Format
    
    A command-line tool for validating, comparing, and exporting electronic circuit designs.
    """
    pass


@main.command()
@click.argument('circuit_file', type=click.Path(exists=True))
@click.option('--verbose', '-v', is_flag=True, help='Show detailed validation results')
@click.option('--schema', '-s', type=click.Path(exists=True), help='Custom schema file')
@click.option('--json', 'output_json', is_flag=True, help='Output results as JSON')
def validate(circuit_file, verbose, schema, output_json):
    """
    Validate a circuit file against the JSON schema.
    
    Checks:
    - JSON schema compliance
    - Component definitions
    - Net connectivity
    - Invalid values
    - Undeclared pads/pins
    
    Example:
        circuit validate power_supply.circuit.json
    """
    try:
        # Load circuit file using safe persistence
        persistence = CircuitPersistence()
        circuit_data = persistence.load_circuit(circuit_file)
        
        # Create validator
        validator = CircuitValidator(circuit_data, schema_path=schema)
        
        # Run validation
        is_valid, results = validator.validate()
        
        if output_json:
            # Output as JSON
            output = {
                'valid': is_valid,
                'file': str(circuit_file),
                'errors': results.get('errors', []),
                'warnings': results.get('warnings', []),
                'info': results.get('info', [])
            }
            print(json.dumps(output, indent=2))
        else:
            # Display results with Rich formatting
            _display_validation_results(circuit_file, is_valid, results, verbose)
        
        # Exit with appropriate code
        sys.exit(0 if is_valid else 1)
        
    except PersistenceError as e:
        console.print(f"[red]❌ Error loading file: {str(e)}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {str(e)}[/red]")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)


@main.command()
@click.argument('old_file', type=click.Path(exists=True))
@click.argument('new_file', type=click.Path(exists=True))
@click.option('--verbose', '-v', is_flag=True, help='Show detailed diff')
@click.option('--json', 'output_json', is_flag=True, help='Output results as JSON')
@click.option('--summary', '-s', is_flag=True, help='Show only summary')
def diff(old_file, new_file, verbose, output_json, summary):
    """
    Compare two circuit files and show differences.
    
    Shows:
    - Components added/removed
    - Components modified (values changed)
    - Nets changed
    - Connections modified
    
    Example:
        circuit diff v1.circuit.json v2.circuit.json
    """
    try:
        # Load circuit files using safe persistence
        persistence = CircuitPersistence()
        old_circuit = persistence.load_circuit(old_file)
        new_circuit = persistence.load_circuit(new_file)
        
        # Create diff
        differ = CircuitDiff(old_circuit, new_circuit)
        diff_results = differ.compute_diff()
        
        if output_json:
            # Output as JSON
            print(json.dumps(diff_results, indent=2))
        else:
            # Display results with Rich formatting
            _display_diff_results(old_file, new_file, diff_results, verbose, summary)
        
        # Exit code 0 if no changes, 1 if changes found
        has_changes = any([
            diff_results.get('components_added'),
            diff_results.get('components_removed'),
            diff_results.get('components_modified'),
            diff_results.get('nets_changed')
        ])
        sys.exit(1 if has_changes else 0)
        
    except FileNotFoundError as e:
        console.print(f"[red]❌ Error: File not found - {str(e)}[/red]")
        sys.exit(1)
    except json.JSONDecodeError as e:
        console.print(f"[red]❌ Error: Invalid JSON - {str(e)}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]❌ Unexpected error: {str(e)}[/red]")
        if verbose:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)


@main.command()
@click.argument('circuit_file', type=click.Path(exists=True))
@click.option('--format', '-f', type=click.Choice(['altium', 'kicad', 'spice', 'bom']), 
              default='altium', help='Export format')
@click.option('--output', '-o', type=click.Path(), help='Output directory or file')
def export(circuit_file, format, output):
    """
    Export circuit to other formats.
    
    Supported formats:
    - altium: Altium Designer (netlist, BOM, placement)
    - kicad: KiCad schematic (planned)
    - spice: SPICE netlist (planned)
    - bom: Bill of Materials CSV
    
    Example:
        circuit export myfile.circuit.json --format altium --output altium_export/
    """
    try:
        # Load circuit file using safe persistence
        persistence = CircuitPersistence()
        circuit_data = persistence.load_circuit(circuit_file)
        
        # Determine output path
        if not output:
            output = f"{Path(circuit_file).stem}_{format}_export"
        
        if format == 'altium':
            # Import and use Altium exporter
            from pathlib import Path
            import sys
            sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / 'adapters'))
            from circuit_to_altium import AltiumExporter
            
            exporter = AltiumExporter(circuit_data, output)
            exporter.export_all()
            console.print(f"\n[green]✅ Successfully exported to {format} format![/green]")
            console.print(f"[green]   Output directory: {output}[/green]")
        
        elif format == 'bom':
            # Simple BOM export
            _export_bom(circuit_data, output)
            console.print(f"\n[green]✅ BOM exported to: {output}[/green]")
        
        else:
            console.print(f"[yellow]⚠️  Format '{format}' is planned but not yet implemented[/yellow]")
            console.print(f"[yellow]   Currently supported: altium, bom[/yellow]")
            sys.exit(1)
        
    except Exception as e:
        console.print(f"[red]❌ Export failed: {str(e)}[/red]")
        import traceback
        console.print(traceback.format_exc())
        sys.exit(1)


@main.command()
@click.argument('circuit_file', type=click.Path(exists=True))
@click.option('--3d', 'render_3d', is_flag=True, help='Render in 3D (requires Blender)')
@click.option('--output', '-o', type=click.Path(), help='Output file (PNG, SVG, etc.)')
def render(circuit_file, render_3d, output):
    """
    Render circuit diagram or 3D model.
    
    Example:
        circuit render myfile.circuit.json --3d --output render.png
    """
    console.print("[yellow]⚠️  The render command is planned but not yet implemented[/yellow]")
    console.print("[yellow]   Coming soon: 2D schematic rendering and 3D visualization[/yellow]")
    sys.exit(1)


def _display_validation_results(filename, is_valid, results, verbose):
    """Display validation results using Rich formatting."""
    
    # Header
    console.print()
    console.print(Panel(
        f"[bold]Circuit Validation Report[/bold]\n"
        f"File: {filename}",
        style="blue"
    ))
    console.print()
    
    errors = results.get('errors', [])
    warnings = results.get('warnings', [])
    info = results.get('info', [])
    
    # Show info messages if verbose
    if verbose and info:
        console.print("[cyan]ℹ️  Information:[/cyan]")
        for msg in info:
            console.print(f"  [cyan]•[/cyan] {msg}")
        console.print()
    
    # Show warnings
    if warnings:
        console.print(f"[yellow]⚠️  Warnings ({len(warnings)}):[/yellow]")
        for msg in warnings:
            console.print(f"  [yellow]•[/yellow] {msg}")
        console.print()
    
    # Show errors
    if errors:
        console.print(f"[red]❌ Errors ({len(errors)}):[/red]")
        for msg in errors:
            console.print(f"  [red]•[/red] {msg}")
        console.print()
    
    # Summary
    if is_valid:
        if warnings:
            console.print(Panel(
                f"✅ [green]Validation PASSED[/green] with [yellow]{len(warnings)} warning(s)[/yellow]\n"
                "Review warnings before fabrication.",
                style="green"
            ))
        else:
            console.print(Panel(
                "✅ [green]Validation PASSED[/green]\n"
                "Circuit looks good!",
                style="green"
            ))
    else:
        console.print(Panel(
            f"❌ [red]Validation FAILED[/red] with [red]{len(errors)} error(s)[/red]\n"
            "Fix errors before fabrication.",
            style="red"
        ))
    
    console.print()


def _display_diff_results(old_file, new_file, results, verbose, summary):
    """Display diff results using Rich formatting."""
    
    # Header
    console.print()
    console.print(Panel(
        f"[bold]Circuit Diff Report[/bold]\n"
        f"Old: {old_file}\n"
        f"New: {new_file}",
        style="blue"
    ))
    console.print()
    
    # Components added
    added = results.get('components_added', [])
    if added:
        console.print(f"[green]➕ Components Added ({len(added)}):[/green]")
        if not summary:
            for comp in added:
                comp_id = comp.get('id', 'unknown')
                comp_type = comp.get('type', 'unknown')
                value = comp.get('value', comp.get('params', {}).get('resistance_ohm', ''))
                console.print(f"  [green]+[/green] {comp_id} ({comp_type}){f' = {value}' if value else ''}")
        else:
            console.print(f"  {len(added)} component(s)")
        console.print()
    
    # Components removed
    removed = results.get('components_removed', [])
    if removed:
        console.print(f"[red]➖ Components Removed ({len(removed)}):[/red]")
        if not summary:
            for comp in removed:
                comp_id = comp.get('id', 'unknown')
                comp_type = comp.get('type', 'unknown')
                value = comp.get('value', comp.get('params', {}).get('resistance_ohm', ''))
                console.print(f"  [red]-[/red] {comp_id} ({comp_type}){f' = {value}' if value else ''}")
        else:
            console.print(f"  {len(removed)} component(s)")
        console.print()
    
    # Components modified
    modified = results.get('components_modified', [])
    if modified:
        console.print(f"[yellow]📝 Components Modified ({len(modified)}):[/yellow]")
        if not summary and verbose:
            for mod in modified:
                comp_id = mod.get('id', 'unknown')
                changes = mod.get('changes', {})
                console.print(f"  [yellow]~[/yellow] {comp_id}:")
                for key, (old_val, new_val) in changes.items():
                    console.print(f"      {key}: [red]{old_val}[/red] → [green]{new_val}[/green]")
        else:
            console.print(f"  {len(modified)} component(s)")
        console.print()
    
    # Nets changed
    nets_changed = results.get('nets_changed', [])
    if nets_changed:
        console.print(f"[blue]🔌 Nets Changed ({len(nets_changed)}):[/blue]")
        if not summary:
            for net_id in nets_changed:
                console.print(f"  [blue]•[/blue] {net_id}")
        else:
            console.print(f"  {len(nets_changed)} net(s)")
        console.print()
    
    # Summary
    total_changes = len(added) + len(removed) + len(modified) + len(nets_changed)
    if total_changes == 0:
        console.print(Panel(
            "✅ [green]No differences found[/green]\n"
            "Circuits are identical.",
            style="green"
        ))
    else:
        console.print(Panel(
            f"📊 [blue]Total Changes: {total_changes}[/blue]\n"
            f"Added: {len(added)} | Removed: {len(removed)} | Modified: {len(modified)} | Nets: {len(nets_changed)}",
            style="blue"
        ))
    
    console.print()


def _export_bom(circuit_data, output):
    """Export Bill of Materials to CSV using safe persistence."""
    import csv
    import tempfile
    
    components = circuit_data.get('components', [])
    
    # Ensure output has .csv extension
    if not output.endswith('.csv'):
        output = f"{output}.csv"
    
    output_path = Path(output).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Use temporary file for atomic write
    temp_fd, temp_path = tempfile.mkstemp(
        dir=output_path.parent,
        prefix=f".{output_path.name}.",
        suffix=".tmp"
    )
    
    try:
        with os.fdopen(temp_fd, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header
            writer.writerow(['Designator', 'Type', 'Value', 'Package', 'Description', 'Quantity'])
            
            # Group components
            bom_groups = {}
            for comp in components:
                comp_type = comp.get('type', '')
                value = comp.get('value', str(comp.get('params', {}).get('resistance_ohm', '')))
                package = comp.get('package', '')
                
                key = (comp_type, value, package)
                if key not in bom_groups:
                    bom_groups[key] = {
                        'designators': [],
                        'description': comp.get('description', ''),
                    }
                bom_groups[key]['designators'].append(comp.get('id', ''))
            
            # Write rows
            for (comp_type, value, package), data in sorted(bom_groups.items()):
                designators = ', '.join(data['designators'])
                quantity = len(data['designators'])
                description = data['description']
                
                writer.writerow([designators, comp_type, value, package, description, quantity])
            
            # Ensure data is written to disk
            f.flush()
            os.fsync(f.fileno())
        
        # Atomic rename
        temp_file = Path(temp_path)
        if os.name == 'nt' and output_path.exists():
            temp_file.replace(output_path)
        else:
            temp_file.rename(output_path)
            
    except Exception as e:
        # Clean up temp file on error
        try:
            Path(temp_path).unlink(missing_ok=True)
        except:
            pass
        raise PersistenceError(f"Failed to export BOM: {e}")


if __name__ == '__main__':
    main()
