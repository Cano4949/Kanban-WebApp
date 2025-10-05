---
title: Value Proposition
parent: Home
nav_order: 1
---

{: .label }
Caner Akgül

{: .no_toc }
# Value proposition

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## The problem

In vielen Teams oder kleinen Projekten wird die Aufgabenverteilung schnell unübersichtlich.  
Wer arbeitet gerade woran? Was ist schon erledigt – und was hängt noch fest?  
Oft werden Tabellen, Chatnachrichten oder Post-its benutzt, die leicht verloren gehen oder veralten.  
Dadurch gehen Informationen verloren, und der Überblick über den Fortschritt fehlt.

## Our solution

Die **Kanban Web App** ist eine einfache, browserbasierte Lösung zur visuellen Aufgabenorganisation.  
Mit einer klaren Benutzeroberfläche, entwickelt mit **Flask**, **Jinja2** und **Bootstrap 5**,  
können Benutzer Projekte erstellen, Aufgaben hinzufügen, diese zwischen Spalten wie  
*To Do*, *In Progress*, *Review* und *Done* verschieben und den Fortschritt jederzeit nachvollziehen.

- Keine Installation nötig – läuft komplett im Browser  
- Übersichtliche Struktur für Teams und Einzelpersonen  
- Einfaches Hinzufügen von Mitgliedern zu Projekten  
- Funktioniert ohne JavaScript, vollständig serverseitig umgesetzt  
- Daten werden lokal in einer **SQLite-Datenbank** gespeichert  

## Target user

- Kleine Teams und Start-ups, die Aufgaben schnell strukturieren wollen  
- Studierende und Projektgruppen, die gemeinsam an Abgaben arbeiten  
- Einzelpersonen, die ihre To-Dos und Fortschritte visuell planen möchten  
- Lehrprojekte oder Schulungen, die eine einfache Kanban-Implementierung ohne externe Tools benötigen  

## Customer journey

**Beispiel: Anna und ihr Team entwickeln ein Uni-Projekt**

1. **Start:** Anna öffnet die Kanban Web App im Browser und registriert sich.  
2. **Projekt anlegen:** Sie erstellt das Projekt *"WebApp Abschlussarbeit"* – automatisch mit den Spalten *To Do*, *In Progress*, *Review* und *Done*.  
3. **Team einladen:** Ihre Kommilitonen melden sich ebenfalls an und werden zum Projekt hinzugefügt.  
4. **Aufgabenplanung:** Anna legt Karten für Aufgaben wie *Frontend-Design*, *Dokumentation*, *Testing* an.  
5. **Fortschritt:** Die Teammitglieder bearbeiten Aufgaben und verschieben sie je nach Fortschritt in die nächste Spalte.  
6. **Projektabschluss:** Wenn alles in *Done* steht, löscht Anna das Projekt oder startet ein neues.

**Zeitaufwand total:** wenige Minuten für die Einrichtung – klare Übersicht für das gesamte Projekt.
