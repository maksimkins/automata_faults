import argparse
from automata_faults.loaders import load_automata_from_json, load_schema_encoding_from_json
from automata_faults.core import (
    is_minimized,
    is_automata_ambiguous,
    number_of_fault_diagnostics,
    is_fault_happened,
)

def main():
    parser = argparse.ArgumentParser(description="Automata Faults Diagnostic Tool")

    parser.add_argument("command", choices=["is_minimized", "is_automata_ambiguous", "number_of_fault_diagnostics", "is_fault_happened"], help="Function to run")
    parser.add_argument("--automata", required=True, help="Path to automata JSON file")
    parser.add_argument("--encoding_schema", required=False, help="Path to schema encoding JSON file (only for ambiguous and fault checks)")

    args = parser.parse_args()

    # Load automata
    Q, A, B, phi, psi, q_start = load_automata_from_json(args.automata)

    # Depending on command, run appropriate logic
    if args.command == "is_minimized":
        print(is_minimized(Q, A, phi, psi, q_start))

    elif args.command == "is_automata_ambiguous":
        if not args.encoding_schema:
            raise ValueError("Encoding schema is required for ambiguity check.")
        schema_encoding = load_schema_encoding_from_json(args.encoding_schema, A)
        print(is_automata_ambiguous(schema_encoding, A, B, Q, phi, psi, q_start))

    elif args.command == "number_of_fault_diagnostics":
        if not args.encoding_schema:
            raise ValueError("Encoding schema is required for ambiguity check.")
        schema_encoding = load_schema_encoding_from_json(args.encoding_schema, A)
        print(number_of_fault_diagnostics(schema_encoding, A, B, Q, phi, psi, q_start))

    elif args.command == "is_fault_happened":
        if not args.encoding_schema:
            raise ValueError("Encoding schema is required for fault detection.")
        schema_encoding = load_schema_encoding_from_json(args.encoding_schema, A)
        print(is_fault_happened(schema_encoding, A, B, Q, phi, psi, q_start))
