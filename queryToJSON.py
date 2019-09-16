import json
from pymongo import MongoClient
from bson import json_util
import PySimpleGUI as sg
import logging
import pipelines


def main():
    gui()
    # execute_query(pipeline, "")


def gui():
    """
    Init the GUI, shows it and handles all the cases of choices
    The values got by the GUI are saved as a dict
    :return:
    """
    # Green & tan color scheme
    sg.ChangeLookAndFeel('DarkBlue')

    sg.SetOptions(text_justification='right')

    addrs_keys = ['btc', 'eth', 'bch', 'ltc', 'doge', 'dash', 'bsv', 'xmr']
    size_keys = ['size ' + x for x in addrs_keys]

    col1 = [
        [sg.Text('Group', font=('Helvetica', 14), size=(19, 1), justification='left')],
        [sg.Checkbox('Bitcoin address', enable_events=True, key=addrs_keys[0])],
        [sg.Checkbox('Ethereum address', enable_events=True, key=addrs_keys[1])],
        [sg.Checkbox('BitcoinCash address', enable_events=True, key=addrs_keys[2])],
        [sg.Checkbox('Litecoin address', enable_events=True, key=addrs_keys[3])],
        [sg.Checkbox('Dogecoin address', enable_events=True, key=addrs_keys[4])],
        [sg.Checkbox('Dash address', enable_events=True, key=addrs_keys[5])],
        [sg.Checkbox('BitcoinSV address', enable_events=True, key=addrs_keys[6])],
        [sg.Checkbox('Monero address', enable_events=True, key=addrs_keys[7])],
        [sg.Checkbox('Users', enable_events=True, key='users', disabled=True)],
        [sg.Checkbox('Sources', enable_events=True, key='sources')]
    ]

    col2 = [
        [sg.Text('By', font=('Helvetica', 14), size=(21, 1), justification="left")],
        [sg.Combo(('User', 'Address', 'Source'), size=(20, 1), enable_events=True)]
    ]

    col3 = [
        [sg.Text(' Sizes of vectors to add to the document', justification='left', font=('Helvetica', 14))],
        [sg.Checkbox('Size BTC', disabled=True, key=size_keys[0])],
        [sg.Checkbox('Size ETH', disabled=True, key=size_keys[1])],
        [sg.Checkbox('Size BCH', disabled=True, key=size_keys[2])],
        [sg.Checkbox('Size LTC', disabled=True, key=size_keys[3])],
        [sg.Checkbox('Size DOGE', disabled=True, key=size_keys[4])],
        [sg.Checkbox('Size DASH', disabled=True, key=size_keys[5])],
        [sg.Checkbox('Size BSV', disabled=True, key=size_keys[6])],
        [sg.Checkbox('Size XMR', disabled=True, key=size_keys[7])],
        [sg.Checkbox('Users', disabled=True, key='size users')],
        [sg.Checkbox('Sources', disabled=True, key='size sources')]
    ]

    layout = [[sg.Text('Deanonomity Addresses Query Selector', font=('Helvetica', 16))],
              [sg.Column(col1, size=(200, 380)),
               sg.VerticalSeparator(),
               sg.Column(col2),
               sg.VerticalSeparator(),
               sg.Column(col3)],
              [sg.Text('Results are sorted in descending order and'
                       ' with respect to order of checks of checkboxes', font=('Helvetica', 8))],
              [sg.SaveAs(file_types=(("JSON", ".json"),), enable_events=True)],
              [sg.Exit()]
    ]

    window = sg.Window('Query Selector', layout, font=("Helvetica", 12), size=(950, 550))

    cbox_order = []

    while True:
        event, values = window.Read()
        print(event, values)
        if event is None or event == 'Exit':
            break

        elif event == 'Save As...':
            if values["Save As..."] != "":
                filename = values["Save As..."]
                if filename[-4:] != 'json':
                    filename = filename + '.json'
                process_data(filename, values, cbox_order)

        elif event == 0:
            cbox_order = []
            if values[0] == 'User':
                window.Element('users').Update(disabled=True)
                window.Element('sources').Update(disabled=False)
                window.Element('users').Update(value=False)
                window.Element('sources').Update(value=False)
                window.Element('size users').Update(value=False)
                window.Element('size users').Update(disabled=True)
                window.Element('size sources').Update(disabled=True)
                window.Element('size sources').Update(value=False)
                for k, sk in zip(addrs_keys, size_keys):
                    window.Element(k).Update(disabled=False)
                    window.Element(k).Update(value=False)
                    window.Element(sk).Update(value=False)
                    window.Element(sk).Update(disabled=True)
            if values[0] == 'Address':
                window.Element('users').Update(value=False)
                window.Element('users').Update(disabled=False)
                window.Element('sources').Update(value=False)
                window.Element('sources').Update(disabled=False)
                window.Element('size users').Update(value=False)
                window.Element('size users').Update(disabled=True)
                window.Element('size sources').Update(disabled=True)
                window.Element('size sources').Update(value=False)
                for k, sk in zip(addrs_keys, size_keys):
                    window.Element(k).Update(disabled=True)
                    window.Element(k).Update(value=False)
                    window.Element(sk).Update(disabled=True)
                    window.Element(sk).Update(value=False)
            if values[0] == 'Source':
                window.Element('users').Update(value=False)
                window.Element('users').Update(disabled=False)
                window.Element('sources').Update(value=False)
                window.Element('sources').Update(disabled=True)
                window.Element('size users').Update(value=False)
                window.Element('size users').Update(disabled=True)
                window.Element('size sources').Update(disabled=True)
                window.Element('size sources').Update(value=False)
                for k, sk in zip(addrs_keys, size_keys):
                    window.Element(k).Update(disabled=False)
                    window.Element(k).Update(value=False)
                    window.Element(sk).Update(disabled=True)
                    window.Element(sk).Update(value=False)

        elif event in addrs_keys or event == 'users' or event == 'sources':
            if values[event]:
                cbox_order.append(event)
                window.Element('size ' + event).Update(disabled=False)
            else:
                cbox_order.remove(event)
                window.Element('size ' + event).Update(value=False)
                window.Element('size ' + event).Update(disabled=True)

    window.Close()


def process_data(filename, values, cbox_order):
    """
    Process data returned by the GUI
    :param filename: filename as the output of data
    :param values: values of the dict returned by GUI
    :param cbox_order: array containing the sort order of fields
    :return:
    """
    pipeline = pipelines.pipelines
    if values[0] == 'User':
        if cbox_order.__len__() != 0:
            pipe = pipeline[0]
            for a in cbox_order:
                pipe[9]["$project"][a] = 1
                pipe[9]["$project"]["or"]["$or"].append({"$size": "$" + a})
                pipe[10]["$sort"]["size " + a] = -1
                if values["size " + a]:
                    del pipe[12]["$project"]["size " + a]
            execute_query(pipe, filename)
    if values[0] == 'Address':
        print()
    if values[0] == 'Source':
        print()


def execute_query(pipeline, file):
    """
    Connects with the MongoDB database, takes the pipeline and executes the query,
    if pipeline is empty executes a 'find' query
    :param pipeline: array containing the pipeline of commands for the aggregation framework of MongoDB
    :param file: filename as the output of data
    :return:
    """
    print(pipeline)
    database = None
    try:
        connection = MongoClient('mongodb://localhost:27017')
        database = connection['research']
    except ConnectionError:
        connection = None
        logging.error("Unable to connect")

    if connection:
        doc = list(database['data'].aggregate(pipeline))
        with open(file, "w+") as jsonfile:
            json.dump(doc, jsonfile, indent=4, default=json_util.default)


if __name__ == '__main__':
    main()
