import random
class Player:
    def __init__(self, name, team, actions, lives):
        self.name = name
        self.team = team
        self.actions = actions
        self.lives = lives

    def reset(self):
        self.reversed = False
        self.blocked = False
        self.effects = {}

    def __str__(self):
        return f"{self.name} ({self.team}) - Lives: {self.lives} - Actions: {self.actions}"

def vote(players, opponents):
    vote = None
    votes = {opponent: 0 for opponent in opponents}
    for player in players:
        opponent = random.choice(opponents)
        votes[opponent] += 1
    max_votes = max(votes.values())
    most_voted_opponents = [opponent for opponent, vote in votes.items() if vote == max_votes]
    if len(most_voted_opponents) == 1:
        vote = most_voted_opponents[0]
        for player in players:
            vote.effects.setdefault(player.name, set()).add("kill")
    return vote

def take_actions(players, opponents):
    for player in players:
        opponent = random.choice(opponents)
        for action in player.actions:
            take_action = random.choice([True, False])
            if take_action:
                if player.actions[action] > 0:
                    player.actions[action] -= 1
                    opponent.effects.setdefault(player.name, set()).add(action)

def check_win_condition(players):
    alive_players = [p for p in players if p.lives > 0]
    alive_wolves = [p for p in alive_players if p.team == "wolf"]
    alive_non_wolves = [p for p in alive_players if p.team != "wolf"]
    if len(alive_wolves) >= len(alive_non_wolves):
        print(f"================================================================================")
        print("🐺 The wolves win")
        return True
    elif len(alive_wolves) == 0:
        print(f"================================================================================")
        print("👨‍👩‍👧‍👦 The villagers win")
        return True
    return False

def play_game(players):
    day = 0
    while True:
        day += 1
        print(f"================================================================================")
        print(f"Day {day}")
        for player in players:
            player.reset()
            
        alive_players = [p for p in players if p.lives > 0]
        alive_wolves = [p for p in alive_players if p.team == "wolf"]
        alive_non_wolves = [p for p in alive_players if p.team != "wolf"]

        # Step 1: Night phase
        # Wolves and non wolves take actions
        print("🌙 Night Phase Begins")
        take_actions(alive_wolves, alive_non_wolves)
        take_actions(alive_non_wolves, players)
        
        # Remove players' blocked effects
        for player in alive_players:
            player.reversed = any("reverse" in v for v in player.effects.values())
            player.blocked = not player.reversed and any("block" in v for v in player.effects.values())
        alive_players_dict = {player.name: player for player in alive_players}
        for player in alive_players:
            for key in list(player.effects.keys()): 
                if alive_players_dict[key].blocked:
                    del player.effects[key]

        # Update players' effects
        for player in alive_players:
            if player.blocked:
                print(f"⛔ {player.name} is blocked.")

            if player.reversed:
                print(f"🔄 {player.name} is reversed.")

            killed = not player.reversed and any("kill" in v for v in player.effects.values())
            if killed and player.lives > 0:
                player.lives -= 1
                print(f"💀 {player.name} is killed with {player.lives} lives left.")
            
            revived = not player.reversed and any("revive" in v for v in player.effects.values())
            if revived:
                player.lives += 1
                print(f"❤️‍🔥 {player.name} is revived with {player.lives} lives.")

            checked = not player.reversed and any("check" in v for v in player.effects.values())
            if checked:
                print(f"🔍 {player.name} team is '{player.team}'.")

        # Wolves vote
        voter = vote(alive_wolves, alive_non_wolves)
        if voter and player.lives > 0:
            voter.lives -= 1
            print(f"💀 {voter.name} is killed with {voter.lives} lives left.")

        # Check win condition
        if check_win_condition(players):
            break

        print("☀️ Day Phase Begins")
        # Players vote
        voter = vote(alive_players, alive_players)
        if voter and player.lives > 0:
            voter.lives -= 1
            print(f"💀 {voter.name} is killed with {voter.lives} lives left.")

        # Check win condition
        if check_win_condition(players):
            break

def print_status(players):
    print("\n🧾 Current Status:")
    for player in players:
        print(player)
    print(f"================================================================================")

# 🧑‍🤝‍🧑 Sample Players
# 🧑‍🤝‍🧑 Extended Sample Players
alice = Player("Alice", "villager", {}, 1)
bob = Player("Bob", "witch", {"revive": 1}, 1)
carol = Player("Carol", "wolf", {}, 1)
dave = Player("Dave", "seer", {"check": 2}, 1)
eve = Player("Eve", "villager", {"block": 1}, 1)
frank = Player("Frank", "wolf", {"kill": 1}, 1)
grace = Player("Grace", "villager", {"revive": 1}, 1)
hannah = Player("Hannah", "wolf", {"check": 1}, 1)
ian = Player("Ian", "villager", {"block": 1}, 1)
jack = Player("Jack", "villager", {}, 1)
kim = Player("Kim", "seer", {"check": 1}, 1)
lucas = Player("Lucas", "hunter", {}, 2)

# Players List
players = [alice, bob, carol, dave, eve, frank, grace, hannah, ian, jack, kim, lucas]

# Sample Game Run
play_game(players)
print_status(players)