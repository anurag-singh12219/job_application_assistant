# GitHub Pre-Commit Cleanup Script
# Run this before pushing to GitHub

Write-Host "=================================================="
Write-Host "  GitHub Pre-Commit Cleanup Script"
Write-Host "=================================================="
Write-Host ""

$projectRoot = Get-Location

# Step 1: Remove unnecessary documentation files
Write-Host "Step 1: Removing redundant documentation files..."
$filesToRemove = @(
    "COMPLETION_CHECKLIST.md",
    "FINAL_GUIDE.md", 
    "IMPROVEMENTS_SUMMARY.md"
)

foreach ($file in $filesToRemove) {
    $filePath = Join-Path $projectRoot $file
    if (Test-Path $filePath) {
        Remove-Item $filePath -Force
        Write-Host "  Removed: $file"
    }
}

# Step 2: Remove __pycache__ directories
Write-Host ""
Write-Host "Step 2: Removing Python cache files..."
Get-ChildItem -Path $projectRoot -Recurse -Directory -Filter "__pycache__" -ErrorAction SilentlyContinue | ForEach-Object {
    Remove-Item $_.FullName -Recurse -Force
    Write-Host "  Removed: $($_.FullName)"
}

# Step 3: Check for .env files
Write-Host ""
Write-Host "Step 3: Checking for API keys in files..."
Get-ChildItem -Path $projectRoot -Recurse -Filter ".env" -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host "  WARNING: Found .env at: $($_.FullName)"
    Write-Host "  Make sure this file is NOT committed to GitHub!"
}

# Step 4: Verify .env.example exists
Write-Host ""
Write-Host "Step 4: Verifying .env.example files..."
$requiredExamples = @(
    "backend\.env.example",
    "ai-frontend\.env.example"
)

foreach ($example in $requiredExamples) {
    $examplePath = Join-Path $projectRoot $example
    if (Test-Path $examplePath) {
        Write-Host "  Found: $example"
    } else {
        Write-Host "  Missing: $example"
    }
}

# Step 5: Summary
Write-Host ""
Write-Host "=================================================="
Write-Host "  Cleanup Complete! Next Steps:"
Write-Host "=================================================="
Write-Host ""
Write-Host "1. Review changes: git status"
Write-Host "2. Stage files: git add ."
Write-Host "3. Commit: git commit -m 'Challenge 2: AI Job Application Assistant'"
Write-Host "4. Push: git push origin main"
Write-Host ""
Write-Host "IMPORTANT REMINDERS:"
Write-Host "  - Verify .env is NOT in git (should be in .gitignore)"
Write-Host "  - API keys should only be in .env.example as placeholders"
Write-Host "  - Test the app one final time before pushing"
Write-Host ""
Write-Host "Documentation Files to Include:"
Write-Host "  README.md (main documentation)"
Write-Host "  ENGINEERING_DOCUMENTATION.md (algorithm proofs)"
Write-Host "  SUBMISSION_CHECKLIST.md (review panel response)"
Write-Host "  LICENSE (MIT license)"
Write-Host ""
Write-Host "Ready for GitHub!"
Write-Host ""

