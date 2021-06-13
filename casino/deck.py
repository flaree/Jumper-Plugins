import random
from collections import deque
from itertools import product, chain
import discord


class Deck:
    """Creates a Deck of playing cards."""

    suites = (":clubs:", ":diamonds:", ":hearts:", ":spades:")
    face_cards = ("King", "Queen", "Jack", "Ace")
    bj_vals = {"Jack": 10, "Queen": 10, "King": 10, "Ace": 1}
    war_values = {"Jack": 11, "Queen": 12, "King": 13, "Ace": 14}

    def __init__(self):
        self._deck = deque()

    def __len__(self):
        return len(self._deck)

    def __str__(self):
        return "Standard deck of cards with {} cards remaining.".format(len(self._deck))

    def __repr__(self):
        return "Deck{!r}".format(self._deck)

    @property
    def deck(self):
        if len(self._deck) < 1:
            self.new()
        return self._deck

    def shuffle(self):
        random.shuffle(self._deck)

    def war_count(self, card):
        try:
            return self.war_values[card[1]]
        except KeyError:
            return card[1]

    def bj_count(self, hand: list, hole=False):
        hand = self._hand_type(hand)
        if hole:
            card = hand[0][1]
            count = self.bj_vals[card] if isinstance(card, str) else card
            return count if count > 1 else 11

        count = sum([self.bj_vals[y] if isinstance(y, str) else y for x, y in hand])
        if any("Ace" in pair for pair in hand) and count <= 11:
            count += 10
        return count

    @staticmethod
    def fmt_hand(hand: list, ctx):
        #print(["{} {}, {}".format(y, discord.utils.get(ctx.bot.emojis, id=int(x)), x) for x, y in hand])
        return ["{} {}".format(y, discord.utils.get(ctx.bot.emojis, id=int(x))) for x, y in hand]

    @staticmethod
    def fmt_card(card, ctx):
        #print(discord.utils.get(ctx.bot.emojis, id=int(card[0])), card[0])
        return "{} {}".format(card[1], discord.utils.get(ctx.bot.emojis, id=int(card[0])))

    @staticmethod
    def hand_check(hand: list, card):
        return any(x[1] == card for x in hand)

    def split(self, position: int):
        self._deck.rotate(-position)

    @staticmethod
    def _true_hand(hand: list):
        return [x.split(" ") for x in hand]

    def draw(self, top=True):
        self._check()

        if top:
            card = self._deck.popleft()
        else:
            card = self._deck.pop()
        return card

    def _check(self, num=1):
        if num > 52:
            raise ValueError("Can not exceed deck limit.")
        if len(self._deck) < num:
            self.new()

    def _hand_type(self, hand: list):
        if isinstance(hand[0], tuple):
            return hand

        try:
            return self._true_hand(hand)
        except ValueError:
            raise ValueError("Invalid hand input.")

    def deal(self, num=1, top=True, hand=None):
        self._check(num=num)

        if hand is None:
            hand = []
        for x in range(0, num):
            if top:
                hand.append(self._deck.popleft())
            else:
                hand.append(self._deck.pop())

        return hand

    def burn(self, num):
        self._check(num=num)
        for x in range(0, num):
            del self._deck[0]

    def new(self):
        #cards = [(536507846830063638, 4), (536507847131791360, 3), (536507847224197120, 2), (536507847224197150, 3), (536507847228522496, 3), (536507847291174923, 5), (536507847320666112, 5), (536507847333380096, 5), (536507847337443358, 2), (536507847341768714, 4), (536507847429718026, 5), (536507847433912320, 2), (536507847496695808, 4), (536507847521861642, 2), (536507847559610368, 4), (536507847559872552, 3), (536507847626719233, 6), (536507848537145346, 8), (536507848646066187, 7), (536507848658649089, 10), (536507848717500445, 6), (536507848759312396, 9), (536507848817901589, 7), (536507848826552320, 8), (536507848834940938, 7), (536507848977416202, 9), (536507848981610496, 6), (536507849052913684, 9), (536507849061302272, 6), (536507849128542208, 10), (536507849212428290, 8), (536507849229074432, 9), (536507849828859929, 8), (536507850055483392, 7), (536507850273587201, 'Ace'), (536507850474651649, 'Ace'), (536507850483040256, 10), (536507850500079618, 'Jack'), (536507850516725771, 'King'), (536507850562732040, 'Ace'), (536507850663657482, 'Jack'), (536507850688692224, 'Queen'), (536507850709532672, 'Queen'), (536507850709794836, 'Ace'), (536507850722115584, 'Queen'), (536507850747281428, 'King'), (536507850747412481, 'Queen'), (536507850810327050, 'Jack'), (536507850814652416, 'King'), (657046607195275265, 'Jack'), (657046607203663874, 10), (657046607321104445, 'King')]
        cards = product(self.suites, chain(range(2, 11), ("King", "Queen", "Jack", "Ace")))
        #print(cards)
        self._deck = deque(cards)
        self.shuffle()
