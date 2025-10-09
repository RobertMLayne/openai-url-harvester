# Test OAuth Token Scope - Run After Token Update

Write-Host "🔍 TESTING OAUTH TOKEN SCOPE" -ForegroundColor Cyan
Write-Host "============================" -ForegroundColor Cyan

# Test in openai-url-harvester (current project)
$testRepo = "C:\dev\Projects\openai-url-harvester"
Set-Location $testRepo

Write-Host "`n📍 Testing in: $(Split-Path $testRepo -Leaf)" -ForegroundColor Blue

# Test 1: Check current branch and status
Write-Host "`n🔍 Step 1: Repository Status" -ForegroundColor Yellow
$currentBranch = git branch --show-current
$status = git status --porcelain
Write-Host "Current branch: $currentBranch" -ForegroundColor White
if ($status)
{
    Write-Host "Status: Has uncommitted changes" -ForegroundColor Yellow
}
else
{
    Write-Host "Status: Clean working directory" -ForegroundColor Green
}

# Test 2: Attempt push
Write-Host "`n🚀 Step 2: Testing Push Capability" -ForegroundColor Yellow
Write-Host "Attempting to push to origin..." -ForegroundColor White

try
{
    $pushResult = git push origin HEAD 2>&1 | Out-String

    if ($LASTEXITCODE -eq 0)
    {
        Write-Host "✅ SUCCESS: Push completed successfully!" -ForegroundColor Green
        Write-Host "OAuth token scope is working correctly." -ForegroundColor Green
        $tokenWorking = $true
    }
    else
    {
        Write-Host "❌ FAILED: Push failed" -ForegroundColor Red
        Write-Host "Error details:" -ForegroundColor Yellow
        Write-Host "$pushResult" -ForegroundColor White

        if ($pushResult -like "*403*" -or $pushResult -like "*token*" -or $pushResult -like "*permission*")
        {
            Write-Host "`n💡 This looks like a token scope issue." -ForegroundColor Cyan
            Write-Host "Please verify your token has 'workflow' scope enabled." -ForegroundColor Cyan
        }
        $tokenWorking = $false
    }
}
catch
{
    Write-Host "❌ ERROR: Push test failed" -ForegroundColor Red
    Write-Host "Error: $($_.Exception.Message)" -ForegroundColor White
    $tokenWorking = $false
}

# Test 3: If working, prepare for full migration push
Write-Host "`n📊 Step 3: Next Actions" -ForegroundColor Yellow

if ($tokenWorking)
{
    Write-Host "✅ Token scope is working!" -ForegroundColor Green
    Write-Host "`n🚀 READY FOR FULL LFS MIGRATION PUSH:" -ForegroundColor Magenta
    Write-Host "- All 11 projects are LFS-ready" -ForegroundColor White
    Write-Host "- Backup branches created for safety" -ForegroundColor White
    Write-Host "- ~860MB will be moved to LFS storage" -ForegroundColor White
    Write-Host "`n💡 Ready to proceed with full push? (Y/N)" -ForegroundColor Cyan
}
else
{
    Write-Host "⚠️  Token scope needs attention" -ForegroundColor Yellow
    Write-Host "`n🔧 TROUBLESHOOTING STEPS:" -ForegroundColor Magenta
    Write-Host "1. Check token scopes at: https://github.com/settings/tokens" -ForegroundColor White
    Write-Host "2. Ensure 'workflow' scope is checked ✅" -ForegroundColor Green
    Write-Host "3. Clear git credentials if needed:" -ForegroundColor White
    Write-Host "   git config --global --unset credential.helper" -ForegroundColor Gray
    Write-Host "4. Try pushing again with new token" -ForegroundColor White
}

Write-Host "`n⏰ Test completed at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Blue
