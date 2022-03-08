from typing import Dict, List, Tuple, Optional
from bisect import bisect_left
from hashlib import sha256
import random
import yaml
import sys

with open("votes.yaml", "r") as f:
	raw = yaml.safe_load(f)

with open("votes.yaml", "rb") as f:
	SEED = sha256(f.read()).hexdigest()

CONFIGS = raw['Configs']
PLAYERS = raw['Players']
random.seed(SEED)

def preamble():
	"""Starting preamble
	
	Basic prints of configurations and players for context.
	"""
	print(f"Total votes per player: {CONFIGS['votes_per_person']}")
	print(f"Counting type: {CONFIGS['counting_type']}")
	print(f"Contended Projects: {CONFIGS['contended_projects']}")
	print(f"Players: {list(PLAYERS.keys())}")
	print(f"Seed: {SEED}")
	print()

def check_violations():
	"""Check for rule violations.
	
	Checks:
	1. Users votes have integer values
	2. Users votes are non-negative
	3. Users have voted for all the projects
	4. The sum of users votes do not exceed the set voted_per_person

	If violations are detected. The program will exit with error flag 1.
	"""
	violations = []
	for player, player_votes in PLAYERS.items():
		# Rule 1
		if not all(isinstance(i, int) for i in player_votes.values()):
			violations.append(f"[{player}] Non integer vote")
			continue
		# Rule 2
		if not all(i >= 0 for i in player_votes.values()):
			violations.append(f"[{player}] Non positive vote")
			continue
		# Rule 3
		if set(player_votes.keys()) != set(CONFIGS['contended_projects']):
			violations.append(f"[{player}] Does not have votes equal to the set of contended projects")
		# Rule 4
		if sum(player_votes.values()) != CONFIGS['votes_per_person']:
			violations.append(f"[{player}] Has {sum(player_votes.values())} votes instead of {CONFIGS['votes_per_person']}")

	# Detail violations if exists. If exists, exit with flag 1
	if violations:
		print("#" + "="*21)
		print("# Violations detected")
		print("#" + "-"*21)
		print(*violations, sep="\n")
		print()
		print("Exiting...")
		sys.exit(1)


def resolve_project(project_name: str, votes: List[Tuple[str, int]]) -> Optional[str]:
	"""Resolve one project
	
	Args:
		project_name (str): The name of the project
		votes (List[Tuple[str, int]]): 
			A list of votes for the project. The first index is the name of the voter. 
			The second is the amount of votes they put in.
	"""
	# Preamble
	print(f"Project: {project_name}")
	print(f"Votes: {votes}")

	# If no votes, skip
	if sum(i[1] for i in votes) <= 0:
		print("No one voted for this project :( Skipping...")
		print()
		return None

	# Create intervals
	intervals = [0]
	for player, player_votes in votes:
		if CONFIGS['counting_type'] == 'linear':
			intervals.append(intervals[-1] + player_votes)
		if CONFIGS['counting_type'] == 'quadratic':
			intervals.append(intervals[-1] + player_votes ** 2)
	print(f"Intervals: {intervals}")

	# Select winner
	winning_number = random.randint(1, intervals[-1])
	winning_index = bisect_left(intervals, winning_number) - 1
	winner = votes[winning_index][0]

	# Success messages
	print(f"Winning Number: {winning_number}")
	print(f"Winner: {winner} [{winning_index}]")
	print()

	return winner


def play():
	"""Play the game

	Attempts to resolve all the projects in descending order of total votes.
	"""
	winners = {}
	projects = sorted(
		CONFIGS['contended_projects'], 
		key=lambda project: sum(v[project] for v in PLAYERS.values()),
		reverse=True
	)

	for project in projects:
		project_votes = list((k, v[project]) for k,v in PLAYERS.items() if k not in winners.keys())
		winner = resolve_project(project, project_votes)
		if winner:
			winners[winner] = project

	print("Winners")
	print("=======")
	print(winners)
	print()
	print("Unallocated")
	print("===========")
	print("Players:", set(PLAYERS.keys()) - set(winners.keys()))
	print("Projects:", set(CONFIGS['contended_projects']) - set(winners.values()))


if __name__ == '__main__':
	preamble()
	assert CONFIGS['counting_type'] in ['linear', 'quadratic']
	check_violations()
	play()
