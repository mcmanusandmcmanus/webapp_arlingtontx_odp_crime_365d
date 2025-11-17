TemplateDoesNotExist at /dashboard/
analytics/base_patriot.html
Request Method:	GET
Request URL:	http://127.0.0.1:8000/dashboard/
Django Version:	5.1.2
Exception Type:	TemplateDoesNotExist
Exception Value:	
analytics/base_patriot.html
Exception Location:	C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\template\backends\django.py, line 130, in reraise
Raised during:	analytics.views.dashboard_overview
Python Executable:	C:\Users\mcman\AppData\Local\Programs\Python\Python310\python.exe
Python Version:	3.10.0
Python Path:	
['C:\\Users\\mcman\\webapp_arlingtontx_odp_crime_365d',
 'C:\\Users\\mcman\\AppData\\Local\\Programs\\Python\\Python310\\python310.zip',
 'C:\\Users\\mcman\\AppData\\Local\\Programs\\Python\\Python310\\DLLs',
 'C:\\Users\\mcman\\AppData\\Local\\Programs\\Python\\Python310\\lib',
 'C:\\Users\\mcman\\AppData\\Local\\Programs\\Python\\Python310',
 'C:\\Users\\mcman\\AppData\\Roaming\\Python\\Python310\\site-packages',
 'C:\\Users\\mcman\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages',
 'C:\\Users\\mcman\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\win32',
 'C:\\Users\\mcman\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\win32\\lib',
 'C:\\Users\\mcman\\AppData\\Local\\Programs\\Python\\Python310\\lib\\site-packages\\Pythonwin']
Server time:	Sun, 16 Nov 2025 18:35:52 -0600
Template-loader postmortem
Django tried loading these templates, in this order:

Using engine django:

django.template.loaders.filesystem.Loader: C:\Users\mcman\webapp_arlingtontx_odp_crime_365d\templates\analytics\base_patriot.html (Source does not exist)
django.template.loaders.app_directories.Loader: C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\contrib\admin\templates\analytics\base_patriot.html (Source does not exist)
django.template.loaders.app_directories.Loader: C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\contrib\auth\templates\analytics\base_patriot.html (Source does not exist)
django.template.loaders.app_directories.Loader: C:\Users\mcman\webapp_arlingtontx_odp_crime_365d\analytics\templates\analytics\base_patriot.html (Source does not exist)
Error during template rendering
In template C:\Users\mcman\webapp_arlingtontx_odp_crime_365d\analytics\templates\analytics\dashboard_overview.html, error at line 1

analytics/base_patriot.html
1	{% extends "analytics/base_patriot.html" %}
2	{% load static %}
3	
4	{% block content %}
5	<section class="hero-panel grid gap-8 lg:grid-cols-[minmax(0,2fr),minmax(0,1fr)]">
6	  <div class="space-y-5">
7	    <span class="hero-pill">Arlington TX &middot; Open Data</span>
8	    <div>
9	      <h2 class="text-3xl md:text-4xl font-semibold text-white tracking-tight">COO Crime Intelligence Lab</h2>
10	      <p class="text-slate-300 text-lg mt-3 max-w-3xl">
11	        Executive-ready situational awareness blending KPIs, cadence heatmaps, and anomaly detection for the command staff briefing.
Traceback Switch to copy-and-paste view
C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\template\backends\django.py, line 107, in render
            return self.template.render(context) …
Local vars
C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\template\base.py, line 171, in render
                    return self._render(context) …
Local vars
C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\template\base.py, line 163, in _render
        return self.nodelist.render(context) …
Local vars
C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\template\base.py, line 1008, in render
        return SafeString("".join([node.render_annotated(context) for node in self])) …
Local vars
C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\template\base.py, line 1008, in <listcomp>
        return SafeString("".join([node.render_annotated(context) for node in self])) …
Local vars
C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\template\base.py, line 969, in render_annotated
            return self.render(context) …
Local vars
C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\template\loader_tags.py, line 134, in render
        compiled_parent = self.get_parent(context) …
Local vars
C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\template\loader_tags.py, line 131, in get_parent
        return self.find_template(parent, context) …
Local vars
C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\template\loader_tags.py, line 109, in find_template
        template, origin = context.template.engine.find_template( …
Local vars
C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\template\engine.py, line 163, in find_template
        raise TemplateDoesNotExist(name, tried=tried) …
Local vars
The above exception (analytics/base_patriot.html) was the direct cause of the following exception:
C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\core\handlers\exception.py, line 55, in inner
                response = get_response(request) …
Local vars
C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\core\handlers\base.py, line 197, in _get_response
                response = wrapped_callback(request, *callback_args, **callback_kwargs) …
Local vars
C:\Users\mcman\webapp_arlingtontx_odp_crime_365d\analytics\views.py, line 107, in dashboard_overview
    return render(request, "analytics/dashboard_overview.html", context) …
Local vars
C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\shortcuts.py, line 25, in render
    content = loader.render_to_string(template_name, context, request, using=using) …
Local vars
C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\template\loader.py, line 62, in render_to_string
    return template.render(context, request) …
Local vars
C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\template\backends\django.py, line 109, in render
            reraise(exc, self.backend) …
Local vars
C:\Users\mcman\AppData\Local\Programs\Python\Python310\lib\site-packages\django\template\backends\django.py, line 130, in reraise
    raise new from exc …
Local vars
Request information
USER
AnonymousUser

GET
No GET data

POST
No POST data

FILES
No FILES data

COOKIES
Variable	Value
csrftoken	
'********************'
homeschoolapp-csrftoken	
'********************'
sessionid	
'********************'
META
Variable	Value
ALLUSERSPROFILE	
'C:\\ProgramData'
APPDATA	
'C:\\Users\\mcman\\AppData\\Roaming'
CHROME_CRASHPAD_PIPE_NAME	
'\\\\.\\pipe\\crashpad_20772_XOZVXCCFKAIWLUWG'
COLORTERM	
'truecolor'
COMMONPROGRAMFILES	
'C:\\Program Files\\Common Files'
COMMONPROGRAMFILES(X86)	
'C:\\Program Files (x86)\\Common Files'
COMMONPROGRAMW6432	
'C:\\Program Files\\Common Files'
COMPUTERNAME	
'PAPI'
COMSPEC	
'C:\\WINDOWS\\system32\\cmd.exe'
CONTENT_LENGTH	
''
CONTENT_TYPE	
'text/plain'
CSRF_COOKIE	
'pnVC7cDOcNznX7XgCXV7qtCIYLvuOGIp'
DJANGO_SETTINGS_MODULE	
'crime_dashboard.settings'
DRIVERDATA	
'C:\\Windows\\System32\\Drivers\\DriverData'
EFC_12924_1592913036	
'1'
FPS_BROWSER_APP_PROFILE_STRING	
'Internet Explorer'
FPS_BROWSER_USER_PROFILE_STRING	
'Default'
GATEWAY_INTERFACE	
'CGI/1.1'
GIT_ASKPASS	
'********************'
HOMEDRIVE	
'C:'
HOMEPATH	
'\\Users\\mcman'
HTTP_ACCEPT	
'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7'
HTTP_ACCEPT_ENCODING	
'gzip, deflate, br, zstd'
HTTP_ACCEPT_LANGUAGE	
'en-US,en;q=0.9'
HTTP_CONNECTION	
'keep-alive'
HTTP_COOKIE	
'********************'
HTTP_HOST	
'127.0.0.1:8000'
HTTP_SEC_CH_UA	
'"Chromium";v="142", "Microsoft Edge";v="142", "Not_A Brand";v="99"'
HTTP_SEC_CH_UA_MOBILE	
'?0'
HTTP_SEC_CH_UA_PLATFORM	
'"Windows"'
HTTP_SEC_FETCH_DEST	
'empty'
HTTP_SEC_FETCH_MODE	
'navigate'
HTTP_SEC_FETCH_SITE	
'same-origin'
HTTP_UPGRADE_INSECURE_REQUESTS	
'1'
HTTP_USER_AGENT	
('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like '
 'Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0')
LANG	
'en_US.UTF-8'
LOCALAPPDATA	
'C:\\Users\\mcman\\AppData\\Local'
LOGONSERVER	
'\\\\PAPI'
NUMBER_OF_PROCESSORS	
'14'
ONEDRIVE	
'C:\\Users\\mcman\\OneDrive'
ONEDRIVECONSUMER	
'C:\\Users\\mcman\\OneDrive'
ONLINESERVICES	
'Online Services'
ORIGINAL_XDG_CURRENT_DESKTOP	
'undefined'
OS	
'Windows_NT'
PATH	
('C:\\Program Files (x86)\\Common Files\\Oracle\\Java\\java8path;C:\\Program '
 'Files (x86)\\Common '
 'Files\\Oracle\\Java\\javapath;C:\\WINDOWS\\system32;C:\\WINDOWS;C:\\WINDOWS\\System32\\Wbem;C:\\WINDOWS\\System32\\WindowsPowerShell\\v1.0\\;C:\\WINDOWS\\System32\\OpenSSH\\;C:\\Users\\mcman\\gs10.04.0\\bin;C:\\Program '
 'Files\\nodejs\\;C:\\Program '
 'Files\\Git\\cmd;C:\\Users\\mcman\\.cargo\\bin;C:\\Users\\mcman\\AppData\\Local\\Programs\\Python\\Python310\\Scripts\\;C:\\Users\\mcman\\AppData\\Local\\Programs\\Python\\Python310\\;C:\\Users\\mcman\\AppData\\Local\\Microsoft\\WindowsApps;C:\\Users\\mcman\\AppData\\Local\\Programs\\Microsoft '
 'VS '
 'Code\\bin;C:\\Users\\mcman\\AppData\\Roaming\\npm;C:\\sqlite;C:\\Users\\mcman\\AppData\\Local\\Programs\\Windsurf\\bin')
PATHEXT	
'.COM;.EXE;.BAT;.CMD;.VBS;.VBE;.JS;.JSE;.WSF;.WSH;.MSC;.CPL'
PATH_INFO	
'/dashboard/'
PLATFORMCODE	
'M8'
PROCESSOR_ARCHITECTURE	
'AMD64'
PROCESSOR_IDENTIFIER	
'Intel64 Family 6 Model 170 Stepping 4, GenuineIntel'
PROCESSOR_LEVEL	
'6'
PROCESSOR_REVISION	
'aa04'
PROGRAMDATA	
'C:\\ProgramData'
PROGRAMFILES	
'C:\\Program Files'
PROGRAMFILES(X86)	
'C:\\Program Files (x86)'
PROGRAMW6432	
'C:\\Program Files'
PSMODULEPATH	
('C:\\Users\\mcman\\OneDrive\\Documentos\\WindowsPowerShell\\Modules;C:\\Program '
 'Files\\WindowsPowerShell\\Modules;C:\\WINDOWS\\system32\\WindowsPowerShell\\v1.0\\Modules')
PUBLIC	
'C:\\Users\\Public'
PYTHONSTARTUP	
'c:\\Users\\mcman\\AppData\\Roaming\\Code\\User\\workspaceStorage\\f03f844c32d78dee026a04cd82bffd9b\\ms-python.python\\pythonrc.py'
PYTHON_BASIC_REPL	
'1'
QUERY_STRING	
''
REGIONCODE	
'NA'
REMOTE_ADDR	
'127.0.0.1'
REMOTE_HOST	
''
REQUEST_METHOD	
'GET'
RUN_MAIN	
'true'
SCRIPT_NAME	
''
SERVER_NAME	
'Papi'
SERVER_PORT	
'8000'
SERVER_PROTOCOL	
'HTTP/1.1'
SERVER_SOFTWARE	
'WSGIServer/0.2'
SESSIONNAME	
'Console'
SYSTEMDRIVE	
'C:'
SYSTEMROOT	
'C:\\WINDOWS'
TEMP	
'C:\\Users\\mcman\\AppData\\Local\\Temp'
TERM_PROGRAM	
'vscode'
TERM_PROGRAM_VERSION	
'1.106.0'
TMP	
'C:\\Users\\mcman\\AppData\\Local\\Temp'
USERDOMAIN	
'PAPI'
USERDOMAIN_ROAMINGPROFILE	
'PAPI'
USERNAME	
'mcman'
USERPROFILE	
'C:\\Users\\mcman'
VSCODE_GIT_ASKPASS_EXTRA_ARGS	
'********************'
VSCODE_GIT_ASKPASS_MAIN	
'********************'
VSCODE_GIT_ASKPASS_NODE	
'********************'
VSCODE_GIT_IPC_HANDLE	
'\\\\.\\pipe\\vscode-git-68024c23c2-sock'
VSCODE_INJECTION	
'1'
VSCODE_PYTHON_AUTOACTIVATE_GUARD	
'1'
WINDIR	
'C:\\WINDOWS'
ZES_ENABLE_SYSMAN	
'1'
wsgi.errors	
<_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>
wsgi.file_wrapper	
<class 'wsgiref.util.FileWrapper'>
wsgi.input	
<django.core.handlers.wsgi.LimitedStream object at 0x00000265BA872D70>
wsgi.multiprocess	
False
wsgi.multithread	
True
wsgi.run_once	
False
wsgi.url_scheme	
'http'
wsgi.version	
(1, 0)
Settings
Using settings module crime_dashboard.settings
Setting	Value
ABSOLUTE_URL_OVERRIDES	
{}
ADMINS	
[]
ALLOWED_HOSTS	
['localhost', '127.0.0.1']
APPEND_SLASH	
True
AUTHENTICATION_BACKENDS	
['django.contrib.auth.backends.ModelBackend']
AUTH_PASSWORD_VALIDATORS	
'********************'
AUTH_USER_MODEL	
'auth.User'
BASE_DIR	
WindowsPath('C:/Users/mcman/webapp_arlingtontx_odp_crime_365d')
CACHES	
{'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}
CACHE_MIDDLEWARE_ALIAS	
'default'
CACHE_MIDDLEWARE_KEY_PREFIX	
'********************'
CACHE_MIDDLEWARE_SECONDS	
600
CRIME_DATA_PATH	
'C:\\Users\\mcman\\webapp_arlingtontx_odp_crime_365d\\data\\crime_365d.csv'
CSRF_COOKIE_AGE	
31449600
CSRF_COOKIE_DOMAIN	
None
CSRF_COOKIE_HTTPONLY	
False
CSRF_COOKIE_NAME	
'csrftoken'
CSRF_COOKIE_PATH	
'/'
CSRF_COOKIE_SAMESITE	
'Lax'
CSRF_COOKIE_SECURE	
False
CSRF_FAILURE_VIEW	
'django.views.csrf.csrf_failure'
CSRF_HEADER_NAME	
'HTTP_X_CSRFTOKEN'
CSRF_TRUSTED_ORIGINS	
['http://localhost', 'http://127.0.0.1']
CSRF_USE_SESSIONS	
False
DATABASES	
{'default': {'ATOMIC_REQUESTS': False,
             'AUTOCOMMIT': True,
             'CONN_HEALTH_CHECKS': False,
             'CONN_MAX_AGE': 600,
             'DISABLE_SERVER_SIDE_CURSORS': False,
             'ENGINE': 'django.db.backends.sqlite3',
             'HOST': '',
             'NAME': 'C:\\Users\\mcman\\webapp_arlingtontx_odp_crime_365d\\db.sqlite3',
             'OPTIONS': {},
             'PASSWORD': '********************',
             'PORT': '',
             'TEST': {'CHARSET': None,
                      'COLLATION': None,
                      'MIGRATE': True,
                      'MIRROR': None,
                      'NAME': None},
             'TIME_ZONE': None,
             'USER': ''}}
DATABASE_ROUTERS	
[]
DATA_DIR	
WindowsPath('C:/Users/mcman/webapp_arlingtontx_odp_crime_365d/data')
DATA_UPLOAD_MAX_MEMORY_SIZE	
2621440
DATA_UPLOAD_MAX_NUMBER_FIELDS	
1000
DATA_UPLOAD_MAX_NUMBER_FILES	
100
DATETIME_FORMAT	
'N j, Y, P'
DATETIME_INPUT_FORMATS	
['%Y-%m-%d %H:%M:%S',
 '%Y-%m-%d %H:%M:%S.%f',
 '%Y-%m-%d %H:%M',
 '%m/%d/%Y %H:%M:%S',
 '%m/%d/%Y %H:%M:%S.%f',
 '%m/%d/%Y %H:%M',
 '%m/%d/%y %H:%M:%S',
 '%m/%d/%y %H:%M:%S.%f',
 '%m/%d/%y %H:%M']
DATE_FORMAT	
'N j, Y'
DATE_INPUT_FORMATS	
['%Y-%m-%d',
 '%m/%d/%Y',
 '%m/%d/%y',
 '%b %d %Y',
 '%b %d, %Y',
 '%d %b %Y',
 '%d %b, %Y',
 '%B %d %Y',
 '%B %d, %Y',
 '%d %B %Y',
 '%d %B, %Y']
DEBUG	
True
DEBUG_PROPAGATE_EXCEPTIONS	
False
DECIMAL_SEPARATOR	
'.'
DEFAULT_AUTO_FIELD	
'django.db.models.BigAutoField'
DEFAULT_CHARSET	
'utf-8'
DEFAULT_EXCEPTION_REPORTER	
'django.views.debug.ExceptionReporter'
DEFAULT_EXCEPTION_REPORTER_FILTER	
'django.views.debug.SafeExceptionReporterFilter'
DEFAULT_FROM_EMAIL	
'webmaster@localhost'
DEFAULT_INDEX_TABLESPACE	
''
DEFAULT_TABLESPACE	
''
DISALLOWED_USER_AGENTS	
[]
DS_LAB_PASSCODE	
'********************'
EMAIL_BACKEND	
'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST	
'localhost'
EMAIL_HOST_PASSWORD	
'********************'
EMAIL_HOST_USER	
''
EMAIL_PORT	
25
EMAIL_SSL_CERTFILE	
None
EMAIL_SSL_KEYFILE	
'********************'
EMAIL_SUBJECT_PREFIX	
'[Django] '
EMAIL_TIMEOUT	
None
EMAIL_USE_LOCALTIME	
False
EMAIL_USE_SSL	
False
EMAIL_USE_TLS	
False
ENTRY_PASSCODE	
'********************'
FILE_UPLOAD_DIRECTORY_PERMISSIONS	
None
FILE_UPLOAD_HANDLERS	
['django.core.files.uploadhandler.MemoryFileUploadHandler',
 'django.core.files.uploadhandler.TemporaryFileUploadHandler']
FILE_UPLOAD_MAX_MEMORY_SIZE	
2621440
FILE_UPLOAD_PERMISSIONS	
420
FILE_UPLOAD_TEMP_DIR	
None
FIRST_DAY_OF_WEEK	
0
FIXTURE_DIRS	
[]
FORCE_SCRIPT_NAME	
None
FORMAT_MODULE_PATH	
None
FORMS_URLFIELD_ASSUME_HTTPS	
False
FORM_RENDERER	
'django.forms.renderers.DjangoTemplates'
IGNORABLE_404_URLS	
[]
IMPORT_PASSCODE	
'********************'
INSTALLED_APPS	
['django.contrib.admin',
 'django.contrib.auth',
 'django.contrib.contenttypes',
 'django.contrib.sessions',
 'django.contrib.messages',
 'django.contrib.staticfiles',
 'django.contrib.humanize',
 'analytics']
INTERNAL_IPS	
[]
LANGUAGES	
[('af', 'Afrikaans'),
 ('ar', 'Arabic'),
 ('ar-dz', 'Algerian Arabic'),
 ('ast', 'Asturian'),
 ('az', 'Azerbaijani'),
 ('bg', 'Bulgarian'),
 ('be', 'Belarusian'),
 ('bn', 'Bengali'),
 ('br', 'Breton'),
 ('bs', 'Bosnian'),
 ('ca', 'Catalan'),
 ('ckb', 'Central Kurdish (Sorani)'),
 ('cs', 'Czech'),
 ('cy', 'Welsh'),
 ('da', 'Danish'),
 ('de', 'German'),
 ('dsb', 'Lower Sorbian'),
 ('el', 'Greek'),
 ('en', 'English'),
 ('en-au', 'Australian English'),
 ('en-gb', 'British English'),
 ('eo', 'Esperanto'),
 ('es', 'Spanish'),
 ('es-ar', 'Argentinian Spanish'),
 ('es-co', 'Colombian Spanish'),
 ('es-mx', 'Mexican Spanish'),
 ('es-ni', 'Nicaraguan Spanish'),
 ('es-ve', 'Venezuelan Spanish'),
 ('et', 'Estonian'),
 ('eu', 'Basque'),
 ('fa', 'Persian'),
 ('fi', 'Finnish'),
 ('fr', 'French'),
 ('fy', 'Frisian'),
 ('ga', 'Irish'),
 ('gd', 'Scottish Gaelic'),
 ('gl', 'Galician'),
 ('he', 'Hebrew'),
 ('hi', 'Hindi'),
 ('hr', 'Croatian'),
 ('hsb', 'Upper Sorbian'),
 ('hu', 'Hungarian'),
 ('hy', 'Armenian'),
 ('ia', 'Interlingua'),
 ('id', 'Indonesian'),
 ('ig', 'Igbo'),
 ('io', 'Ido'),
 ('is', 'Icelandic'),
 ('it', 'Italian'),
 ('ja', 'Japanese'),
 ('ka', 'Georgian'),
 ('kab', 'Kabyle'),
 ('kk', 'Kazakh'),
 ('km', 'Khmer'),
 ('kn', 'Kannada'),
 ('ko', 'Korean'),
 ('ky', 'Kyrgyz'),
 ('lb', 'Luxembourgish'),
 ('lt', 'Lithuanian'),
 ('lv', 'Latvian'),
 ('mk', 'Macedonian'),
 ('ml', 'Malayalam'),
 ('mn', 'Mongolian'),
 ('mr', 'Marathi'),
 ('ms', 'Malay'),
 ('my', 'Burmese'),
 ('nb', 'Norwegian Bokmål'),
 ('ne', 'Nepali'),
 ('nl', 'Dutch'),
 ('nn', 'Norwegian Nynorsk'),
 ('os', 'Ossetic'),
 ('pa', 'Punjabi'),
 ('pl', 'Polish'),
 ('pt', 'Portuguese'),
 ('pt-br', 'Brazilian Portuguese'),
 ('ro', 'Romanian'),
 ('ru', 'Russian'),
 ('sk', 'Slovak'),
 ('sl', 'Slovenian'),
 ('sq', 'Albanian'),
 ('sr', 'Serbian'),
 ('sr-latn', 'Serbian Latin'),
 ('sv', 'Swedish'),
 ('sw', 'Swahili'),
 ('ta', 'Tamil'),
 ('te', 'Telugu'),
 ('tg', 'Tajik'),
 ('th', 'Thai'),
 ('tk', 'Turkmen'),
 ('tr', 'Turkish'),
 ('tt', 'Tatar'),
 ('udm', 'Udmurt'),
 ('ug', 'Uyghur'),
 ('uk', 'Ukrainian'),
 ('ur', 'Urdu'),
 ('uz', 'Uzbek'),
 ('vi', 'Vietnamese'),
 ('zh-hans', 'Simplified Chinese'),
 ('zh-hant', 'Traditional Chinese')]
LANGUAGES_BIDI	
['he', 'ar', 'ar-dz', 'ckb', 'fa', 'ug', 'ur']
LANGUAGE_CODE	
'en-us'
LANGUAGE_COOKIE_AGE	
None
LANGUAGE_COOKIE_DOMAIN	
None
LANGUAGE_COOKIE_HTTPONLY	
False
LANGUAGE_COOKIE_NAME	
'django_language'
LANGUAGE_COOKIE_PATH	
'/'
LANGUAGE_COOKIE_SAMESITE	
None
LANGUAGE_COOKIE_SECURE	
False
LOCALE_PATHS	
[]
LOGGING	
{}
LOGGING_CONFIG	
'logging.config.dictConfig'
LOGIN_REDIRECT_URL	
'/accounts/profile/'
LOGIN_URL	
'/accounts/login/'
LOGOUT_REDIRECT_URL	
None
MANAGERS	
[]
MEDIA_ROOT	
''
MEDIA_URL	
'/'
MESSAGE_STORAGE	
'django.contrib.messages.storage.fallback.FallbackStorage'
MIDDLEWARE	
['django.middleware.security.SecurityMiddleware',
 'whitenoise.middleware.WhiteNoiseMiddleware',
 'django.contrib.sessions.middleware.SessionMiddleware',
 'django.middleware.common.CommonMiddleware',
 'django.middleware.csrf.CsrfViewMiddleware',
 'django.contrib.auth.middleware.AuthenticationMiddleware',
 'django.contrib.messages.middleware.MessageMiddleware',
 'django.middleware.clickjacking.XFrameOptionsMiddleware']
MIGRATION_MODULES	
{}
MONTH_DAY_FORMAT	
'F j'
NUMBER_GROUPING	
0
PASSWORD_HASHERS	
'********************'
PASSWORD_RESET_TIMEOUT	
'********************'
PREPEND_WWW	
False
ROOT_URLCONF	
'crime_dashboard.urls'
SECRET_KEY	
'********************'
SECRET_KEY_FALLBACKS	
'********************'
SECURE_CONTENT_TYPE_NOSNIFF	
True
SECURE_CROSS_ORIGIN_OPENER_POLICY	
'same-origin'
SECURE_HSTS_INCLUDE_SUBDOMAINS	
False
SECURE_HSTS_PRELOAD	
False
SECURE_HSTS_SECONDS	
0
SECURE_PROXY_SSL_HEADER	
None
SECURE_REDIRECT_EXEMPT	
[]
SECURE_REFERRER_POLICY	
'same-origin'
SECURE_SSL_HOST	
None
SECURE_SSL_REDIRECT	
False
SERVER_EMAIL	
'root@localhost'
SESSION_CACHE_ALIAS	
'default'
SESSION_COOKIE_AGE	
1209600
SESSION_COOKIE_DOMAIN	
None
SESSION_COOKIE_HTTPONLY	
True
SESSION_COOKIE_NAME	
'sessionid'
SESSION_COOKIE_PATH	
'/'
SESSION_COOKIE_SAMESITE	
'Lax'
SESSION_COOKIE_SECURE	
False
SESSION_ENGINE	
'django.contrib.sessions.backends.db'
SESSION_EXPIRE_AT_BROWSER_CLOSE	
False
SESSION_FILE_PATH	
None
SESSION_SAVE_EVERY_REQUEST	
False
SESSION_SERIALIZER	
'django.contrib.sessions.serializers.JSONSerializer'
SETTINGS_MODULE	
'crime_dashboard.settings'
SHORT_DATETIME_FORMAT	
'm/d/Y P'
SHORT_DATE_FORMAT	
'm/d/Y'
SIGNING_BACKEND	
'django.core.signing.TimestampSigner'
SILENCED_SYSTEM_CHECKS	
[]
STATICFILES_DIRS	
[WindowsPath('C:/Users/mcman/webapp_arlingtontx_odp_crime_365d/static')]
STATICFILES_FINDERS	
['django.contrib.staticfiles.finders.FileSystemFinder',
 'django.contrib.staticfiles.finders.AppDirectoriesFinder']
STATICFILES_STORAGE	
'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT	
WindowsPath('C:/Users/mcman/webapp_arlingtontx_odp_crime_365d/staticfiles')
STATIC_URL	
'/static/'
STORAGES	
{'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
 'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'}}
TEMPLATES	
[{'APP_DIRS': True,
  'BACKEND': 'django.template.backends.django.DjangoTemplates',
  'DIRS': [WindowsPath('C:/Users/mcman/webapp_arlingtontx_odp_crime_365d/templates')],
  'OPTIONS': {'context_processors': ['django.template.context_processors.debug',
                                     'django.template.context_processors.request',
                                     'django.contrib.auth.context_processors.auth',
                                     'django.contrib.messages.context_processors.messages']}}]
TEST_NON_SERIALIZED_APPS	
[]
TEST_RUNNER	
'django.test.runner.DiscoverRunner'
THOUSAND_SEPARATOR	
','
TIME_FORMAT	
'P'
TIME_INPUT_FORMATS	
['%H:%M:%S', '%H:%M:%S.%f', '%H:%M']
TIME_ZONE	
'America/Chicago'
USE_I18N	
True
USE_THOUSAND_SEPARATOR	
False
USE_TZ	
True
USE_X_FORWARDED_HOST	
False
USE_X_FORWARDED_PORT	
False
WSGI_APPLICATION	
'crime_dashboard.wsgi.application'
X_FRAME_OPTIONS	
'DENY'
YEAR_MONTH_FORMAT	
'F Y'
You’re seeing this error because you have DEBUG = True in your Django settings file. Change that to False, and Django will display a standard page generated by the handler for this status code.