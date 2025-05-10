#!/usr/bin/env python3
"""
HRIM Wellness Plan Generator

This script provides a command-line interface to generate wellness plans.
"""

import os
import sys
import argparse

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="HRIM Wellness Plan Generator")
    parser.add_argument("--random", action="store_true", help="Generate a plan with random data")
    parser.add_argument("--input", type=str, help="Path to JSON input file with form data")
    parser.add_argument("--output", type=str, help="Output directory for wellness plan")
    parser.add_argument("--pdf", action="store_true", help="Generate PDF output (requires WeasyPrint)")
    parser.add_argument("--preview", action="store_true", help="Show a preview of the wellness plan")
    parser.add_argument("--web", action="store_true", help="Start the web interface")
    parser.add_argument("--port", type=int, default=5000, help="Port for the web interface")
    
    args = parser.parse_args()
    
    # Start the web interface if requested
    if args.web:
        print(f"Starting web interface on port {args.port}...")
        print("Access the wellness form at: http://localhost:{args.port}/wellness_form")
        from app.app import app
        app.run(debug=True, port=args.port)
        return
    
    # Run the command-line generator
    print("Running wellness plan generator...")
    import tests.wellness_plan_generator as generator_cli
    
    # Pass arguments to the CLI generator
    sys.argv = [sys.argv[0]]
    if args.random:
        sys.argv.append("--random")
    if args.input:
        sys.argv.extend(["--input", args.input])
    if args.output:
        sys.argv.extend(["--output", args.output])
    if args.pdf:
        sys.argv.append("--pdf")
    if args.preview:
        sys.argv.append("--preview")
    
    # Run the generator
    generator_cli.main()

if __name__ == "__main__":
    print("=== HRIM Wellness Plan Generator ===")
    main() 