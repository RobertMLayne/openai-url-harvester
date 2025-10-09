# Push All LFS Migrations to GitHub
# Pushes all 11 LFS-migrated projects to their GitHub repositories

Write-Host "🚀 PUSHING ALL LFS MIGRATIONS TO GITHUB" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green

# Define all projects that were LFS migrated
$projects = @(
    # Priority 1: Content Extractors (6 projects)
    @{
        Name = "content-extractor-copy"
        Path = "C:\dev\Projects\content-extractor-copy"
        LFSPatterns = "*.html,*.json"
    },
    @{
        Name = "content-extractor-v1"
        Path = "C:\dev\Projects\content-extractor-v1"
        LFSPatterns = "*.html,*.json"
    },
    @{
        Name = "content-extractor-v2"
        Path = "C:\dev\Projects\content-extractor-v2"
        LFSPatterns = "*.html,*.json"
    },
    @{
        Name = "content-extractor-v3"
        Path = "C:\dev\Projects\content-extractor-v3"
        LFSPatterns = "*.html,*.json"
    },
    @{
        Name = "content-extractor-v4"
        Path = "C:\dev\Projects\content-extractor-v4"
        LFSPatterns = "*.html,*.json"
    },
    @{
        Name = "content-extractor-onedrive"
        Path = "C:\Users\rmlaynetech\OneDrive\Projects\content-extractor"
        LFSPatterns = "*.html,*.json"
    },
    
    # Priority 1: Doc Harvesters (3 projects)
    @{
        Name = "doc-harvester-pro"
        Path = "C:\dev\Projects\doc-harvester-pro"
        LFSPatterns = "*.exe,*.bin,*.dll"
    },
    @{
        Name = "doc-harvester-pro-v2"
        Path = "C:\dev\Projects\doc-harvester-pro-v2"
        LFSPatterns = "*.exe,*.bin,*.dll"
    },
    @{
        Name = "doc-harvester-pro-v3"
        Path = "C:\dev\Projects\doc-harvester-pro-v3"
        LFSPatterns = "*.exe,*.bin,*.dll"
    },
    
    # Priority 2: Individual Projects (2 projects)
    @{
        Name = "openai-url-harvester"
        Path = "C:\dev\Projects\openai-url-harvester"
        LFSPatterns = "*.exe,*.bin,*.dll"
    },
    @{
        Name = "html-to-markdown-v4"
        Path = "C:\dev\Projects\html-to-markdown-v4"
        LFSPatterns = "*.bin,*.dll,*.lm,*.pyd"
    }
)

$successCount = 0
$failureCount = 0
$results = @()

Write-Host "`n📊 MIGRATION SUMMARY:" -ForegroundColor Cyan
Write-Host "- Total projects: $($projects.Count)" -ForegroundColor White
Write-Host "- Content Extractors: 6 projects (HTML/JSON files)" -ForegroundColor White
Write-Host "- Doc Harvesters: 3 projects (Node.exe files)" -ForegroundColor White
Write-Host "- Individual projects: 2 projects (various large files)" -ForegroundColor White

Write-Host "`n🔄 Starting push process..." -ForegroundColor Blue
Write-Host "=" * 50 -ForegroundColor Blue

foreach ($project in $projects) {
    Write-Host "`n📁 Processing: $($project.Name)" -ForegroundColor Yellow
    Write-Host "   Path: $($project.Path)" -ForegroundColor Gray
    Write-Host "   LFS patterns: $($project.LFSPatterns)" -ForegroundColor Gray
    
    if (Test-Path $project.Path) {
        try {
            Set-Location $project.Path
            
            # Check if it's a git repository
            if (Test-Path ".git") {
                
                # Check LFS status
                Write-Host "   🔍 Checking LFS status..." -ForegroundColor Blue
                $lfsFiles = git lfs ls-files 2>$null
                if ($lfsFiles) {
                    Write-Host "   ✅ LFS files found: $($lfsFiles.Count) files" -ForegroundColor Green
                } else {
                    Write-Host "   ⚠️  No LFS files detected" -ForegroundColor Yellow
                }
                
                # Check for uncommitted changes
                $status = git status --porcelain
                if ($status) {
                    Write-Host "   📝 Has uncommitted changes - committing first" -ForegroundColor Yellow
                    git add -A
                    git commit -m "LFS migration and configuration"
                }
                
                # Attempt push
                Write-Host "   🚀 Pushing to GitHub..." -ForegroundColor Blue
                $pushOutput = git push origin HEAD 2>&1
                $pushExitCode = $LASTEXITCODE
                
                if ($pushExitCode -eq 0) {
                    Write-Host "   ✅ SUCCESS: Pushed successfully!" -ForegroundColor Green
                    $successCount++
                    $results += @{
                        Project = $project.Name
                        Status = "Success"
                        Message = "Pushed successfully"
                    }
                } else {
                    Write-Host "   ❌ FAILED: Push failed" -ForegroundColor Red
                    Write-Host "   Error: $pushOutput" -ForegroundColor Red
                    $failureCount++
                    $results += @{
                        Project = $project.Name
                        Status = "Failed"
                        Message = $pushOutput
                    }
                }
                
            } else {
                Write-Host "   ⚠️  Not a git repository" -ForegroundColor Yellow
                $failureCount++
                $results += @{
                    Project = $project.Name
                    Status = "Skipped"
                    Message = "Not a git repository"
                }
            }
            
        } catch {
            Write-Host "   ❌ ERROR: $($_.Exception.Message)" -ForegroundColor Red
            $failureCount++
            $results += @{
                Project = $project.Name
                Status = "Error"
                Message = $_.Exception.Message
            }
        }
        
    } else {
        Write-Host "   ⚠️  Path not found: $($project.Path)" -ForegroundColor Yellow
        $failureCount++
        $results += @{
            Project = $project.Name
            Status = "Not Found"
            Message = "Path does not exist"
        }
    }
}

# Final summary
Write-Host "`n" + "=" * 50 -ForegroundColor Green
Write-Host "🏁 FINAL RESULTS" -ForegroundColor Green
Write-Host "=" * 50 -ForegroundColor Green

Write-Host "`n📊 SUMMARY:" -ForegroundColor Cyan
Write-Host "✅ Successful pushes: $successCount" -ForegroundColor Green
Write-Host "❌ Failed pushes: $failureCount" -ForegroundColor Red
Write-Host "📁 Total processed: $($projects.Count)" -ForegroundColor Blue

Write-Host "`n📋 DETAILED RESULTS:" -ForegroundColor Yellow
foreach ($result in $results) {
    $color = switch ($result.Status) {
        "Success" { "Green" }
        "Failed" { "Red" }
        "Error" { "Red" }
        default { "Yellow" }
    }
    Write-Host "   $($result.Project): $($result.Status)" -ForegroundColor $color
    if ($result.Status -ne "Success") {
        Write-Host "      → $($result.Message)" -ForegroundColor Gray
    }
}

if ($successCount -eq $projects.Count) {
    Write-Host "`n🎉 MISSION ACCOMPLISHED!" -ForegroundColor Green
    Write-Host "All LFS migrations successfully pushed to GitHub!" -ForegroundColor Green
    Write-Host "Your repositories are now optimized with Git LFS! 🚀" -ForegroundColor Green
} elseif ($successCount -gt 0) {
    Write-Host "`n⚠️  Partial success - some pushes need attention" -ForegroundColor Yellow
} else {
    Write-Host "`n❌ No successful pushes - troubleshooting needed" -ForegroundColor Red
}

Write-Host "`n⏰ Completed at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Blue

# Return to original directory
Set-Location "C:\dev\Projects\openai-url-harvester"