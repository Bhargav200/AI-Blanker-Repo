🧩 UI ARCHITECTURE OVERVIEW
This MVP UI will support:
File ingestion (single + batch)


Configuration (redaction policies)


Processing status


Results dashboard


File-level detail view


Evaluation report


Compliance summary


Logs & export


API access documentation



🖥 SCREEN 1 — Landing / Home Screen
Purpose
Entry point into the system.

Layout Structure
Top Section
Application Title


Short product description (1–2 lines)


Primary CTA button: “Start New Redaction”



Middle Section (Navigation Cards)
Four clickable cards:
New Redaction Job


View Previous Jobs


Evaluation Mode


API Access


Each card contains:
Title


Short description


Action button



Bottom Section
System status indicator


Version number


Processing queue status (if any running jobs)



📂 SCREEN 2 — File Upload Screen
Purpose
Upload files or select folder for processing.

Layout Structure
Section A — Upload Panel
Components:
Drag-and-drop upload area


“Browse Files” button


“Upload Folder” button


File type validation message area


After upload:
File table appears



Section B — Uploaded File Table
Columns:
File name


File type


File size


Status (Ready / Error)


Remove button


If batch:
Total files counter


Total size counter



Section C — Continue Section
“Configure Redaction” button


Cancel button



⚙ SCREEN 3 — Configuration Panel
Purpose
Define detection and redaction behavior.
This is the most important configuration screen.

Layout Structure (Two-Column Layout)

Left Column — Detection Configuration
1. PII Category Selection (Checkbox Group)
Grouped by category:
Structured:
Emails


Phone numbers


SSN


Credit cards


IP addresses


Bank accounts


Passport numbers


Driver licenses


Contextual:
Person names


Locations


Organizations


Dates


Custom:
Upload custom regex (textarea input)


Add regex button


Validation feedback



2. Confidence Threshold
Component:
Slider (0.0 to 1.0)


Numeric input field


Tooltip explaining impact



3. Language Hint Dropdown
Options:
English


Hindi assist


Telugu assist



Right Column — Redaction & Compliance

1. Redaction Mode Selector (Radio Buttons)
Mask


Label


Pseudonym


Synthetic replacement


If Pseudonym:
Toggle: “Maintain cross-file consistency”


If Synthetic:
Toggle: “Preserve gender context”



2. Compliance Profile Dropdown
Default


GDPR


HIPAA


DPDP


Display:
Small info panel describing selected profile



3. OCR Settings Section
Enable OCR preprocessing (checkbox)


Enable image visual masking (checkbox)



Bottom Section
Buttons:
Back


Start Processing



⏳ SCREEN 4 — Processing Screen
Purpose
Show real-time pipeline execution.

Layout Structure
Top Section
Job ID


File count


Start time



Middle Section — Progress Tracker
Progress bar with steps:
File parsing


OCR (if applicable)


Regex detection


NLP detection


Merge & scoring


Redaction


Output generation


Each step:
Status icon (Pending / Running / Complete)


Time taken



Bottom Section
Cancel job button


Expandable live log console



📊 SCREEN 5 — Results Dashboard (Batch Summary)
Purpose
High-level overview of results.

Layout Structure

Section A — Summary Metrics Row
Cards:
Total files processed


Total PII detected


High-risk entities


Average confidence score



Section B — Entity Distribution
Component:
Pie chart (entity types)


Bar chart (counts per file)



Section C — Confidence Heatmap Summary
Histogram of confidence distribution


Threshold indicator line



Section D — File Results Table
Columns:
File name


Entities detected


Risk level


View details button


Download redacted file button



Section E — Export Section
Buttons:
Download all redacted files


Export JSON audit log


Download compliance summary


Download evaluation report (if applicable)



📄 SCREEN 6 — File Detail View
Purpose
Deep dive into one processed file.

Layout Structure

Top Section
File name


Total entities


Risk level badge



Left Panel — Redacted Preview
If text:
Scrollable redacted content


Hover shows original entity + confidence


If image:
Redacted image


Toggle between original and redacted



Right Panel — Entity Table
Columns:
Entity text


Entity type


Source (Regex / NLP)


Confidence


Risk level


Position in document



Bottom Section
Reprocess file button


Download redacted version



📈 SCREEN 7 — Evaluation Report Screen
Visible only in evaluation mode.

Layout Structure

Section A — Overall Metrics
Cards:
Precision


Recall


F1 Score



Section B — Confusion Matrix
Table:
True positives


False positives


False negatives



Section C — Per-Entity Metrics
Table:
Entity type


Precision


Recall


F1



Section D — Export Button
Download evaluation report (PDF/CSV)



📘 SCREEN 8 — Compliance Summary Screen

Layout Structure

Section A — Selected Profile Overview
Compliance profile name


Summary explanation



Section B — Alignment Mapping Table
Columns:
Regulation principle


System feature


Status


Example:
Data minimization → Redaction engine → Implemented


Audit logging → JSON export → Implemented



Section C — Download Button
Download 1-page summary



🔍 SCREEN 9 — Logs & Audit Screen

Layout Structure

Section A — Job History Table
Columns:
Job ID


Date


Files processed


Status


View logs



Section B — Structured Log Viewer
Expandable JSON viewer


Search bar


Filter by entity type


Filter by risk level



Section C — Export Logs Button

🔗 SCREEN 10 — API Access Screen

Layout Structure

Section A — API Endpoint Information
POST /redact


GET /status/{job_id}


GET /download/{job_id}



Section B — Example Request
Code block display.

Section C — Example Response
JSON sample.

Section D — Generate API Key Button

🔄 COMPLETE UI FLOW (Brief Overview)
Home Screen


File Upload


Configuration


Processing


Results Dashboard


File Detail View (optional drill-down)


Export outputs


Evaluation screen (optional)


Compliance summary (optional)


Logs & API access (optional)

