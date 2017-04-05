#!/usr/bin/python
import random, time, sys, datetime

WEEKS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

class Maze:
	def __init__(self, w, h):
		self.w, self.h = w, h
		self.generate()

	def generate(self):
		w, h = self.w, self.h
		maze = [["X" for j in range(h)] for i in range(w)]
		start = 1, h//2
		maze[start[0]][start[1]] = "S"
		last_pos = start
		while True:
			if random.choice([True, False]):
				rand_x = random.choice([1, 1, 1, -1])
				rand_y = 0
			else:
				rand_x = 0
				rand_y = random.choice([1, -1])
			next_pos = last_pos[0] + rand_x, last_pos[1] + rand_y
			next_pos = max(next_pos[0], 0), max(next_pos[1], 0)
			next_pos = min(next_pos[0], w - 1), min(next_pos[1], h - 1)

			# start over if we tried to do an invalid move
			if next_pos == last_pos:
				continue

			if maze[next_pos[0]][next_pos[1]] == "X":
				maze[next_pos[0]][next_pos[1]] = " "

			if next_pos == (w - 1, h - 1):
				# we've reached the end
				maze[next_pos[0]][next_pos[1]] = "*"
				break
			last_pos = next_pos

		# remove some random Xes
		for i in range(w):
			for j in range(h):
				if maze[i][j] == "X" and random.random() < 0.7:
					maze[i][j] = " "

		# fix the bug
		for j in range(0, h):
			maze[0][j] = "X"

		self.maze = maze

	def pretty_print(self):
		for j in range(self.h):
			row = []
			for i in range(self.w):
				row.append(self.maze[i][j])
			print("".join(row))

	def check_solution(self, solution):
		last_pos = [1, self.h // 2]
		for step in solution:
			s = step.lower()
			if s == "u":
				last_pos[1] -= 1
			elif s == "d":
				last_pos[1] += 1
			elif s == "l":
				last_pos[0] -= 1
			elif s == "r":
				last_pos[0] += 1
			else:
				continue
			maze_char = self.maze[last_pos[0]][last_pos[1]]
			# uncomment to show the solution
			# self.maze[last_pos[0]][last_pos[1]] = "Q"
			if maze_char == " ":
				continue
			elif maze_char == "X":
				return False
			elif maze_char == "*":
				return True
		return False

def print_center(s):
	print(" "*(40 - len(s) // 2) + s)

if __name__ == "__main__":
	s = int(time.time())
	d = datetime.datetime.fromtimestamp(s)
	random.seed(s)

	print("#" * 80)
	print_center("Happy {}! It's {}".format(WEEKS[d.weekday()], d.isoformat()))
	print_center("Now that we've fixed all of our security vulnerabilities,")
	print_center("we've released the source of our project1")
	print_center("Solve 10 mazes in under 1 second!")
	print_center("Accepts a list of u, d, l, and r characters to move from S to *")
	print("#" * 80)
	total_time = 0.0
	for i in range(10):
		m = Maze(80, 20)
		m.pretty_print()
		sys.stdout.flush()
		print("Your solution: ", end="")
		start = time.time()
		attempt = input()
		if m.check_solution(attempt):
			print("Valid solution! {} remaining".format(9 - i))
			finish = time.time()
			total_time += finish - start
			if total_time >= 1.0:
				print("Too slow! ({} seconds!)".format(total_time))
				exit(0)
		else:
			print("Invalid!")
			exit(0)

	print("flag{???}")
	sys.stdout.flush()

