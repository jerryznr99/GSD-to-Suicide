import sys
from searchRecord import searchRecord
from typing import List
import matplotlib.pyplot as plt
import csv

current_timestamp = "07/01/2021 20:30".split(" ")
current_date = current_timestamp[0].split("/")
current_time = current_timestamp[1].split(":")

list_of_keywords = ["kill myself", "kill yourself", "suicide methods", "commit suicide", "fast suicide",
                    "easy suicide", "quick suicide", "painless suicide", "crisis text line",
                    "national suicide prevention lifeline", "national suicide hotline",
                    "disaster distress helpline", "disaster distress hotline", "depression",
                    "panic attack", "anxiety", "unemployment", "I lost my job", "laid off", "furlough", "loan"]

def check_keyword(searchRecords: List[searchRecord]):
    wordCount = 0
    for i in range(len(searchRecords)):
        for j in range(len(list_of_keywords)):
            if list_of_keywords[j] in searchRecords[i].keyword:
                wordCount += 1
    return wordCount

def data_filter(searchRecords: List[searchRecord]):
    newRecords = []
    for i in range(len(searchRecords)):
        if("suicide squad" in searchRecords[i].keyword or
                "economic depression" in searchRecords[i].keyword):
            searchRecords[i].keyword = "unrelated"
        if not (searchRecords[i].keyword == "" or searchRecords[i].date == ""):
            newRecords.append(searchRecords[i])
    return newRecords

def filter_hour(searchRecords: List[searchRecord]):
    hourRecords = []
    for i in range(len(searchRecords)):
        search_timestamp = searchRecords[i].date.split(" ")
        search_time = search_timestamp[1].split(":")
        if(int(search_time[1]) < int(current_time[1]) and
           int(search_time[0]) == int(current_time[0]) and
           search_timestamp[0] == current_timestamp[0]):
            hourRecords.append(searchRecords[i])
    return hourRecords

def filter_day(searchRecords: List[searchRecord]):
    dayRecords = []
    for i in range(len(searchRecords)):
        search_timestamp = searchRecords[i].date.split(" ")
        if search_timestamp[0] == current_timestamp[0]:
            dayRecords.append(searchRecords[i])
    return dayRecords

def filter_month(searchRecords: List[searchRecord]):
    monthRecords = []
    for i in range(len(searchRecords)):
        search_timestamp = searchRecords[i].date.split(" ")
        search_date = search_timestamp[0].split("/")
        if(int(search_date[1]) == int(current_date[1]) and
           int(search_date[2]) == int(current_date[2])):
            monthRecords.append(searchRecords[i])
    return monthRecords

def produce_pie_chart1(labels: List[str], fractions: List[int], explode: List[float]) -> None:
    axes[0].pie(fractions, explode=explode, labels=labels, autopct='%.0f%%', shadow=False)
    axes[0].set_title("Fig 1. Total google searches in an hour")
    return None

def produce_pie_chart2(labels: List[str], fractions: List[int], explode: List[float]) -> None:
    axes[1].pie(fractions, explode=explode, labels=labels, autopct='%.0f%%', shadow=False)
    axes[1].set_title("Fig 2. Total google searches in a day")
    return None

def produce_pie_chart3(labels: List[str], fractions: List[int], explode: List[float]) -> None:
    axes[2].pie(fractions, explode=explode, labels=labels, autopct='%.0f%%', shadow=False)
    axes[2].set_title("Fig 3. Total google searches in a month")
    return None

def calculate_risk_level(percentage_hour: float, percentage_day: float, percentage_month: float):
    weighted_average = percentage_hour * 0.7 + percentage_day * 0.2 + percentage_month * 0.1
    if weighted_average == 0:
        return 0
    elif weighted_average < 20:
        return 1
    elif weighted_average < 40:
        return 2
    elif weighted_average < 60:
        return 3
    elif weighted_average < 80:
        return 4
    else:
        return 5

def read_csv(filename: str):
    list_of_search_records = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            search_record = searchRecord(row[0], row[1])
            list_of_search_records.append(search_record)
    return list_of_search_records

if __name__ == "__main__":
    print("program ›start")
    search_records = read_csv("test2.csv")
    search_records = data_filter(search_records)
    suicide_related_hour = check_keyword(filter_hour(search_records))
    total_searches_hour = len(filter_hour(search_records))
    suicide_related_day = check_keyword(filter_day(search_records))
    total_searches_day = len(filter_day(search_records))
    suicide_related_month = check_keyword(filter_month(search_records))
    total_searches_month = len(filter_month(search_records))
    risk_level = calculate_risk_level(suicide_related_hour/total_searches_hour * 100.0,
                                      suicide_related_day/total_searches_day * 100.0,
                                      suicide_related_month/total_searches_month * 100.0)
    fig, axj = plt.subplots(nrows=2, ncols=2, sharey=True, sharex=True, figsize=(10, 10), dpi=90)
    axes = axj.flatten()
    produce_pie_chart1(["suicide related", "non-suicide related"],
                       [suicide_related_hour, total_searches_hour - suicide_related_hour], [0.1, 0])
    produce_pie_chart2(["suicide related", "non-suicide related"],
                       [suicide_related_day, total_searches_day - suicide_related_day], [0.1, 0])
    produce_pie_chart3(["suicide related", "non-suicide related"],
                       [suicide_related_month, total_searches_month - suicide_related_month], [0.1, 0])
    axes[3].set_title("Level of suicide risk (from a scale of 0-5)")
    if risk_level == 0:
        axes[3].text(0, 0, "Minimal (0)", color="green", fontsize=20, horizontalalignment="center",
                     verticalalignment="center")
    elif risk_level == 1:
        axes[3].text(0, 0, "Mild (1)", color="green", fontsize=20, horizontalalignment="center",
                     verticalalignment="center")
    elif risk_level == 2:
        axes[3].text(0, 0, "Moderate (2)", color="orange", fontsize=20, horizontalalignment="center",
                     verticalalignment="center")
    elif risk_level == 3:
        axes[3].text(0, 0, "Severe (3)", color="orange", fontsize=20, horizontalalignment="center",
                     verticalalignment="center")
    elif risk_level == 4:
        axes[3].text(0, 0, "Extreme (4)", color="red", fontsize=20, horizontalalignment="center",
                     verticalalignment="center")
    else:
        axes[3].text(0, 0, "Chronic (5)", color="red", fontsize=20, horizontalalignment="center",
                     verticalalignment="center")
    plt.show()


