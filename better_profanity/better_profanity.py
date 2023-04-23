# -*- coding: utf-8 -*-

from collections.abc import Iterable
import ahocorasick

from .constants import ALLOWED_CHARACTERS
from .utils import (
    any_next_words_form_swear_word,
    get_complete_path_of_file,
    get_replacement_for_swear_word,
    read_wordlist,
)
from .varying_string import VaryingString


class Profanity:
    def __init__(self, words=None):
        """
        Args:
            words (Iterable/str): Collection of words or file path for a list of
                words to censor. `None` to use the default word list.

        Raises:
            TypeError: If `words` is not a valid type.
            FileNotFoundError: If `words` is a `str` and is not a valid file path.
        """
        self.automaton = ahocorasick.Automaton(ahocorasick.STORE_INTS)

        if (
            words is not None
            and not isinstance(words, str)
            and not isinstance(words, Iterable)
        ):
            raise TypeError("words must be of type str, list, or None")
        self.CENSOR_WORDSET = []
        self.CHARS_MAPPING = {
            "a": ("a", "@", "*", "4"),
            "i": ("i", "*", "l", "1"),
            "o": ("o", "*", "0", "@"),
            "u": ("u", "*", "v"),
            "v": ("v", "*", "u"),
            "l": ("l", "1"),
            "e": ("e", "*", "3"),
            "s": ("s", "$", "5"),
            "t": ("t", "7"),
        }
        self.MAX_NUMBER_COMBINATIONS = 1
        self.ALLOWED_CHARACTERS = ALLOWED_CHARACTERS
        self._default_wordlist_filename = get_complete_path_of_file(
            "profanity_wordlist.txt"
        )
        if type(words) == str:
            self.load_censor_words_from_file(words)
        else:
            self.load_censor_words(custom_words=words)

    ## PUBLIC ##

    def censor(self, text: str, censor_char="*"):
        """Replace the swear words in the text with `censor_char`."""
        
        for end_index, value in self.automaton.iter(text.lower()):
            start_index = end_index - len(value) + 1
            
            text = text[:start_index] + get_replacement_for_swear_word(censor_char) + text[end_index + 1:]
            
        return text

    def load_censor_words_from_file(self, filename, **kwargs):
        words = read_wordlist(filename)
        self._populate_words_to_wordset(words, **kwargs)

    def load_censor_words(self, custom_words=None, **kwargs):
        """Generate a set of words that need to be censored."""
        # Replace the words from `profanity_wordlist.txt` with a custom list
        custom_words = custom_words or read_wordlist(self._default_wordlist_filename)
        self._populate_words_to_wordset(custom_words, **kwargs)

    def add_censor_words(self, custom_words):
        if not isinstance(custom_words, (list, tuple, set)):
            raise TypeError(
                "Function 'add_censor_words' only accepts list, tuple or set."
            )
        for w in custom_words:
            self.CENSOR_WORDSET.append(VaryingString(w, char_map=self.CHARS_MAPPING))

    def contains_profanity(self, text):
        """Return True if  the input text has any swear words."""
        
        return len(tuple(self.automaton.iter(text.lower()))) != 0

    ## PRIVATE ##

    def _populate_words_to_wordset(self, words, *, whitelist_words=None):
        if whitelist_words is not None and not isinstance(
            whitelist_words, (list, set, tuple)
        ):
            raise TypeError(
                "The 'whitelist_words' keyword argument only accepts list, tuple or set."
            )

        # Validation
        whitelist_words = whitelist_words or []
        for index, word in enumerate(whitelist_words):
            if not isinstance(word, str):
                raise ValueError(
                    "Each word in 'whitelist_words' must be 'str' type, "
                    "but '{word}' found.".format(word=type(word))
                )
            whitelist_words[index] = word.lower()

        # Populate the words into an internal wordset
        whitelist_words = set(whitelist_words)
        all_censor_words = []
        for word in set(words):
            # All words in CENSOR_WORDSET must be in lowercase
            word = word.lower()

            if word in whitelist_words:
                continue

            num_of_non_allowed_chars = self._count_non_allowed_characters(word)
            if num_of_non_allowed_chars > self.MAX_NUMBER_COMBINATIONS:
                self.MAX_NUMBER_COMBINATIONS = num_of_non_allowed_chars

            all_censor_words.append(VaryingString(word, char_map=self.CHARS_MAPPING))

        # The default wordlist takes ~5MB+ of memory
        self.CENSOR_WORDSET = all_censor_words
        
        self._create_character_map()

    def _count_non_allowed_characters(self, word):
        count = 0
        for char in iter(word):
            if char not in self.ALLOWED_CHARACTERS:
                count += 1
        return count


    def _create_character_map(self) -> None:
        new_automaton = ahocorasick.Automaton()

        for varying_word in self.CENSOR_WORDSET:
            for word in varying_word.get_all_combos():
                new_automaton.add_word(word, word)
            
        new_automaton.make_automaton()
        
        self.automaton = new_automaton
    
    