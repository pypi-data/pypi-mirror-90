import json
import logging
import re
from functools import partial
from pathlib import Path

import requests
from symspellpy import SymSpell, Verbosity, editdistance

from mtgscan.box_text import BoxTextList
from mtgscan.deck import Deck, Pile


def load_json(url):
    print(f"Loading {url}")
    r = requests.get(url)
    return r.json()


class MagicRecognition:

    def __init__(self, file_all_cards, file_keywords, max_ratio_diff=0.3, max_ratio_diff_keyword=0.2) -> None:
        """Load cards and keywords in memory

        Parameters
        ----------
        max_ratio_diff : float, optional
            Maximum ratio (distance/length) for a text to be considered as a card name, by default 0.3
        max_ratio_diff_keyword : float, optional
            Maximum ratio (distance/length) for a text to be considered as a (ignored) keyword, by default 0.2
        """
        self.max_ratio_diff = max_ratio_diff
        self.max_ratio_diff_keyword = max_ratio_diff_keyword

        assert Path(file_all_cards).is_file()

        self.sym_all_cards = SymSpell(max_dictionary_edit_distance=6)
        self.sym_all_cards._distance_algorithm = editdistance.DistanceAlgorithm.LEVENSHTEIN
        self.sym_all_cards.load_dictionary(file_all_cards, 0, 1, separator="$")
        self.all_cards = self.sym_all_cards._words
        print(f"Loaded {file_all_cards}: {len(self.all_cards)} cards")
        self.edit_dist = editdistance.EditDistance(
            editdistance.DistanceAlgorithm.LEVENSHTEIN)

        assert Path(file_keywords).is_file()

        def concat_lists(LL):
            res = []
            for L in LL:
                res.extend(L)
            return res
        keywords_json = json.load(file_keywords.open())
        keywords = concat_lists(keywords_json["data"].values())
        keywords.extend(["Display", "Land", "Search", "Profile"])
        self.sym_keywords = SymSpell(max_dictionary_edit_distance=3)
        for k in keywords:
            self.sym_keywords.create_dictionary_entry(k, 1)

    def preprocess(self, text: str) -> str:
        """Remove characters which can't appear on a Magic card (OCR error)"""
        return re.sub("[^a-zA-Z',. ]", '', text).rstrip(' ')

    def preprocess_texts(self, box_texts: BoxTextList) -> None:
        """Apply `preprocess` on each text"""
        for box_text in box_texts:
            box_text.text = self.preprocess(box_text.text)

    def box_texts_to_cards(self, box_texts: BoxTextList) -> BoxTextList:
        """Recognize cards from raw texts"""
        box_texts.sort()
        box_cards = BoxTextList()
        for box, text, _ in box_texts:
            sug = self.sym_keywords.lookup(text, Verbosity.CLOSEST,
                                           max_edit_distance=min(3, int(self.max_ratio_diff_keyword*len(text))))
            if sug != []:
                logging.info(f"Keyword rejected: {text} {sug[0].distance/len(text)} {sug[0].term}")
            else:
                card = self.search(self.preprocess(text))
                if card is not None:
                    box_cards.add(box, card)
        return box_cards

    def assign_stacked(self, box_texts: BoxTextList, box_cards: BoxTextList) -> None:
        """Set multipliers (e.g. x4) for each (stacked) card in `box_cards`

        Parameters
        ----------
        box_texts : BoxTextList
            BoxTextList containing potential multipliers
        box_cards : BoxTextList
            BoxTextList containing recognized cards
        """
        def assign_stacked_one(box_cards: BoxTextList, m: int, comp) -> None:
            i_min = 0
            for i, box_card in enumerate(box_cards):
                if comp(box_card.box, box_cards[i_min].box):
                    i_min = i
            box_cards[i_min].n = m
            logging.info(f"{box_cards[i_min].text} assigned to x{m}")

        def dist(p: tuple, q: tuple) -> float:
            return (p[0] - q[0])**2 + (p[1] - q[1])**2

        def comp_md(box1: tuple, box2: tuple, box: tuple) -> float:
            if box1[0] > box[0] or box1[1] > box[1]:
                return False
            return dist(box, box1) < dist(box, box2)

        def comp_sb(box1: tuple, box2: tuple, box: tuple) -> float:
            return dist(box, box1) < dist(box, box2)

        comp = (comp_md, comp_sb)
        for box, text, _ in box_texts:
            if len(text) == 2:
                for i in [0, 1]:
                    if text[i] in '×xX' and text[1 - i].isnumeric():
                        assign_stacked_one(box_cards, int(
                            text[1 - i]), partial(comp[i], box=box))

    def box_cards_to_deck(self, box_cards: BoxTextList) -> Deck:
        """Convert recognized cards to decklist"""
        maindeck, sideboard = Pile(), Pile()
        n_cards = sum(c.n for c in box_cards)
        n_added = 0
        last_main_card = max(60, n_cards - 15)
        for _, card, n in box_cards:
            def add_cards(c, deck, p):
                if c in deck.cards:
                    deck.cards[c] += p
                elif p > 0:
                    deck.cards[c] = p
            n_added_main = max(min(n, last_main_card - n_added), 0)
            add_cards(card, maindeck, n_added_main)
            add_cards(card, sideboard, n - n_added_main)
            n_added += n
        deck = Deck()
        deck.maindeck = maindeck
        deck.sideboard = sideboard
        return deck

    def box_texts_to_deck(self, box_texts: BoxTextList) -> Deck:
        """Convert raw texts to decklist

        Parameters
        ----------
        box_texts : BoxTextList
            Raw texts given by an OCR

        Returns
        -------
        Deck
            Decklist obtained from `box_texts`
        """
        box_cards = self.box_texts_to_cards(box_texts)
        self.assign_stacked(box_texts, box_cards)
        return self.box_cards_to_deck(box_cards)

    def search(self, text):
        """If `text` can be recognized as a Magic card, return that card. Otherwise, return None."""
        if len(text) < 3:  # a card name is never that short
            return None
        if len(text) > 30:  # a card name is never that long
            logging.info(f"Too long: {text}")
            return None
        if text in self.all_cards:
            return text
        i = text.find("..")  # search for truncated card name
        if i != -1:
            dist = int(self.max_ratio_diff * i)
            card = None
            for c in self.all_cards:
                d = self.edit_dist.compare(text[:i], c[:i], dist)
                if d != -1 and d < dist:
                    card = c
                    dist = d
            if card is None:
                logging.info(f"Not prefix: {text}")
            else:
                logging.info(f"Found prefix: {text} {dist/i} {card}")
                return card
        else:
            text = text.replace('.', '').rstrip(' ')
            sug = self.sym_all_cards.lookup(text, Verbosity.CLOSEST,
                                            max_edit_distance=min(6, int(self.max_ratio_diff * len(text))))
            if sug != []:
                card = sug[0].term
                ratio = sug[0].distance/len(text)
                if len(text) < len(card) + 7:
                    logging.info(f"Corrected: {text} {ratio} {card}")
                    return card
                logging.info(f"Not corrected (too long): {text} {ratio} {card}")
            else:
                logging.info(f"Not found: {text}")
        return None
