;
; AutoHotkey Version: 1.x
; Language:       English
; Platform:       Win9x/NT
; Author:         A.N.Other <myemail@nowhere.com>
;
; Script Function:
;   Template script (you can customize this template by editing "ShellNew\Template.ahk" in your Windows folder)
;

#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

n := 1
While (n < 6) {
    ws := 5
    While (ws < 12) {
        Run, python NMote.py %n% %ws%,,Min
        Process, WaitClose, python.exe, 240
        Process, Close, python.exe
        ws := ws + 1
    }
    n := n + 1
}