try {
    $sapGui = [System.Runtime.InteropServices.Marshal]::GetActiveObject("SAPGUI")
    $app = $sapGui.GetScriptingEngine()
    $conn = $app.Children(0)
    $sess = $conn.Children(0)
    Write-Host "CONNECTED TO SAP GUI!"
    Write-Host "System: $($sess.Info.SystemName)"
    Write-Host "Client: $($sess.Info.Client)"
    Write-Host "User: $($sess.Info.User)"
    Write-Host "Transaction: $($sess.Info.Transaction)"
} catch {
    Write-Host "Scripting error: $($_.Exception.Message)"
}
