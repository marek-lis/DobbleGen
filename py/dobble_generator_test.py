import pytest
from dobble_generator import Dobble_Generator

symbols_per_card = 4

prime = symbols_per_card - 1

total_number_of_cards = prime ** 2 + prime + 1


def test_Dobble_Generator_creation():
    dg = Dobble_Generator(symbols_per_card, False)
    assert dg != None


def test_Dobble_Generator_number_of_generated_cards():
    dg = Dobble_Generator(symbols_per_card, False)
    cards = dg.generate_cards()
    assert cards != None
    assert len(cards) == total_number_of_cards


def test_Dobble_Generator_simple_cards_consistiency():
    dg = Dobble_Generator(symbols_per_card, False)
    cards = dg.generate_cards()
    assert cards != None
    i = 1
    length = len(cards)
    assert length == total_number_of_cards
    while i < length:
        c1 = set(cards[i-1])
        # check number of symbols on the first card
        assert len(c1) == symbols_per_card
        c2 = set(cards[i])
        # check number of symbols on the second card
        assert len(c2) == symbols_per_card
        # make sure there is only 1 common symbol per card
        assert len(c1 & c2) == 1
        i += 1


def test_Dobble_Generator_advanced_cards_consistiency():
    dg = Dobble_Generator(symbols_per_card, False)
    cards = dg.generate_cards()
    assert cards != None
    i = 1
    length = len(cards)
    assert length == total_number_of_cards
    while i < length:
        c1 = set(cards[i])
        # check number of symbols on the first card
        assert len(c1) == symbols_per_card
        j = 0
        # check all previous up to current
        while j < i:
            c2 = set(cards[j])
            # make sure there is only 1 common symbol per card
            assert len(c1 & c2) == 1
            j += 1
        # check all cards after current
        j = i + 1
        while j < length:
            c2 = set(cards[j])
            # make sure there is only 1 common symbol per card
            assert len(c1 & c2) == 1
            j += 1
        i += 1
