# eCFR
Project: eCFR Analyzer : Federal Regulations

The goal of this project is to create a simple website to analyze Federal Regulations. The eCFR is available at https://www.ecfr.gov/. There is a public api for it.
This code will:
Analyze the current eCFR API and merge it for items (Word Count per Agency and Historical Changes over time)
We will also explore other opportunities for custom metrics.

There will be a front end visualization for the content where we can click around and ideally query items. 
Additionally, all code will be available on a public github project with the code and documentation.

Preliminary Steps
1.  Analyze the API Endpoints at ecfr.gov
2.  Understand current data structures of each Endpoint
3.  Verify data Endpoints to fullfill requirements (Word Count per Agency and Historical Changes over time)
4.  Review data Endpoints to expand on for Custom Metrics
5.  Document API Endpoint Flow.
6.  Found there were many issues with Search functionality within the API.

Coding
1. I have chosen to use Python's FastAPI for it's speed, ease of use, type checking, automatic interactive API documentation and asynchronous support.
2. The backend will interact with the API which will combine data from a number of endpoints.
3. The Front-end will use React - Vite : Tailwinds CSS for responsive UI - ShadCN/UI for reusable and cool components (table,tabs,cards)
4. Testing with (see code) main.py - FastAPI to retrieve data for each Title (Display Name and Amended date)
5. The main.py program was tested against many of the eCFR API endpoints to get a better understanding of the data structures.
6. A Metrics and Change History will be implemented as a tree structure on the front-end.

I try to follow the 12 Point Guide to Developing Code...
Point 12 is: 12. Optimize When Needed -Don’t prematurely optimize. First make it work, then make it fast if it becomes a bottleneck.
That is why I am only pulling a small (10) population of data in the backend during my development phase.

Please review the eCFR Agency Rule Explorer doc.  This details my understanding of the requirements for this project.
In all cases, review of the requirements would be hashed out in a Scrum session. 
This is on ongoing development...

