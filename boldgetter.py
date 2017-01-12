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
with open("boldedNames.txt", "w") as out:
    out.writelines(bolded_names)
    
print("Done!")
