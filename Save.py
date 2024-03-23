import adsk, adsk.core, adsk.fusion, adsk.cam, traceback, Document
from .lib import fusion360utils as futil
from pprint import pprint

app = adsk.core.Application.get()
ui = app.userInterface

WORKSPACE_ID = 'FusionSolidEnvironment'
CMD_ID = "SaveOnLocalDrive"

_handlers = []

files = {}
documentFilePath = ""

def application_documentOpening(args: adsk.core.DocumentEventArgs):
    global documentFilePath
    documentFilePath = args.fullPath

def application_documentOpened(args: adsk.core.DocumentEventArgs):
    file = {}
    file["name"] = documentFilePath.split('/').pop()
    file["path"] = documentFilePath
    files[app.activeDocument.creationId] = file


### Save Menu
def addSaveMenuOption():
    cmdDef = ui.commandDefinitions.itemById(CMD_ID)
    
    if not cmdDef:
        cmdDef = ui.commandDefinitions.addButtonDefinition(CMD_ID, "Save on local drive", "", "resources_saveFile")
    
    onCommandCreated = saveFile()
    cmdDef.commandCreated.add(onCommandCreated)
    _handlers.append(onCommandCreated)
    
    # Originaler Save Button löschen
    #if ui.toolbars.itemById('QAT').controls.itemById("PLM360SaveCommand"): 
    #    ui.toolbars.itemById('QAT').controls.itemById("PLM360SaveCommand").deleteMe()
    
    # Neuer löschen, falls schon da
    if ui.toolbars.itemById('QAT').controls.itemById(CMD_ID): 
        ui.toolbars.itemById('QAT').controls.itemById(CMD_ID).deleteMe()
    
    # Neuer ins QAT Menu
    ui.toolbars.itemById('QAT').controls.addCommand(cmdDef, 'OpenDocumentCommand')

    # Neuer ins Menu
    fileDropDown = ui.toolbars.itemById('QAT').controls.itemById('FileSubMenuCommand')
    control = fileDropDown.controls.addCommand(cmdDef, 'ExportCommand', True)


class saveFile(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, eventArgs: adsk.core.CommandCreatedEventArgs) -> None:
        if app.activeDocument.creationId in files:
            
            file = files[app.activeDocument.creationId]
            
            design = adsk.fusion.Design.cast(app.activeProduct)
            option = design.exportManager.createFusionArchiveExportOptions(file["path"], design.rootComponent)
            design.exportManager.execute(option)
            
            ui.messageBox('Gespeichert unter: \n"' + file["path"] + '"', 'Gespeichert!')
            
        else:            
            filedlg = ui.createFileDialog()
            filedlg.initialDirectory = '~'
            filedlg.filter = '*.f3d'
            if filedlg.showSave() == adsk.core.DialogResults.DialogOK:
                design = adsk.fusion.Design.cast(app.activeProduct)
                option = design.exportManager.createFusionArchiveExportOptions(filedlg.filename, design.rootComponent)
                design.exportManager.execute(option)
                
                ui.messageBox('Gespeichert unter: \n"' + filedlg.filename + '"', 'Gespeichert!')
                
                file = {}
                file["name"] = filedlg.filename.split('/').pop()
                file["path"] = filedlg.filename
                files[app.activeDocument.creationId] = file
                app.activeDocument.name = file["name"].split(".f3d")[0]           

### OPEN MENU
def addOpenMenuOption():
    id = "OpenLocalFile"
    
    cmdDef = ui.commandDefinitions.itemById(id)
    
    if not cmdDef:
        cmdDef = ui.commandDefinitions.addButtonDefinition(id, "Open local File", "", "resources_openFile")
    
    onCommandCreated = openFile()
    cmdDef.commandCreated.add(onCommandCreated)
    _handlers.append(onCommandCreated)
    
    # Neuer löschen, falls schon da
    if ui.toolbars.itemById('QAT').controls.itemById(id): 
        ui.toolbars.itemById('QAT').controls.itemById(id).deleteMe()
    # Neuer ins QAT Menu
    ui.toolbars.itemById('QAT').controls.addCommand(cmdDef, CMD_ID)
    
class openFile(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()
    def notify(self, eventArgs: adsk.core.CommandCreatedEventArgs) -> None:
        filedlg = ui.createFileDialog()  
        filedlg.initialDirectory = '~'
        filedlg.filter = '*.f3d'
        if filedlg.showOpen() == adsk.core.DialogResults.DialogOK:
            importManager = app.importManager
            archiveOptions = importManager.createFusionArchiveImportOptions(filedlg.filename)
            importManager.importToNewDocument(archiveOptions)
            
            file = {}
            file["name"] = filedlg.filename.split('/').pop()
            file["path"] = filedlg.filename
            files[app.activeDocument.creationId] = file
            app.activeDocument.name = file["name"].split(".f3d")[0]


### RUN
def run(context):    
    global _handlers
    
    addSaveMenuOption()
    addOpenMenuOption()
    
    futil.add_handler(app.documentOpening, application_documentOpening, local_handlers=_handlers)
    futil.add_handler(app.documentOpened, application_documentOpened, local_handlers=_handlers)
    

def stop(context):
    global _handlers
    _handlers = []

    try:
        ui.commandDefinitions.itemById(CMD_ID).deleteMe()
    except:
        pass

    qat = ui.toolbars.itemById('QAT')
    fileDropDown = qat.controls.itemById('FileSubMenuCommand')
    try:
        fileDropDown.controls.itemById(CMD_ID).deleteMe()
    except:
        pass
