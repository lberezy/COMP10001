# Modified 9/5/13, to fix bug in test cases for 'search'
# Modified 9/5/13, to fix float issue in test case for 'search'
# Modified 9/5/13, to add test cases for word_freq_graph() and batch_evaluate()
# Modified 11/5/13, to update the final test case for make_index() to actual DF value
# Modified 11/5/13, to add a test case with a duplicate term in it
# Modified 12/5/13, to add test cases for Q1 with __TOTAL__ in them

test_cases = {"make_index":
                  [("""test_index("english.csv","tf['http://www.youtube.com/watch?v=-4wsuPCjDBc#t=5s']['chipmunk']")""",4),
                   ("""test_index("english.csv","df['chipmunk']")""",3),
                   ("""test_index("english-small1.csv","tf['http://www.youtube.com/watch?v=ZbzDGXEwtGc#t=6s']['bird']")""",1),
                   ("""test_index("english-small1.csv","df['bird']")""",2),
                   ("""test_index("english.csv","tf['http://www.youtube.com/watch?v=ZbzDGXEwtGc#t=6s']['__TOTAL__']")""",116),
                   ("""test_index("english.csv","df['__TOTAL__']")""",2026)
                 ],
              "single_word_search":
                  [("""submission.single_word_search("test-big.pkl","bird")""",['http://www.youtube.com/watch?v=cJOZp2ZftCw#t=1s', 'http://www.youtube.com/watch?v=O2qiPS2NCeY#t=2s', 'http://www.youtube.com/watch?v=mv89psg6zh4#t=33s', 'http://www.youtube.com/watch?v=2G9fkvBzzQE#t=10s', 'http://www.youtube.com/watch?v=Ce7equ9zCxk#t=4s', 'http://www.youtube.com/watch?v=uiLr9bdOL0M#t=23s', 'http://www.youtube.com/watch?v=-8rBYNP0UKM#t=194s', 'http://www.youtube.com/watch?v=jsEUFYhiqxU#t=121s', 'http://www.youtube.com/watch?v=ao-9B8IV9_E#t=87s', 'http://www.youtube.com/watch?v=ScdUht-pM6s#t=53s', 'http://www.youtube.com/watch?v=a8PAY4rvzRM#t=1s', 'http://www.youtube.com/watch?v=QsC8__3lwO0#t=50s']),
                   ("""submission.single_word_search("test-big.pkl","chipmunk")""",['http://www.youtube.com/watch?v=a1Y73sPHKxw#t=0s', 'http://www.youtube.com/watch?v=-4wsuPCjDBc#t=5s', 'http://www.youtube.com/watch?v=sqy2CMDl7U0#t=7s']),
                   ("""submission.single_word_search("test-big.pkl","gull")""",[]),
                   ("""submission.single_word_search("test-big.pkl","ship")""",['http://www.youtube.com/watch?v=wLUH7qA_6sA#t=90s', 'http://www.youtube.com/watch?v=dtn0PuxgfkM#t=0s', 'http://www.youtube.com/watch?v=xgIIcPSh4EU#t=0s', 'http://www.youtube.com/watch?v=UwlALS1AKb4#t=0s', 'http://www.youtube.com/watch?v=YmXCfQm0_CA#t=7s']),
                 ],
              "search":
                  [("""submission.search("test-big.pkl","bird")""",['http://www.youtube.com/watch?v=-8rBYNP0UKM#t=194s', 'http://www.youtube.com/watch?v=2G9fkvBzzQE#t=10s', 'http://www.youtube.com/watch?v=Ce7equ9zCxk#t=4s', 'http://www.youtube.com/watch?v=O2qiPS2NCeY#t=2s', 'http://www.youtube.com/watch?v=QsC8__3lwO0#t=50s', 'http://www.youtube.com/watch?v=ScdUht-pM6s#t=53s', 'http://www.youtube.com/watch?v=a8PAY4rvzRM#t=1s', 'http://www.youtube.com/watch?v=ao-9B8IV9_E#t=87s', 'http://www.youtube.com/watch?v=cJOZp2ZftCw#t=1s', 'http://www.youtube.com/watch?v=jsEUFYhiqxU#t=121s', 'http://www.youtube.com/watch?v=mv89psg6zh4#t=33s', 'http://www.youtube.com/watch?v=uiLr9bdOL0M#t=23s']),
                   ("""submission.search("test-big.pkl","bird tree")""",['http://www.youtube.com/watch?v=O2qiPS2NCeY#t=2s', 'http://www.youtube.com/watch?v=-8rBYNP0UKM#t=194s', 'http://www.youtube.com/watch?v=1dmVuwO1RZk#t=0s', 'http://www.youtube.com/watch?v=2G9fkvBzzQE#t=10s', 'http://www.youtube.com/watch?v=2YhDTpzxd3c#t=98s', 'http://www.youtube.com/watch?v=5E66Gk3V1Bc#t=23s', 'http://www.youtube.com/watch?v=8yuPGwxwdPs#t=1s', 'http://www.youtube.com/watch?v=BApIQn69EVE#t=10s', 'http://www.youtube.com/watch?v=Ce7equ9zCxk#t=4s', 'http://www.youtube.com/watch?v=G-M78KIy19E#t=315s', 'http://www.youtube.com/watch?v=I9gLTZY1ouc#t=142s', 'http://www.youtube.com/watch?v=L9wD3kw-8FE#t=65s', 'http://www.youtube.com/watch?v=MWvCcwTw7Ac#t=78s', 'http://www.youtube.com/watch?v=PJnJMp2ZpbA#t=3s', 'http://www.youtube.com/watch?v=QsC8__3lwO0#t=50s', 'http://www.youtube.com/watch?v=RX6NSOuCCAE#t=13s', 'http://www.youtube.com/watch?v=ScdUht-pM6s#t=53s', 'http://www.youtube.com/watch?v=SrDE9-cDz48#t=4s', 'http://www.youtube.com/watch?v=YmXCfQm0_CA#t=68s', 'http://www.youtube.com/watch?v=a8PAY4rvzRM#t=1s', 'http://www.youtube.com/watch?v=ao-9B8IV9_E#t=87s', 'http://www.youtube.com/watch?v=bmvD4HlPFxg#t=20s', 'http://www.youtube.com/watch?v=c2MwqFYVE7A#t=40s', 'http://www.youtube.com/watch?v=cJOZp2ZftCw#t=1s', 'http://www.youtube.com/watch?v=dc4UltkRJsw#t=53s', 'http://www.youtube.com/watch?v=dfOuTx66bJU#t=34s', 'http://www.youtube.com/watch?v=dtwXtwJByYk#t=5s', 'http://www.youtube.com/watch?v=g1Gldu1KS44#t=8s', 'http://www.youtube.com/watch?v=hWhKdXcqYeU#t=3s', 'http://www.youtube.com/watch?v=hkkmKk9LcQk#t=36s', 'http://www.youtube.com/watch?v=jDFn-1lXJ98#t=71s', 'http://www.youtube.com/watch?v=jsEUFYhiqxU#t=121s', 'http://www.youtube.com/watch?v=kRNHJSc4AXE#t=220s', 'http://www.youtube.com/watch?v=mv89psg6zh4#t=33s', 'http://www.youtube.com/watch?v=tZzJ9dDnncY#t=43s', 'http://www.youtube.com/watch?v=uB9zRlV47qA#t=17s', 'http://www.youtube.com/watch?v=uRo_vJ-zy-U#t=35s', 'http://www.youtube.com/watch?v=uiLr9bdOL0M#t=23s', 'http://www.youtube.com/watch?v=umjc1CkO4JA#t=290s', 'http://www.youtube.com/watch?v=zlS1_zBYluY#t=15s']),
                   ("""submission.search("test-big.pkl","cauliflower tyre")""",['http://www.youtube.com/watch?v=UI3Cbj9fbxQ#t=2s', 'http://www.youtube.com/watch?v=aeA-HN7BMdo#t=34s', 'http://www.youtube.com/watch?v=c53HKs39i28#t=26s', 'http://www.youtube.com/watch?v=jbzaMtPYtl8#t=48s', 'http://www.youtube.com/watch?v=kEGmZDpZ_RE#t=352s', 'http://www.youtube.com/watch?v=m1NR0uNNs5Y#t=160s', 'http://www.youtube.com/watch?v=xxHx6s_DbUo#t=121s']),
                   ("""submission.search("test-big.pkl","bird curmudgeonly curmudgeonly")""",['http://www.youtube.com/watch?v=-8rBYNP0UKM#t=194s', 'http://www.youtube.com/watch?v=2G9fkvBzzQE#t=10s', 'http://www.youtube.com/watch?v=Ce7equ9zCxk#t=4s', 'http://www.youtube.com/watch?v=O2qiPS2NCeY#t=2s', 'http://www.youtube.com/watch?v=QsC8__3lwO0#t=50s', 'http://www.youtube.com/watch?v=ScdUht-pM6s#t=53s', 'http://www.youtube.com/watch?v=a8PAY4rvzRM#t=1s', 'http://www.youtube.com/watch?v=ao-9B8IV9_E#t=87s', 'http://www.youtube.com/watch?v=cJOZp2ZftCw#t=1s', 'http://www.youtube.com/watch?v=jsEUFYhiqxU#t=121s', 'http://www.youtube.com/watch?v=mv89psg6zh4#t=33s', 'http://www.youtube.com/watch?v=uiLr9bdOL0M#t=23s']),
                 ],
              "rr":
                  [("""submission.rr("bird",['http://www.youtube.com/watch?v=jDFn-1lXJ98#t=71s', 'http://www.youtube.com/watch?v=YmXCfQm0_CA#t=68s', 'http://www.youtube.com/watch?v=umjc1CkO4JA#t=290s', 'http://www.youtube.com/watch?v=O2qiPS2NCeY#t=2s', 'http://www.youtube.com/watch?v=BApIQn69EVE#t=10s', 'http://www.youtube.com/watch?v=5E66Gk3V1Bc#t=23s', 'http://www.youtube.com/watch?v=RX6NSOuCCAE#t=13s', 'http://www.youtube.com/watch?v=cJOZp2ZftCw#t=1s', 'http://www.youtube.com/watch?v=G-M78KIy19E#t=315s', 'http://www.youtube.com/watch?v=dc4UltkRJsw#t=53s', 'http://www.youtube.com/watch?v=mv89psg6zh4#t=33s', 'http://www.youtube.com/watch?v=2G9fkvBzzQE#t=10s', 'http://www.youtube.com/watch?v=I9gLTZY1ouc#t=142s', 'http://www.youtube.com/watch?v=zlS1_zBYluY#t=15s', 'http://www.youtube.com/watch?v=g1Gldu1KS44#t=8s', 'http://www.youtube.com/watch?v=Ce7equ9zCxk#t=4s', 'http://www.youtube.com/watch?v=uiLr9bdOL0M#t=23s', 'http://www.youtube.com/watch?v=kRNHJSc4AXE#t=220s', 'http://www.youtube.com/watch?v=L9wD3kw-8FE#t=65s', 'http://www.youtube.com/watch?v=SrDE9-cDz48#t=4s', 'http://www.youtube.com/watch?v=hWhKdXcqYeU#t=3s', 'http://www.youtube.com/watch?v=tZzJ9dDnncY#t=43s', 'http://www.youtube.com/watch?v=-8rBYNP0UKM#t=194s', 'http://www.youtube.com/watch?v=jsEUFYhiqxU#t=121s', 'http://www.youtube.com/watch?v=dtwXtwJByYk#t=5s', 'http://www.youtube.com/watch?v=bmvD4HlPFxg#t=20s', 'http://www.youtube.com/watch?v=ao-9B8IV9_E#t=87s', 'http://www.youtube.com/watch?v=MWvCcwTw7Ac#t=78s', 'http://www.youtube.com/watch?v=PJnJMp2ZpbA#t=3s', 'http://www.youtube.com/watch?v=ScdUht-pM6s#t=53s', 'http://www.youtube.com/watch?v=hkkmKk9LcQk#t=36s', 'http://www.youtube.com/watch?v=uRo_vJ-zy-U#t=35s', 'http://www.youtube.com/watch?v=dfOuTx66bJU#t=34s', 'http://www.youtube.com/watch?v=c2MwqFYVE7A#t=40s', 'http://www.youtube.com/watch?v=uB9zRlV47qA#t=17s', 'http://www.youtube.com/watch?v=8yuPGwxwdPs#t=1s', 'http://www.youtube.com/watch?v=2YhDTpzxd3c#t=98s', 'http://www.youtube.com/watch?v=a8PAY4rvzRM#t=1s', 'http://www.youtube.com/watch?v=1dmVuwO1RZk#t=0s', 'http://www.youtube.com/watch?v=QsC8__3lwO0#t=50s'],"test.qrels")""",0.125),
                   ("""submission.rr("bird",[],"test.qrels")""",0),
                   ("""submission.rr("bird",['http://www.youtube.com/watch?v=cJOZp2ZftCw#t=1s', 'http://www.youtube.com/watch?v=O2qiPS2NCeY#t=2s', 'http://www.youtube.com/watch?v=mv89psg6zh4#t=33s', 'http://www.youtube.com/watch?v=2G9fkvBzzQE#t=10s', 'http://www.youtube.com/watch?v=Ce7equ9zCxk#t=4s', 'http://www.youtube.com/watch?v=uiLr9bdOL0M#t=23s', 'http://www.youtube.com/watch?v=-8rBYNP0UKM#t=194s', 'http://www.youtube.com/watch?v=jsEUFYhiqxU#t=121s', 'http://www.youtube.com/watch?v=ao-9B8IV9_E#t=87s', 'http://www.youtube.com/watch?v=ScdUht-pM6s#t=53s', 'http://www.youtube.com/watch?v=a8PAY4rvzRM#t=1s', 'http://www.youtube.com/watch?v=QsC8__3lwO0#t=50s'],"test.qrels")""",1.0),
                   ("""submission.rr("bird tree tree",[],"test.qrels")""",0),
                   ("""submission.rr("bird tree tree",['http://www.youtube.com/watch?v=O2qiPS2NCeY#t=2s', 'http://www.youtube.com/watch?v=cJOZp2ZftCw#t=1s', 'http://www.youtube.com/watch?v=jDFn-1lXJ98#t=71s', 'http://www.youtube.com/watch?v=mv89psg6zh4#t=33s', 'http://www.youtube.com/watch?v=YmXCfQm0_CA#t=68s', 'http://www.youtube.com/watch?v=umjc1CkO4JA#t=290s', 'http://www.youtube.com/watch?v=BApIQn69EVE#t=10s', 'http://www.youtube.com/watch?v=2G9fkvBzzQE#t=10s', 'http://www.youtube.com/watch?v=5E66Gk3V1Bc#t=23s', 'http://www.youtube.com/watch?v=RX6NSOuCCAE#t=13s', 'http://www.youtube.com/watch?v=G-M78KIy19E#t=315s', 'http://www.youtube.com/watch?v=dc4UltkRJsw#t=53s', 'http://www.youtube.com/watch?v=Ce7equ9zCxk#t=4s', 'http://www.youtube.com/watch?v=uiLr9bdOL0M#t=23s', 'http://www.youtube.com/watch?v=I9gLTZY1ouc#t=142s', 'http://www.youtube.com/watch?v=zlS1_zBYluY#t=15s', 'http://www.youtube.com/watch?v=g1Gldu1KS44#t=8s', 'http://www.youtube.com/watch?v=kRNHJSc4AXE#t=220s', 'http://www.youtube.com/watch?v=L9wD3kw-8FE#t=65s', 'http://www.youtube.com/watch?v=-8rBYNP0UKM#t=194s', 'http://www.youtube.com/watch?v=SrDE9-cDz48#t=4s', 'http://www.youtube.com/watch?v=jsEUFYhiqxU#t=121s', 'http://www.youtube.com/watch?v=hWhKdXcqYeU#t=3s', 'http://www.youtube.com/watch?v=ao-9B8IV9_E#t=87s', 'http://www.youtube.com/watch?v=tZzJ9dDnncY#t=43s', 'http://www.youtube.com/watch?v=ScdUht-pM6s#t=53s', 'http://www.youtube.com/watch?v=dtwXtwJByYk#t=5s', 'http://www.youtube.com/watch?v=bmvD4HlPFxg#t=20s', 'http://www.youtube.com/watch?v=MWvCcwTw7Ac#t=78s', 'http://www.youtube.com/watch?v=PJnJMp2ZpbA#t=3s', 'http://www.youtube.com/watch?v=a8PAY4rvzRM#t=1s', 'http://www.youtube.com/watch?v=hkkmKk9LcQk#t=36s', 'http://www.youtube.com/watch?v=uRo_vJ-zy-U#t=35s', 'http://www.youtube.com/watch?v=dfOuTx66bJU#t=34s', 'http://www.youtube.com/watch?v=c2MwqFYVE7A#t=40s', 'http://www.youtube.com/watch?v=uB9zRlV47qA#t=17s', 'http://www.youtube.com/watch?v=QsC8__3lwO0#t=50s', 'http://www.youtube.com/watch?v=8yuPGwxwdPs#t=1s', 'http://www.youtube.com/watch?v=2YhDTpzxd3c#t=98s', 'http://www.youtube.com/watch?v=1dmVuwO1RZk#t=0s'],"test.qrels")""",0.125),
                 ],
              "batch_evaluate":
                  [("""submission.batch_evaluate("test-big.pkl",["bird tree","bird","cauliflower"],"test.qrels","out.html")""",None),
                   ("""submission.batch_evaluate("test-big.pkl",["bird","tyre","cauliflower tyre"],"test.qrels","out.html")""",None)
                  ],
              "word_freq_graph":
                  [("""submission.word_freq_graph("test-big.pkl","bird.svg","bird")""",None),
                   ("""submission.word_freq_graph("test-big.pkl","curmudgeonly.svg","curmudgeonly")""",None),
                  ],
              }