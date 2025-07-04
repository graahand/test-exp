


# Park Explorer: Web Application for Sydney’s Parks

Our project **“Park Explorer”** is a web application that aggregates information on Sydney’s public parks and helps users discover suitable parks based on their needs.  Sydney has over 400 parks of various sizes, but current resources (e.g. government websites or generic map searches) do not make it easy to find parks by amenities or user ratings. Park Explorer will list at least 100 parks in Sydney (e.g. **Centennial Park, Barangaroo Reserve, Hyde Park** etc.) with detailed attributes (toilets, seating, lighting, parking, dog zones, accessibility, etc.), show their locations on an embedded map, and allow user reviews.  The app supports **user registration/login**, location-based search (showing nearby parks on a Google map with directions), and filtering by criteria (e.g. *“park with toilets and dog-friendly”*).  In short, the app becomes a one-stop guide to Sydney’s parks – addressing diverse user needs (families, dog owners, recreational groups) by aggregating park data in a user-friendly interface.

By integrating open data and user-generated content, Park Explorer fills a gap.  For example, the U.S. NRPA’s Park Path app demonstrates how GPS and park amenities data help users discover recreational activities; our app similarly uses GPS-based maps and amenity listings to guide Sydney residents to parks.  Research shows many factors (maintenance, amenities, affordability) strongly influence park accessibility and attractiveness.  By highlighting features like toilets, lighting, cafes, and ratings, Park Explorer lets users make informed choices.  This project, led by a team of four, leverages agile methods (iterative development and sprints), open datasets, and user engagement to deliver a practical system in the university’s timeframe.

## Scope

Our scope covers the **design, development, and deployment** of a web application for listing Sydney parks and amenities. Key features **included** are:

* **Park listings and details:** A database of \~100 parks with fields for location, description, and amenities (toilets, benches, cafes, lights, disability access, transport links, dog areas, parking, entry fee, monuments, etc.). These attributes are populated from open sources (e.g. City of Sydney’s open data) and manual research.
* **Interactive map integration:** Google Maps API (or similar) integration so users can view parks on a map, see nearby parks based on their current location, and get directions. Users must grant location permission to view “parks near me.”
* **Search and filters:** Ability to search parks by name or location and filter by the above attributes (e.g. “has toilets”, “outdoor lighting”, “dog off-leash area”). This makes finding a suitable park quick and easy.
* **User registration and login:** A basic authentication system (e.g. via email/password or OAuth). Registered users can leave reviews or ratings for parks. This promotes community engagement (similar to Yelp or Google reviews) and provides dynamic content.

We will **exclude** out-of-scope items such as a comprehensive admin panel or advanced backend analytics. For example, we will not build a complex CMS for park data; instead, park info is pre-loaded from data sets and manually verified. Also excluded are offline mobile app versions (the app is strictly web-based, accessible via desktop or mobile browser). The focus is on core functionality and usability rather than optional extras.

**Data collection and preparation:** We will use public data (City of Sydney open dataset on parks and related amenity layers) as a starting point, supplementing missing attributes through research (official park websites, user-contributed info). The St. Louis City open data portal provides a model for park amenity data. No private data sources are needed. All data handling will respect privacy – we only use location data with user permission for map services.

**Real-world applicability:** To simulate deployment as a practical system, we will host the app on a web server or cloud platform.  All features (maps, login, search) use production-ready tools (e.g. Google Maps API, a cloud database, and HTTPS). We will follow responsive design so the site works on various devices. Software tools include a modern web framework (such as React or Angular for front-end, Node.js/Django for back-end), GitHub for version control, Trello for agile backlog tracking, and Google Meet or Slack for team communication.

## Problem Statement
in
Sydney’s large park network offers many recreation opportunities, but **discoverability is poor**.  With 400+ parks in the City of Sydney, people must currently rely on generic map searches, word-of-mouth, or multiple websites to find parks.  There is no unified platform to search and compare parks by features (public toilets, BBQs, accessible paths, etc.), nor to see community reviews. This creates two problems: first, users (families, elderly, dog owners) may waste time visiting unsuitable parks or miss parks entirely. Second, park usage and community engagement suffer.

For example, research on park usage shows that amenities and affordability strongly influence whether people visit or enjoy parks. Inaccessible or poorly-equipped parks tend to be under-used. Yet this information is hard to obtain centrally. The City of Sydney mentions the diversity of its parks, but residents often cannot easily find the nearest park with, say, a playground and restroom. An integrated park directory with search and map (like a “Park Google”) would solve this.

**Summary of problem:** There is a lack of an easy-to-use web interface that aggregates park data (amenities, reviews, location) for Sydney. Our app solves this by collating park information into a searchable portal, thereby improving public access to park resources and encouraging use of public green spaces.

## Literature Review (Existing Solutions and Gaps)

We surveyed existing tools and research on park discovery and location-based services. While some applications exist, they do not fully meet our needs:

* **Existing apps and websites:** The U.S. NRPA’s *Park Path* app is a good example of a park finder. It uses GPS to find local park activities, shows park descriptions, photos, and amenities (restrooms, parking, Wi-Fi). Features include searching by activity, favoriting parks, and social sharing. However, Park Path focuses on recreational programming (classes, events) and is region-specific; it is also a **mobile app**, not tailored to Sydney. Similarly, Google Maps lists parks and some reviews, but lacks detailed amenity filters. No known Sydney-specific platform provides combined search on amenities and reviews.

* **Open Data models:** Some cities publish raw park datasets. For instance, the City of St. Louis provides an open dataset “City Parks” with park locations and amenities. Such data-driven sources confirm that comprehensive park inventories with amenity attributes *can* be compiled, but these are not end-user interfaces. In Sydney, City of Sydney open data notes “over 400 parks” but doesn’t supply a user-friendly directory. Thus, the gap is not a lack of data, but the lack of an application to consume it.

* **Research on parks and technology:** Studies have shown that **supporting infrastructure** in parks (toilets, lighting, seating) strongly affects accessibility and attractiveness. Another recent review of Cairo’s parks found user satisfaction tied to maintenance, activities, cost, and cultural features. This underscores our focus on amenity data: users care about these attributes. Moreover, a 2022 study demonstrated that **smartphone mobility data** can track park visits over time, highlighting the value of location-based analysis. Although our project is not analyzing pandemic trends, it suggests that location-based tools and data are valuable for understanding park usage.

* **User privacy and ethics:** Location-based services (LBS) are powerful but raise privacy issues. Research notes users will share sensitive location data if they receive valuable services in return. However, ethical use requires transparency and consent. We will address this by asking users explicitly for location permission (for “nearby parks” search) and by explaining privacy practices (no tracking beyond needed features).

**Gap summary:** In short, no solution currently provides Sydney citizens with an integrated, interactive park directory.  Existing apps either target different regions or needs, and the available open data is not readily accessible to lay users. Our literature review shows: parks offer many amenities and attract users if well-presented, location services can deliver value if used responsibly, and agile development is suited to iterative user-focused projects. We will apply these lessons: build an iteratively-tested prototype, emphasize amenity and accessibility data, and maintain ethical handling of location info.

## Aims and Objectives

**Aim:** Develop a user-friendly web application (“Park Explorer”) to **increase accessibility and usage of Sydney’s parks** by aggregating detailed park information and enabling tailored search.

**Objectives (SMART):**

1. **Comprehensive Park Database:** Compile a database of ≥100 Sydney parks with attributes (toilets, lighting, benches, dog zones, etc.) by week 6. *Specific:* List of parks with amenity fields. *Measurable:* At least 100 entries entered. *Achievable:* Using City data and research. *Relevant:* Addresses info gap. *Time-bound:* Completed mid-project.

2. **Google Maps Integration:** Integrate the Google Maps API by week 8 so users can view parks on a map and get directions. *Specific:* Map shows park markers, “near me” functionality. *Measurable:* Map displays all parks, location-based search works. *Relevant:* Key interactive feature for location-based discovery. *Time-bound:* Done before final testing.

3. **Search and Filter Functionality:** Implement search by park name/location and filters by amenities (e.g. “must have toilets and lighting”) by week 9. *Specific:* Text search box; checkboxes for each amenity. *Measurable:* User can filter to find parks meeting criteria. *Relevant:* Core user need. *Time-bound:* Functioning before project end.

4. **User Authentication & Reviews:** Provide user registration/login (using secure framework) and allow logged-in users to rate or review parks by week 10. *Specific:* User accounts created; rating system implemented. *Measurable:* Test user accounts and sample reviews. *Relevant:* Engages community in data enrichment. *Time-bound:* Ready for final submission.

5. **Documentation and Deliverables:** Prepare project documentation (requirements, design docs, testing reports) and a final report by week 12. *Specific:* Agile backlog report, sprint summaries, final user guide. *Measurable:* All deliverables completed and peer-reviewed. *Relevant:* Ensures project clarity and grading requirements. *Time-bound:* Submitted at end.

**Deliverables:** A functional website hosted (with source code on GitHub), project plan and sprint backlog (e.g. on Trello), user documentation, a final report, and a brief demonstration.

## Project Plan

We will follow an **Agile Scrum** methodology with an 8-week timeline (Weeks 4–12). The project will have 4 two-week sprints. Key tasks include requirement analysis, design, development, testing, and deployment.

* **Sprint 1 (Weeks 4-5):** Requirements and design. We’ll refine specifications (from project proposal), set up tools (GitHub, Trello), and design the database schema (parks table with amenity flags). We will also design wireframes for the UI (homepage, park details page, map view).

* **Sprint 2 (Weeks 6-7):** Basic development. Implement the backend database and API, populate initial park data (using open data). Develop front-end pages (park list and detail view, user registration form).

* **Sprint 3 (Weeks 8-9):** Advanced features. Add Google Maps integration and “nearby parks” functionality, implement search and filter controls. Begin user login and review posting functionality.

* **Sprint 4 (Weeks 10-11):** Testing and polishing. Conduct system and user testing, fix bugs, refine UI/UX. Implement final user review features (displaying ratings). Prepare deployment (e.g. hosting on cloud).

* **Week 12:** Final reports and buffer. Complete documentation, prepare demo, address any remaining issues.

Throughout, we’ll hold **weekly team meetings** (via Google Meet) to review progress. Daily stand-ups (or check-ins) on Slack will track individual tasks. We’ll use Trello for backlog and sprint planning (user stories and tasks), and GitHub issues for task tracking. The iterative approach ensures we adjust features based on progress.

**Methodology:** Our approach is iterative and incremental. Each sprint delivers a working increment of the app. Early feedback (peer and instructor) will guide refinements. We will use test-driven development where practical and continuously integrate code (pull requests on GitHub). This flexible approach handles scope changes and uncovers issues early.

**Contingency Plan:** We list potential problems and responses:

* *API Limits/Key Issues:* If Google Maps API quotas or keys fail, we can switch to an alternative (e.g. OpenStreetMap) or degrade gracefully. We will acquire any necessary API keys early.
* *Data Gaps:* If open data is incomplete, we will manually research (e.g. Council park pages) or allow “Unknown” in fields. A backup plan is to mark missing amenities clearly.
* *Time Overruns:* If certain features lag (e.g. user reviews), we may postpone them to post-delivery, ensuring core features (park list, map search) are complete first.
* *Team Availability:* If a member is unavailable, others will share tasks (all members are cross-trained on basics). Buffer time in Sprint 4 handles minor delays.
* *Technical Bugs:* Dedicated testing in each sprint (with tasks for bug fixes) will manage defects promptly. We’ll use GitHub to track bugs.

We will create a Gantt chart (separate) showing milestones: sprint boundaries, demo, report submission. Using agile avoids rigid deadlines: our backlog is prioritized (park data and map first, then search, then reviews).

## Roles and Responsibilities

Our team of four will have defined roles while maintaining collaboration:

* **Project Manager / Scrum Master (Member A):** Coordinates the project. Creates and maintains the project backlog, leads sprint planning and retrospectives, schedules meetings, ensures milestones are met. Also assists with front-end tasks as needed. Responsible for overall project documentation and communication with stakeholders.

* **Back-end Developer (Member B):** Designs and implements the server-side and database. Sets up the database schema for parks and users, implements APIs for park lookup, user authentication (e.g. using Express/Node or Django REST). Integrates Google Maps web services. Ensures data security (hashed passwords, sanitized inputs).

* **Front-end Developer (Member C):** Designs user interface and client-side logic. Implements responsive web pages (park listing, details, login page, search filters) using HTML/CSS/JS or a framework (React/Vue/Angular). Integrates map into UI. Handles user input, communicates with back-end APIs, and displays results.

* **Quality Assurance / DevOps (Member D):** Develops and runs test plans (unit, integration, user acceptance). Ensures cross-browser compatibility and mobile responsiveness. Manages deployment (configuring hosting, continuous integration scripts). Also contributes to front-end tasks if needed and coordinates code reviews.

Each member contributes to documenting their work and writes part of the final report (in respective areas). We will have **weekly group meetings** (e.g. every Monday) via Google Meet to discuss progress, and ad-hoc channels (Slack or email) for day-to-day communication. Code and documents are shared via GitHub (with protected branches and peer review on pull requests). To ensure accountability, each member updates Trello tasks they work on and demonstrates their results at sprint reviews. This clear division of labor, combined with frequent communication, ensures the project stays on track and all voices are heard.

## References

1. City of Sydney. (2024). *Our parks and open spaces provide for the diverse recreational needs of our communities \[Dataset].* Data.NSW. [https://data.nsw.gov.au/data/dataset/5-cityofsydney--parks-1](https://data.nsw.gov.au/data/dataset/5-cityofsydney--parks-1)

2. National Recreation and Park Association (NRPA). (2025). *Park Path App*. \[Online] [https://www.nrpa.org/our-work/park-path-app/](https://www.nrpa.org/our-work/park-path-app/)

3. Jay, J., Heykoop, F., Hwang, L., Courtepatte, A., de Jong, J., & Kondo, M. (2022). *Use of smartphone mobility data to analyze city park visits during the COVID-19 pandemic*. Landscape and Urban Planning, 228, 104554. [https://doi.org/10.1016/j.landurbplan.2022.104554](https://doi.org/10.1016/j.landurbplan.2022.104554)

4. Mohamed, A. A., & Kronenberg, J. (2025). *Users’ experiences of park accessibility and attractiveness based on online review analytics*. Scientific Reports, 15, 4268. [https://www.nature.com/articles/s41598-025-88500-8](https://www.nature.com/articles/s41598-025-88500-8)

5. SCRUMstudy®. (2024). *What is the iterative approach?*. [https://www.scrumstudy.com/article/iterative-approach](https://www.scrumstudy.com/article/iterative-approach)

6. National Institute for Health and Care Research (NIHR). (2023). *Green spaces are linked with better mental health*. NIHR Evidence (podcast transcript). [https://evidence.nihr.ac.uk/alert/local-green-spaces-are-linked-with-better-mental-health/](https://evidence.nihr.ac.uk/alert/local-green-spaces-are-linked-with-better-mental-health/)

7. City of St. Louis. (n.d.). *City Parks Dataset – Amenity attributes.* Open Data Portal. [https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=46](https://www.stlouis-mo.gov/data/datasets/dataset.cfm?id=46)

8. DevelopersAppIndia. (2024). *The Ethical Considerations of Location Tracking in Mobile Apps*. [https://developersappindia.com/blog/the-ethical-considerations-of-location-tracking-in-mobile-apps](https://developersappindia.com/blog/the-ethical-considerations-of-location-tracking-in-mobile-apps)

9. Schmidtke, H. R. (2020). *Location-aware systems or location-based services: a survey with applications to COVID-19 contact tracking*. Journal of Reliable Intelligent Environments, 6(4), 191–214. [https://doi.org/10.1007/s40860-020-00111-4](https://doi.org/10.1007/s40860-020-00111-4)

10. City of Sydney. (n.d.). *Parks*. City of Sydney official website. [https://www.cityofsydney.nsw.gov.au/places/parks](https://www.cityofsydney.nsw.gov.au/places/parks)
