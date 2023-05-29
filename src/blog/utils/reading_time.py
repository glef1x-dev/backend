import math
from typing import Callable, cast, List, Tuple, TypedDict


class WordCountStats(TypedDict):
    total: int


class ReadingTimeStats(TypedDict):
    time: int
    minutes: int


class ReadingTimeResult(ReadingTimeStats):
    words: WordCountStats


def is_ansi_word_bound(c: str) -> bool:
    return c in " \n\r\t"


def reading_time(
    text: str,
    words_per_minute: int = 200,
    word_bound: Callable[[str], bool] = is_ansi_word_bound,
) -> ReadingTimeResult:
    words = count_words(text, word_bound)
    return cast(
        ReadingTimeResult,
        {**reading_time_with_count(words, words_per_minute), "words": words},
    )


def count_words(text: str, is_word_bound: Callable[[str], bool]) -> WordCountStats:
    words = 0
    start = 0
    end = len(text) - 1

    # fetch bounds
    while is_word_bound(text[start]):
        start += 1
    while is_word_bound(text[end]):
        end -= 1

    # Add a trailing word bound to make handling edges more convenient
    normalized_text = f"{text}\n"

    # calculate the number of words
    i = start
    while i <= end:
        # A CJK character is a always word;
        # A non-word bound followed by a word bound / CJK is the end of a word.
        if is_cjk(normalized_text[i]) or (
            not is_word_bound(normalized_text[i])
            and (
                is_word_bound(normalized_text[i + 1]) or is_cjk(normalized_text[i + 1])
            )
        ):
            words += 1
        # In case of CJK followed by punctuations, those characters have to be eaten as well
        if is_cjk(normalized_text[i]):
            while i <= end and (
                is_punctuation(normalized_text[i + 1])
                or is_word_bound(normalized_text[i + 1])
            ):
                i += 1
        i += 1
    return {"total": words}


def reading_time_with_count(
    words: WordCountStats, words_per_minute: int
) -> ReadingTimeStats:
    # reading time stats
    minutes = words["total"] / words_per_minute
    # round used to resolve floating point funkiness
    #   http://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html
    time = round(minutes * 60 * 1000)
    displayed = math.ceil(int(minutes * 100 + 0.5) / 100)

    return {"minutes": displayed, "time": time}


def code_is_in_ranges(number: int, array_of_ranges: List[Tuple[int, int]]) -> bool:
    return any(
        lowerBound <= number <= upperBound for lowerBound, upperBound in array_of_ranges
    )


def is_cjk(c: str) -> bool:
    char_code = ord(c)
    # Help wanted!
    # This should be good for most cases, but if you find it unsatisfactory
    # (e.g. some other language where each character should be standalone words),
    # contributions welcome!
    return code_is_in_ranges(
        char_code,
        [
            # Hiragana (Katakana not included on purpose,
            # context: https://github.com/ngryman/reading-time/pull/35#issuecomment-853364526)
            # If you think Katakana should be included and have solid reasons, improvement is welcomed
            (0x3040, 0x309F),
            # CJK Unified ideographs
            (0x4E00, 0x9FFF),
            # Hangul
            (0xAC00, 0xD7A3),
            # CJK extensions
            (0x20000, 0x2EBE0),
        ],
    )


def is_punctuation(c: str) -> bool:
    char_code = ord(c)
    return code_is_in_ranges(
        char_code,
        [
            (0x21, 0x2F),
            (0x3A, 0x40),
            (0x5B, 0x60),
            (0x7B, 0x7E),
            # CJK Symbols and Punctuation
            (0x3000, 0x303F),
            # Full-width ASCII punctuation variants
            (0xFF00, 0xFFEF),
        ],
    )
