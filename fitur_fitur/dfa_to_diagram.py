def dfa_to_diagram(dfa):
    states = dfa['states']
    alphabet = dfa['alphabet']
    start_state = dfa['start_state']
    accept_states = dfa['accept_states']
    transition_function = dfa['transition_function']
    
    lines = []
    lines.append("stateDiagram-v2")
    lines.append(f"    [*] --> {start_state}")
    
    for accept_state in accept_states:
        lines.append(f"    state {accept_state} <<accept>>")
    
    for (state, symbol), next_state in transition_function.items():
        lines.append(f"    {state} --> {next_state} : {symbol}")
    
    return "\n".join(lines)

