import json
import collections

nested_data = {}

deleted_post = {
        "subject": "[deleted]",
        "author": "[unknown]",
        "data": "",
        "link": "none",
        "parent": "-1",
        "post":"[removed]",
        "replies": {}
    }

def load_file(file_name):
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)

def loopjson(jsondata):
    for i in jsondata:
        # // if there is a parent
        if 'parent' not in jsondata[i].keys():
            print(f'Missing parent for postid {i}')
            continue
        if jsondata[i]['parent'] != "-1":
            p = jsondata[i]['parent']
            # if we haven't loaded the parent yet:
            if p not in nested_data:
                # load the parent if we have it
                if p in jsondata:
                    nested_data[p] = jsondata[p]
                    nested_data[p]['replies'] = {}
                else:
                    print(f"missing post id {p}")
                    nested_data[p] = deleted_post
            # append this child to its parent
            nested_data[p]['replies'][i] = jsondata[i]
            #remove from root
            if i in nested_data:
                del nested_data[i]
        else: 
            nested_data[i] = jsondata[i]
            nested_data[i]['replies'] = {}

def save(data):
    with open('nested_data_sorted.json', "w",encoding="utf-8") as file:
            json.dump(data,file,indent=4)

# jd = load_file("test.json")
jd = load_file("updated_data.json")
loopjson(jd)
# convert keys to int in order to sort non-alpha numeric
nested_data_int = {int(k):v for k,v in nested_data.items()}
nested_data_sort = collections.OrderedDict(sorted(nested_data_int.items()))
save(nested_data_sort)

