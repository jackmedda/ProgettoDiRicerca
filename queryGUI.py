# This software is distributed under MIT/X11 license
# Copyright (c) 2019 Giacomo Medda - University of Cagliari
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import json
from pymongo import MongoClient
from bson import json_util
import PySimpleGUI as sg
import logging
import queries
import copy
from addrfilter import findalladdresses


def main():
    gui()


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
    input_keys = ['InputUser', 'InputAddr', 'InputSource', 'InputCustom']

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
        [sg.Combo(('User', 'Address', 'Source'), size=(20, 1), enable_events=True, text_color='white')],
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

    tab1_layout = [
        [sg.Text('Deanonomity Addresses Query Selector', font=('Helvetica', 16))],
        [sg.Column(col1, size=(200, 380)),
         sg.VerticalSeparator(),
         sg.Column(col2),
         sg.VerticalSeparator(),
         sg.Column(col3)],
        [sg.Text('Preserve null and empty arrays of groups?', font=('Helvetica', 12)),
         sg.Checkbox('', key='preserve_null')],
        [sg.Text('Results are added to a set, then sorted in descending order and'
                 ' with respect to order of checks of checkboxes', font=('Helvetica', 8))]
    ]

    tab2_col1 = [
        [sg.Text('')],
        [sg.Text('Find data of ', font=('Helvetica', 18, 'bold'))]
    ]

    tab2_col2 = [
        [sg.Text('User', font=('Helvetica', 14), size=(7, 1), justification='left'),
         sg.InputText(justification='left', key=input_keys[0])],
        [sg.Text('Address', font=('Helvetica', 14), size=(7, 1), justification='left'),
         sg.InputText(justification='left', key=input_keys[1])],
        [sg.Text('Source', font=('Helvetica', 14), size=(7, 1), justification='left'),
         sg.InputText(justification='left', key=input_keys[2])]
    ]

    tab2_layout = [
        [sg.Text('', size=(1, 3))],
        [sg.Column(tab2_col1), sg.Column(tab2_col2)],
        [sg.Text('', size=(1, 3))],
        [sg.Text('Custom find (query for other fields inside object "data")', font=('Helvetica', 14),
                 justification='center', size=(300, 1))],
        [sg.Text('Ex -> Location %% United States', font=('Helvetica', 9), justification='center', size=(300, 1))],
        [sg.Text("To query for multiple custom fields "
                 "separate them with ' $$ '", font=('Helvetica', 14), justification='center', size=(300, 1))],
        [sg.Text("Ex -> Location %% United States $$ Signature %% I am American",
                 font=('Helvetica', 9), justification='center', size=(300, 1))],
        [sg.Text('', size=(1, 1))],
        [sg.Text('', size=(22, 1)), sg.InputText(justification='left', size=(50, 1), key=input_keys[3])]
    ]

    layout = [[sg.TabGroup([[sg.Tab('Group by', tab1_layout),
                             sg.Tab('Find', tab2_layout)]], title_color='#071833', key='Tab')],
              [sg.SaveAs(file_types=(("JSON", ".json"),), enable_events=True)],
              [sg.Exit()]]

    window = sg.Window('Query Selector', layout, font=("Helvetica", 12), size=(950, 600))

    cbox_order = []

    def save_action(_values, **kwargs):
        """
        Takes the filename, adds ".json" at the end if not present
        :param _values: dictionary containing the values of the GUI
        :param kwargs: args useful to process data with aggregation ('group by') query
        :return:
        """
        filename = _values["Save As..."]
        if filename[-4:] != 'json':
            filename = filename + '.json'
        if values['Tab'] == 'Group by':
            process_data(filename, _values, **kwargs, preserve_null=values['preserve_null'])
        elif values['Tab'] == 'Find':
            process_data(filename, _values)

    while True:
        event, values = window.Read()

        if event is None or event == 'Exit':
            break

        elif values['Tab'] == 'Group by':
            if event == 'Save As...':
                if values["Save As..."] != "":
                    if cbox_order.__len__() != 0:
                        if values[0] == 'Address':
                            one_checked = False
                            for x in group_addr:
                                if values[x]:
                                    one_checked = True
                                    break
                            if one_checked:
                                save_action(values, cbox_order=cbox_order, addrs_keys=addrs_keys, group_addr=group_addr)
                            else:
                                sg.PopupError('No parameters specified for the address group by')
                        else:
                            save_action(values, cbox_order=cbox_order, addrs_keys=addrs_keys, group_addr=group_addr)
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

        elif values['Tab'] == 'Find':
            if event == 'Save As...':
                if values["Save As..."] != "":
                    if True not in [bool(values[x].strip()) for x in input_keys]:  # if all strings are empty
                        sg.PopupError('No parameters specified for the query, all inputs are empty')
                    else:
                        save_action(values)

    window.Close()


def process_data(filename, values, **kwargs):
    """
    Process data returned by the GUI
    :param filename: filename as the output of data
    :param values: values of the dict returned by GUI
    :param kwargs:
            cbox_order: array containing the sort order of fields
            addrs_keys: array containing the fields of addresses
            group_addr: array containing the fields of addresses by which data are grouped
            preserve_null; a boolean to preserve Null or Empty arrays or not
    :return:
    """
    cbox_order = kwargs.get('cbox_order')
    addrs_keys = kwargs.get('addrs_keys')
    group_addr = kwargs.get('group_addr')
    preserve_null = kwargs.get('preserve_null')

    query = copy.deepcopy(queries.queries)

    if values['Tab'] == 'Group by':
        # It is called pipeline because of the aggregation framework
        pipeline = query[0]
        unwind_dict = []

        if values[0] != 'Address':
            field_group = "Name" if values[0] == 'User' else 'Source'
            pipeline[0]["$group"]["_id"][values[0]] = "$data." + field_group
            pipeline[1]["$project"][values[0]] = "$_id." + values[0]

        for a in cbox_order:
            if a == 'users':
                field = "Name"
            elif a == 'sources':
                field = "Source"
            else:
                field = group_addr[addrs_keys.index(a)]
                unwind_dict.append({"$unwind": {"path": "$data." + group_addr[addrs_keys.index(a)],
                                                "preserveNullAndEmptyArrays": preserve_null}})

            pipeline[0]["$group"][a] = {"$addToSet": "$data." + field}
            pipeline[1]["$project"][a] = 1
            pipeline[1]["$project"]["size " + a] = {"$size": "$" + a}
            pipeline[1]["$project"]["or"]["$or"].append({"$size": "$" + a})
            pipeline[2]["$sort"]["size " + a] = -1
            if not values["size " + a]:
                pipeline[4]["$project"]["size " + a] = 0

        if values[0] == 'Address':
            for a in group_addr:
                if values[a]:  # if equals to True
                    pipeline[0]["$group"]["_id"][a] = "$data." + a
                    pipeline[1]["$project"][a] = "$_id." + a
                    unwind_dict.append({"$unwind": {"path": "$data." + a}})

        for u in unwind_dict:
            pipeline.insert(0, u)

        execute_query('Aggregation', pipeline, filename)

    if values['Tab'] == 'Find':
        query = {}
        if values['InputUser'].strip():
            query['data.Name'] = values['InputUser'].strip()

        if values['InputAddr'].strip():
            result = findalladdresses(values['InputAddr'].strip())
            if result:
                query["$or"] = []
                for r in result:
                    query["$or"].append({"data." + r[0]: r[1]})
            else:
                sg.PopupError('Address not valid')
                return

        if values['InputSource'].strip():
            query['data.Source'] = values['InputSource'].strip()

        if values['InputCustom'].strip():
            inputs = values['InputCustom'].split('$$')
            for inp in inputs:
                vals = inp.split('%%')
                vals = [x.strip() for x in vals]
                in_check = [vals[1]]

                if (vals[1][0] in ['+', '-'] and vals[1][1:].isdigit()) or vals[1].isdigit():
                    in_check.append(int(vals[1]))

                if vals[1] == 'True' or vals[1] == 'true':
                    in_check.append(True)

                query['data.' + vals[0]] = {"$in": in_check}

        execute_query('Find', query, filename)


def execute_query(_type, query, file):
    """
    Connects with the MongoDB database, takes the query and executes it
    :param _type: type of query (Aggregation, Find, ...)
    :param query: array containing the queries for the database of MongoDB
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
        doc = []
        if _type == 'Aggregation':
            doc = list(database['data'].aggregate(query))
        elif _type == 'Find':
            doc = list(database['data'].find(query, {"_id": 0, "data": 1}))
        with open(file, "w+") as jsonfile:
            if doc:
                json.dump(doc, jsonfile, indent=4, default=json_util.default)


if __name__ == '__main__':
    main()
