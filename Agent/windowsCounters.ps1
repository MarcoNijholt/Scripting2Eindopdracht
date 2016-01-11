$memory = Get-WmiObject win32_OperatingSystem |%{"`"totalMem`": `"{0}`", `"freeMem`": `"{1}`"" -f ($_.totalvisiblememorysize / 1KB), ($_.freephysicalmemory / 1KB)}
$diskspace = Get-CimInstance Win32_LogicalDisk | where Caption -eq "C:" | %{"`"size`": `"{0}`", `"free`": `"{1}`"" -f ($_.Size / 1MB), ($_.FreeSpace / 1MB)}
$ipaddresses = Get-WMIObject win32_NetworkAdapterConfiguration | Where-Object { $_.IPEnabled -eq $true } | Foreach-Object { $_.IPAddress } | Foreach-Object { [IPAddress]$_ } | Where-Object { $_.AddressFamily -eq 'Internetwork'  } | %{"`"{0}`"," -f $_.IPAddressToString} | out-string
$ipaddresses = $ipaddresses -replace "`n","" -replace "`r",""
$ipaddresses = $ipaddresses.subString(0,$ipaddresses.length-1);
$osdata = Get-WmiObject win32_operatingsystem
$uptime = (Get-Date) - ($osdata.convertToDateTime($osdata.lastbootuptime))
$proccount =  ps | measure-object | select -expandproperty count
Write-Host "{`"memory`": { $($memory) }, `"disk`": {$($diskspace)}, `"ips`": [$($ipaddresses)], `"uptime`": `"$($uptime)`", `"proccount`": $($proccount) }";