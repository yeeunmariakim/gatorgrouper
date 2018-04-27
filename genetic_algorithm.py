"""Generate grouping based on student skills and preferences."""
from typing import List
import random
from colors import bold
import numpy as np
import workbook


class Student:
    """Represent student."""
    def __init__(self, email: str, skills: List[int], preferences: List[str]):
        self.email = email
        self.skills = skills
        self.preferences = preferences

    def __str__(self):
        student_str = self.email + "\n"
        student_str += "\tPreferences: " + str(self.preferences) + "\n"
        student_str += "\tSkills: " + str(self.skills)
        return student_str


class Individual:
    """Represent individual."""
    def __init__(self, grouping: List[List[Student]], fitness):
        self.grouping = grouping
        self.fitness = fitness

    def __str__(self):
        grouping_str = ""
        for number, group in self.grouping:
            grouping_str += "Group {}".format(number) + "\n"
            for student in group:
                grouping_str += student + "\n"
        return bold("Grouping\n") + grouping_str + bold("Fitness") + self.fitness


class Fitness:
    """Represent fitness."""
    def __init__(self, preference, balance, fairness):
        self.preference = preference
        self.balance = balance
        self.fairness = fairness
        # FIXME
        self.value = preference + balance + fairness

    def __gt__(self, other):
        return self.value > other.value

    def __str__(self):
        return "{:0.2f}".format(self.value)


def create():
    students_to_group = workbook.STUDENTS[:]
    random.shuffle(students_to_group)

    grouping = list()

    for _ in range(workbook.GROUPING_SIZE):
        grouping.append(list())

    for index, student in enumerate(students_to_group):
        grouping[index % workbook.GROUPING_SIZE].append(student)

    return grouping

"""population_size: int, mutation_rate: float, crossover_rate: float, fitness, mutations, create"""
def evolve(population_size, mutation_rate, crossover_rate, fitness, mutations, create):
    pass

def crossover(individual_one, individual_two):
    grouping1 = individual_one.grouping[:]
    grouping2 = individual_two.grouping[:]

    equal_groups = set()
    for group1 in grouping1:
        for group2 in grouping2:
            if set(group1) == set(group2):
                equal_groups.add(group1)

    for equal_group in equal_groups:
        for group in grouping1:
            if set(group) == set(equal_group):
                grouping1.remove(group)

        for group in grouping2:
            if set(group) == set(equal_group):
                grouping2.remove(group)

    # # FIXME: for now just adding the rest of students randomly
    # students_so_far = set()
    # for group in equal_groups:
    #     for student in group:
    #         students_so_far.add(student)



def mutate(mutations, grouping: List[List[Student]]):
    """Mutate a grouping with a randomly chosen mutation."""
    return random.choice(mutations)(grouping)


def spawn(population: List[Individual], mutation_rate: float, crossover_rate: float, mutations, create):
    pass

def select(population: List[Individual]):
    """Select random individuals from population and find most fit tournament-style."""
    SELECT_NUMBER = 10
    selected = random.sample(population, SELECT_NUMBER)
    while len(selected) > 1:
        individual_one = selected.pop(0)
        individual_two = selected.pop(0)
        if (individual_one.fitness > individual_two.fitness):
            selected.append(individual_one)
        else:
            selected.append(individual_two)
    return selected[0]


def calculate_fitness(grouping: List[List[Student]]):
    # student preferences
    preferences_total = 0
    for group in grouping:
        for student in group:
            preferences_total += len(student.preferences)

    preferences_respected = 0
    for group in grouping:
        for student in group:
            for other in group:
                if other in student.preferences:
                    preferences_respected += 1

    preferences_value = preferences_respected / preferences_total  # 0 to 1

    # skill balance, measured by the standard deviation of student skills from the group average
    # low balance:
    # average of [5, 5, 5] = 5
    # average of [1, 1, 1] = 1
    # average of 5 and 1 is 3
    # standard deviation of 5 and 1 from 6 is 2 (then, invert)
    # high balance:
    # average of [5, 5, 1] = 3.6
    # average of [1, 1, 5] = 2.3
    # average of 5 and 1 is 2.95
    # standard deviation of 5 and 1 from 6 is 0.65 (then, invert)

    group_stds = list()
    for group in grouping:
        student_skill_averages = list()
        for student in group:
            student_skill_total = 0
            for skill in student.skills:
                student_skill_total += skill
            student_skill_averages.append(student_skill_total / len(student.skills))
        group_stds.append(np.std(student_skill_averages))

    balance_value = sum(group_stds)

    # create balance value ranging from 0 to 1 from group stds

    # skill fairness

    # num_of_skills = len(grouping[0][0].skills)
    # grouping_skills = [list()] * 5
    # for group in grouping:
    #     group_averages = [list()] *
    #     for student in group:
    #         for index, skill in enumerate(student.skills):
    #             grouping_skills
    fairness_value = 0

    return Fitness(preferences_value, balance_value, fairness_value)
