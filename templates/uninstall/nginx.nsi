ExecWait '"sc.exe" stop {{ NGINXDIR }}'
ExecWait '"$INSTDIR\nssm.exe" remove {{ NGINXDIR }} confirm'

RMDir /r /REBOOTOK "$INSTDIR\{{ NGINXDIR }}"

Delete /REBOOTOK "$DESKTOP\www.lnk"
Delete /REBOOTOK "$DESKTOP\Restart Nginx.lnk"
Delete /REBOOTOK "$DESKTOP\Start Nginx.lnk"
Delete /REBOOTOK "$DESKTOP\Stop Nginx.lnk"

RMDir /r /REBOOTOK "$SMPROGRAMS\{{ APP_TITLE }}\Nginx"