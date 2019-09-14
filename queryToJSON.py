import json
from pymongo import MongoClient
from bson import json_util
import PySimpleGUI as sg
import logging
import pipelines


def main():
    pipeline = pipelines.pipelines[0]
    gui()
    # execute_query(pipeline, "")


def gui():
    # Green & tan color scheme
    sg.ChangeLookAndFeel('TanBlue')

    sg.SetOptions(text_justification='right')

    layout = [[sg.Text('Machine Learning Command Line Parameters', font=('Helvetica', 16))],
              [sg.Checkbox('Normalize', size=(12, 1), default=True), sg.Checkbox('Verbose', size=(20, 1))],
              [sg.Checkbox('Cluster', size=(12, 1)), sg.Checkbox('Flush Output', size=(20, 1), default=True)],
              [sg.Checkbox('Write Results', size=(12, 1)), sg.Checkbox('Keep Intermediate Data', size=(20, 1))],
              [sg.SaveAs(file_types=(("JSON", ".json"),), enable_events=True)],
              [sg.Cancel()]]

    window = sg.Window('Query Selector', layout, font=("Helvetica", 12))

    while True:
        event, values = window.Read()
        if event is None or event == 'Cancel':
            break
        elif event == 'Save As...':
            if values["Save As..."] != "":
                filename = values["Save As..."]
                break

    window.Close()


def execute_query(pipeline, file):
    database = None
    try:
        connection = MongoClient('mongodb://localhost:27017')
        database = connection['test']
    except ConnectionError:
        connection = None
        logging.error("Unable to connect")

    if connection:
        doc = list(database["allAddresses"].aggregate(pipeline))
        with open(file, "w+") as jsonfile:
            json.dump(doc, jsonfile, indent=4, default=json_util.default)


if __name__ == '__main__':
    main()
