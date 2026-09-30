# Small Trading Card Game (TCG)
## Files Created

1. **cards.txt** - Contains 15 cards with the following attributes:
   - Name
   - Attack (numeric value)
   - Defense (numeric value)
   - Element (Fire, Water, Earth, Air, Light, Dark, Nature, Ice, Thunder, Shadow, Holy, Poison, Crystal, Wind, Stone)
   - Rarity (Common, Uncommon, Rare, Epic, Legendary)
   - Description

2. **tcg_game.py** - Interactive Python game with these features:
   - Loads cards from cards.txt
   - Presents 5 random cards to the user
   - User chooses 1 card to swap out (gets replaced with new random card)
   - Continues until user quits with 'q'
   - Displays hand power (total attack + defense)
   - Tracks rounds and total swaps
   - Shows final hand with rarity indicators
   - Proper parsing of card attributes

## How to Play
Run the game with: `python tcg_game.py`

Gameplay:
- You're dealt 5 random cards
- Choose which card to swap (1-5)
- That card gets replaced with a new random card from the deck
- Continue swapping to build a stronger hand
- Quit anytime by entering 'q'
- See your final hand and statistics

The game follows your specifications:
- 10-20 cards saved in a txt file (15 cards)
- User presented with 5 random cards
- User chooses 1 that gets replaced by a new one
- Interactive terminal-based gameplay