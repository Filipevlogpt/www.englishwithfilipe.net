# English with Filipe — Teacher Guide

## Start the platform

Run:

`python start_server.py`

Then open `http://localhost:8000`.

For another computer on the same network, use the LAN address shown by the server.

## Teacher account

- Email: teacher@englishwithfilipe.com
- Password: Filipe2026!

Change this password before using the system with real students.

## Student demo

- Email: student@englishwithfilipe.com
- Password: English123!

Students can also create their own accounts from the login window.

## Teacher Lab

The Teacher Lab records every completed test on the server's SQLite database.

It shows:
- tests completed;
- average score;
- latest result;
- errors grouped by skill;
- errors grouped by topic;
- recommendations for what to practice next.

The current diagnostic skills are:
- grammar;
- meaning;
- vocabulary;
- usage;
- precision.

This is designed to help plan the next lesson from evidence rather than only from the final score.

## Audio

Every vocabulary item contains two local MP3 files:
- normal speed;
- slow speed.

They are stored inside `web/audio/`, so the platform does not need browser text-to-speech for vocabulary playback.

## Production note

This version is ready for HTTP/LAN and uses SQLite locally. For public internet deployment with HTTPS, domain, backups, stronger authentication, multiple teachers and cloud hosting, deploy the same application behind a production web server and move SQLite to a managed database when the number of students grows.

## Private credentials
The teacher login details are stored separately in `PRIVATE_TEACHER_NOTES.txt`. Do not send that file to students.
