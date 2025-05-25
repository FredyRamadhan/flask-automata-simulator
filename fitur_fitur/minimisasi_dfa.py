# minimisasi_dfa.py

from collections import defaultdict
import ast
from pprint import pprint

def minimize_dfa(dfa):
    states = dfa['states']
    alphabet = dfa['alphabet']
    start_state = dfa['start_state']
    accept_states = dfa['accept_states']
    tf = dfa['transition_function']

    non_accepting = states - accept_states
    partition = [accept_states, non_accepting]

    def get_group(state, groups):
        for i, group in enumerate(groups):
            if state in group:
                return i
        return -1

    while True:
        new_partition = []
        for group in partition:
            group_map = defaultdict(set)
            for state in group:
                signature = tuple(get_group(tf.get((state, a), ''), partition) for a in alphabet)
                group_map[signature].add(state)
            new_partition.extend(group_map.values())
        if new_partition == partition:
            break
        partition = new_partition

    state_mapping = {}
    new_states = set()
    new_accept_states = set()
    new_tf = {}

    for i, group in enumerate(partition):
        name = f'q{i}'
        new_states.add(name)
        for state in group:
            state_mapping[state] = name
        if group & accept_states:
            new_accept_states.add(name)

    new_start_state = state_mapping[start_state]

    for (old_state, symbol), dest_state in tf.items():
        new_src = state_mapping[old_state]
        new_dest = state_mapping[dest_state]
        new_tf[(new_src, symbol)] = new_dest

    minimized_dfa = {
        'states': new_states,
        'alphabet': alphabet,
        'start_state': new_start_state,
        'accept_states': new_accept_states,
        'transition_function': new_tf
    }

    return minimized_dfa


if __name__ == '__main__':
    print("=== INPUT DFA UNTUK DIMINIMALKAN ===")
    print("Masukkan semua dalam format Python seperti contoh di bawah ini.")
    print("Contoh states        : q0,q1,q2")
    print("Contoh alphabet      : 0,1")
    print("Contoh start state   : q0")
    print("Contoh accept states : q1")
    print("Contoh transition_function:\n  {('q0', '0'): 'q2', ('q0', '1'): 'q1', ('q1', '0'): 'q2', ('q1', '1'): 'q1', ('q2', '0'): 'q2', ('q2', '1'): 'q1'}")

    states = set(input("\nStates: ").replace(" ", "").split(","))
    alphabet = set(input("Alphabet: ").replace(" ", "").split(","))
    start_state = input("Start state: ").strip()
    accept_states = set(input("Accept states: ").replace(" ", "").split(","))
    tf_raw = input("Transition function: ").strip()

    try:
        transition_function = ast.literal_eval(tf_raw)
        if not isinstance(transition_function, dict):
            raise ValueError
    except Exception:
        print("❌ Format transition_function salah. Pastikan menggunakan format dictionary Python.")
        exit(1)

    dfa_input = {
        'states': states,
        'alphabet': alphabet,
        'start_state': start_state,
        'accept_states': accept_states,
        'transition_function': transition_function
    }

    print("\n=== DFA HASIL MINIMISASI ===")
    pprint(minimize_dfa(dfa_input))
