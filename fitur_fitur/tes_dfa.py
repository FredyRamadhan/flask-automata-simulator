def run_dfa(dfa, input_string):
    current_state = dfa['start_state']
    log = []

    for symbol in input_string:
        if symbol not in dfa['alphabet']:
            log.append((symbol, current_state, "Simbol tidak valid"))
            return False, log

        from_state = current_state
        transition_key = (current_state, symbol)

        if transition_key in dfa['transition_function']:
            current_state = dfa['transition_function'][transition_key]
            log.append((symbol, from_state, current_state))
        else:
            log.append((symbol, from_state, "Tidak ada transisi"))
            return False, log

    return current_state in dfa['accept_states'], log
