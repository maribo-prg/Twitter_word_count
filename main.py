import csv

import MeCab
import collections
import re
import csv
import datetime

import get_tweet
import unnecessary

Serch_Word = "エンジニア" #キーワード
Tweet_num = 4000 #取得するツイート数
rank = 400 #頻出が高い単語rank位まで

def main():
    tweet_list = serch(Serch_Word)
    word_count_list = Keitaiso(tweet_list)
    csv_file(word_count_list)

#ツイートリスト返す
def serch(word):
    list = get_tweet.search(word)
    return list

#多かった順に[単語,カウント数]が入ったリストを返す
def Keitaiso(tweet_list):
    word_counts = []
    for text in tweet_list:
        m = MeCab.Tagger()
        s = m.parse(text)
        s = s.split('\n')
        for i in s:
            i = re.split('[\t,]', i)
            try:
                if i[1] == "名詞" or i[1] == "形容詞":
                    if len(i[0])!=1 and i[0] not in unnecessary.unnec:
                        word_counts.append(i[0])
            except:
                pass
    c = collections.Counter(word_counts)#要素の出現回数
    tmp = c.most_common(rank)#rank位まで
    for j in tmp[1:]:
        print(j)

    return tmp

def csv_file(lists):
    now_time = datetime.datetime.now()
    file_name = now_time.strftime('%Y-%m-%d') + "_" + Serch_Word + "_" + str(Tweet_num)

    f = open('%s.csv'%file_name,'w',encoding='utf_8_sig',newline='')
    writer = csv.writer(f)
    for i in lists[1:]:
        writer.writerow(i)
    f.close()

if __name__ == "__main__":
    main()