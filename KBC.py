# kbc.py
# KBC-style quiz game (console)
# Save as kbc.py and run: python kbc.py
# Written for a friendly interactive experience.

import random
import sys
import time

# ========== Questions ==========
# Format: { "q": str, "options": [str,...], "correct": index }
QUESTIONS = [
    {"q": "Which planet is known as the Red Planet?",
     "options": ["Earth", "Mars", "Venus", "Jupiter"], "correct": 1},
    {"q": "Who is known as the father of computers?",
     "options": ["Nikola Tesla", "Charles Babbage", "Thomas Edison", "Alan Turing"], "correct": 1},
    {"q": "What is the national animal of India?",
     "options": ["Lion", "Peacock", "Tiger", "Elephant"], "correct": 2},
    {"q": "Which gas do plants absorb from the atmosphere?",
     "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Helium"], "correct": 2},
    {"q": "How many continents are there on Earth?",
     "options": ["5", "6", "7", "8"], "correct": 2},
    {"q": "Which is the largest ocean on Earth?",
     "options": ["Atlantic", "Indian", "Pacific", "Arctic"], "correct": 2},
    {"q": "Who wrote 'Romeo and Juliet'?",
     "options": ["Charles Dickens", "William Shakespeare", "Mark Twain", "Leo Tolstoy"], "correct": 1},
    {"q": "What is H2O commonly known as?",
     "options": ["Salt", "Water", "Hydrogen Peroxide", "Ozone"], "correct": 1},
    {"q": "Which instrument measures temperature?",
     "options": ["Barometer", "Hygrometer", "Thermometer", "Voltmeter"], "correct": 2},
    {"q": "Which metal is liquid at room temperature?",
     "options": ["Iron", "Mercury", "Gold", "Aluminium"], "correct": 1},
    {"q": "Which country is known as the Land of the Rising Sun?",
     "options": ["China", "Japan", "Thailand", "India"], "correct": 1},
    {"q": "Which element has the chemical symbol 'O'?",
     "options": ["Gold", "Oxygen", "Osmium", "Silver"], "correct": 1},
    {"q": "Which is the fastest land animal?",
     "options": ["Lion", "Cheetah", "Tiger", "Leopard"], "correct": 1},
    {"q": "Which organ pumps blood through the body?",
     "options": ["Lungs", "Liver", "Heart", "Kidneys"], "correct": 2},
    {"q": "Which planet is the largest in our solar system?",
     "options": ["Saturn", "Jupiter", "Neptune", "Earth"], "correct": 1},
]

# ========== Prize ladder ==========
PRIZES = ["₹100", "₹200", "₹300", "₹500", "₹1,000",
          "₹2,000", "₹4,000", "₹8,000", "₹16,000", "₹32,000",
          "₹64,000", "₹1,25,000", "₹2,50,000", "₹5,00,000", "₹1,00,00,000"]

# ========== Lifelines state ==========
lifelines = {
    "50-50": True,
    "audience": True,
    "phone": True
}

def slow_print(s, delay=0.02):
    for ch in s:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

def show_intro():
    slow_print("=== Welcome to KBC (Console Version) ===\n", 0.01)
    slow_print("Rules simple hain: 15 questions. Har correct answer aapko aage badhata hai.\n", 0.01)
    slow_print("Aapke paas 3 lifelines hain: 50-50, Audience Poll, Phone-a-Friend (ek-ek baar use karein).\n", 0.01)
    slow_print("Agar aap kisi waqt quit karna chahte hain, type kariye 'quit' or 'q'.\n", 0.01)
    input("Press Enter to start...")

def format_options(opts, removed=None):
    """Return list of (label, text) for options A-D, skipping removed indices."""
    labels = ['A', 'B', 'C', 'D']
    out = []
    for i, text in enumerate(opts):
        if removed and i in removed:
            out.append((labels[i], "-----"))
        else:
            out.append((labels[i], text))
    return out

def ask_question(qobj, qnum):
    print("\nQuestion", qnum+1, "for", PRIZES[qnum])
    print(qobj["q"])
    removed = set()
    while True:
        opts = format_options(qobj["options"], removed)
        for lab, txt in opts:
            print(f"  {lab}. {txt}")
        print("\nAvailable lifelines:", ", ".join([k for k,v in lifelines.items() if v]) or "None")
        ans = input("Answer (A/B/C/D) or type lifeline name (50-50 / audience / phone) or 'quit': ").strip().lower()

        if ans in ('quit', 'q'):
            return 'quit', None

        # lifeline handling
        if ans in ('50-50', '50 50', '50'):
            if not lifelines["50-50"]:
                print("50-50 already used.")
                continue
            lifelines["50-50"] = False
            removed = do_50_50(qobj)
            continue
        if ans in ('audience', 'audience poll', 'poll'):
            if not lifelines["audience"]:
                print("Audience poll already used.")
                continue
            lifelines["audience"] = False
            do_audience(qobj, removed)
            continue
        if ans in ('phone', 'phone-a-friend', 'phone a friend', 'friend'):
            if not lifelines["phone"]:
                print("Phone-a-Friend already used.")
                continue
            lifelines["phone"] = False
            do_phone(qobj, removed)
            continue

        # answer handling
        if ans in ('a','b','c','d'):
            idx = {'a':0,'b':1,'c':2,'d':3}[ans]
            if idx in removed:
                print("Option removed. Choose another.")
                continue
            return 'answer', idx
        else:
            print("Invalid input. Try again.")

def do_50_50(qobj):
    correct = qobj["correct"]
    options = list(range(len(qobj["options"])))
    wrongs = [i for i in options if i != correct]
    removed = set(random.sample(wrongs, k=2))
    print("\n50-50 activated. Two wrong options removed.")
    return removed

def do_audience(qobj, removed):
    correct = qobj["correct"]
    base = [0,0,0,0]
    # create a poll favoring the correct answer
    correct_pct = random.randint(50, 80)
    remaining = 100 - correct_pct
    others = [i for i in range(4) if i != correct]
    # if some options removed, distribute differently
    active_others = [i for i in others if not removed or i not in removed]
    if not active_others:
        active_others = others
    parts = [random.
    randint(0, remaining) for _ in active_others]
    # normalize
    s = sum(parts) if sum(parts) > 0 else len(parts)
    parts = [int(round(p * remaining / s)) for p in parts]
    # correct small rounding fix
    while sum(parts) + correct_pct < 100:
        parts[random.randrange(len(parts))] += 1
    while sum(parts) + correct_pct > 100:
        parts[random.randrange(len(parts))] = max(0, parts[random.randrange(len(parts))]-1)

    for i, p in zip(active_others, parts):
        base[i] = p
    base[correct] = correct_pct

    # display
    labels = ['A','B','C','D']
    print("\nAudience Poll results (approx):")
    for i, pct in enumerate(base):
        txt = "-----" if removed and i in removed else f"{pct}%"
        print(f"  {labels[i]}. {txt}")

def do_phone(qobj, removed):
    correct = qobj["correct"]
    # Simulated friend who is somewhat likely to know
    knows = random.random() < 0.7  # 70% chance friend suggests correct
    labels = ['A','B','C','D']
    if knows:
        suggestion = correct
    else:
        # suggest a random non-removed wrong
        possibles = [i for i in range(4) if i != correct and (not removed or i not in removed)]
        suggestion = random.choice(possibles) if possibles else correct
    print("\nPhone-a-Friend: (friend thinking...)")
    time.sleep(1.2)
    print(f"Friend: Mera suggestion {labels[suggestion]}. ho sakta hai main sahi hoon.")
    return

def play_game():
    show_intro()
    q_indices = list(range(len(QUESTIONS)))
    # keep original order or shuffle? KBC typically fixed increasing difficulty.
    # We'll use QUESTIONS order (already mixed), but you can randomize:
    # random.shuffle(q_indices)
    guaranteed_prize_index = -1  # last safe level (not used strictly)
    for i, qidx in enumerate(q_indices):
        if i >= len(PRIZES):
            break
        qobj = QUESTIONS[qidx]
        result_type, value = ask_question(qobj, i)
        if result_type == 'quit':
            slow_print(f"\nAap ne quit kiya. Aapne jit liya: {PRIZES[i-1] if i>0 else '₹0'}", 0.02)
            return
        else:
            selected = value
            if selected == qobj["correct"]:
                slow_print("Sahi jawaab! 🎉", 0.01)
                slow_print(f"Aap jeet gaye: {PRIZES[i]}\n", 0.01)
                # If last question answered
                if i == len(PRIZES)-1 or i == len(QUESTIONS)-1:
                    slow_print("Badhai ho! Aap champion ho. 🏆", 0.01)
                    return
                continue
            else:
                slow_print("Galat jawaab. 😔", 0.01)
                slow_print(f"Aapne jeeta: {PRIZES[max(0, i-1)] if i>0 else '₹0'}", 0.01)
                return
    slow_print("Game khatam. Thanks for playing!")

if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\nExiting... bye!")
        sys.exit(0)
