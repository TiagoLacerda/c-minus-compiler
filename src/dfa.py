from copy import deepcopy
import json


class DFA:
    """
    Deterministic Finite Automaton.
    """

    def __init__(self, states: list[str], alphabet: list[str], transitions: dict[str, dict[str, str]], initial_state: str, accept_states: list[str], tags=dict[str: list[str]]):
        """
        Create a Deterministic Finite Automaton.

        Keyword arguments:
        states: a finite set of states.
        alphabet: a finite set of input symbols.
        transitions: transition function.
        initial_state: initial state.
        accept_states: a set of accept states.
        tags: a collection of optional <str> tags for each state.
        """
        # https://stackoverflow.com/questions/5278122/checking-if-all-elements-in-a-list-are-unique

        # Every element of [states] is unique.
        if len(states) != len(set(states)):
            raise ValueError("Every element of [states] must be unique!")

        # Every element of [alphabet] is unique.
        if len(alphabet) != len(set(alphabet)):
            raise ValueError("Every element of [alphabet] must be unique!")

        # Every element of [accept_states] is unique.
        if len(accept_states) != len(set(accept_states)):
            raise ValueError(
                "Every element of [accept_states] must be unique!")

        # Every key in [tags] is an element of states.
        for state in tags.keys():
            if state not in states:
                raise ValueError(
                    f"\"{state}\" is not an element of [states]!")

        # [initial_state] is an element of [states].
        if initial_state not in states:
            raise ValueError("[initial_state] is not an element of [states]!")

        # Evert state in [accept_states] is an element of [states].
        for accept_state in accept_states:
            if accept_state not in states:
                raise ValueError(
                    f"\"{accept_state}\" is not an element of [states]!")

        for state in transitions.keys():
            # Every origin state in [transitions] is an element of [states].
            if state not in states:
                raise ValueError(f"\"{state}\" is not a member of [states]!")

            for letter in transitions[state].keys():
                # Every letter in [transitions] is an element of [alphabet].
                if letter not in alphabet:
                    raise ValueError(
                        f"\"{letter}\" is not a member of [alphabet]!")

                # Every destination state in [transitions] is an element of [states].
                if transitions[state][letter] not in states:
                    raise ValueError(
                        f"\"{state}\" is not a member of [states]!")

            for letter in alphabet:
                # Every origin state in [transitions] has a transition with each letter in [alphabet].
                if letter not in transitions[state].keys():
                    raise ValueError(
                        f"No transition found from state \"{state}\" with letter \"{letter}\"!")

        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accept_states = accept_states
        self.tags = tags

    def to_dict(self):
        """
        Returns an equivalent to this class instance as a <dict>.
        """
        return {
            "states": self.states,
            "alphabet": self.alphabet,
            "transitions": self.transitions,
            "initial_state": self.initial_state,
            "accept_states": self.accept_states,
            "tags": self.tags
        }

    def from_dict(data: dict):
        """
        Returns a class instance from an equivalent <dict>.
        """
        return DFA(
            states=data["states"],
            alphabet=data["alphabet"],
            transitions=data["transitions"],
            initial_state=data["initial_state"],
            accept_states=data["accept_states"],
            tags=data["tags"]
        )

    def to_json(self):
        """
        Returns an equivalent to this class instance as a json <str>.
        """
        return json.dumps(self.to_dict())

    def from_json(data: str):
        """
        Returns a class instance from an equivalent json <str>.
        """
        return DFA.from_dict(json.loads(data))

    def accepts(self, string: str):
        """
        Returns whether this automaton accepts the [string].
        """
        state = self.initial_state
        for letter in string:
            if letter not in self.alphabet:
                raise ValueError(
                    f"\"{letter}\" is not a member of [alphabet]!")
            state = self.transitions[state][letter]
        return state in self.accept_states

    def accepts_as(self, string: str):
        """
        Returns whether this automaton accepts the [string] and the tags corresponding to the state it ends at.
        """
        state = self.initial_state
        for letter in string:
            if letter not in self.alphabet:
                raise ValueError(
                    f"\"{letter}\" is not a member of [alphabet]!")
            state = self.transitions[state][letter]

        accept_tags = []
        if (state in self.tags.keys()):
            accept_tags = self.tags[state]

        return (state in self.accept_states, accept_tags)

    def expand_alphabet(self, letters: list[str]):
        """
        Returns a copy of this DFA with an expanded alphabet, with every state transitioning with new letters into a trash state.
        """
        letters = [letter for letter in letters if letter not in self.alphabet]

        dfa = deepcopy(self)

        if len(letters) == 0:
            return dfa

        # Create new trash state
        trash = 0
        while (f"{trash}" in dfa.states):
            trash += 1
        dfa.states.append(f"{trash}")

        # Expand alphabet
        for letter in letters:
            dfa.alphabet.append(letter)

        # Create new transitions
        for state in dfa.transitions.keys():
            for letter in letters:
                dfa.transitions[state][letter] = f"{trash}"

        # Create trash state transitions
        dfa.transitions[f"{trash}"] = {}
        for letter in dfa.alphabet:
            dfa.transitions[f"{trash}"][letter] = f"{trash}"

        return dfa

    def union(self, other: "DFA"):
        """
        Returns a DFA that accepts strings from both automata. Supports DFA's with different alphabets.

        This can be done because a DFA with alphabet S is equivalent to another with alphabet S', |S'| > |S|, with every transition through s in S' but not in S going into some non-accept state.

        TODO: Will possibly introduce ambiguity once two-character special symbols are introduced, for example, two automata with alphabets {<} and {<, =}
        """
        # Expanding both DFA's alphabets
        a = self.expand_alphabet(other.alphabet)
        b = other.expand_alphabet(self.alphabet)

        # From this point on, [a] and [b] share the same alphabet

        # Create states
        states = [f"{i}" for i in range(len(a.states) * len(b.states))]

        # Create a map from a pair of states, one from each original automaton, to a state in the new automaton
        map = {}
        state = 0
        for a_state in a.states:
            map[a_state] = {}
            for b_state in b.states:
                map[a_state][b_state] = f"{state}"
                state += 1

        # Create alphabet as a union of both original alphabets
        alphabet = []
        for letter in a.alphabet:
            if letter not in alphabet:
                alphabet.append(letter)

        for letter in b.alphabet:
            if letter not in alphabet:
                alphabet.append(letter)

        # Create transitions
        transitions = {}
        state = 0
        for a_state in a.states:
            for b_state in b.states:
                transitions[f"{state}"] = {}
                for letter in alphabet:
                    a_next = a.transitions[a_state][letter]
                    b_next = b.transitions[b_state][letter]

                    transitions[f"{state}"][letter] = map[a_next][b_next]
                state += 1

        initial_state = ""
        for a_state in a.states:
            for b_state in b.states:
                if a_state == a.initial_state and b_state == b.initial_state:
                    initial_state = map[a_state][b_state]
                    break

        accept_states = []
        for a_state in a.states:
            for b_state in b.states:
                if a_state in a.accept_states or b_state in b.accept_states:
                    accept_states.append(map[a_state][b_state])

        tags = {}
        for a_state in a.states:
            for b_state in b.states:
                state = map[a_state][b_state]
                a_tags = []
                if (a_state in a.tags.keys()):
                    a_tags = a.tags[a_state]

                b_tags = []
                if (b_state in b.tags.keys()):
                    b_tags = b.tags[b_state]

                if (len(a_tags) + len(b_tags) > 0):
                    tags[state] = a_tags + b_tags

        return DFA(
            states=states,
            alphabet=alphabet,
            transitions=transitions,
            initial_state=initial_state,
            accept_states=accept_states,
            tags=tags
        )

    def remove_unreachable_states(self):
        # https://en.wikipedia.org/wiki/DFA_minimization#:~:text=Unreachable%20states%20are%20the%20states,is%20required%20to%20be%20complete.

        dfa = deepcopy(self)

        # Determine which states are unreachable
        reachable_states = [dfa.initial_state]
        new_states = [dfa.initial_state]

        while (True):
            temp = []
            for state in new_states:
                for letter in dfa.alphabet:
                    target = dfa.transitions[state][letter]
                    if target not in temp:
                        temp.append(target)
            new_states = [
                state for state in temp if state not in reachable_states]
            reachable_states = reachable_states + new_states
            if (len(new_states) == 0):
                break

        unreachable_states = [
            state for state in dfa.states if state not in reachable_states]

        # Remove unreachable states from automaton
        for unreachable_state in unreachable_states:
            if unreachable_state in dfa.states:
                dfa.states.remove(unreachable_state)

            if unreachable_state in dfa.transitions.keys():
                del dfa.transitions[unreachable_state]

            if unreachable_state in dfa.accept_states:
                dfa.accept_states.remove(unreachable_state)

            if unreachable_state in dfa.tags.keys():
                del dfa.tags[unreachable_state]

        return dfa

    def minimized(self):
        """
        Returns an equivalent DFA that has the same amount of states or less.

        TODO: Currently merges parts that accepts different types of tokens, introducing ambiguity to the resulting automaton.
        """
        dfa = deepcopy(self)

        def target(state: str, letter: str, partition: list[list[str]]):
            """
            Index of subset of [partition] containing transition destination of [state] through [letter].
            """
            state = dfa.transitions[state][letter]
            for index in range(len(partition)):
                if state in partition[index]:
                    return index
            raise ValueError("Could not find target state in partition!")

        def split(partition: list[list[str]]):
            """
            Split subsets of partition. See algorithm for details (TBD).
            """
            for subset_index in range(len(partition)):
                for letter_index in range(len(dfa.alphabet)):
                    letter = dfa.alphabet[letter_index]
                    old_target = None
                    for state_index in range(len(partition[subset_index])):
                        new_target = target(
                            partition[subset_index][state_index], letter, partition)
                        if new_target != old_target and old_target != None:
                            partition.append(
                                partition[subset_index][:state_index])
                            partition.append(
                                partition[subset_index][state_index:])
                            partition.remove(partition[subset_index])
                            return True
                        old_target = new_target
            return False

        partition = [
            dfa.accept_states,
            [state for state in dfa.states if state not in dfa.accept_states]
        ]

        # Create final partition
        while split(partition):
            pass  # Do nothing

        # Create new states
        dfa.states = [f"{i}" for i in range(len(partition))]

        # Create new transitions
        transitions = {}
        for subset_index in range(len(partition)):
            transitions[f"{subset_index}"] = {}
            for letter in dfa.alphabet:
                state = partition[subset_index][0]
                transitions[f"{subset_index}"][letter] = f"{target(state, letter, partition)}"
        dfa.transitions = transitions

        # Create new initial_state
        for subset_index in range(len(partition)):
            if dfa.initial_state in partition[subset_index]:
                dfa.initial_state = f"{subset_index}"
                break

        # Create new accept states
        accept_states = []
        for subset_index in range(len(partition)):
            for accept_state in dfa.accept_states:
                if accept_state in partition[subset_index]:
                    accept_states.append(f"{subset_index}")
                    break
        dfa.accept_states = accept_states

        # Create new tags
        tags = {}
        for subset_index in range(len(partition)):
            subset_tags = []
            for state in partition[subset_index]:
                if state in dfa.tags.keys():
                    subset_tags += dfa.tags[state]
            if len(subset_tags):
                tags[f"{subset_index}"] = subset_tags
        dfa.tags = tags
        return dfa
