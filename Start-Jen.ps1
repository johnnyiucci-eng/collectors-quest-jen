param([string]$Session = 'johnny-main', [switch]$Check)
$ErrorActionPreference = 'Stop'
Push-Location -LiteralPath $PSScriptRoot
$jenKeyWasPrompted = $false
try {
    if ($Check) {
        python -m jen_agent --check
    } else {
        if (-not $env:OPENAI_API_KEY) {
            Write-Host 'Enter your OpenAI API key privately. It will be used only for this process and will not be saved to disk.'
            $jenSecureKey = Read-Host 'API key' -AsSecureString
            $jenKeyPointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($jenSecureKey)
            try {
                $env:OPENAI_API_KEY = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($jenKeyPointer)
                $jenKeyWasPrompted = $true
            } finally {
                [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($jenKeyPointer)
                $jenSecureKey.Dispose()
            }
        }
        python -m jen_agent --session $Session
    }
} finally {
    if ($jenKeyWasPrompted) { Remove-Item Env:OPENAI_API_KEY -ErrorAction SilentlyContinue }
    Pop-Location
}
