cd ifrit-xlsx;
./create_xlsx_release.sh;
cd ..;
mkdir -p release/ifrit-enhanced-0.x; 
mkdir -p release/ifrit-enhanced-0.x/ifrit-gui;
mkdir -p release/ifrit-enhanced-0.x/ifrit-xlsx;
cp -R ifrit-xlsx/release/* release/ifrit-enhanced-0.x/ifrit-xlsx/;
cp -R ifrit-gui/publish/* release/ifrit-enhanced-0.x/ifrit-gui/;
cd release/ifrit-enhanced-0.x;
"C:\Program Files\7-Zip\7z.exe" a -tzip ../ifrit-enhanced-0.x.zip .;
cd ..;
rm -r ifrit-enhanced-0.x