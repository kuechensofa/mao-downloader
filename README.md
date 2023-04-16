# MAO Downloader

Skript zum Downloaden und Konvertieren von Dokumenten aus dem Portal
[Materialien zur Analyse von Opposition (MAO)](https://www.mao-projekt.de/).

Die Bilder einer Seite des MAO-Archivs werden heruntergeladen und anschließend
in eine PDF-Datei konvertiert.

Die Python-Abhängigkeiten sind in [requirements.txt](requirements.txt) zu finden
und können so installiert werden:

    pip install -r requirements.txt

Benutzung:

    python mao_downloader.py URL PDF_PFAD