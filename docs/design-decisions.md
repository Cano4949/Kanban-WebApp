---
title: Design Decisions
nav_order: 3
---

{: .label }
Caner Akgül

{: .no_toc }
# Design decisions

<details open markdown="block">
{: .text-delta }
<summary>Table of contents</summary>
+ ToC
{: toc }
</details>

## Legende

{: .info }
> **Bewertungssymbole in den Tabellen:**
> - ✔️ = **Vorteil/Gut**  
> - ❌ = **Nachteil/Schlecht**  
> - ❔ = **Neutral/Abhängig**

---

## 01: Datenbankwahl – SQLite vs. SQLAlchemy

### Meta

Status
: **Decided**

Updated
: 02-Okt-2025

### Problem statement

Für die Kanban Web App wird eine einfache, stabile Datenbank benötigt, die alle User-, Projekt- und Aufgabeninformationen speichert.  
Da das Projekt ein Prototyp ist, soll keine komplexe Server-Datenbank eingerichtet werden.

### Decision

Verwendung von **SQLite** mit **plain SQL** (kein ORM).

SQLite ist file-basiert, benötigt keine Installation und ist perfekt für lokale Prototypen.  
Plain SQL gibt volle Kontrolle und fördert das Verständnis der Datenbanklogik.

*Decision taken by:* Caner Akgül

### Regarded options

| Criterion | SQLite | MySQL | PostgreSQL | SQLAlchemy |
| --- | --- | --- | --- | --- |
| **Setup Aufwand** | ✔️ Keine Installation | ❌ Server nötig | ❌ Server nötig | ❔ Zusätzliche Abstraktion |
| **Lernaufwand** | ✔️ Leicht verständlich | ❌ Hoch | ❌ Hoch | ❌ ORM-Konzepte lernen |
| **Prototyp geeignet** | ✔️ Perfekt | ❌ Overkill | ❌ Overkill | ❔ Teilweise |
| **Performance lokal** | ✔️ Schnell | ❔ Abhängig | ❔ Abhängig | ❔ Abhängig |

---

## 02: Frontend – Bootstrap 5 vs. eigenes CSS

### Meta

Status
: **Decided**

Updated
: 02-Okt-2025

### Problem statement

Das Design soll modern, responsiv und ohne großen Styling-Aufwand entstehen. Da das Projekt ohne Design-Team entwickelt wird, ist eine fertige Lösung sinnvoll.

### Decision

Verwendung von **Bootstrap 5** als Haupt-CSS-Framework.

Bootstrap bietet sofort ein professionelles Layout und spart Entwicklungszeit. Das Grid-System sorgt für responsive Darstellung auf Desktop und Mobilgeräten.

*Decision taken by:* Caner Akgül

### Regarded options

| Criterion | Bootstrap 5 | Eigenes CSS | Tailwind CSS |
| --- | --- | --- | --- |
| **Lernaufwand** | ✔️ Minimal | ❌ Hoch | ❌ Mittel |
| **Entwicklungszeit** | ✔️ Schnell | ❌ Langsam | ❔ Mittel |
| **Responsiveness** | ✔️ Automatisch | ❌ Manuell | ✔️ Automatisch |
| **Design-Konsistenz** | ✔️ Hoch | ❌ Variabel | ✔️ Hoch |

---

## 03: Template-Engine – Jinja2

### Meta

Status
: **Decided**

Updated
: 02-Okt-2025

### Problem statement

HTML-Seiten sollen dynamisch erzeugt werden, um Benutzerdaten, Projekte und Karten anzuzeigen. Eine serverseitige Template-Lösung ist notwendig.

### Decision

Verwendung von **Jinja2**, der integrierten Template-Engine von Flask.

Jinja2 ermöglicht eine klare Trennung von Backend-Logik und Frontend-Darstellung. Variablen, Schleifen und Bedingungen lassen sich einfach in HTML integrieren.

*Decision taken by:* Caner Akgül

### Regarded options

| Criterion | Jinja2 | React/Vue | Reines HTML |
| --- | --- | --- | --- |
| **Einfachheit** | ✔️ Direkt in Flask | ❌ Hoher Aufwand | ✔️ Einfach |
| **Integration** | ✔️ Nahtlos | ❌ Getrennt | ❌ Keine Dynamik |
| **JS-frei** | ✔️ Ja | ❌ Nein | ✔️ Ja |
| **Geeignet für Server-Rendering** | ✔️ Perfekt | ❌ Client-basiert | ❌ Statisch |

---

## 04: Authentifizierung – Session-basiert

### Meta

Status
: **Decided**

Updated
: 02-Okt-2025

### Problem statement

Die App benötigt Login/Logout-Funktionalität. Sicherheit ist wichtig, aber das System soll einfach bleiben.

### Decision

Verwendung von **Flask Sessions** für Authentifizierung.

Sessions sind direkt integriert, leicht zu verwenden und ausreichend sicher für lokale oder Prototyp-Anwendungen.

*Decision taken by:* Caner Akgül

### Regarded options

| Criterion | Flask Sessions | JWT Tokens | OAuth |
| --- | --- | --- | --- |
| **Einfachheit** | ✔️ Built-in | ❌ Setup nötig | ❌ Komplex |
| **Sicherheit** | ✔️ Ausreichend | ✔️ Hoch | ✔️ Hoch |
| **Prototyp geeignet** | ✔️ Ideal | ❌ Overkill | ❌ Overkill |
| **Abhängigkeiten** | ✔️ Keine | ❌ Zusätzliche Lib | ❌ Externe API |

---

## 05: Kein JavaScript – rein serverseitige Interaktion

### Meta

Status
: **Decided**

Updated
: 02-Okt-2025

### Problem statement

Das Projekt soll vollständig ohne JavaScript umgesetzt werden. Trotzdem müssen Karten verschoben und Daten geändert werden können.

### Decision

Verwendung von **HTML-Formularen** für alle Aktionen.  
Kartenbewegungen, Spaltenänderungen und Mitglieder-Management erfolgen über POST-Requests.

Das hält die App schlank, verständlich und kompatibel mit allen Browsern.

*Decision taken by:* Caner Akgül

### Regarded options

| Criterion | Ohne JavaScript | Mit JavaScript (Drag & Drop) |
| --- | --- | --- |
| **Einfachheit** | ✔️ Sehr hoch | ❌ Erhöhter Aufwand |
| **Barrierefreiheit** | ✔️ Sehr gut | ❔ Abhängig |
| **Interaktivität** | ❌ Weniger dynamisch | ✔️ Sehr hoch |
| **Stabilität** | ✔️ Robust | ❔ Browser-abhängig |

---

## 06: Minimalistisches UI-Design

### Meta

Status
: **Decided**

Updated
: 02-Okt-2025

### Problem statement

Soll die Benutzeroberfläche viele Funktionen enthalten oder auf die Kern-Features reduziert werden? Ziel ist ein klarer, übersichtlicher Workflow.

### Decision

Verwendung eines **minimalistischen Layouts** mit Fokus auf Funktionalität.  
Nur die wichtigsten Elemente – Projekte, Spalten, Karten – sind sichtbar.  
Klare Buttons, einfache Strukturen und wenige Farben unterstützen die Übersichtlichkeit.

*Decision taken by:* Caner Akgül

### Regarded options

| Criterion | Minimalistisch | Feature-reich |
| --- | --- | --- |
| **Lernkurve** | ✔️ Sehr gering | ❌ Hoch |
| **Performance** | ✔️ Schnell | ❌ Langsam |
| **Mobile Nutzung** | ✔️ Sehr gut | ❌ Eingeschränkt |
| **Ablenkung** | ✔️ Keine | ❌ Viele Elemente |




