test_cases = {"kinda_fermat":
                  [('submission.kinda_fermat(1,1,1)',False),  # to get the ball rolling
                   ('submission.kinda_fermat(3,4,5)',2),      # first pythagorean triple
                   ('submission.kinda_fermat(4,3,5)',2),      # ...and some permutations
                   ('submission.kinda_fermat(4,5,3)',False),  #
                   ('submission.kinda_fermat(-3,-4,5)',2),    # negatives should work
                   ('submission.kinda_fermat(5,12,13)',2),    # and so should another pythagorean triple
                   ('submission.kinda_fermat(0,0,0)',2)],     # also the trivial case
              
              
              "unique_long_words":
                  [('submission.unique_long_words("The quick onyx goblin jumps over the lazy dwarf..",3)',8),
                   ('submission.unique_long_words("Monsieur Jack, vous dactylographiez bien mieux que votre ami Wolf",5)',4),
                   ('submission.unique_long_words("... ... ...",1)',0), # test punc->nullstring stripping
                   ('submission.unique_long_words("""Punctuation... Test ... ? 12 3""",2)',3)],         # test punctuation
              
              
              "symmetric_words":
              # numbers (12345...) not tested as apparently we can assume they won't be in the test data
                  [('submission.symmetric_words("cat boy bevy hello by a cox")',["a","bevy","boy","by", "cox"]), # I couldn't find many other symmetric words
                   ('submission.symmetric_words("60 cats and 70 dogs and I am a fish, oh my!")',['a', 'i']),
                   ('submission.symmetric_words("zyxcba abcxyz xyzabc cbazyx lmno a\'")',['a', 'abcxyz', 'cbazyx', 'lmno', 'xyzabc', 'zyxcba']),
                   ('submission.symmetric_words("That\'s a double two-em-dashed lie, you etaoin shrdlu so-and-so!")',['a'])],

             
              "least_vowel_words":
                  [('submission.least_vowel_words("Eighty Megs And Constantly Swapping?")',["constantly"]),
                   ('submission.least_vowel_words("qwerty dvorak colemak workman")',["qwerty"]),
                   ('submission.least_vowel_words("GNU - A new fragrance by RMS")',['by', 'rms']),
                   ('submission.least_vowel_words("")',[]), # test empty string
                   ('submission.least_vowel_words(",.:;!?- word,.:;!?-")',["word"]), # punctuation test
                   ('submission.least_vowel_words("The quality of mercy is not strain\'d ... Percy.")',["mercy","percy"])], # just testing 
              }