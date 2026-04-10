\
        ; NSIS installer script - edit paths before use
        Name "MCreator Plugin Porter"
        OutFile "build\\MCreatorPluginPorterInstaller.exe"
        InstallDir "$PROGRAMFILES\\MCreatorPluginPorter"
        SetCompress lzma

        Section ""
          SetOutPath "$INSTDIR"
          File "dist\\mcreator_porter.exe"
          CreateShortCut "$DESKTOP\\MCreator Plugin Porter.lnk" "$INSTDIR\\mcreator_porter.exe"
        SectionEnd
