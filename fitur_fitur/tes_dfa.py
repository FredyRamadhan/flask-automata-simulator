def run_dfa(dfa, input_string):
    current_state = dfa['start_state']
    log = []

    # iterasi setiap simbol dalam string input
    for symbol in input_string:
        # jika simbol tidak ada dalam alfabet DFA, maka input tidak valid
        if symbol not in dfa['alphabet']:
            log.append((symbol, current_state, "Simbol tidak valid"))
            return False, log

        from_state = current_state
        transition_key = (current_state, symbol)

        # cek apakah transisi ada untuk pasangan (state, simbol)
        if transition_key in dfa['transition_function']:
            current_state = dfa['transition_function'][transition_key]
            log.append((symbol, from_state, current_state))
        else:
            # proses berhenti apabila tidak ada transisi yang valid
            log.append((symbol, from_state, "Tidak ada transisi"))
            return False, log

    # setelah simbol diproses, cek apakah state akhir adalah state penerima
    return current_state in dfa['accept_states'], log
