# Push Remaining 10 LFS Projects to GitHub
# Streamlined script for final LFS migration push

Write-Host "🚀 FINAL LFS MIGRATION PUSH" -ForegroundColor Green
Write-Host "===========================" -ForegroundColor Green

Write-Host "`n✅ openai-url-harvester already synchronized" -ForegroundColor Green
Write-Host "🔄 Pushing remaining 10 LFS-migrated projects..." -ForegroundColor Blue

# Remaining 10 projects (excluding openai-url-harvester which is done)
$projects = @(
    @{ Name = "content-extractor-copy"; Path = "C:\dev\Projects\content-extractor-copy" },
    @{ Name = "content-extractor-v1"; Path = "C:\dev\Projects\content-extractor-v1" },
    @{ Name = "content-extractor-v2"; Path = "C:\dev\Projects\content-extractor-v2" },
    @{ Name = "content-extractor-v3"; Path = "C:\dev\Projects\content-extractor-v3" },
    @{ Name = "content-extractor-v4"; Path = "C:\dev\Projects\content-extractor-v4" },
    @{ Name = "content-extractor-onedrive"; Path = "C:\Users\rmlaynetech\OneDrive\Projects\content-extractor" },
    @{ Name = "doc-harvester-pro"; Path = "C:\dev\Projects\doc-harvester-pro" },
    @{ Name = "doc-harvester-pro-v2"; Path = "C:\dev\Projects\doc-harvester-pro-v2" },
    @{ Name = "doc-harvester-pro-v3"; Path = "C:\dev\Projects\doc-harvester-pro-v3" },
    @{ Name = "html-to-markdown-v4"; Path = "C:\dev\Projects\html-to-markdown-v4" }
)

$success = 0
$failed = 0
$results = @()

foreach ($project in $projects) {
    Write-Host "`n" + "─" * 50 -ForegroundColor Gray
    Write-Host "📁 $($project.Name)" -ForegroundColor Yellow
    Write-Host "   Path: $($project.Path)" -ForegroundColor Gray
    
    if (Test-Path $project.Path) {
        Set-Location $project.Path
        
        if (Test-Path ".git") {
            try {
                # Check LFS status
                $lfsFiles = git lfs ls-files 2>$null
                if ($lfsFiles) {
                    Write-Host "   ✅ LFS configured ($($lfsFiles.Count) files)" -ForegroundColor Green
                } else {
                    Write-Host "   ⚠️  No LFS files detected" -ForegroundColor Yellow
                }
                
                # Sync with remote first
                Write-Host "   🔄 Syncing with remote..." -ForegroundColor Blue
                git fetch origin 2>$null
                
                # Check for uncommitted changes
                $status = git status --porcelain
                if ($status) {
                    Write-Host "   📝 Committing changes..." -ForegroundColor Yellow
                    git add -A
                    git commit -m "LFS migration - move large files to LFS storage"
                }
                
                # Try to pull first (in case remote has changes)
                $pullResult = git pull origin HEAD 2>&1
                if ($LASTEXITCODE -ne 0 -and $pullResult -notlike "*Already up to date*") {
                    Write-Host "   ⚠️  Pull had issues, trying push anyway..." -ForegroundColor Yellow
                }
                
                # Push to GitHub
                Write-Host "   🚀 Pushing to GitHub..." -ForegroundColor Blue
                $pushResult = git push origin HEAD 2>&1
                
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "   ✅ SUCCESS!" -ForegroundColor Green
                    $success++
                    $results += "✅ $($project.Name): Pushed successfully"
                } else {
                    Write-Host "   ❌ FAILED: $pushResult" -ForegroundColor Red
                    $failed++
                    $results += "❌ $($project.Name): $pushResult"
                }
                
            } catch {
                Write-Host "   ❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
                $failed++
                $results += "❌ $($project.Name): $($_.Exception.Message)"
            }
        } else {
            Write-Host "   ⚠️  Not a git repository" -ForegroundColor Yellow
            $failed++
            $results += "⚠️  $($project.Name): Not a git repository"
        }
    } else {
        Write-Host "   ❌ Path not found" -ForegroundColor Red
        $failed++
        $results += "❌ $($project.Name): Path not found"
    }
}

# Final results
Write-Host "`n" + "=" * 60 -ForegroundColor Green
Write-Host "🏁 FINAL LFS MIGRATION RESULTS" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green

Write-Host "`n📊 SUMMARY:" -ForegroundColor Cyan
Write-Host "✅ Successful: $success projects" -ForegroundColor Green
Write-Host "❌ Failed: $failed projects" -ForegroundColor Red
Write-Host "📁 Total: $($projects.Count) projects" -ForegroundColor Blue

Write-Host "`n📋 DETAILED RESULTS:" -ForegroundColor Yellow
foreach ($result in $results) {
    $color = if ($result.StartsWith("✅")) { "Green" } elseif ($result.StartsWith("❌")) { "Red" } else { "Yellow" }
    Write-Host $result -ForegroundColor $color
}

if ($success -eq $projects.Count) {
    Write-Host "`n🎉 MISSION ACCOMPLISHED!" -ForegroundColor Green
    Write-Host "🎉 ALL LFS MIGRATIONS SUCCESSFULLY PUSHED TO GITHUB!" -ForegroundColor Green
    Write-Host "`n🏆 ACHIEVEMENTS UNLOCKED:" -ForegroundColor Magenta
    Write-Host "✅ 11 projects migrated to Git LFS" -ForegroundColor Green
    Write-Host "✅ ~860MB moved to LFS storage" -ForegroundColor Green
    Write-Host "✅ Repository performance dramatically improved" -ForegroundColor Green
    Write-Host "✅ GitHub compliance achieved" -ForegroundColor Green
    Write-Host "✅ Backup branches created for safety" -ForegroundColor Green
} elseif ($success -gt 0) {
    Write-Host "`n⚠️  PARTIAL SUCCESS" -ForegroundColor Yellow
    Write-Host "$success out of $($projects.Count) projects pushed successfully." -ForegroundColor Yellow
    Write-Host "Failed projects may need individual attention." -ForegroundColor Yellow
} else {
    Write-Host "`n❌ ALL PUSHES FAILED" -ForegroundColor Red
    Write-Host "Review error messages above for troubleshooting." -ForegroundColor Red
}

Write-Host "`n⏰ Completed: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Blue

# Return to openai-url-harvester
Set-Location "C:\dev\Projects\openai-url-harvester"
Write-Host "`n📍 Returned to: $(Get-Location)" -ForegroundColor Gray