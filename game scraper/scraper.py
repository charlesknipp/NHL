import requests

url = requests.get("http://www.nhl.com/scores/htmlreports/20202021/GS020151.HTM")
raw_html = url.text

html = raw_html.split("\n")

for i in range(len(html)):
    if "Goal Scorer" in html[i]:
        idx = i-7
        break

table = []
row = []

while True:
    item = html[idx]

    if "<td" in item:
        row.append(item[item.find(">")+1:item.find("</")].strip())
    elif "</tr>" in item:
        table.append(row)
        row = []

    # this extracts the text from the table
    item_text = item[item.find(">")+1:item.find("</")].strip()
    if item_text != "":
        print(item_text)

    # this condition breaks the while loop
    if "</table>" in item:
        break

    # iteration over list index
    idx += 1


print(table)