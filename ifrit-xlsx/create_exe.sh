venv/Scripts/pyinstaller.exe -n ifrit-enhanced -F --specpath release/build --distpath release --workpath release/build --paths venv/Lib/site-packages main.py;
mkdir -p release/ifrit-enhanced-0.x; cp -R Resources/ release/ifrit-enhanced-0.x/;
cp release/ifrit-enhanced.exe release/ifrit-enhanced-0.x/
