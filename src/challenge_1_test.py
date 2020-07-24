#!/usr/bin/env python
import sys
import numpy as np
import random

import unittest

from path_finder import PathFinder
from path_validator import PathValidator
from path_visualizer import PathVisualizer
from waypoint import Waypoint


class Challenge1TestCase(unittest.TestCase):

    VIZ = False

    def setUp(self):
        self.path_finder = PathFinder()

    def tearDown(self):
        self.path_finder = None

    def _run_test(self, grid, queries):
        for query in queries:
            path = self.path_finder.get_path(grid, query[0], query[1])
            if Challenge1TestCase.VIZ:
                PathVisualizer.viz_path(grid, query, path)
            self.assertTrue(PathValidator.is_valid_path(grid, query, path),
                            "Invalid path %s for query %s." % (path, query))

    def _run_test_with_no_solution(self, grid, queries):
        for query in queries:
            path = self.path_finder.get_path(grid, query[0], query[1])
            if Challenge1TestCase.VIZ:
                PathVisualizer.viz_path(grid, query, path)
            self.assertTrue(len(path) == 2, "No path should be return from this one")

    def test_no_obstacles_straight_line(self):
        grid = np.zeros((20, 20)).astype(np.bool)
        queries = [
            [Waypoint(5, 5, 0), Waypoint(5, 8, 0)],
            [Waypoint(16, 5, 1), Waypoint(8, 5, 1)],
            [Waypoint(5, 15, 3), Waypoint(16, 15, 3)],
        ]
        self._run_test(grid, queries)

    def test_no_obstacles_with_turns(self):
        grid = np.zeros((20, 20)).astype(np.bool)
        queries = [
            [Waypoint(5, 7, 0), Waypoint(15, 8, 3)],
            [Waypoint(16, 5, 2), Waypoint(8, 5, 1)],
            [Waypoint(15, 15, 1), Waypoint(16, 15, 3)],
        ]
        self._run_test(grid, queries)

    def test_with_one_obstacle(self):
        grid = np.zeros((20, 20)).astype(np.bool)
        grid[10:14, 10:14] = True
        queries = [
            [Waypoint(5, 7, 0), Waypoint(15, 11, 3)],
            [Waypoint(16, 5, 2), Waypoint(8, 5, 1)],
            [Waypoint(15, 15, 1), Waypoint(16, 15, 3)],
        ]
        self._run_test(grid, queries)

    def test_with_random_obstacle(self):
        grid = np.zeros((20, 20)).astype(np.bool)

        for variable in range(1,4):
            rand_a = random.randint(1, 10)
            rand_b = random.randint(0, 5)
            rand_c = random.randint(5, 10)
            rand_d = random.randint(0, 5)

            grid[rand_a:rand_a + rand_b, rand_c:rand_c + rand_d] = True

        queries = [
            [Waypoint(0, 0, 0), Waypoint(19, 19, 3)],
        ]
        self._run_test(grid, queries)

    def test_with_multiple_obstacles(self):
        grid = np.zeros((20, 20)).astype(np.bool)

        grid[3:4, 0:15] = True
        grid[13:14, 5:20] = True

        queries = [
            [Waypoint(0, 0, 0), Waypoint(19, 19, 3)]
        ]
        self._run_test(grid, queries)

    def test_with_complex_obstacles(self):
        grid = np.zeros((20, 20)).astype(np.bool)

        grid[3:4, 5:20] = True
        grid[7:8, 0:15] = True
        grid[13:14, 5:20] = True
        grid[11:14, 4:5] = True
        grid[14:17, 7:8] = True
        grid[15:20, 12:13] = True

        queries = [
            [Waypoint(0, 0, 0), Waypoint(19, 19, 3)]
        ]
        self._run_test(grid, queries)

    def test_with_no_solution(self):
        grid = np.zeros((20, 20)).astype(np.bool)

        grid[15:16, 0:10] = True
        grid[15:20, 10:11] = True

        queries = [
            [Waypoint(0, 0, 0), Waypoint(19, 2, 3)]
        ]
        self._run_test_with_no_solution(grid, queries)


if __name__ == '__main__':
    if '--viz' in sys.argv:
        Challenge1TestCase.VIZ = True
        sys.argv.pop()
    unittest.main()
