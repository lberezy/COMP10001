test_cases = {"kinda_fermat":
                  [('submission.kinda_fermat(1,2,3)',False),
                   ('submission.kinda_fermat(3,4,5)',2),
                   ('submission.kinda_fermat(4,3,5)',2),
                   ('submission.kinda_fermat(5,12,13)',2)], # 4 of your own tests, none provided
              "unique_long_words":
                  [('submission.unique_long_words("The quick brown fox jumps over the lazy dog.",3)',8),
                   ('submission.unique_long_words("How much wood could a wood chuck chuck.",2)',5),
                   ('submission.unique_long_words("""Punctuation... Test ... ? 12 3""",2)',3)],
              "symmetric_words":
                  [('submission.symmetric_words("boy dog bevy bully")',["bevy","boy"]),
                   ('submission.symmetric_words("Neither a borrower nor a lender be;")',['a']),
                   ('submission.symmetric_words("That\'s a double two-em-dashed lie, you etaoin shrdlu so-and-so!")',['a'])],
              
              
              "least_vowel_words":
                  [('submission.least_vowel_words("the rhythm of life")',["rhythm"]),
                   ('submission.least_vowel_words("The quality of mercy is not strain\'d ... Percy.")',["mercy","percy"])],
              }