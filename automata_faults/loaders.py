import json

def load_automata_from_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    Q = data.get('Q')
    A = data.get('A')
    B = data.get('B')
    phi_raw = data.get('phi')
    psi_raw = data.get('psi')
    q_start = data.get('q_start')

  
    if not isinstance(Q, list) or not all(isinstance(q, str) for q in Q):
        raise ValueError("Q must be a list of strings.")
    if not isinstance(A, list) or not all(isinstance(a, str) for a in A):
        raise ValueError("A must be a list of strings.")
    if B != ['0', '1']:
        raise ValueError("B must be exactly ['0', '1'].")
    if q_start not in Q:
        raise ValueError("q_start must be one of the states in Q.")

    phi = {}
    psi = {}
    expected_keys = {(q, a) for q in Q for a in A}

    for key_str, val in phi_raw.items():
        key = tuple(k.strip() for k in key_str.strip("()").split(","))
        if len(key) != 2 or key[0] not in Q or key[1] not in A:
            raise ValueError(f"Invalid key in phi: {key}")
        if val not in Q:
            raise ValueError(f"Invalid state target in phi({key}): {val}")
        phi[(key[0], key[1])] = val

    for key_str, val in psi_raw.items():
        key = tuple(k.strip() for k in key_str.strip("()").split(","))
        if len(key) != 2 or key[0] not in Q or key[1] not in A:
            raise ValueError(f"Invalid key in psi: {key}")
        if val not in B:
            raise ValueError(f"Invalid output symbol in psi({key}): {val}")
        psi[(key[0], key[1])] = val

    for q in Q:
        for a in A:
            if (q, a) not in phi:
                raise ValueError(f"Missing transition in phi for state {q} and symbol {a}")
            if (q, a) not in psi:
                raise ValueError(f"Missing transition in psi for state {q} and symbol {a}")

    return Q, A, B, phi, psi, q_start

def load_schema_encoding_from_json(filename, A):
    with open(filename, 'r') as f:
        schema_encoding = json.load(f)

    if not isinstance(schema_encoding, dict):
        raise ValueError("Encoding must be a dictionary.")

    keys = set(schema_encoding.keys())
    expected = set(A)

    if keys != expected:
        missing = expected - keys
        extra = keys - expected
        msg = []
        if missing:
            msg.append(f"Missing keys: {missing}")
        if extra:
            msg.append(f"Unexpected keys: {extra}")
        raise ValueError("Invalid encoding keys. " + "; ".join(msg))

    for k, v in schema_encoding.items():
        if not isinstance(v, str):
            raise ValueError(f"Encoding for {k} must be a string.")

    return schema_encoding