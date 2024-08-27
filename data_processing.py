import pandas as pd

def book_processing():
    data_path = "data/Books.csv"
    data = pd.read_csv(data_path)
    for i in range(len(data)):
        row = list(data.iloc[i])
        published = row[3]
        title = row[1]
        publisher = row[4]
        genre = row[5]
        if len(title) >= 100 or len(publisher)>=50 or len(genre)>=50:
            continue
        row[3] = int(published)
        if row[-1] == ";;":
            row.remove(row[-1])
        if isinstance(row[-1],str) and row[-1].endswith(";;"):
            row[-1] = row[-1].rstrip(";;")
        print(tuple(row),",")

book_processing()