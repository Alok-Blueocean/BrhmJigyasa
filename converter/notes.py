# Bhagavad Gita
# no of verses will not add up to 700 because some verse are combined e.g. verse 10.4-5 (id345)
# Minor corrections to BG.xlsx
# Bhagavad Gita16.13-15 to Bhagavad Gita 16.13-15 and changing shloka to h_BG
# BG 9. to Bhagavad Gita 9. and changing shloka to h_BG
# 'Bhagavad Gita  ' to 'Bhagavad Gita ' and changing shloka to h_BG , # '2.23', '2.31', '2.39', '2.45', '9.18', '16.13', '16.14', '16.15'
# [113, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 1076]

import warnings

warnings.filterwarnings("ignore")


def generateDataFrame():
    file = 'bhagavadGita.xlsx'
    import pandas as pd
    df = pd.read_excel(file, index_col=False, skiprows=10)
    return df


def cleanDataFrame(df):
    import numpy as np
    df = df.replace(np.nan, '', regex=True)[['Prefix', 'Body', 'Theme']]
    tags = ['intro', 'h_BG', 'h_w2w', '"w2w', 'h_translation', '"translation', 'h_purport', 'shloka', 'questions',
            'normal', 'ch_end']
    for tag in tags:
        df.loc[df['Prefix'].str.contains(tag, na=False), 'Prefix'] = tag
    df.describe()
    print(len(df[df['Prefix'] == 'h_BG'].index), 'Shlokas found')  # check no of tagged shlokas
    assert len(df['Prefix'].unique()) - len(tags) == 1
    len(df[df['Prefix'] == 'h_w2w'].index) == len(df[df['Prefix'] == 'h_BG'].index)  # no of tagged w2w = h_BG
    return df
    # df.loc[(df['Body'].str.contains('Bhagavad Gita  ', na=False)) & (df['Prefix'] == 'shloka'), 'Prefix'] = 'h_BG'  # fix errors in excel file
    # df = df.replace('Bhagavad Gita  ', 'Bhagavad Gita ', regex=True)[['Prefix', 'Body', 'Theme']]  # fix errors in excel file
    # df = df.replace('Bhagavad Gita16.', 'Bhagavad Gita 16.', regex=True)
    # df.loc[(df['Body'].str.contains('BG ', na=False)) & (df['Prefix'] == 'shloka'), 'Prefix'] = 'h_BG'
    # df.loc[(df['Body'].str.contains('Bhagavad Gita', na=False)) & (df['Prefix'] == 'shloka'), 'Prefix'] = 'h_BG'
    # df.loc[df['Body'].str.contains('Bhagavad Gita a book of', na=False), 'Prefix'] = 'questions'
    # print(df[df['Prefix'] == 'h_BG'].tail(1))
    # print(df.loc[df['Body'].str.contains('Bhagavad Gita  ', na=False, regex=True)].Prefix)
    # print(len(df[df['Prefix'] == 'h_BG'].index)) # check no of tagged shlokas


def getAllVerses(df):
    indices = df.loc[df['Prefix'] == 'h_BG'].index.values.tolist()
    start = list(indices)
    end = [index - 1 for index in indices[1:]] + [None]
    verses = []
    for starting, ending in zip(start, end):  # verse = df.loc[446:470], verse = df.loc[471:485]
        verse = df.loc[starting:ending]  # verse.describe()
        verses.append(verse)

    return verses


def processVerse(verse, book='Bhagavad Gita', canto=0):
    verse.reset_index(drop=True, inplace=True)
    print('processing', verse.loc[0].Body)
    h_w2w = verse.loc[verse['Prefix'] == 'h_w2w'].index.values.tolist()[0]
    id = verse.iloc[0].Body.split(' ').pop()
    chapter, number = id.split('.')
    # shloka = '\n'.join(verse.loc[verse['Prefix'] == 'shloka'].Body.tolist())
    text = '\n'.join(verse.loc[1:h_w2w - 1].Body.values.tolist())
    w2w = verse.loc[verse['Prefix'] == '"w2w'].Body.values[0]
    translation = verse.loc[verse['Prefix'] == '"translation'].Body.values[0]
    questionThemes = verse.loc[verse['Prefix'] == 'questions'][['Body', 'Theme']].values.tolist()
    questionIndices = verse.loc[verse['Prefix'] == 'questions'][['Body', 'Theme']].index.values.tolist()
    answerStart = [index + 1 for index in questionIndices]
    answerEnd = [index - 1 for index in answerStart[1:]] + [None]
    # answers = verse.loc[verse['Prefix'] == 'normal'].Body.values.tolist()
    # assert len(questions) == len(answers)
    shlokaArgs = {'text': text, 'book': book, 'canto': canto, 'chapter': chapter, 'number': number, 'w2w': w2w,
                  'translation': translation}
    purportParas = []
    for index, (questionTheme, start, end) in enumerate(zip(questionThemes, answerStart, answerEnd), start=1):
        questionText, theme = questionTheme
        purportText = '\n'.join(verse.loc[start:end].Body.values.tolist())
        question = {}
        question['text'] = questionText
        question['theme'] = theme
        purportParas.append([index, purportText, question])

    response = {}
    response['shlokaArgs'] = shlokaArgs
    response['purportParas'] = purportParas
    return response


def getNthVerse(df, verseNo='2.7'):
    dfn = df.loc[df['Prefix'] == 'h_BG'].reset_index()
    serialNo = dfn.loc[dfn['Body'] == 'Bhagavad Gita ' + verseNo].index.values[0]
    startIndex = dfn.loc[serialNo]['index']
    endIndex = dfn.loc[serialNo + 1]['index'] - 1
    verse = df.loc[startIndex:endIndex]
    return verse


def createDjangoObjects(kwargs):
    from converter.models import Book, Shloka, PurportPara, Question, Theme
    shlokaArgs = kwargs.get('shlokaArgs', {})
    purportParas = kwargs.get('purportParas', [])
    shlokaArgs['book'] = Book.objects.get(name=shlokaArgs.get('book', 'Bhagavad Gita'))
    # shloka = Shloka.objects.create(text=text, book=book, canto=canto, chapter=chapter, number=number, w2w=w2w,
    #                                translation=translation)
    shloka, created = Shloka.objects.get_or_create(**shlokaArgs)
    print(shloka, 'created' if created else 'fetched')
    for purport_no, purportText, question in purportParas:
        purportpara, created = PurportPara.objects.get_or_create(number=purport_no, text=purportText, shloka=shloka)
        print(purportpara, 'created' if created else 'fetched')
        shloka.purport.add(purportpara)
        theme, created = Theme.objects.get_or_create(name=question['theme'])
        print(theme, 'created' if created else 'fetched')
        question, created = Question.objects.get_or_create(text=question['text'], para=purportpara)
        print(question, 'created' if created else 'fetched')
        question.theme.add(theme)
        theme.question.add(question)


def findDataErrors(verses):
    h_BGs = dfc[(dfc['Prefix'] == 'h_BG') | (dfc['Prefix'] == 'h_w2w')].Prefix.values.tolist()
    h_w2ws = headersSeries[1:]
    culprits = []
    for index, (h_BG, h_w2w) in enumerate(zip(h_BGs, h_w2ws), start=1):
        if h_BG == h_w2w:
            culprits.append(index)
    sample = dfc[(dfc['Prefix'] == 'h_BG') | (dfc['Prefix'] == 'h_w2w')].Body.values.tolist()[113]
    print(sample)
    return culprits


df = cleanDataFrame(generateDataFrame())


def runVerse(vNo='1.19'):
    verse = getNthVerse(df, vNo)
    kwargs = processVerse(verse)
    createDjangoObjects(kwargs)


from converter.notes import *
# verses = getAllVerses(df)

def clearDB():
    from converter.models import Question, Theme, PurportPara, Shloka
    models = [Question, Theme, PurportPara, Shloka]
    for model in models:
        model.objects.all().delete()

def testFirstN(n):
    verses = getAllVerses(df)[:n]
    for verse in verses:
        createDjangoObjects(processVerse(verse))
