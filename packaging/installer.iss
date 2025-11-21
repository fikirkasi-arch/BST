#define MyAppName "JinniBell Pro"
#define MyAppVersion "1.0"
#define MyAppPublisher "Emre Esen"
#define MyAppExeName "JinniBellPro.exe"

[Setup]
AppId={{F3E126CE-0F67-4A2A-A5ED-0BC1F0C6B9BA}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\JinniBellPro
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputBaseFilename=JinniBellPro-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x86 x64
ArchitecturesInstallIn64BitMode=x64
SetupIconFile=
LicenseFile=

[Languages]
Name: "turkish"; MessagesFile: "compiler:Languages/Turkish.isl"

[Tasks]
Name: "desktopicon"; Description: "\"{#MyAppName}\" için masaüstü kısayolu oluştur"; GroupDescription: "Ek görevler:"; Flags: unchecked

[Files]
Source: "dist\JinniBellPro\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\JinniBellPro\bell_app\*"; DestDir: "{app}\bell_app"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "dist\JinniBellPro\ffmpeg\*"; DestDir: "{app}\ffmpeg"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{#MyAppName}'ı hemen başlat"; Flags: nowait postinstall skipifsilent
