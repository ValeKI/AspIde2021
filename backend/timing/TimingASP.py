import os
import time
from subprocess import Popen, PIPE, getoutput, STDOUT
import csv


# 0. timing asp
NAME_SOLUTION = 'solution'


def is_file_empty(file_name):
    """ Check if file is empty by confirming if its size is 0 bytes"""
    # Check if file exist and it is empty
    return os.path.isfile(file_name) == 0


class TimingASP:
    def __init__(self, program=None, facts=None, N=31):
        self.program = (program if program is not None else '')
        self.facts = (facts if facts is not None else [])

        self.N = N
        self.dlv_path = '../timing/dlv2.win.x64_5'
        self.benchmarks = []
        self.keyBenchmark = None

    def clearAnswerSet(self, txt: str):
        if len(txt.split("{")) > 1:
            return txt.split("{")[1][:-1]

    def runProgram(self, program: str) -> str:
        p = Popen([self.dlv_path, '--stdin'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
        stdout_data = p.communicate(input=str.encode(program))[0]
        return stdout_data.decode().strip()

    def runPrograms(self):
        rows = []
        for test in self.facts:
            rows.append(f'{self.program} {test}')
        if len(rows) == 0:
            rows.append(self.program)
        answerSets = []
        for row in rows:
            s = self.clearAnswerSet(self.runProgram(row))
            if s is not None:
                answerSets.append(s)
        return answerSets

    def clocks(self, fact):
        initial_time = time.time()
        print(f"{self.dlv_path} {self.program} {fact}")
        self.runProgram(f"{self.program} {fact}")
        end_time = time.time()
        return end_time - initial_time

    def clocksNTime(self, program, fact):
        t = 0

        if self.program != program:
            self.program = program

        if fact not in self.facts:
            self.facts.append(fact)

        if self.keyBenchmark != program:
            self.keyBenchmark = program
            self.benchmarks = []

        for i in range(0, self.N):
            t = t + self.clocks(fact)
        t = t / self.N
        self.benchmarks.append(t)
        return t

    def clocksAll(self):
        row = {}
        for fact in self.facts:
            row[f"{fact}"] = self.clocksNTime(self.program, fact)
        return row

    def reset(self):
        self.benchmarks = []
        self.facts = []
        self.program = ''


if __name__ == '__main__':
    tim = TimingASP('print(T):- text(T).', ['text(ciao).', 'text(buonasera).'])

    print(tim.runPrograms())
