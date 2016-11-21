{% extends "base.nsi" %}

{% block MultiUser %}
    {{ super() }}

    !define MULTIUSER_INSTALLMODEPAGE_TEXT_TOP "Выберите режим установки"
    !define MULTIUSER_INSTALLMODEPAGE_TEXT_ALLUSERS "Для всех пользователей"
    !define MULTIUSER_INSTALLMODEPAGE_TEXT_CURRENTUSER "Для одного пользователя"
{% endblock %}

{% block OnInit %}
    ReadRegStr $0 HKLM "Software\{{ APP_TITLE }}" ""

    ${If} $0 != ""
        MessageBox MB_OK|MB_ICONEXCLAMATION "Перед обновлением удалите приложение" /SD IDOK
        ;Abort
    ${EndIf}
{% endblock %}


{% block StartSection %}
    {{ super() }}
{% endblock %}


{% block FinishSection %}
    {{ super() }}
{% endblock %}


{% block UnOnInit %}
    ;!insertmacro FindProc $0 "{{ APP_NAME }}.exe"

    ;${If} $0 == 0
    ;  MessageBox MB_OK|MB_ICONEXCLAMATION "Для удаления закройте приложение" /SD IDOK
    ;  Abort
    ;${EndIf}
{% endblock %}