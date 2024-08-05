@echo on
cd /d "%~dp0"
echo Starting TwitterScraper...
if exist "dist\TwitterScraper.exe" (
    echo TwitterScraper.exe found. Launching...
    dist\TwitterScraper.exe
    echo TwitterScraper.exe execution completed.
) else (
    echo TwitterScraper.exe not found in the dist folder.
    echo Please make sure you have built the project correctly.
)
echo Script execution completed.
pause