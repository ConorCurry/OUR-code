import uno

localContext = uno.getComponentContext()
resolver = localContext.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", localContext )
ctx = resolver.resolve( "uno:socket,host=localhost,port=2002;urp;StarOffice.ComponentContext" )
smgr = ctx.ServiceManager
desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
model = desktop.getCurrentComponent()
active_sheet = model.CurrentController.ActiveSheet


cols = ['S', 'T', 'U', 'V', 'W', 'X']
rows = [i for i in range(2, 213)]
bolded_names = []
for col in cols:
    for row in rows:
        cellID = col + str(row)
        cell = active_sheet.getCellRangeByName(cellID)
        if cell.CharWeight > 100:
            bolded_names.append(cell.String.strip().split())
bolded_names.sort(key = lambda name: name[-1])
bolded_names = [name[-1] + ', ' + ' '.join(name[:-1]) +'\n' for name in bolded_names]
with open("boldedNames.txt", "w") as out:
    out.writelines(bolded_names)
    
remaining_names = bolded_names
while True:
    search_substring = input("Enter your search string: ")
    results = [name for name in bolded_names if search_substring.lower().strip() in name.lower()]
    [print("{}. {}".format(i, res)) for i, res in enumerate(results)]
    if len(results) == 1:
        remaining_names.remove(results[0])
        continue
    selection = input("Select one or type none, or done: ")
    if selection == "none":
        pass
    elif selection == "done":
        break
    else:
        try:
            remaining_names.remove(results[int(selection)])
        except:
            print("invalid entry")
            continue
with open("namesNotFound.txt", "w") as out:
    out.writelines(remaining_names)

print("Done!")
