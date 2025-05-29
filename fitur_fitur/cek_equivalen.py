def are_equivalent_dfas(dfa1, dfa2):

    def validate_dfa(dfa):
        """
        Memvalidasi sebuah DFA. Sebuah DFA valid jika mengandung kunci-kunci:
        'states', 'alphabet', 'start_state', 'accept_states', 'transition_function'
        dan semua nilai memiliki tipe dan format yang benar.
        """

        if not isinstance(dfa, dict):
            raise ValueError("DFA harus berupa kamus")
        required_keys = ['states', 'alphabet', 'start_state', 'accept_states', 'transition_function']
        for key in required_keys:
            if key not in dfa:
                raise ValueError(f"DFA tidak memiliki kunci yang diperlukan: {key}")

        if not isinstance(dfa['states'], set):
            raise ValueError("States DFA harus berupa set")
        if not isinstance(dfa['alphabet'], set):
            raise ValueError("Alphabet DFA harus berupa set")
        if not isinstance(dfa['start_state'], str):
            raise ValueError("Start_state DFA harus berupa string")
        if not isinstance(dfa['accept_states'], set):
            raise ValueError("Accept_states DFA harus berupa set")
        if not isinstance(dfa['transition_function'], dict):
            raise ValueError("Transition_function DFA harus berupa kamus")

        if dfa['start_state'] not in dfa['states']:
            raise ValueError("Start_state DFA tidak ada di states DFA")
        for state in dfa['accept_states']:
            if state not in dfa['states']:
                raise ValueError("Accept_states DFA mengandung state yang tidak ada di states DFA")
        for (state, symbol), next_state in dfa['transition_function'].items():
            if state not in dfa['states']:
                raise ValueError("Transition_function DFA mengandung state yang tidak ada di states DFA")
            if symbol not in dfa['alphabet']:
                raise ValueError("Transition_function DFA mengandung simbol yang tidak ada di alphabet DFA")
            if next_state not in dfa['states']:
                raise ValueError("Transition_function DFA mengandung next_state yang tidak ada di states DFA")
        return "ya"  # Mengembalikan 'ya' jika DFA valid

    # Validasi input DFA
    validate_dfa(dfa1)
    validate_dfa(dfa2)

    # 1. Cek apakah alphabetnya sama. Jika tidak sama, DFA tidak mungkin ekuivalen.
    if dfa1['alphabet'] != dfa2['alphabet']:
        return "tidak"

    alphabet = dfa1['alphabet'] # Gunakan salah satu alphabet karena mereka sama

    # 2. Inisialisasi antrean untuk state yang akan dibandingkan, dan set untuk melacak pasangan state yang sudah dikunjungi.
    queue = [(dfa1['start_state'], dfa2['start_state'])]
    visited = set()

    # 3. Lakukan pencarian breadth-first untuk membandingkan pasangan state yang dapat dijangkau.
    while queue:
        state1, state2 = queue.pop(0)

        # Jika pasangan ini sudah pernah dikunjungi, lewati.
        if (state1, state2) in visited:
            continue
        visited.add((state1, state2))

        # Cek apakah satu state adalah accepting dan yang lainnya bukan. Jika ya, DFA tidak ekuivalen.
        is_accepting1 = state1 in dfa1['accept_states']
        is_accepting2 = state2 in dfa2['accept_states']
        if is_accepting1 != is_accepting2:
            return "tidak"

        # Untuk setiap simbol di alphabet, temukan next state untuk kedua DFA.
        for symbol in alphabet:
            next_state1 = dfa1['transition_function'].get((state1, symbol))
            next_state2 = dfa2['transition_function'].get((state2, symbol))
            # Jika transisi hilang, anggap ia menuju ke dead state.
            if next_state1 is None:
                next_state1 = "dead_state_dfa1" # Buat dead state dummy jika tidak ada
                if "dead_state_dfa1" not in dfa1['states']:
                    dfa1['states'].add("dead_state_dfa1")
            if next_state2 is None:
                next_state2 = "dead_state_dfa2"
                if "dead_state_dfa2" not in dfa2['states']:
                    dfa2['states'].add("dead_state_dfa2")

            queue.append((next_state1, next_state2))

    # 4. Jika loop selesai tanpa menemukan perbedaan, DFA ekuivalen.
    return "ya"