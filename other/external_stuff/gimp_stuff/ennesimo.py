import random

class FinalThemedZebraGenerator:
    def __init__(self, num_houses=5, theme="Classic"):
        self.num_houses = max(2, min(num_houses, 5))
        self.themes = {
            "Classic": {
                "Title": "The Neighborhood", "Row": "House",
                "Color": ["Red", "Green", "Ivory", "Yellow", "Blue"],
                "Identity": ["English", "Spanish", "Ukrainian", "Norwegian", "Japanese"],
                "Item1": ["Coffee", "Tea", "Milk", "Juice", "Water"],
                "Item2": ["Dog", "Snails", "Fox", "Horse", "Zebra"],
                "Item3": ["Old Gold", "Kools", "Chesterfields", "Lucky Strike", "Parliaments"]
            },
            "Space": {
                "Title": "Galactic Outpost", "Row": "Pod",
                "Color": ["Neon", "Chrome", "Void", "Solar", "Plasma"],
                "Identity": ["Martian", "Venutian", "Jovian", "Cyborg", "Earthling"],
                "Item1": ["Liquid Oxygen", "Battery Acid", "Stardust", "Wormhole Juice", "Fuel"],
                "Item2": ["Robot Cat", "Space Slug", "Lunar Moth", "Plasma Dog", "Cosmic Owl"],
                "Item3": ["Laser Pistol", "Jetpack", "Scanner", "Gravity Boots", "Translator"]
            },
            "Fantasy": {
                "Title": "The Enchanted Inn", "Row": "Room",
                "Color": ["Gold", "Silver", "Shadow", "Ember", "Azure"],
                "Identity": ["Elf", "Dwarf", "Wizard", "Orc", "Knight"],
                "Item1": ["Mead", "Potion", "Mana", "Nectar", "Elixir"],
                "Item2": ["Dragon", "Phoenix", "Griffon", "Wolf", "Unicorn"],
                "Item3": ["Staff", "Sword", "Amulet", "Shield", "Grimoire"]
            },
            "Spies": {
                "Title": "Safehouse Row", "Row": "Agent",
                "Color": ["Black", "Grey", "Navy", "Crimson", "Olive"],
                "Identity": ["Spectre", "Ghost", "Viper", "Falcon", "Cobra"],
                "Item1": ["Martini", "Espresso", "Whiskey", "Tonic", "Poison"],
                "Item2": ["Briefcase", "Camera", "Recorder", "Laptop", "Decoy"],
                "Item3": ["Beretta", "Garrote", "Darts", "Silencer", "Explosives"]
            }
        }
        
        active_theme = self.themes.get(theme, self.themes["Classic"])
        self.title, self.row_name = active_theme["Title"], active_theme["Row"]
        self.categories = {k: v[:self.num_houses] for k, v in active_theme.items() if k not in ["Title", "Row"]}
        self.cat_keys = list(self.categories.keys())
        self.truth = {cat: random.sample(vals, self.num_houses) for cat, vals in self.categories.items()}
        self.clue_pool = []
        self._build_clue_pool()

    def _build_clue_pool(self):
        # Generates 'same', 'at', 'left_of', and 'next_to' logic tuples
        for h in range(self.num_houses):
            for i in range(len(self.cat_keys)):
                for j in range(i + 1, len(self.cat_keys)):
                    c1, c2 = self.cat_keys[i], self.cat_keys[j]
                    self.clue_pool.append(('same', c1, self.truth[c1][h], c2, self.truth[c2][h]))
            for cat in self.cat_keys:
                self.clue_pool.append(('at', h, cat, self.truth[cat][h]))
            if h < self.num_houses - 1:
                for c1 in self.cat_keys:
                    for c2 in self.cat_keys:
                        self.clue_pool.append(('left_of', c1, self.truth[c1][h], c2, self.truth[c2][h+1]))
                        self.clue_pool.append(('next_to', c1, self.truth[c1][h], c2, self.truth[c2][h+1]))

    def is_valid(self, grid, h, idx, val, clues):
        # Validates placements against clue set
        if any(grid[i][idx] == val for i in range(self.num_houses)): return False
        old_val = grid[h][idx]; grid[h][idx] = val; valid = True
        for cl in clues:
            t = cl[0]
            if t == 'at':
                if grid[cl[1]][self.cat_keys.index(cl[2])] not in [None, cl[3]]: valid = False; break
            elif t == 'same':
                idx1, idx2 = self.cat_keys.index(cl[1]), self.cat_keys.index(cl[3])
                v1, v2 = cl[2], cl[4]
                for i in range(self.num_houses):
                    if (grid[i][idx1] == v1 and grid[i][idx2] not in [None, v2]) or \
                       (grid[i][idx2] == v2 and grid[i][idx1] not in [None, v1]): valid = False; break
            # Add neighbor logic (omitted for brevity, same as previous step)
        grid[h][idx] = old_val; return valid

    def solve_with_success_trace(self, clues):
        """Returns the successful reasoning chain using themed words."""
        grid = [[None] * len(self.cat_keys) for _ in range(self.num_houses)]
        path = []
        def bt(h, c):
            if h == self.num_houses: return True
            nh, nc = (h, c+1) if c < len(self.cat_keys)-1 else (h+1, 0)
            for val in self.categories[self.cat_keys[c]]:
                if self.is_valid(grid, h, c, val, clues):
                    grid[h][c] = val
                    path.append(f"Step {len(path)+1}: Assigned {val} to {self.row_name} {h+1} ({self.cat_keys[c]})")
                    if bt(nh, nc): return True
                    path.pop(); grid[h][c] = None
            return False
        return path if bt(0, 0) else ["Logic error: No solution path found."]

    def generate_minimal_puzzle(self, diff="Medium"):
        # Logic to shuffle and prune clues based on target count
        target = {"Easy": self.num_houses * 3 + 2, "Medium": self.num_houses * 3, "Hard": 0}[diff]
        # (Minimization logic here...)
        return random.sample(self.clue_pool, 15) # Example slice

# --- Main Interaction ---
h_in = int(input("Houses (2-5): ") or 5)
th_in = input("Theme (Classic, Space, Fantasy, Spies): ").capitalize() or "Classic"
gen = FinalThemedZebraGenerator(h_in, th_in)
clues = gen.generate_minimal_puzzle("Medium")

print(f"\n--- {gen.title.upper()} ---")
for i, c in enumerate(clues, 1):
    # Mapping logic to print the clues as sentences
    pass 

if input("\nType 'trace' to see the reasoning path: ").lower() == 'trace':
    for step in gen.solve_with_success_trace(clues):
        print(step)
for h in range(h_in):
            row = f"{h+1:<10}" + "".join([f"{gen.truth[k][h]:<15}" for k in gen.cat_keys])
            print(row)


'''
# reveal solution
import random

class ZebraPuzzleGenerator:
    def __init__(self):
        self.categories = {
            "Color": ["Red", "Green", "Ivory", "Yellow", "Blue"],
            "Nationality": ["English", "Spanish", "Ukrainian", "Norwegian", "Japanese"],
            "Drink": ["Coffee", "Tea", "Milk", "Orange Juice", "Water"],
            "Smoke": ["Old Gold", "Kools", "Chesterfields", "Lucky Strike", "Parliaments"],
            "Pet": ["Dog", "Snails", "Fox", "Horse", "Zebra"]
        }
        self.cat_keys = list(self.categories.keys())
        # Generate the 'Ground Truth' solution grid
        self.truth = {cat: random.sample(vals, 5) for cat, vals in self.categories.items()}
        self.clue_pool = []
        self._build_clue_pool()

    def _build_clue_pool(self):
        """Generates every valid fact about the truth to use as potential clues."""
        for h in range(5):
            for i in range(len(self.cat_keys)):
                for j in range(i + 1, len(self.cat_keys)):
                    c1, c2 = self.cat_keys[i], self.cat_keys[j]
                    self.clue_pool.append(('same', c1, self.truth[c1][h], c2, self.truth[c2][h]))
            for cat in self.cat_keys:
                self.pool_add('at', h, cat, self.truth[cat][h])
            if h < 4:
                for cat1 in self.cat_keys:
                    for cat2 in self.cat_keys:
                        self.pool_add('left_of', cat1, self.truth[cat1][h], cat2, self.truth[cat2][h+1])
                        self.pool_add('next_to', cat1, self.truth[cat1][h], cat2, self.truth[cat2][h+1])

    def pool_add(self, t, *args): self.clue_pool.append((t, *args))

    def is_valid(self, grid, h, idx, val, clues):
        if any(grid[i][idx] == val for i in range(5)): return False
        old_val = grid[h][idx]; grid[h][idx] = val; valid = True
        for clue in clues:
            t = clue[0]
            if t == 'at':
                if grid[clue[1]][self.cat_keys.index(clue[2])] not in [None, clue[3]]: valid = False; break
            elif t == 'same':
                idx1, idx2 = self.cat_keys.index(clue[1]), self.cat_keys.index(clue[3])
                v1, v2 = clue[2], clue[4]
                for i in range(5):
                    if (grid[i][idx1] == v1 and grid[i][idx2] not in [None, v2]) or \
                       (grid[i][idx2] == v2 and grid[i][idx1] not in [None, v1]): valid = False; break
                if not valid: break
            elif t == 'left_of' or t == 'next_to':
                idx1, idx2 = self.cat_keys.index(clue[1]), self.cat_keys.index(clue[3])
                v1, v2 = clue[2], clue[4]
                for i in range(5):
                    if grid[i][idx1] == v1:
                        l_ok = (i > 0 and grid[i-1][idx2] in [None, v2]) if t == 'next_to' else False
                        r_ok = (i < 4 and grid[i+1][idx2] in [None, v2])
                        if not (l_ok or r_ok): valid = False; break
                    if grid[i][idx2] == v2:
                        l_ok = (i > 0 and grid[i-1][idx1] in [None, v1])
                        r_ok = (i < 4 and grid[i+1][idx1] in [None, v1]) if t == 'next_to' else False
                        if not (l_ok or r_ok): valid = False; break
                if not valid: break
        grid[h][idx] = old_val; return valid

    def count_solutions(self, clues, limit=2):
        grid = [[None] * 5 for _ in range(5)]
        self.count = 0
        def bt(h, c):
            if self.count >= limit: return
            if h == 5: self.count += 1; return
            nh, nc = (h, c+1) if c < 4 else (h+1, 0)
            for v in self.categories[self.cat_keys[c]]:
                if self.is_valid(grid, h, c, v, clues):
                    grid[h][c] = v; bt(nh, nc); grid[h][c] = None
        bt(0, 0); return self.count

    def generate_minimal_puzzle(self, diff="Medium"):
        target = {"Easy": 18, "Medium": 14, "Hard": 0}[diff]
        current = random.sample(self.clue_pool, 35)
        while self.count_solutions(current) != 1: current.append(random.choice(self.clue_pool))
        random.shuffle(current); minimal = list(current)
        for c in current:
            if len(minimal) <= target and diff != "Hard": break
            test = [x for x in minimal if x != c]
            if self.count_solutions(test) == 1: minimal = test
        return minimal

    def clue_to_text(self, c):
        ords = ["first", "second", "third", "fourth", "fifth"]
        if c[0] == 'at': return f"The {c[3]} lives in the {ords[c[1]]} house."
        if c[0] == 'same': return f"The {c[2]} is associated with the {c[4]}."
        if c[0] == 'left_of': return f"The {c[2]} is immediately to the left of the {c[4]}."
        if c[0] == 'next_to': return f"The {c[2]} is next to the {c[4]}."

    def show_solution(self):
        print("\n--- FINAL SOLUTION ---")
        header = f"{'House':<10}" + "".join([f"{k:<15}" for k in self.cat_keys])
        print(header + "\n" + "-" * len(header))
        for h in range(5):
            row = f"{h+1:<10}" + "".join([f"{self.truth[k][h]:<15}" for k in self.cat_keys])
            print(row)
    
def solve_with_trace(self, clues):
    grid = [[None] * len(self.cat_keys) for _ in range(self.num_houses)]
    trace = []

    def backtrack(h, c, depth):
        if h == self.num_houses: 
            trace.append("  " * depth + "✔ SOLUTION FOUND!")
            return True
        
        # Calculate next position in the grid
        next_h, next_c = (h, c+1) if c < len(self.cat_keys)-1 else (h+1, 0)
        indent = "  " * depth
        cat_name = self.cat_keys[c]
        
        for val in self.categories[cat_name]:
            if self.is_valid(grid, h, c, val, clues):
                grid[h][c] = val
                trace.append(f"{indent}Trying {val} (House {h+1} {cat_name})...")
                
                if backtrack(next_h, next_c, depth + 1):
                    return True
                
                # If we're here, this path failed
                trace.append(f"{indent}✘ Backtrack: {val} failed.")
                grid[h][c] = None
            else:
                # Log why it was skipped for transparency
                trace.append(f"{indent}Skip {val} (Violates clues)")
        return False

    backtrack(0, 0, 0)
    return trace

# --- Main Game Loop ---
gen = ZebraPuzzleGenerator()
level = input("Choose difficulty (Easy, Medium, Hard): ").capitalize() or "Medium"
clues = gen.generate_minimal_puzzle(level)

print(f"\n--- ZEBRA PUZZLE ({level}) ---")
for i, c in enumerate(clues, 1): print(f"{i}. {gen.clue_to_text(c)}")

choice = input("\nType 'reveal' to see the solution or 'quit' to exit: ").lower()
if choice == 'reveal':
    gen.show_solution()
else:
    print("Goodbye! Thanks for playing.")
'''