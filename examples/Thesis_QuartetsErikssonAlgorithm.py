import pandas as pd
import splitp as sp
import time
import trees
import itertools
import matplotlib as mpl
import matplotlib.pyplot as plt

def sort(string):
    return ''.join(sorted(string))

# Settings
true_splits = trees.trees['T4A'][2]
scalingFactors = [None, 1, 2, 3, 10]
sequenceLengths = [100*n for n in range(1, 11)]
numRuns = 1000

bigResults = []
theTrees = [trees.trees['T4A'][0], trees.trees['T4B'][0], trees.trees['T4C'][0], trees.trees['T4D'][0]]
for t, tree in enumerate(theTrees):
    print("TREE", t)
    finalResults = {str(lam) : [0 for sequenceLength in sequenceLengths] for lam in scalingFactors}
    numSpecies = tree.get_num_taxa()
    all_splits = sp.generateAllSplits(numSpecies, trivial=False)
    patternProbs = tree.get_pattern_probabilities()
    for i, sequenceLength in enumerate(sequenceLengths):
        start = time.time()
        for run in range(numRuns):
            print("Run", run, "of", numRuns, end='')
            print(" (length: " + str(sequenceLength) + ")")
            empericalProbs = tree.draw_from_multinomial(patternProbs, sequenceLength)
            flattenings = {}
            for lam in scalingFactors:
                #print("\t" + str(lam), end='')
                taxa = [str(i) for i in range(numSpecies)]
                chosenSplits = set()
                done = False
                for c in range(numSpecies, 3, -1):
                    if not done:
                        results = dict()
                        for pair in itertools.combinations(taxa, 2):
                            split = ("".join(t for t in taxa if t not in pair[0]+pair[1]) , pair[0] + pair[1])
                            split = sort(split[0]) + '|' + sort(split[1]) if '0' in split[0] else sort(split[1]) + '|' + sort(split[0])
                            F = None
                            if split in flattenings:
                                F = flattenings[split]
                            else:
                                F = tree.flattening(split, empericalProbs)
                                flattenings[split] = F
                            if lam != None:
                                F = tree.subflattening_alt(F, sp.scaledHMatrix(lam)[0])
                            results[(pair, split)] = tree.split_score(F)
                        bestSplit = min(results, key=results.get)
                        if bestSplit[1] not in true_splits:
                            done = True
                        for p in bestSplit[0]:
                            taxa.remove(p)
                        taxa.append("".join(bestSplit[0]))
                        chosenSplits.add(bestSplit[1])
                if chosenSplits == true_splits:
                    finalResults[str(lam)][i] += 1
        end = time.time()
        print("Time taken:", end - start)

    f = open("ErikksonAlgorithmResults.csv", "w")
    f.write(pd.DataFrame(finalResults).to_csv(index=False))
    f.close()

    data = pd.read_csv("ErikksonAlgorithmResults.csv")
    finalResults = {}
    for column in data:
        finalResults[column] = data[column].to_list()

    bigResults.append(finalResults)

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(6,5))
axes = [ax1, ax2, ax3, ax4]
nice_fonts = {
            # Use LaTeX to write all text
            "text.usetex": True,
            "font.family": "serif",
            "axes.labelsize": 11,
            "font.size": 11,
            "legend.fontsize": 10,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
}
import seaborn as sns
sns.set()
plt.style.use('default')
mpl.rcParams.update(nice_fonts)

for t, finalResults in enumerate(bigResults):

    with sns.color_palette("colorblind"):
        for k in finalResults.keys():
            axes[t].plot(sequenceLengths, [n*100/numRuns for n in finalResults[k]], marker='o', markersize=3, linewidth=0.75, label="Flattening" if k == 'None' else "$\lambda =\ $" + k)
        axes[t].set_ylim(-0.5, 105)

fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.xlabel('Sequence Length')
plt.ylabel('\% Trees Correctly Reconstructed')
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center', ncol=3, frameon=False)
fig.savefig('_Quartets_Eriksson_Alg_Scaling_FULLAX.pdf')

plt.show()