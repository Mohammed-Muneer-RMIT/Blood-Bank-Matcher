Blood Bank Matcher
===================

This Blood Bank Matcher project is a web application that helps match blood donors with recipients
based on blood type compatibility, donation recency, and geographic distance.
It was designed and implemented entirely by Mohammed Muneer.

------------------------------------------------------------
FEATURES
------------------------------------------------------------
- Store donor and recipient details
- Match based on:
    * ABO and Rh factor compatibility
    * Donors who have not donated within the past 56 days
    * Geographic proximity (Haversine distance)
    * Urgency score for recipient priority
- Interactive web interface built with Streamlit
- CSV-based data storage for easy portability
- Clear explanations of why each donor matches
- Ability to add new donors and recipients dynamically

------------------------------------------------------------
TECHNOLOGIES USED
------------------------------------------------------------
- Python 3.x
- Streamlit for the web UI
- Pandas for data handling
- Haversine formula for distance calculation
- CSV files for data storage
- Standard Python libraries for date/time calculations

------------------------------------------------------------
FOLDER STRUCTURE
------------------------------------------------------------
- app.py
    Main entry point for the Streamlit web app.

- matcher/matching.py
    Contains all donor matching logic.

- data/donors.csv
    Sample donor records.

- data/recipients.csv
    Sample recipient records.

- data/inventory.csv
    Optional stock/inventory data for blood types.

- requirements.txt
    Python dependencies list.

- README.md / README.txt
    Project documentation.

------------------------------------------------------------
HOW TO RUN
------------------------------------------------------------
1) Install dependencies:
    pip install -r requirements.txt

2) Start the application:
    streamlit run app.py

3) The application will open in your browser automatically.

------------------------------------------------------------
SAMPLE DATA
------------------------------------------------------------
Example Donor:
    ID: D001
    Name: Alice Smith
    Blood Type: O+
    Last Donation: 2025-05-01
    Location: Melbourne, VIC

Example Recipient:
    ID: R001
    Name: Bob Johnson
    Blood Type: A+
    Location: Geelong, VIC
    Urgency: High

------------------------------------------------------------
AUTHORSHIP
------------------------------------------------------------
This Blood Bank Matcher project was designed, coded, and implemented entirely by
Mohammed Muneer. Any resemblance to other projects is purely coincidental.

© Mohammed Muneer
