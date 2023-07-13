from definitions import *

def batch(iterable, max_batch_size):
    """ Batches an iterable into lists of given maximum size, yielding them one by one. """
    batch = []
    for element in iterable:
        batch.append(element)
        if len(batch) >= max_batch_size:
            yield batch
            batch = []
    if len(batch) > 0:
        yield batch

def fEven(start, n):
    return [start + (i*2) for i in range(0,n)]

def getChromaticFromNote(tonic, octaves=1):
    chromscale = CHROMATICS[accidents]
    index = chromscale.index(tonic.lower())
    return (chromscale[index:] + chromscale[:index]) * octaves

def getKeyNotes(chromscale, struct="MAJOR"):
    ind = 0
    notes = []
    for dif in KEYSTRUCTURES[struct]:
        notes.append(chromscale[ind])
        ind += dif
    return notes

def getKeyChords(key, notenum=3):

    rng = fEven(0, notenum)
    key = key * 16
    outlist = []
    for i in range(7): 
        for j in rng:
            outlist.append(key[i + j])

    return list(batch(outlist, notenum))

def getIntervalsBetweenNotes(notelist):
    chromscale = getChromaticFromNote(notelist[0], octaves=4)
    chrom = list(batch(chromscale, 12))
    flag = len(notelist)
    outlist = []

    for octindex, octave in enumerate(chrom):
        notecount = 0
        for octnote in octave:
            if len(outlist) == flag:
                break
            if octnote == notelist[notecount]:
                if octindex == 0:
                    outlist.append(chromscale.index(octnote))
                else:
                    outlist.append(chromscale.index(octnote) + 7 * (octindex + 1))
                octave.pop(octave.index(octnote))
                notecount += 1

    for i in range(len(outlist)):
        outlist[i] = INTERVALS[outlist[i]]
        
    return outlist

def getChordFromNotes(notelist):
    pass

global accidents
accidents = "SHARPS"

chromscale = getChromaticFromNote("c", octaves=4)
key = getKeyNotes(chromscale, struct="MAJOR")
keychords = getKeyChords(key, notenum=4)

for degree, each in enumerate(keychords):
    print(degree + 1, each, getIntervalsBetweenNotes(each))
