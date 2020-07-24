
class PathFinder(object):

    def get_path(self, grid, start_wp, end_wp):
        """ A simple A* pathfinding between start_wp and end_wp in a specific grid

        The time complexity of A* depends on the heuristic. In the worst case, the number of waypoint
        |h(x) - h*(x)| = O(logh*(x))

        @param grid: A 2D narray of True/False values to represent the field and obstacles
        @param start_wp: The Waypoint that the path should start from.
        @param end_wp: The Waypoint that the path should end on.
        @return: path: The path from the start waypoint to the end waypoint that follows the movement model without
                going off the grid or intersecting an obstacle.
        """
        # The open and closed sets
        openset = set()
        closedset = set()

        # Add the starting point to the open set
        openset.add(start_wp)

        # While the open set is not empty
        while openset:
            # Find the waypoint in the open set with the lowest G + H score
            current_wp = min(openset, key=lambda o: o.G + o.H)
            # Found the goal
            if current_wp == end_wp:
                path = []
                while current_wp.parent:
                    path.append(current_wp)
                    current_wp = current_wp.parent
                path.append(current_wp)
                print("Path found in {} moves: {}".format(len(path), path))
                return path[::-1]

            # Remove the waypoint from the open set
            openset.remove(current_wp)
            # Add it to the closed set
            closedset.add(current_wp)

            # Generate children
            children = current_wp.generate_children(grid)

            for waypoint in children:
                # If it is already in the closed set, skip it
                if waypoint in closedset:
                    continue
                # Otherwise if it is already in the open set
                if waypoint in openset:
                    # Check if we beat the G score
                    new_g = current_wp.G + 1

                    if waypoint.G > new_g:
                        # If so, update the waypoint to have a new parent
                        waypoint.G = new_g
                        waypoint.parent = current_wp
                else:
                    # If it isn't in the open set, calculate the G and H score for the waypoint
                    if waypoint.orientation != current_wp.orientation:
                        waypoint.G = current_wp.G + 1.5  # Avoiding zigzag move by increase the cost of a rotation
                    else:
                        waypoint.G = current_wp.G + 1

                    waypoint.H = abs(waypoint.x - end_wp.x) + abs(waypoint.y - end_wp.y)
                    # Set the parent to our current_wp
                    waypoint.parent = current_wp
                    # Add it to the set
                    openset.add(waypoint)

        # If there is no solution
        return [start_wp, end_wp]
