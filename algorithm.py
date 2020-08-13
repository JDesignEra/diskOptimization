class Algorithm:
    def __init__(self, seq: list, cylinder: int, curr: int, prev: int):
        self.seq = seq
        self.cylinder = cylinder
        self.curr = curr
        self.prev = prev

    def start(self, algorithm: str):
        if algorithm == 'fcfs':
            return self.fcfs()
        elif algorithm == 'sstf':
            return self.sstf()
        elif algorithm == 'scan':
            return self.scan()
        elif algorithm == 'look':
            return self.look()
        elif algorithm == 'cscan':
            return self.cscan()
        elif algorithm == 'clook':
            return self.clook()
        else:
            return None

    def buildFormula(self, seq: list):
        """
        @param seq: List of arranged Sequence
        @return: String of concat formula
        """
        formula = ''

        for i, v in enumerate(seq):
            if i + 1 < len(seq):
                if v > seq[i + 1]:
                    formula += '({} - {}) + '.format(v, seq[i + 1])
                else:
                    formula += '({} - {}) + '.format(seq[i + 1], v)

        return formula[:-3]

    def fcfs(self):
        arranged = [self.curr]
        arranged += self.seq.copy()
        distance = sum([abs(v - arranged[i + 1]) for i, v in enumerate(arranged[:len(arranged) - 1])])

        return {'distance': distance, 'formula': self.buildFormula(arranged), 'sequence': arranged}

    def sstf(self):
        sequence = self.seq.copy()
        arranged = [self.curr]
        distance = 0
        curr = arranged[0]

        # Arrange and calculate distance logic
        while len(sequence) > 0:
            assign = min(enumerate(sequence), key=lambda x: abs(x[1] - curr))    # Returns index, nearest value.
            distance += abs(arranged[-1] - assign[1])
            curr = assign[1]

            arranged.append(assign[1])
            del sequence[assign[0]]

        return {'distance': distance, 'formula': self.buildFormula(arranged), 'sequence': arranged}

    def scan(self):
        sequence = [self.curr]
        sequence += self.seq.copy()

        # Arranged Logic
        if self.prev > self.curr:   # Working towards smaller end first
            sequence.sort()     # Sort ascending
            idx = sequence.index(self.curr)     # Find current head index

            arranged = sequence[idx:: -1]
            arranged.append(0)
            arranged += sequence[idx + 1:]
        else:   # Working towards larger end first
            sequence.sort(reverse=True)  # Sort ascending
            idx = sequence.index(self.curr)  # Find current head index

            arranged = sequence[idx::-1]
            arranged.append(self.cylinder)
            arranged += sequence[idx + 1:]

        # Calculate Distance
        distance = sum([abs(v - arranged[i + 1]) for i, v in enumerate(arranged[:len(arranged) - 1])])

        return {'distance': distance, 'formula': self.buildFormula(arranged), 'sequence': arranged}

    def look(self):
        sequence = [self.curr]
        sequence += self.seq.copy()

        # Arranged Logic
        if self.prev > self.curr:  # Working towards smaller end first
            sequence.sort()  # Sort ascending
            idx = sequence.index(self.curr)  # Find current head index

            arranged = sequence[idx:: -1]
            arranged += sequence[idx + 1:]
        else:  # Working towards larger end first
            sequence.sort(reverse=True)  # Sort ascending
            idx = sequence.index(self.curr)  # Find current head index

            arranged = sequence[idx::-1]
            arranged += sequence[idx + 1:]

        # Calculate Distance
        distance = sum([abs(v - arranged[i + 1]) for i, v in enumerate(arranged[:len(arranged) - 1])])

        return {'distance': distance, 'formula': self.buildFormula(arranged), 'sequence': arranged}

    def cscan(self):
        sequence = [self.curr]
        sequence += self.seq.copy()

        # Arranged Logic
        if self.prev > self.curr:  # Working towards smaller end first
            sequence.sort()  # Sort ascending
            idx = sequence.index(self.curr)  # Find current head index

            arranged = sequence[idx:: -1]
            arranged.append(0)
            arranged += sequence[idx + 1:]
            arranged.append(self.cylinder)
        else:  # Working towards larger end first
            sequence.sort(reverse=True)  # Sort ascending
            idx = sequence.index(self.curr)  # Find current head index

            arranged = sequence[idx::-1]
            arranged.append(self.cylinder)
            arranged.append(0)
            arranged += sequence[idx + 1:]

        # Calculate Distance
        distance = sum([abs(v - arranged[i + 1]) for i, v in enumerate(arranged[:len(arranged) - 1])])

        return {'distance': distance, 'formula': self.buildFormula(arranged), 'sequence': arranged}

    def clook(self):
        sequence = self.seq.copy()  # Copy disk sequence over
        sequence.append(self.curr)

        if self.prev > self.curr:  # Working towards end of cylinder
            sequence.sort(reverse=True)
            idx = sequence.index(self.curr)
            arranged = sequence[idx:]
            arranged += sequence[idx - 1::-1]
        else:  # Working towards smaller end of cylinder
            sequence.sort()
            idx = sequence.index(self.curr)
            arranged = sequence[idx:]
            arranged += sequence[idx - 1::-1]

        # Calculate distance
        distance = 0

        for i, val in enumerate(arranged):
            if i + 1 < len(arranged):
                distance += abs(val - arranged[i + 1])

        return {'distance': distance, 'formula': self.buildFormula(arranged), 'sequence': arranged}
