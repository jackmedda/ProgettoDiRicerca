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
    group_addr = ['Bitcoin address', 'Ethereum address', 'BitcoinCash address', 'Litecoin address',
                  'Dogecoin address', 'Dash address', 'BitcoinSV address', 'Monero address']

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
        [sg.Combo(('User', 'Address', 'Source'), size=(20, 1), enable_events=True)],
    ]

    for x in group_addr:
        col2.append([sg.Checkbox(x, enable_events=True, disabled=True, key=x)])

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

    def save_action(values, cbox_order, addrs_keys, group_addr):
        filename = values["Save As..."]
        if filename[-4:] != 'json':
            filename = filename + '.json'
        process_data(filename, values, cbox_order, addrs_keys, group_addr)

    while True:
        event, values = window.Read()
        print(event, values)
        if event is None or event == 'Exit':
            break

        elif event == 'Save As...':
            if values["Save As..."] != "":
                if cbox_order.__len__() != 0:
                    if values[0] == 'Address':
                        one_checked = False
                        for x in group_addr:
                            if values[x]:
                                one_checked = True
                                break
                        if one_checked:
                            save_action(values, cbox_order, addrs_keys, group_addr)
                        else:
                            sg.PopupError('No parameters specified for the address group by')
                    else:
                        save_action(values, cbox_order, addrs_keys, group_addr)
                else:
                    sg.PopupError('No parameters specified for the query')

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
                for k, sk, addr in zip(addrs_keys, size_keys, group_addr):
                    window.Element(k).Update(disabled=False)
                    window.Element(k).Update(value=False)
                    window.Element(sk).Update(value=False)
                    window.Element(sk).Update(disabled=True)
                    window.Element(addr).Update(value=False)
                    window.Element(addr).Update(disabled=True)

            if values[0] == 'Address':
                window.Element('users').Update(value=False)
                window.Element('users').Update(disabled=False)
                window.Element('sources').Update(value=False)
                window.Element('sources').Update(disabled=False)
                window.Element('size users').Update(value=False)
                window.Element('size users').Update(disabled=True)
                window.Element('size sources').Update(disabled=True)
                window.Element('size sources').Update(value=False)
                for k, sk, addr in zip(addrs_keys, size_keys, group_addr):
                    window.Element(k).Update(disabled=False)
                    window.Element(k).Update(value=False)
                    window.Element(sk).Update(disabled=True)
                    window.Element(sk).Update(value=False)
                    window.Element(addr).Update(value=False)
                    window.Element(addr).Update(disabled=False)

            if values[0] == 'Source':
                window.Element('users').Update(value=False)
                window.Element('users').Update(disabled=False)
                window.Element('sources').Update(value=False)
                window.Element('sources').Update(disabled=True)
                window.Element('size users').Update(value=False)
                window.Element('size users').Update(disabled=True)
                window.Element('size sources').Update(disabled=True)
                window.Element('size sources').Update(value=False)
                for k, sk, addr in zip(addrs_keys, size_keys, group_addr):
                    window.Element(k).Update(disabled=False)
                    window.Element(k).Update(value=False)
                    window.Element(sk).Update(disabled=True)
                    window.Element(sk).Update(value=False)
                    window.Element(addr).Update(value=False)
                    window.Element(addr).Update(disabled=True)

        elif event in addrs_keys or event == 'users' or event == 'sources':
            if values[event]:
                cbox_order.append(event)
                window.Element('size ' + event).Update(disabled=False)
                if values[0] == 'Address':
                    if event != 'users' and event != 'sources':
                        cbox = group_addr[addrs_keys.index(event)]
                        window.Element(cbox).Update(disabled=True)
            else:
                cbox_order.remove(event)
                window.Element('size ' + event).Update(value=False)
                window.Element('size ' + event).Update(disabled=True)
                if values[0] == 'Address':
                    if event != 'users' and event != 'sources':
                        cbox = group_addr[addrs_keys.index(event)]
                        window.Element(cbox).Update(disabled=False)

        elif event in group_addr:
            cbox = addrs_keys[group_addr.index(event)]
            if values[event]:
                window.Element(cbox).Update(disabled=True)
            else:
                window.Element(cbox).Update(disabled=False)

    window.Close()


def process_data(filename, values, cbox_order, addrs_keys, group_addr):
    """
    Process data returned by the GUI
    :param filename: filename as the output of data
    :param values: values of the dict returned by GUI
    :param cbox_order: array containing the sort order of fields
    :return:
    """
    pipeline = pipelines.pipelines
    pipe = []
    print(pipe)

    if values[0] == 'User':
        for _dict in pipeline[0]:
            pipe.append(_dict.copy())
        for a in cbox_order:
            pipe[9]["$project"][a] = 1
            pipe[9]["$project"]["or"]["$or"].append({"$size": "$" + a})
            pipe[10]["$sort"]["size " + a] = -1
            if values["size " + a]:
                del pipe[12]["$project"]["size " + a]

    elif values[0] == 'Address':
        for _dict in pipeline[1]:
            pipe.append(_dict.copy())
        unwind_dict = []
        for a in cbox_order:
            if a == 'users':
                field = "Name"
            elif a == 'sources':
                field = "Source"
            else:
                field = group_addr[addrs_keys.index(a)]
                unwind_dict.append({"$unwind": {"path": "$data." + group_addr[addrs_keys.index(a)],
                                                "preserveNullAndEmptyArrays": True}})

            pipe[0]["$group"][a] = {"$addToSet": "$data." + field}
            pipe[1]["$project"][a] = 1
            pipe[1]["$project"]["size " + a] = {"$size": "$" + a}
            pipe[1]["$project"]["or"]["$or"].append({"$size": "$" + a})
            pipe[2]["$sort"]["size " + a] = -1
            if not values["size " + a]:
                pipe[4]["$project"]["size " + a] = 0

        for a in group_addr:
            if values[a]:  # if equals to True
                pipe[0]["$group"]["_id"][a] = "$data." + a
                pipe[1]["$project"][a] = "$_id." + a
                unwind_dict.append({"$unwind": {"path": "$data." + a}})
        for u in unwind_dict:
            pipe.insert(0, u)

    elif values[0] == 'Source':
        print()

    execute_query(pipe, filename)


def execute_query(pipeline, file):
    """
    Connects with the MongoDB database, takes the pipeline and executes the query,
    if pipeline is empty executes a 'find' query
    :param pipeline: array containing the pipeline of commands for the aggregation framework of MongoDB
    :param file: filename as the output of data
    :return:
    """
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
