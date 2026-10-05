# mood_cloud.py v0.0.1

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import daylio
from tqdm import tqdm
from datetime import datetime, timedelta
import spacy

DAYLIO_FILENAME = daylio.get_filename()

data = daylio.load_data(DAYLIO_FILENAME)
dates = daylio.get_first_last_dates(DAYLIO_FILENAME)


strings = ["","","","",""]

date = datetime.strptime(dates[0], "%Y-%m-%d")
end_date = date.strptime(dates[1], "%Y-%m-%d")

nlp = spacy.load("en_core_web_sm")
allowed_tags = ["ADJ"]

while(date != end_date):
    print(f"Analyzing {str(date).split(" ")[0]}")
    mood = daylio.get_mood_for_date_preloaded(date.strftime("%Y-%m-%d"),data)
    note = daylio.get_note_for_date_preloaded(date.strftime("%Y-%m-%d"),data)
    doc = nlp(note)
    filtered_words = [token.text for token in doc if token.pos_ in allowed_tags]
    strings[mood-1] += " ".join(filtered_words)
    date+=timedelta(days=1)


# in the future, could implement one plot with words size determined by frequency and colour by mood category

for i in range(len(strings)):
    wordcloud = WordCloud().generate(strings[i])
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title(daylio.DAYLIO_INT_TO_MOOD[i+1])
    plt.show()