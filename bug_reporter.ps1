Write-Host "=== 🐛 GitHub Bug Report Generator ===" -ForegroundColor Cyan

$module_name = Read-Host "1. Enter Module Name (e.g., OH01)"
$browser_env = Read-Host "2. Enter Browser/Environment (e.g., Chrome / Safari)"
$description = Read-Host "3. Enter Description of the issue`n   (e.g., The discount text shows 40% in Figma but 30% in preview)`n   >"
$media_path = Read-Host "4. Enter the full path to the Image or Screen Recording`n   (You can drag and drop the file here, or leave blank)`n   >"

# Remove quotes if user dragged and dropped
$media_path = $media_path -replace '^"|"$|^''|''$', ''

$reports_dir = "bug_reports"
$media_dir = Join-Path $reports_dir "media"

if (-Not (Test-Path $media_dir)) {
    New-Item -ItemType Directory -Path $media_dir | Out-Null
}

$media_filename = ""
if ($media_path -and (Test-Path $media_path)) {
    $ext = [System.IO.Path]::GetExtension($media_path)
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $module_clean = $module_name -replace ' ', '_'
    $media_filename = "${module_clean}_${timestamp}${ext}"
    $dest_path = Join-Path $media_dir $media_filename
    Copy-Item -Path $media_path -Destination $dest_path -Force
    Write-Host "`n✅ Image/Video copied securely." -ForegroundColor Green
} elseif ($media_path) {
    Write-Host "`n⚠️ Warning: Image/Video file not found. Proceeding without it." -ForegroundColor Yellow
}

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$module_clean = $module_name -replace ' ', '_'
$report_filename = "${module_clean}_${timestamp}.md"
$report_path = Join-Path $reports_dir $report_filename

$content = @"
# 🐛 Bug Report: $module_name

- **Module:** `$module_name`
- **Environment:** $browser_env

## 📝 Description
$description

"@

if ($media_filename) {
    $content += "`n## 📸 Attachments`n"
    if ($media_filename -match '(?i)\.(png|jpg|jpeg|gif|webp)$') {
        $content += "![Bug Screenshot](./media/$media_filename)`n"
    } else {
        $content += "🎥 [View Screen Recording or Media](./media/$media_filename)`n"
    }
}

Set-Content -Path $report_path -Value $content -Encoding UTF8

Write-Host "✅ Developer bug report generated successfully at: $report_path" -ForegroundColor Green

$push_to_git = Read-Host "`n🚀 Do you want to push this to GitHub now? (y/n)"
if ($push_to_git -match '^[yY]') {
    Write-Host "`nSyncing with GitHub..." -ForegroundColor Cyan
    try {
        git add .
        git commit -m "🐛 Add bug report for $module_name"
        git push
        Write-Host "🎉 Successfully pushed to GitHub! Developers can now see it." -ForegroundColor Green
    } catch {
        Write-Host "`n❌ Error during Git operations. Make sure this folder is connected to a GitHub repository." -ForegroundColor Red
    }
}
