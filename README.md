# even_better_profanity

*Blazingly fast cleaning swear words (and their leetspeak) in strings*

Hi! This is a fork of [@snguyenthanh](https://github.com/snguyenthanh)'s [better_profanity](https://github.com/snguyenthanh/better_profanity) library. I just started this recently, but I wanted to catch some additional edge cases not found in the original filter:

```
"fuck
fuckk
```

This fork is an attempt to fix that, even to the extent of going overboard and censoring too much. For example, `Assignment` and `Classic` will be censored to `****ignment` and `Cl****ic`.

Given how the censor catches too many words (*and that it is slower and uses more memory than the original library*), I didn't end up implementing this filter myself, rather relying on the original filter; however, I figured some other people might want to use this, so I hope this is helpful!

To the extent possible, I want to build on and use better_profanity's interface so that the matching versions of these two libraries are interchangeable. I may change this in the future, but my plan for now is to make the two libraries have the same functions. For example, if you use v0.7.0 of better_profanity, you should be able to substitute in subjectively_better_profanity and your program should work the same.

Inspired from package [better_profanity](https://github.com/snguyenthanh/better_profanity) by [@snguyenthanh](https://github.com/snguyenthanh), which was in turn inspired by [profanity](https://github.com/ben174/profanity) of [Ben Friedland](https://github.com/ben174). This library is slower and more memory-intensive than `better_profanity`.

This utilizes Aho-Corasick algorithm (as implemented in the [pyahocorasick](https://github.com/WojciechMula/pyahocorasick) library by [WojciechMula](https://github.com/WojciechMula)).

It supports [modified spellings](https://en.wikipedia.org/wiki/Leet) (such as `p0rn`, `h4NDjob`, `handj0b` and `b*tCh`).

## Requirements

This package works with `Python 3.5+` and `PyPy3`. Run `pip install -r requirements.txt`

## Installation

```sh
pip3 install better_profanity
```

## Unicode characters

Only Unicode characters from categories `Ll`, `Lu`, `Mc` and `Mn` are added. More on Unicode categories can be found [here][unicode category link].

[unicode category link]: https://en.wikipedia.org/wiki/Template:General_Category_(Unicode)

Not all languages are supported yet, such as *Chinese*.

## Usage

```python
from subjectively_better_profanity import profanity

if __name__ == "__main__":
    profanity.load_censor_words()

    text = "You p1ec3 of sHit."
    censored_text = profanity.censor(text)
    print(censored_text)
    # You **** of ****.
```

All modified spellings of words in [profanity_wordlist.txt](./subjectively_better_profanity/profanity_wordlist.txt) will be generated. For example, the word `handjob` would be loaded into:

```python
'handjob', 'handj*b', 'handj0b', 'handj@b', 'h@ndjob', 'h@ndj*b', 'h@ndj0b', 'h@ndj@b',
'h*ndjob', 'h*ndj*b', 'h*ndj0b', 'h*ndj@b', 'h4ndjob', 'h4ndj*b', 'h4ndj0b', 'h4ndj@b'
```

The full mapping of the library can be found in [profanity.py](./subjectively_better_profanity/better_profanity.py).

### 1. Censor swear words from a text

By default, `profanity` replaces each swear words with 4 asterisks `****`.

```python
from subjectively_better_profanity import profanity

if __name__ == "__main__":
    text = "You p1ec3 of sHit."

    censored_text = profanity.censor(text)
    print(censored_text)
    # You **** of ****.
```

### 2. Censor doesn't care about word dividers

The function `.censor()` also hide words separated not just by an empty space ` ` but also other dividers, such as `_`, `,` and `.`. Except for `@, $, *, ", '`.

```python
from better_profanity import profanity

if __name__ == "__main__":
    text = "...sh1t...hello_cat_fuck,,,,123"

    censored_text = profanity.censor(text)
    print(censored_text)
    # "...****...hello_cat_****,,,,123"
```

### 3. Censor swear words with custom character

4 instances of the character in second parameter in `.censor()` will be used to replace the swear words.

```python
from subjectively_better_profanity import profanity

if __name__ == "__main__":
    text = "You p1ec3 of sHit."

    censored_text = profanity.censor(text, '-')
    print(censored_text)
    # You ---- of ----.
```

### 4. Check if the string contains any swear words

Function `.contains_profanity()` return `True` if any words in the given string has a word existing in the wordlist.

```python
from subjectively_better_profanity import profanity

if __name__ == "__main__":
    dirty_text = "That l3sbi4n did a very good H4ndjob."

    profanity.contains_profanity(dirty_text)
    # True
```

### 5. Censor swear words with a custom wordlist

#### 5.1. Wordlist as a `List`

Function `load_censor_words` takes a `List` of strings as censored words.
The provided list will replace the default wordlist.

```python
from subjectively_better_profanity import profanity

if __name__ == "__main__":
    custom_badwords = ['happy', 'jolly', 'merry']
    profanity.load_censor_words(custom_badwords)

    print(profanity.contains_profanity("Have a merry day! :)"))
    # Have a **** day! :)
```

#### 5.2. Wordlist as a file

Function `load_censor_words_from_file` takes a filename, which is a text file and each word is separated by lines.

```python
from subjectively_better_profanity import profanity

if __name__ == "__main__":
    profanity.load_censor_words_from_file('/path/to/my/project/my_wordlist.txt')
```

### 6. Whitelist

Function `load_censor_words` and `load_censor_words_from_file` takes a keyword argument `whitelist_words` to ignore words in a wordlist.

It is best used when there are only a few words that you would like to ignore in the wordlist.

```python
# Use the default wordlist
profanity.load_censor_words(whitelist_words=['happy', 'merry'])

# or with your custom words as a List
custom_badwords = ['happy', 'jolly', 'merry']
profanity.load_censor_words(custom_badwords, whitelist_words=['merry'])

# or with your custom words as a text file
profanity.load_censor_words_from_file('/path/to/my/project/my_wordlist.txt', whitelist_words=['merry'])
```

### 7. Add more censor words

```python
from subjectively_better_profanity import profanity

if __name__ == "__main__":
    custom_badwords = ['happy', 'jolly', 'merry']
    profanity.add_censor_words(custom_badwords)

    print(profanity.contains_profanity("Happy you, fuck!"))
    # **** you, ****!
```

## Improvements

### 1. Due to a change in the algorithm, words with non-space separators are now supported (fixing [this issue](https://github.com/snguyenthanh/better_profanity/issues/5))


## Limitations

### 1. The library no longer compares each word by characters, so it will be more likely to catch profanity:

```python
profanity.censor('I just have sexx')
# returns 'I just have ****x'

profanity.censor('jerkk off')
# returns '****k off'
```

However, it comes at the cost of being oversensitive:
```python
profanity.censor('classic assignment')
# returns cl****ic ***ignment'
```

### 2. The library is slower and requires more memory

## Testing

```sh
python3 tests.py
```

## Contributing

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Special thanks to

- [Andrew Grinevich](https://github.com/Derfirm) - Add support for Unicode characters.
- [Jaclyn Brockschmidt](https://github.com/jcbrockschmidt) - Optimize string comparison.

## Acknowledgments

- [Son Nguyen](https://github.com/snguyenthanh) - For the inspiring package (from which much of this code is copied from) [better_profanity](https://github.com/snguyenthanh/better_profanity)
- [Wojciech Mula](https://github.com/WojciechMula) for the [pyahocorasick](https://github.com/WojciechMula/pyahocorasick) library
- [Ben Friedland](https://github.com/ben174) - For the original inspiring package [profanity](https://github.com/ben174/profanity).
