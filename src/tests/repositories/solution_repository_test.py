import unittest
from build.database_connection import DatabaseConnection
from entities.sudoku import Sudoku
from entities.solution import Solution
from entities.user import User
from repositories.solution_repository import SolutionRepository
from repositories.sudoku_repository import SudokuRepository
from repositories.user_repository import UserRepository


class TestSolutionRepository(unittest.TestCase):
    def setUp(self):
        connection = DatabaseConnection(test=True).connect_to_database()
        self.user_repo = UserRepository(connection)
        self.user_repo.delete_all()
        self.sudoku_repo = SudokuRepository(connection)
        self.sudoku_repo.delete_all()
        self.solution_repo = SolutionRepository(connection)
        self.solution_repo.delete_all()

        self.user_jonne = User('Jonne')
        self.sudoku1 = Sudoku('Easy 1',
                              '800930002009000040702100960200000090060000070070006005027008406030000500500062008',
                              '846937152319625847752184963285713694463859271971246385127598436638471529594362718',
                              'easy')
        self.user_repo.create(self.user_jonne)
        self.sudoku_repo.create(self.sudoku1)

        self.user_jonne = self.user_repo.find_all()[0]
        self.sudoku1 = self.sudoku_repo.find_all()[0]
        self.solution1 = Solution(self.user_jonne, self.sudoku1, True, 60)
        self.solution2 = Solution(self.user_jonne, self.sudoku1, False, 120)
        self.solution3 = Solution(self.user_jonne, self.sudoku1, True, 180)
        self.solution4 = Solution(self.user_jonne, self.sudoku1, False, 240)
        self.solution5 = Solution(self.user_jonne, self.sudoku1, True, 300)

    def test_create(self):
        self.solution_repo.create(self.solution1)
        solutions = self.solution_repo.find_all()
        self.assertEqual(1, len(solutions))
        self.assertEqual(self.solution1.is_correct, solutions[0].is_correct)
        self.assertEqual(self.solution1.time, solutions[0].time)

    def test_find_all(self):
        self.solution_repo.create(self.solution1)
        solutions = self.solution_repo.find_all()
        self.assertEqual(1, len(solutions))
        self.solution_repo.create(self.solution2)
        solutions = self.solution_repo.find_all()
        self.assertEqual(2, len(solutions))
        self.assertEqual(self.solution1.is_correct, solutions[0].is_correct)
        self.assertEqual(self.solution1.time, solutions[0].time)
        self.assertEqual(self.solution2.is_correct, solutions[1].is_correct)
        self.assertEqual(self.solution2.time, solutions[1].time)

    def test_find_last_4_solutions_by_user_when_3_solutions(self):
        self.solution_repo.create(self.solution1)
        self.solution_repo.create(self.solution2)
        self.solution_repo.create(self.solution3)
        solutions = self.solution_repo.find_last_4_solutions_by_user(
            self.user_jonne)
        self.assertEqual(3, len(solutions))
        self.assertEqual(180, solutions[0].time)
        self.assertEqual(60, solutions[2].time)

    def test_find_last_4_solutions_by_user_when_4_solutions(self):
        self.solution_repo.create(self.solution1)
        self.solution_repo.create(self.solution2)
        self.solution_repo.create(self.solution3)
        self.solution_repo.create(self.solution4)
        solutions = self.solution_repo.find_last_4_solutions_by_user(
            self.user_jonne)
        self.assertEqual(4, len(solutions))
        self.assertEqual(240, solutions[0].time)
        self.assertEqual(60, solutions[3].time)

    def test_find_last_4_solutions_by_user_when_5_solutions(self):
        self.solution_repo.create(self.solution1)
        self.solution_repo.create(self.solution2)
        self.solution_repo.create(self.solution3)
        self.solution_repo.create(self.solution4)
        self.solution_repo.create(self.solution5)
        solutions = self.solution_repo.find_last_4_solutions_by_user(
            self.user_jonne)
        self.assertEqual(4, len(solutions))
        self.assertEqual(300, solutions[0].time)
        self.assertEqual(120, solutions[3].time)

    def test_find_by_id(self):
        self.solution_repo.create(self.solution1)
        solution_to_find = self.solution_repo.find_all()[0]
        solution = self.solution_repo.find_by_id(solution_to_find.id)
        self.assertEqual(solution_to_find.id, solution.id)
