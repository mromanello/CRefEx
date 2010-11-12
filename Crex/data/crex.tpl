# model for canonical references training
#unigram
U018:%x[-2,0]
U019:%x[-1,0]
U020:%x[0,0]
U021:%x[1,0]
U022:%x[2,0]

# punctuation feature
U01:%x[-2,1]
U26:%x[-1,1]
U27:%x[0,1]
U28:%x[1,1]
U29:%x[2,1]

# bracket feature
U02:%x[0,2]

# case feature
U03:%x[-2,3]
U34:%x[1,3]
U35:%x[0,3]
U36:%x[1,3]
U347:%x[2,3]

# number feature
#U04:%x[-2,4]
U30:%x[-1,4]
U31:%x[0,4]
U32:%x[1,4]
#U33:%x[2,4]

# lowercase no punct string length
U06:%x[0,6]

#lowercase unigram
U07:%x[-2,5]
U24:%x[-1,5]
U08:%x[0,5]
U23:%x[1,5]
U25:%x[2,5]

# first 4 chars
U09:%x[0,6]
U10:%x[0,7]
U11:%x[0,8]
U12:%x[0,9]

#last 4 chars
U13:%x[0,10]
U14:%x[0,11]
U15:%x[0,12]
U16:%x[0,13]
U17:%x[0,14]

# bigram template
B0