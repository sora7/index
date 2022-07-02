import os

NAMES = ['abukuma', 'akagi', 'akatsuki', 'akizuki', 'aoba', 'arashio', 'asashio', 'bismarck', 'fubuki', 'gotland', 'hagikaze', 'hamakaze', 'haruna', 'hatsuzuki', 'hibiki', 'inazuma', 'iowa', 'isokaze', 'isonami', 'kaga', 'kagerou', 'kashima', 'kasumi', 'kitakami', 'kongou', 'lexington', 'matsuwa', 'maya', 'mikazuki', 'minazuki', 'missouri', 'mizuho', 'murakumo', 'murasame', 'Prinz Eugen', 'saratoga', 'sendai', 'shigure', 'shimakaze', 'shiranui', 'suzukaze', 'suzuya', 'taigei', 'unryuu', 'ushio', 'Yamato', 'yayoi', 'yuubari', 'yuudachi', 'zuihou', 'zuikaku']

path = r''


for fname in os.listdir(path):
    for name in NAMES:
        if name in fname:
            new_name = name + '=_=' + fname
            os.rename(os.path.join(path, fname), os.path.join(path, new_name))
            break


'''
words = []

char_del = ['(', ')']
char_sep = ['_', '.', '-']

for name in os.listdir(path):
    name_ = name
    for ch in char_del:
        name_ = name_.replace(ch, '')

    for ch in char_sep:
        name_ = name_.replace(ch, ' ')

    words.extend(name_.split(' '))

print(words[:10])

w2 = {}

for w in words:
	try:
		w2[w] += 1
	except KeyError:
		w2[w] = 1
'''
