from converter.models import Book, Shloka, PurportPara, Question, Theme

para = PurportPara.objects.get(id=2)
shloka = Shloka.objects.first()
theme = Theme.objects.first()
text = 'What are the 2 specialties of Bhagavad Gita ?'
question=Question.objects.create(number=2, text=text, para=para)
question.theme.add(theme)
Theme.objects.create(name='Siddhanta')
import pandas as pd
file = 'chapter1.xlsx'
df=pd.read_excel(file, index_col=False)
df.head(3)
df.tail(3)
df.columns
df[['startTag', 'Content']]
df.loc[df['startTag'] == '<p class="normal">']
df.iloc[4]
df.describe()
df.iloc[4]
df.iloc[4,2]
for index, row in df.iterrows():
    print(index, row['endTag'])
df.loc[df['startTag'] == '<p class="normal">']
df['complete'] = df['startTag'] + df['Content']+ df['endTag']
df.to_excel('modified.xlsx', index=false)
answerTag = '<p class="normal">'

new_df = df.loc[df['startTag'] == answerTag]
modified = new_df.reset_index()
modified = new_df.reset_index(drop=True)
new_df.reset_index(drop=True, inplace=True) # mutates new_df to new one

df.loc[df['startTag'].str.contains('normal')]
df.loc[~ df['startTag'].str.contains('normal')]
df.loc[df['startTag'].str.contains('normal|BG', regex=True)]

import re
df.loc[df['startTag'].str.contains('normal|bg', regex=True)]
df.loc[df['startTag'].str.contains('normal|bg', flags=re.I, regex=True)] # ignore capitalization
df.loc[df['startTag'].str.contains('normal'), 'startTag'] = 'normal'
df.loc[df['startTag'].str.contains('shloka'), 'startTag'] = 'shloka'
df.loc[df['startTag'].str.contains('translation'), 'startTag'] = 'translation'
df.loc[df['startTag'].str.contains('h_purport'), 'startTag'] = 'h_purport'
df.loc[df['startTag'].str.contains('intro'), 'startTag'] = 'intro'
df.loc[df['startTag'].str.contains('h_BG'), 'startTag'] = 'h_BG'
df.loc[df['startTag'].str.contains('ch_end'), 'startTag'] = 'ch_end'
df.loc[df['startTag'].str.contains('h_w2w'), 'startTag'] = 'h_w2w'
df.loc[df['startTag'].str.contains('questions'), 'endTag'] = 'questions'

intro = df.loc[df['startTag'] == 'intro']

del df['QuestionIds']

# aggregate statistics
df.groupby(['startTag']).count()

