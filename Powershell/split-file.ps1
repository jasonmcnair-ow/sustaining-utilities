# Get the input file name and number of files from the command line arguments
$inputFile = $args[0]
$numberOfFiles = [int]$args[1]

# Read the input file
$lines = Get-Content $inputFile

# Split the header row and data rows
$headerRow = $lines[0]
$dataRows = $lines[1..($lines.Count - 1)]

# Calculate the number of lines per output file (excluding the header row)
$linesPerFile = [math]::Floor(($dataRows.Count) / $numberOfFiles)

# Split the data rows into multiple output files
for ($i = 0; $i -lt $numberOfFiles; $i++) {
    $startIndex = $i * $linesPerFile
    $endIndex = $startIndex + $linesPerFile - 1
    if ($i -eq ($numberOfFiles - 1)) {
        $endIndex = $dataRows.Count - 1
    }
    $outputData = $dataRows[$startIndex..$endIndex]

    # Add a newline character between each line
    $outputData = $outputData -join "`r`n"

    # Add the header row to each output file
    $outputData = $headerRow + "`r`n" + $outputData

    # Generate the output file name with leading zeros
    $outputNumber = $i.ToString().PadLeft(8, '0')
    $outputFile = "output_$outputNumber.txt"

    # Export the output data to a file in UTF-8 format
    $outputData | Out-File -Encoding UTF8 $outputFile
}
