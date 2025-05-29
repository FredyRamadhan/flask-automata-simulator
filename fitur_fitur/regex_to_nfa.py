from collections import defaultdict

class NFA:
    def __init__(self):
        self.transitions = defaultdict(lambda: defaultdict(set))
        self.start_state = None
        self.accept_states = set()
        self.states = set()

    def add_transition(self, src, symbol, dest):
        self.transitions[src][symbol].add(dest)
        self.states.update({src, dest})

    def simulate(self, string):
        def epsilon_closure(states):
            stack = list(states)
            closure = set(states)
            while stack:
                state = stack.pop()
                for next_state in self.transitions[state].get("", []):
                    if next_state not in closure:
                        closure.add(next_state)
                        stack.append(next_state)
            return closure

        current_states = epsilon_closure({self.start_state})
        for symbol in string:
            next_states = set()
            for state in current_states:
                next_states.update(self.transitions[state].get(symbol, []))
            current_states = epsilon_closure(next_states)
        return bool(self.accept_states & current_states)

    def to_dict(self):
        return {
            "states": list(self.states),
            "alphabet": sorted({symb for trans in self.transitions.values() for symb in trans if symb != ""}),
            "start_state": self.start_state,
            "accept_states": list(self.accept_states),
            "transitions": {
                state: {symbol: list(dests) for symbol, dests in self.transitions[state].items()}
                for state in self.transitions
            }
        }

def regex_to_nfa(regex):
    state_id = [0]

    def new_state():
        sid = "q" + str(state_id[0])
        state_id[0] += 1
        return sid

    def parse_regex(expr, pos=0):
        nfa = NFA()
        start = new_state()
        nfa.start_state = start
        current_states = {start}

        while pos < len(expr):
            char = expr[pos]
            if char in {"a", "b"}:
                dest = new_state()
                for s in current_states:
                    nfa.add_transition(s, char, dest)
                current_states = {dest}
                pos += 1
            elif char == "(":
                depth = 1
                sub_pos = pos + 1
                while sub_pos < len(expr) and depth > 0:
                    if expr[sub_pos] == "(": depth += 1
                    elif expr[sub_pos] == ")": depth -= 1
                    sub_pos += 1
                if depth != 0:
                    raise ValueError("Unmatched parenthesis")
                sub_nfa = parse_regex(expr[pos + 1:sub_pos - 1])[0]
                for s in current_states:
                    nfa.add_transition(s, "", sub_nfa.start_state)
                for src in sub_nfa.transitions:
                    for symb in sub_nfa.transitions[src]:
                        for dst in sub_nfa.transitions[src][symb]:
                            nfa.add_transition(src, symb, dst)
                current_states = sub_nfa.accept_states
                pos = sub_pos
            elif char == "*":
                if not current_states:
                    raise ValueError("Invalid Kleene star: no preceding expression")
                prev_start = nfa.start_state
                prev_end = new_state()
                nfa.accept_states = {prev_end}
                for s in current_states:
                    nfa.add_transition(s, "", prev_start)
                    nfa.add_transition(s, "", prev_end)
                nfa.add_transition(prev_start, "", prev_end)
                current_states = {prev_end}
                pos += 1
            elif char == "|":
                end = new_state()
                right_nfa, new_pos = parse_regex(expr, pos + 1)
                for src in right_nfa.transitions:
                    for symb in right_nfa.transitions[src]:
                        for dst in right_nfa.transitions[src][symb]:
                            nfa.add_transition(src, symb, dst)
                nfa.add_transition(nfa.start_state, "", right_nfa.start_state)
                for s in right_nfa.accept_states:
                    nfa.add_transition(s, "", end)
                for s in current_states:
                    nfa.add_transition(s, "", end)
                nfa.accept_states = {end}
                return nfa, new_pos
            else:
                raise ValueError(f"Invalid character at position {pos}: {char}")
        nfa.accept_states = current_states
        return nfa, pos

    nfa, _ = parse_regex(regex)
    return nfa

def test_regex_with_string(regex, input_string):
    try:
        nfa = regex_to_nfa(regex)
        accepted = nfa.simulate(input_string)
        return {
            "regex": regex,
            "input_string": input_string,
            "accepted": accepted,
            "nfa": nfa.to_dict()
        }
    except ValueError as e:
        return {
            "regex": regex,
            "input_string": input_string,
            "error": str(e)
        }