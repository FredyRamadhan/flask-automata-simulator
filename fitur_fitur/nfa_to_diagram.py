def nfa_to_mermaid(nfa_dict):
    lines = ["stateDiagram-v2"]
    
    start = nfa_dict["start_state"]
    accepts = set(nfa_dict["accept_states"])
    transitions = nfa_dict["transitions"]

    # Start transition
    lines.append(f"[*] --> {start}")

    # Transitions
    for src, trans in transitions.items():
        for symbol, dests in trans.items():
            label = "ε" if symbol == "" else symbol
            for dst in dests:
                lines.append(f"{src} --> {dst} : {label}")

    # Accept states (optional styling or end links)
    for accept in accepts:
        lines.append(f"{accept} --> [*]")

    return "\n".join(lines)
