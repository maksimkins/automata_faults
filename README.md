# Automata Faults

Algorithms and tools for **diagnostics and recovery of faults in finite automata under alphabetic coding**.  
This project was developed as part of my **Bachelor's diploma thesis** at **Moscow State University, Baku Branch**.

---

## Overview

The project implements a set of algorithms for analyzing deterministic finite automata (DFAs) with respect to:

- **Minimization check** (whether an automaton is reduced / minimized)  
- **Unambiguity check** under alphabetic coding  
- **Diagnosis of single-output faults**  
- **Testing an automaton for the presence of a single fault**

The algorithms are based on classical results in automata theory (Moore, Markov, Hopcroft–Ullman, etc.) and were tested on all automata with 2–3 states.

---

## Implemented Algorithms

1. **Check if an automaton is minimized**  
   - Uses reachability and Moore’s partition refinement method.  
   - Returns `True` if minimized, `False` otherwise.  

2. **Check automaton for unambiguity**  
   - Implements Markov’s algorithm to verify uniqueness of alphabetic coding.  
   - Returns `True` if unambiguous, `False` if ambiguous, `None` if not minimized.  

3. **Diagnosis of single faults**  
   - Iterates through all transitions, flips the output bit, and checks if the new automaton remains valid.  
   - Returns the number of successfully diagnosable faults.  

4. **Testing for the presence of a single fault**  
   - Determines whether a given automaton has a single output fault compared to its original reduced and unambiguous version.  
   - If possible, locates the exact transition where the fault occurred.  

---

## Installation

Clone the repository:

```bash
git clone https://github.com/maksimkins/automata_faults.git
cd automata_faults
```

## Usage Example
from automata_faults import is_minimized, is_ambigous, number_of_fault_diagnostics, is_fault_happened

# Define your automaton (Q, A, phi, psi, q_start, etc.)
Q = {"q0", "q1"}
A = {"0", "1"}
B = {"0", "1"}
q_start = "q0"

phi = {("q0","0"):"q1", ("q0","1"):"q0", ("q1","0"):"q0", ("q1","1"):"q1"}
psi = {("q0","0"):"0", ("q0","1"):"1", ("q1","0"):"1", ("q1","1"):"0"}

schema_encoding = {"0":"0", "1":"1"}

print(is_minimized(Q, A, phi, psi, q_start))                     # True/False
print(is_ambigous(schema_encoding, A, B, Q, phi, psi, q_start))  # True/False/None
print(number_of_fault_diagnostics(schema_encoding, A, B, Q, phi, psi, q_start))
print(is_fault_happened(schema_encoding, A, B, Q, phi, psi, q_start))

## Testing

The algorithms were tested on all DFAs with 2 and 3 states, and results matched theoretical expectations (see diploma text for details).

## References

- A. A. Markov – Introduction to Coding Theory

- V. B. Kudryavtsev, S. V. Aleshin – Introduction to Automata Theory

- J. Hopcroft, R. Motwani, J. Ullman – Introduction to Automata Theory, Languages, and Computation

- Diploma Thesis: On Diagnostics and Recovery of Faults in Automata under Alphabetic Coding (MSU Baku Branch, 2025)

## Author

Maksim Aleshkov
Moscow State University, Baku Branch – Faculty of Applied Mathematics
Supervisor: PhD P. S. Dergach
