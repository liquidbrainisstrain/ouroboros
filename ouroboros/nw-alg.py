import numpy as np

seq1 = 'RGSRRPGQPP'
seq2 = 'RGQGRRWRPP'

mainm = np.zeros((len(seq1)+1, len(seq2)+1))
matchm = np.zeros((len(seq1), len(seq2)))

reward = 1
mism = -1
gappen = -2

for i in range(len(seq1)):
    for j in range(len(seq2)):
        if seq1[i] == seq2[j]:
            matchm[i][j] = reward
        else:
            matchm[i][j] = mism

#init
for i in range(len(seq1)+1):
    mainm[i][0] = i*gappen
for j in range(len(seq2)+1):
    mainm[0][j] = j*gappen
#fill
for i in range(1, len(seq1)+1):
    for j in range(1, len(seq2) + 1):
        mainm[i][j] = max(mainm[i-1][j-1]+matchm[i-1][j-1],
                          mainm[i-1][j]+gappen,
                          mainm[i][j-1]+gappen)
#traceback
al_seq1 = ''
al_seq2 = ''
ls1 = len(seq1)
ls2 = len(seq2)

while ls1>0 and ls2>0:
    if ls1>0 and ls2>0 and mainm[ls1][ls2] == mainm[ls1-1][ls2-1] + matchm[ls1-1][ls2-1]:
        al_seq1 = seq1[ls1-1] + al_seq1
        al_seq2 = seq2[ls2-1] + al_seq2
        ls1 -= 1
        ls2 -= 1
    elif ls1>0 and mainm[ls1][ls2] == mainm[ls1-1][ls2] + gappen:
        al_seq1 = seq1[ls1 - 1] + al_seq1
        al_seq2 = "_" + al_seq2
        ls1 -= 1
    else:
        al_seq1 = "_" + al_seq1
        al_seq2 = seq2[ls2 - 1] + al_seq2
        ls2 -= 1

print(al_seq1)
print(al_seq2)


