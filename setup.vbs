Set objFSO = CreateObject("Scripting.FileSystemObject")
basePath = "C:\Users\pradheepa jaya shree\Desktop\neww\Time-Table-Scheduler"
dirs = Array("utils", "data", "agent", "tests")

For Each dirName In dirs
    dirPath = basePath & "\" & dirName
    If Not objFSO.FolderExists(dirPath) Then
        objFSO.CreateFolder(dirPath)
    End If
    
    initPath = dirPath & "\__init__.py"
    If Not objFSO.FileExists(initPath) Then
        objFSO.CreateTextFile(initPath)
    End If
    
    WScript.Echo "✓ Created: " & dirName & "/__init__.py"
Next

WScript.Echo ""
WScript.Echo "--- Directory Structure ---"
WScript.Echo ""

Set folder = objFSO.GetFolder(basePath)
For Each subFolder In folder.SubFolders
    If (subFolder.Name = "utils" Or subFolder.Name = "data" Or subFolder.Name = "agent" Or subFolder.Name = "tests") Then
        WScript.Echo "📁 " & subFolder.Name & "/"
        For Each file In subFolder.Files
            WScript.Echo "  📄 " & file.Name
        Next
    End If
Next

WScript.Echo ""
WScript.Echo "✓ Directory structure created successfully!"
