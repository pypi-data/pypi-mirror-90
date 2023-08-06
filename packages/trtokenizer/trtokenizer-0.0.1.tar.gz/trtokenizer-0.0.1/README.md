# TrTokenizer 🇹🇷

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

TrTokenizer is a complete solution for Turkish sentence and word tokenization with extensively-covering language
conventions.

If you think that Natural language models always need robust, fast and accurate tokenizers, be sure that you are at the
right place now.

Sentence tokenization approach uses non-prefix keyword given in 'tr_non_suffixes file'. This file can be expanded if
required, for developer convenience lines start with # symbol are evaluated comments.

Designed regular expression are pre-compiled to speed-up performance.


### Basic Usage

```sh
from TrTokenizer import SentenceTokenize, WordTokenize

sentence_tokenizer_object = SentenceTokenize()  # during object creation regexes are compiled only at once

sentence_tokenizer_object.tokenize(<given paragraph as string>)

word_tokenizer_object = WentenceTokenize()  # # during object creation regexes are compiled only at once

word_tokenizer_object.tokenize(<given sentence as string>)

```

### TODO

- Usage examples
- Limitations
- Prepare a simple guide for contribution
- Cython C-API for performance
- Release platform specific shared dynamic libraries 
 
