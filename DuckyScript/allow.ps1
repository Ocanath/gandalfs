#This script must be run in an administrator powershell

# Define the path to the executable you want to exclude
$executablePath = "C:\path\to\your\executable.exe"

# Add the exclusion for the specified executable
Add-MpPreference -ExclusionProcess $executablePath


# Output the added exclusions for verification
Get-MpPreference | Select-Object -ExpandProperty ExclusionProcess
Get-MpPreference | Select-Object -ExpandProperty ExclusionPath