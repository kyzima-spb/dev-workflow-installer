SetOverwrite ifdiff

SetOutPath "$INSTDIR"

${If} ${RunningX64}
    File "for_copy\{{ NSSMDIR }}\win64\nssm.exe"
${Else}
    File "for_copy\{{ NSSMDIR }}\win32\nssm.exe"
${EndIf}

CreateShortCut "$SMPROGRAMS\{{ APP_TITLE }}\nssm.lnk" "$INSTDIR\nssm.exe"