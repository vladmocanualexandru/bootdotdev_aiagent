#!/usr/bin/env python3
"""Small TCG Game - Pick & Replace"""

import random
import os

def load_cards(filename="cards.txt"):
    """Load cards from txt file. Format: Name,Attack:X,Defense:X,Element:X,Rarity:X,Description"""
    cards = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            # Format: Name,Attack:X,Defense:X,Element:Y,Rarity:Z,Description
            name = parts[0]
            attack = int(parts[1].split(":")[1])
            defense = int(parts[2].split(":")[1])
            element = parts[3].split(":")[1]
            rarity = parts[4].split(":")[1]
            description = parts[5] if len(parts) > 5 else ""
            cards.append({
                "name": name,
                "attack": attack,
                "defense": defense,
                "element": element,
                "rarity": rarity,
                "description": description
            })
    return cards

def display_hand(hand, title="Your Hand"):
    """Display cards in a numbered list."""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")
    for i, card in enumerate(hand, 1):
        rarity_color = {"Common": "⭐", "Uncommon": "🌟", "Rare": "💎", "Epic": "🔮", "Legendary": "👑"}
        rarity_icon = rarity_color.get(card["rarity"], "•")
        print(f"  [{i}] {rarity_icon} {card['name']}")
        print(f"      ATK: {card['attack']}  DEF: {card['defense']}  Element: {card['element']}  ({card['rarity']})")
        print(f"      {card['description']}")
        print()

def get_valid_choice(hand_size):
    """Get valid card choice from user."""
    while True:
        try:
            choice = input(f"Pick a card to swap (1-{hand_size}) or 'q' to quit: ").strip()
            if choice.lower() == 'q':
                return None
            choice = int(choice)
            if 1 <= choice <= hand_size:
                return choice - 1  # Convert to 0-indexed
            print(f"Please enter a number between 1 and {hand_size}.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def draw_random_card(all_cards, hand):
    """Draw a random card not currently in hand."""
    available = [c for c in all_cards if c not in hand]
    if not available:
        available = all_cards  # Allow duplicates if deck exhausted
    return random.choice(available)

def calculate_score(hand):
    """Calculate total hand power."""
    return sum(card["attack"] + card["defense"] for card in hand)

def main():
    # Load cards
    if not os.path.exists("cards.txt"):
        print("Error: cards.txt not found!")
        return
    
    all_cards = load_cards()
    print(f"Loaded {len(all_cards)} cards from deck.")
    
    # Deal initial hand of 5
    hand = random.sample(all_cards, 5)
    
    round_num = 1
    total_swaps = 0
    
    print("\n" + "="*50)
    print("  WELCOME TO THE TCG PICK & REPLACE GAME")
    print("="*50)
    print("\nRules: You have 5 cards. Pick one to swap out,")
    print("it gets replaced with a new random card.")
    print("Build the strongest hand possible!")
    
    while True:
        display_hand(hand, f"Round {round_num} - Your Hand")
        
        score = calculate_score(hand)
        print(f"Current Hand Power: {score}")
        
        choice = get_valid_choice(len(hand))
        if choice is None:
            break
        
        # Show chosen card
        chosen = hand[choice]
        print(f"\n  >> You swapped: {chosen['name']} (ATK:{chosen['attack']}, DEF:{chosen['defense']})")
        
        # Replace with new random card
        new_card = draw_random_card(all_cards, hand)
        hand[choice] = new_card
        total_swaps += 1
        
        print(f"  >> New card: {new_card['name']} (ATK:{new_card['attack']}, DEF:{new_card['defense']})")
        
        round_num += 1
    
    # Game over summary
    print("\n" + "="*50)
    print("  GAME OVER")
    print(f"{'='*50}")
    print(f"Rounds played: {round_num - 1}")
    print(f"Total swaps: {total_swaps}")
    print(f"Final hand power: {calculate_score(hand)}")
    display_hand(hand, "Final Hand")
    
    # Check for rare cards
    legendaries = [c for c in hand if c["rarity"] == "Legendary"]
    epics = [c for c in hand if c["rarity"] == "Epic"]
    if legendaries:
        print(f"\n🏆 Legendaries in hand: {', '.join(c['name'] for c in legendaries)}")
    if epics:
        print(f"✨ Epics in hand: {', '.join(c['name'] for c in epics)}")
    
    print("\nThanks for playing!")

if __name__ == "__main__":
    main()