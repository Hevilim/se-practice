# SIS #01 — Software Engineering Fundamentals, With an AI in the Loop

<!--
  This is the only file you write your report in. README.md tells you what goes where.

  Rules the checker relies on:
  - Do not delete, rename or renumber the ## headings, the ### headings, or the **Label:** words.
  - Replace every "(write here)" and "(paste here)". None may be left when you submit.
  - Comments like this one are ignored by the word counter. Delete them or leave them.
-->

**Topic:** 1.1

<!-- Exactly one of 1.1 … 1.10, e.g.  **Topic:** 1.4  -->

---

## 1. Scenario

<!-- 100–150 words, labels included. One small scenario, used in every prompt and in your
     whole answer. Anything fictional is labelled in Assumptions. -->

**Question:** When we give the Smart Campus room booking system to the university, what does the customer need besides the program code?

**Users:** Students who book study rooms, and one administrator who blocks rooms and checks room use.

**Problem:** The booking function works and passes its tests. But the university must install the system, teach people to use it and fix it later. Code alone does not help them do this.

**Constraints:** The team is two students with four weeks. After delivery the university IT staff, not the team, must support the system.

**Risk:** Someone changes the booking rules later, nobody runs the tests, and two students get the same room at the same time.

**Assumptions:** The university, the team size, the four weeks and the IT staff are fictional. The booking rules come from my week-05 lab.

## 2. Analysis

<!-- 350–400 words. Your answer to the question, the trade-offs, and how it applies to your
     scenario. Explain at least two engineering decisions and why they fit the scenario. -->

Sommerville says software is computer programs and associated documentation (slide 7). So when we give Smart Campus to the university, the code is only one part. The IT staff, not our team, will run and change the system later, and slide 13 says most costs come after a system is in use. So the customer needs things that let other people install, use and change the system.

First, installation. The IT staff need a step by step installation guide and the configuration data: the room list, the 120 minute limit and the administrator account. Without it nobody can book a room.

Second, use. Students need a one page guide to find, book and cancel a room, and the admin needs a guide to block rooms and check room use. Slide 11 says good software must be acceptable, which means understandable and usable, so the guides are part of the product. I assume login is the university single sign-on, so we do not store passwords, but this must be confirmed.

Third, acceptance. We hand over the requirements list and the acceptance test cases, so the university can check every requirement before it starts to use the system.

Fourth, maintenance. Slide 11 also says software must be maintainable. IT needs the source code in a repository, a README that explains how to run the system and the tests, database documentation, backup and restore steps and a list of known limitations.

Engineering decision 1: write the booking rule down and test it. The rule is that bookings for the same room must not overlap, but one can start when another ends. Our risk is that someone changes the rules and two students get the same room. Our tests run one request at a time, so the team adds one test where two requests for the same room and time come at the same time, and only one may pass. A database rule against overlaps is a possible extra protection, but it depends on how bookings are stored.

Engineering decision 2: two students in four weeks can not make everything perfect. We put most time into things IT can not easily make later: the installation guide, the configuration data, the README with test instructions, the written booking rule and the backup steps. User guides stay one page, and the handover is one demonstration. The trade-off is that features get less time.

## 3. Review

<!-- 250–300 words. What Prompt B's critique said and what you did with it; your two source
     checks and your two substantive revisions, each with a reason. Point at the rows of the
     tables in section 9 ("verification row 2", "change-log row 1"). -->

Prompt B gave 13 points. I accepted points 1, 2, 3, 5, 6, 9, 10 and 12. For example, the draft said "code alone supports none of these tasks", which is too strong. It also said students need passwords, but my scenario does not say how users log in, so I made single sign-on an assumption. I qualified points 4, 7 and 8: the single admin is a decision for the university, a database rule is only one option, and automatic test runs only help if IT owns them. For point 11 I accepted backup and known limitations, but rejected licence and versions because of the word limit. For point 13 I rejected the word count note, because it is not about content.

I challenged one AI claim. Prompt A said Sommerville 1.1 says software is programs, documentation and configuration data. The slide only says programs and associated documentation (verification row 1), so I qualified it. I still need configuration data, but as a need of my scenario, not as a textbook quote. The second check, slide 11, confirmed the attributes of good software, so I kept it (verification row 2). I opened the slides myself, and Claude also read them. I did not open the book itself.

Then I changed the revised draft. Change-log row 1: the AI listed opening hours, but my rules have no opening hours, so I wrote the 120 minute limit. Change-log row 2: the AI only said that two requests at the same time are not tested. Double booking is my main risk, so I added a test for it. Change-log row 3: I used slide 11 for maintainability and acceptability, not only for security.

## 4. Conclusion

<!-- 100–150 words. Your recommendation for the scenario and its main limitation. -->

My recommendation is that the team hands over the code together with the configuration data, an installation guide, a README with test instructions, short user and admin guides, the requirements and acceptance test cases, maintenance documents with backup steps, and one handover demonstration. The most important extra work is to write the booking rule down and add a test for two requests at the same time, because double booking is the main risk after the team leaves.

The main limitation is that my evidence comes only from the Chapter 1 slides, not from the book, and that some points are assumptions: the login method, the database and the repository. With two students and four weeks the documents will also be short, so the IT staff may still have questions that no document answers.

## 5. Reflection

<!-- 150–200 words. NOT part of the main total. Written by you, not by the assistant:
     what helped, what you changed, what you learned. Specific beats flattering. -->

Before this lecture I thought that software is just a program, some code that run on computer. But in the first slide I learned that software is not only programs, it is also documentation. This was a little surprise for me, because I usually don't write documentation for my projects. Now I understand that without documentation other people can't understand or change the program easy.

Also I learned the four attributes of good software: maintainability, dependability and security, efficiency and acceptability. For me the most important one is maintainability. I do some small projects for clients, and almost every time client come back and ask to change something. When my code was messy, it took a lot of time to fix it. So I agree with the idea that software must can evolve, because the business always changing.

The last slide said that most of the cost is not writing the program, but changing it after people start using it. At first I didn't believe it, but then I remember my own experience and it is true. Fixing and adding features take more time than first version.

## 6. References

<!-- Full references, one per line, each starting with "- ". Only sources you actually opened.
     Every URL used in the verification table must also appear here. Example:
     - Sommerville, I. (2016). Software Engineering, 10th ed., Global Edition. Pearson. Ch. 1.
-->

- Sommerville, I. (2014). Software Engineering, 10th ed., Chapter 1 Introduction lecture slides (Ch1 Introduction.pptx). https://software-engineering-book.com/slides/ (accessed 2026-10-07).

## 7. Appendix A — Initial outline

<!-- Written BEFORE you run Prompt A. Five points, your own words, numbered. These are the
     "five points" you paste into Prompt A. -->

1. The university needs a server or cloud, the needed software (database, web server), and a simple step-by-step installation guide.
2. Students need a login and a short user guide, and the admin needs an admin account and an admin guide.
3. The university can test the main tasks with real users and check that every requirement works, and the system should show errors in logs.
4. The IT team needs the full source code on GitHub, a README on how to run it, and technical documentation about the structure and database.
5. Security of student data, user training, and clear documentation are as important as the code, because without them the system is hard to use and hard to support.

## 8. Appendix B — AI exchanges

<!-- Complete prompts and complete responses, as text — never screenshots. Paste each inside
     the fenced block that follows its label. If a response itself contains ``` lines, open
     and close that block with ~~~~ instead. You may add B4, B5 … after B3 if you ran more. -->

### B1 — Draft (Prompt A)

- **Tool:** Claude (claude.ai)
- **Model:** Claude Opus 5.5
- **Date:** 2026-10-07
- **Purpose:** contextual draft

<!-- Model: the exact model with its version, as the tool shows it (e.g. "GPT-5 Thinking",
     "Claude Sonnet 4.5"). If the tool does not show it, write: not displayed
     Date: YYYY-MM-DD -->

**Prompt:**

```text
Act as a software engineering tutor. Help me analyze topic 1.1 Professional software delivery: When we give the Smart Campus room booking system to the university, what does the customer need besides the program code? for a first-year-level university assignment.

My scenario is Users: students who book study rooms, and one administrator who blocks rooms and checks room use. Problem: the booking function works and passes its tests, but the university must install the system, teach people to use it and fix it later; code alone does not help them do this. Constraints: the team is two students with four weeks; after delivery the university IT staff, not the team, must support the system. Risk: someone changes the booking rules later, nobody runs the tests, and two students get the same room at the same time. My initial ideas are 1. The university needs a server or cloud, the needed software (database, web server), and a simple step-by-step installation guide. 2. Students need a login and a short user guide, and the admin needs an admin account and an admin guide. 3. The university can test the main tasks with real users and check that every requirement works, and the system should show errors in logs. 4. The IT team needs the full source code on GitHub, a README on how to run it, and technical documentation about the structure and database. 5. Security of student data, user training, and clear documentation are as important as the code, because without them the system is hard to use and hard to support. Draft a 400–500 word explanation using these details.

Separate facts from assumptions. Explain trade-offs and identify claims I should verify. Do not invent quotations, references or page numbers.
```

**Response:**

```text
Here's a 421-word draft built from your five ideas, plus the fact/assumption split and what to check.

---

**What the customer needs besides the program code**

When software is delivered professionally, the customer receives a product, not only a program. The Smart Campus booking function works and passes its tests, but the university must still install the system, teach people to use it and maintain it after the team leaves. Code alone supports none of these tasks.

**Installation.** The university needs a server or cloud account, the required software (for example a database and a web server) and a step-by-step installation guide. Configuration settings, such as database connection details, should be listed in one place so IT staff do not have to search the code.

**Users.** Students need a login and a short user guide on how to find, book and cancel a room. The administrator needs a separate admin account and a guide on blocking rooms and checking room use. Because there is only one administrator, the guide should also say what to do when that person is unavailable.

**Acceptance.** Before the system goes live, the university should test the main tasks with real students and the administrator and check each requirement. The system should record errors in logs so problems can be found after delivery.

**Maintenance.** The main risk appears after delivery: someone changes the booking rules, nobody runs the tests, and two students get the same room at the same time. To reduce this, the IT staff need the full source code in a repository, a README explaining how to run the system and the tests, and technical documentation of the structure and database. The tests should run automatically whenever the code changes, and the database itself should reject two bookings for the same room and time, so the rule is protected even if a test is skipped.

**Security and training.** The system stores student data, so access must be limited to the right accounts and passwords must be stored safely. Users and IT staff also need a short training or handover session.

**Trade-offs.** Two students in four weeks cannot produce everything at full quality. The most valuable items are those the IT staff cannot easily create themselves: the installation guide, the README, automated tests and database documentation. User guides can be short, and training can be one demonstration instead of a full course. Documentation takes time away from features, but without it the university cannot use or support the system.

In conclusion, the customer needs the code together with installation instructions, user and admin guides, tests, documentation and a handover, so the university can run the system safely after the team has gone.

---

**Facts (given in your scenario)**
- Users are students plus one administrator.
- The booking function works and passes its tests.
- The team is two students with four weeks.
- The university IT staff, not the team, support the system after delivery.
- The double-booking risk comes from rule changes made without running the tests.

**Assumptions (I or you added these, so state them as such)**
- It's a web app with a database and web server. Your scenario never says so.
- The university uses GitHub. It may require its own internal repository.
- The university can choose between a server and the cloud. Its IT policy may decide this.
- A database constraint can block double bookings. Whether this works depends on how bookings are stored, for example with overlapping time ranges rather than fixed slots.
- Training fits into one session.

**Trade-offs to be ready to defend**
- **Documentation vs features.** Four weeks is tight, so I put IT-facing documents first. You could argue user guides matter more if students struggle with the interface.
- **Automated tests vs a database constraint.** Tests catch more kinds of bugs but only help if someone runs them. A constraint always runs but only protects one rule. The draft uses both.
- **Logs vs privacy.** Error logs help support, but they shouldn't record personal data unnecessarily.

**Claims to verify**
- **The textbook definition.** Check what Sommerville's section 1.1 says software includes (programs plus documentation and configuration data). Don't quote it from memory or add a page number you haven't checked.
- **Your topic title.** You wrote "professional software delivery." Make sure it matches the name your course uses for 1.1.
- **Data protection rules.** "Student data must be protected" is true in general. If you want to name a specific law or KBTU policy, find the actual one first.
- **Your assignment format.** If your Software Engineering assignments need an AI-use evidence appendix, include this conversation in it.
```

### B2 — Critique (Prompt B)

- **Tool:** Claude (claude.ai)
- **Model:** Claude Opus 5.5
- **Date:** 2026-10-07
- **Purpose:** critical review of the draft

**Prompt:**

```text
Review the draft below against my chosen question and scenario. Identify inaccuracies, missing reasoning, vague claims and unsupported assumptions.
For each concern, explain why it matters and how I could check it. Include a counterexample or alternative interpretation. Do not rewrite the answer yet.
Question: When we give the Smart Campus room booking system to the university, what does the customer need besides the program code? Scenario: Users: students who book study rooms, and one administrator who blocks rooms and checks room use. Problem: the booking function works and passes its tests, but the university must install the system, teach people to use it and fix it later; code alone does not help them do this. Constraints: the team is two students with four weeks; after delivery the university IT staff, not the team, must support the system. Risk: someone changes the booking rules later, nobody runs the tests, and two students get the same room at the same time. Assumptions: the university, the team size, the four weeks and the IT staff are fictional. Draft: Here's a 421-word draft built from your five ideas, plus the fact/assumption split and what to check.

---

**What the customer needs besides the program code**

When software is delivered professionally, the customer receives a product, not only a program. The Smart Campus booking function works and passes its tests, but the university must still install the system, teach people to use it and maintain it after the team leaves. Code alone supports none of these tasks.

**Installation.** The university needs a server or cloud account, the required software (for example a database and a web server) and a step-by-step installation guide. Configuration settings, such as database connection details, should be listed in one place so IT staff do not have to search the code.

**Users.** Students need a login and a short user guide on how to find, book and cancel a room. The administrator needs a separate admin account and a guide on blocking rooms and checking room use. Because there is only one administrator, the guide should also say what to do when that person is unavailable.

**Acceptance.** Before the system goes live, the university should test the main tasks with real students and the administrator and check each requirement. The system should record errors in logs so problems can be found after delivery.

**Maintenance.** The main risk appears after delivery: someone changes the booking rules, nobody runs the tests, and two students get the same room at the same time. To reduce this, the IT staff need the full source code in a repository, a README explaining how to run the system and the tests, and technical documentation of the structure and database. The tests should run automatically whenever the code changes, and the database itself should reject two bookings for the same room and time, so the rule is protected even if a test is skipped.

**Security and training.** The system stores student data, so access must be limited to the right accounts and passwords must be stored safely. Users and IT staff also need a short training or handover session.

**Trade-offs.** Two students in four weeks cannot produce everything at full quality. The most valuable items are those the IT staff cannot easily create themselves: the installation guide, the README, automated tests and database documentation. User guides can be short, and training can be one demonstration instead of a full course. Documentation takes time away from features, but without it the university cannot use or support the system.

In conclusion, the customer needs the code together with installation instructions, user and admin guides, tests, documentation and a handover, so the university can run the system safely after the team has gone.

---

**Facts (given in your scenario)**
- Users are students plus one administrator.
- The booking function works and passes its tests.
- The team is two students with four weeks.
- The university IT staff, not the team, support the system after delivery.
- The double-booking risk comes from rule changes made without running the tests.

**Assumptions (I or you added these, so state them as such)**
- It's a web app with a database and web server. Your scenario never says so.
- The university uses GitHub. It may require its own internal repository.
- The university can choose between a server and the cloud. Its IT policy may decide this.
- A database constraint can block double bookings. Whether this works depends on how bookings are stored, for example with overlapping time ranges rather than fixed slots.
- Training fits into one session.

**Trade-offs to be ready to defend**
- **Documentation vs features.** Four weeks is tight, so I put IT-facing documents first. You could argue user guides matter more if students struggle with the interface.
- **Automated tests vs a database constraint.** Tests catch more kinds of bugs but only help if someone runs them. A constraint always runs but only protects one rule. The draft uses both.
- **Logs vs privacy.** Error logs help support, but they shouldn't record personal data unnecessarily.

**Claims to verify**
- **The textbook definition.** Check what Sommerville's section 1.1 says software includes (programs plus documentation and configuration data). Don't quote it from memory or add a page number you haven't checked.
- **Your topic title.** You wrote "professional software delivery." Make sure it matches the name your course uses for 1.1.
- **Data protection rules.** "Student data must be protected" is true in general. If you want to name a specific law or KBTU policy, find the actual one first.
- **Your assignment format.** If your Software Engineering assignments need an AI-use evidence appendix, include this conversation in it.
```

**Response:**

```text
# Review of the draft

Each concern lists the problem, why it matters, how to check it, and a counterexample or alternative interpretation.

### 1. "Code alone supports none of these tasks" is overstated
- **Why it matters:** An absolute claim is easy to attack. One counterexample weakens the whole opening.
- **Check:** Ask whether install scripts, a Dockerfile or test files count as "code" in your course's definition.
- **Counterexample:** A repository with a `docker-compose` file and seed scripts partly supports installation without any written guide. A weaker claim would be safer, for example that code alone is not enough for a non-author to install, use and maintain the system.

### 2. Configuration data is missing, even though it is part of the textbook definition
- **Why it matters:** The draft's own "claims to verify" says Sommerville 1.1 defines software as programs plus documentation plus configuration data. The answer still never says what the configuration data is. For a booking system, that means the list of rooms, capacities, opening hours, booking limits and the admin account. Without this data, the system installs but cannot be used.
- **Check:** Reread 1.1 and list which deliverable in the draft covers each part of the definition.
- **Alternative interpretation:** Someone could argue that the university enters rooms itself. Even then, it needs to know the format and where to enter them, so this has to be documented.

### 3. The "login" assumption is unsupported
- **Why it matters:** "Students need a login" and "passwords must be stored safely" assume the system has its own accounts. The scenario never mentions how users log in.
- **Check:** Look at whether the scenario mentions authentication. It doesn't.
- **Counterexample:** The university may require its existing single sign-on with student ID. Then the system stores no passwords, and the security point changes to role mapping (student vs admin). This is not in the assumptions list, so it should either be added there or the claim should be removed.

### 4. "What to do when the administrator is unavailable" may be scope creep
- **Why it matters:** It sounds like a deliverable, but a real fix needs either a second admin role (a requirement change) or an organisational rule (the university's decision, not the team's).
- **Check:** Does the scenario's "one administrator" describe the current situation or a requirement?
- **Alternative interpretation:** The point is better framed as a risk handed over to the university than as content for a guide.

### 5. The Acceptance section mixes up who does what
- **Why it matters:** "The university should test…" describes the customer's activity, but the question asks what the customer needs from the team. The answer would be acceptance criteria, a test plan and test data. "Check each requirement" also assumes a requirements document exists, yet that document is never listed as a deliverable. Logging is an operational feature, not acceptance, so it belongs in the wrong section.
- **Check:** For each sentence, ask whether it names something the team hands over.
- **Counterexample:** If no written requirements exist, "check each requirement" cannot be done.

### 6. Passing tests does not prove the double-booking risk is covered
- **Why it matters:** The scenario says the function passes its tests. It does not say there is a test for two simultaneous requests. Typical unit tests run sequentially, so a race condition can pass all tests and still produce double bookings. The draft treats running the tests as the protection without asking what the tests check.
- **Check:** Is there a test where two bookings for the same room and time arrive at once?
- **Alternative interpretation:** This makes the database constraint the stronger argument, and the draft should say why.

### 7. The database constraint is stated more confidently than the assumptions list allows
- **Why it matters:** The essay states "the database should reject two bookings" as a fact. The assumptions section admits it depends on how bookings are stored. Overlapping time ranges need an exclusion constraint, which PostgreSQL supports directly. Fixed slots only need a unique constraint. Other databases may not support the first option easily.
- **Check:** Find out whether the scenario's system uses slots or free time ranges, and which database it uses.
- **Counterexample:** A later legitimate rule change, such as allowing shared group rooms, may require dropping the constraint. Then the protection disappears, which is exactly the risk scenario. A strong point to add is that the booking rule itself must be documented as an invariant, so whoever changes it knows what must stay true.

### 8. Automatic test runs (CI) are assumed without saying who maintains them
- **Why it matters:** "Tests should run automatically whenever the code changes" needs a CI setup on the university's infrastructure. The team leaves, so the IT staff must own and understand that setup.
- **Check:** Does the university's environment support CI? Is the CI configuration and how to use it part of the handover?
- **Counterexample:** If IT changes code directly on the server, outside the repository, CI never runs. That repeats the scenario's risk.

### 9. The trade-offs section is inconsistent and unsupported
- **Why it matters:**
  - It lists "automated tests" as a high-value item to produce, but tests already exist. The real gap is automation and concurrency coverage.
  - "Two students in four weeks cannot produce everything at full quality" has no estimate behind it.
  - It is unclear whether the four weeks includes the already finished booking function or is the remaining time.
- **Check:** Make a rough list of effort per deliverable and see if it fits.
- **Alternative interpretation:** If most of the four weeks remains, the team may be able to produce everything in a minimal form. In that case the trade-off is about depth, not about which items to drop.

### 10. Several claims are vague
- "Delivered professionally… a product, not only a program": "professionally" and "product" are not defined. Link them to the 1.1 definition, or drop them.
- "Access must be limited to the right accounts": does not say who should see what. For example, can a student see who booked a room?
- "Short training or handover session": does not say who attends, what is covered, or how long it takes.
- "Student data": does not say which data is stored (name, ID, booking history) or for how long.
- **Check:** For each vague phrase, ask whether a reader could check that it was done.

### 11. Handover items that are missing entirely
These are relevant because the team will not support the system after delivery:
- known limitations and open bugs
- backup and restore procedure
- ownership and licence of the code and of third-party libraries
- the exact versions of dependencies
- **Check:** Imagine the system breaks six months later and the team is unreachable. What would IT need that is not on the list?
- **Counterexample to the draft's priorities:** Backup may matter more than training. A lost bookings database cannot be recovered with a user guide.

### 12. The facts/assumptions section doesn't match the draft
- **Why it matters:** It lists "the university uses GitHub" as an assumption, but the essay says only "a repository." It also misses assumptions the essay does make: separate logins, CI availability, and a written requirements document.
- **Check:** Go through the essay sentence by sentence and tag each claim as given in the scenario or added.

### 13. Small checks
- Verify the "421 words" claim against your assignment's word limit.
- The conclusion lists "tests" as something besides code, but tests are code. Say "automated test runs" or "test documentation" instead.
- If you link the answer to Sommerville, chapter 1 also discusses essential attributes of good software, such as maintainability and dependability. Check whether your edition lists them. If it does, they give the Maintenance and Security sections a textbook basis instead of opinion.

**Highest priority to fix:** #2 (configuration data), #6–7 (the double-booking reasoning), and #3 (the login assumption). These affect the core argument. The rest are about precision.
```

### B3 — Revision (Prompt C)

- **Tool:** Claude (claude.ai)
- **Model:** Claude Opus 5.5
- **Date:** 2026-10-07
- **Purpose:** revision using my decisions and verified evidence

**Prompt:**

```text
Revise the draft using my review decisions and source notes below. Keep the answer relevant to my scenario and preserve uncertainty where evidence is limited.

My decisions: 1 accept: code alone is not enough for other people to install, use and maintain the system, so I will not say "none". 2 accept: add configuration data for our system (list of rooms, opening hours, booking limits, the admin account). But the slides I checked only say programs and documentation, so I keep this as our scenario need, not as a textbook quote. 3 accept: the scenario does not say how users log in. Write it as an assumption (maybe the university single sign-on) and remove the password claim. 4 qualify: keep "only one administrator" as a risk the university must decide on, not as text for the guide. 5 accept: the team hands over a list of requirements and acceptance test cases. Move logs to maintenance. 6 accept: the existing tests do not test two requests at the same time. Say this clearly. 7 qualify: a database rule against double booking is an option, not a fact. Add that the booking rule (no overlap, touching bookings allowed) must be written down so anyone who changes it knows what must stay true. 8 qualify: automatic test runs are useful, but the IT staff must own them, so the README must explain how to run them. 9 accept: tests already exist. The trade-off is how deep each item is, not which items to drop. 10 accept: link "professional" to the textbook. Say who sees what: a student sees free times, the admin sees who booked. 11 accept backup and restore and known limitations. Reject licence and exact versions, because of the word limit; versions go in the README. 12 accept: fix the assumptions list. 13 accept: tests are code, so say "test instructions". Reject the word count point, it is not about content. Verified evidence: Sommerville, I. Software Engineering, 10th ed., Chapter 1 Introduction lecture slides (Ch1 Introduction.pptx), https://software-engineering-book.com/slides/, accessed 2026-10-07. Slide 7: "What is software? Computer programs and associated documentation." Configuration data is not on this slide. Slide 11, Essential attributes of good software: maintainability, dependability and security, efficiency, acceptability. Slide 13: for most types of system, the majority of costs are the costs of changing the software after it has gone into use. Draft: Here's a 421-word draft built from your five ideas, plus the fact/assumption split and what to check.

---

**What the customer needs besides the program code**

When software is delivered professionally, the customer receives a product, not only a program. The Smart Campus booking function works and passes its tests, but the university must still install the system, teach people to use it and maintain it after the team leaves. Code alone supports none of these tasks.

**Installation.** The university needs a server or cloud account, the required software (for example a database and a web server) and a step-by-step installation guide. Configuration settings, such as database connection details, should be listed in one place so IT staff do not have to search the code.

**Users.** Students need a login and a short user guide on how to find, book and cancel a room. The administrator needs a separate admin account and a guide on blocking rooms and checking room use. Because there is only one administrator, the guide should also say what to do when that person is unavailable.

**Acceptance.** Before the system goes live, the university should test the main tasks with real students and the administrator and check each requirement. The system should record errors in logs so problems can be found after delivery.

**Maintenance.** The main risk appears after delivery: someone changes the booking rules, nobody runs the tests, and two students get the same room at the same time. To reduce this, the IT staff need the full source code in a repository, a README explaining how to run the system and the tests, and technical documentation of the structure and database. The tests should run automatically whenever the code changes, and the database itself should reject two bookings for the same room and time, so the rule is protected even if a test is skipped.

**Security and training.** The system stores student data, so access must be limited to the right accounts and passwords must be stored safely. Users and IT staff also need a short training or handover session.

**Trade-offs.** Two students in four weeks cannot produce everything at full quality. The most valuable items are those the IT staff cannot easily create themselves: the installation guide, the README, automated tests and database documentation. User guides can be short, and training can be one demonstration instead of a full course. Documentation takes time away from features, but without it the university cannot use or support the system.

In conclusion, the customer needs the code together with installation instructions, user and admin guides, tests, documentation and a handover, so the university can run the system safely after the team has gone.

---

**Facts (given in your scenario)**
- Users are students plus one administrator.
- The booking function works and passes its tests.
- The team is two students with four weeks.
- The university IT staff, not the team, support the system after delivery.
- The double-booking risk comes from rule changes made without running the tests.

**Assumptions (I or you added these, so state them as such)**
- It's a web app with a database and web server. Your scenario never says so.
- The university uses GitHub. It may require its own internal repository.
- The university can choose between a server and the cloud. Its IT policy may decide this.
- A database constraint can block double bookings. Whether this works depends on how bookings are stored, for example with overlapping time ranges rather than fixed slots.
- Training fits into one session.

**Trade-offs to be ready to defend**
- **Documentation vs features.** Four weeks is tight, so I put IT-facing documents first. You could argue user guides matter more if students struggle with the interface.
- **Automated tests vs a database constraint.** Tests catch more kinds of bugs but only help if someone runs them. A constraint always runs but only protects one rule. The draft uses both.
- **Logs vs privacy.** Error logs help support, but they shouldn't record personal data unnecessarily.

**Claims to verify**
- **The textbook definition.** Check what Sommerville's section 1.1 says software includes (programs plus documentation and configuration data). Don't quote it from memory or add a page number you haven't checked.
- **Your topic title.** You wrote "professional software delivery." Make sure it matches the name your course uses for 1.1.
- **Data protection rules.** "Student data must be protected" is true in general. If you want to name a specific law or KBTU policy, find the actual one first.
- **Your assignment format.** If your Software Engineering assignments need an AI-use evidence appendix, include this conversation in it.

Show what you changed and why. Use only the sources I supplied. Flag remaining gaps instead of inventing details.
```

**Response:**

```text
Here's the revised draft (505 words, up from 421; the extra length comes mostly from the backup, known-limitations and booking-rule additions). I used only the Sommerville Chapter 1 slides you checked.

---

**What the customer needs besides the program code**

Sommerville defines software as computer programs and associated documentation (Sommerville, Ch. 1 slides, slide 7). Professional delivery therefore means handing over a product that other people can install, use and maintain. The Smart Campus booking function works and passes its tests, but after the team leaves, the university IT staff must run and change it. Code alone is not enough for that.

**Installation.** The IT staff need a step-by-step installation guide and the configuration data for our system: the room list, opening hours, booking limits and the administrator account. The slide does not mention configuration data, but our system cannot run without it, so it should be documented in one place.

**Users.** Students need a short guide to finding, booking and cancelling a room. The administrator needs one on blocking rooms and checking room use. The scenario does not say how users log in. I assume the university single sign-on, which must be confirmed. Because there is only one administrator, the university must decide who acts when that person is unavailable.

**Acceptance.** The team hands over the requirements list and the acceptance test cases. The university can then check each requirement with real students and the administrator before go-live.

**Maintenance.** For most systems, most costs come from changing the software after it is in use (slide 13). Our main risk is that someone changes the booking rules and two students get the same room. The existing tests do not test two requests arriving at the same time, so this case is not covered. The booking rule must therefore be written down: bookings for the same room must not overlap, but one may start exactly when another ends. Anyone changing the code then knows what must stay true. A database rule rejecting overlaps is one option for enforcing it. The IT staff also need:
- the source code in a repository
- a README explaining how to run the system and the tests
- structure and database documentation
- error logs
- backup and restore steps
- a list of known limitations

Automatic test runs help only if the IT staff own them, so the README must explain how to run the tests.

**Security.** Good software is maintainable, dependable and secure, efficient and acceptable (slide 11). Each role should see only what it needs: a student sees free times, and the administrator sees who booked.

**Trade-offs.** Two students in four weeks cannot produce everything in full detail. The tests already exist, so the question is how deep each item goes, not which items to drop. The following should be complete, because the IT staff cannot easily recreate them:
- the installation guide
- the configuration data
- the README with test instructions
- the written booking rule
- the backup steps

User guides can be one page each, and the handover can be one demonstration. This time comes from features, but without it the university cannot run or support the system.

In conclusion, besides the code the customer needs configuration data, installation and test instructions, user and admin guides, requirements and acceptance test cases, maintenance documentation and a handover.

**Reference:** Sommerville, I. *Software Engineering*, 10th ed., Chapter 1 Introduction lecture slides (Ch1 Introduction.pptx), https://software-engineering-book.com/slides/, accessed 7 October 2026.

---

**What I changed and why**

1. I replaced "Code alone supports none of these tasks" with "Code alone is not enough for that."
2. I added configuration data (rooms, hours, limits, admin account) as a need of our system. The draft also says outright that the slide does not list it, so it doesn't read as a textbook quote.
3. I removed the password sentence. Single sign-on is now marked as an assumption to confirm.
4. "Only one administrator" is now a decision the university must make. It is no longer guide content.
5. Acceptance now means handing over the requirements and acceptance test cases. I moved logs to Maintenance.
6. I added: "The existing tests do not test two requests arriving at the same time."
7. A database rule is now "one option." I added the written booking rule: no overlap, but touching bookings are allowed.
8. I removed "tests should run automatically." Automatic runs are now conditional on the IT staff owning them, and the README must explain how to run the tests.
9. The trade-off is now about depth per item. I removed "automated tests" from the priority list because the tests already exist.
10. "Professional" is now tied to slide 7, and Security to slide 11. Who sees what is stated per role.
11. I added backup and restore and known limitations. Licence and versions are left out, and versions are covered by the README.
12. I rewrote the assumptions list (below).
13. "Automated tests" is now "README with test instructions" as a deliverable. The word count point is unchanged.

I also used slide 13 to justify why Maintenance carries the main risk. I cut "logs vs privacy" because it had no source and didn't come from your decisions.

**Facts (from your scenario and review)**
- Users are students plus one administrator.
- The booking function works and passes its tests.
- The existing tests do not cover two requests at the same time.
- The team is two students with four weeks.
- The university IT staff support the system after delivery.
- The risk is double booking after someone changes the booking rules.
- The booking rule is no overlap, with touching bookings allowed.

**Assumptions (state them as such)**
- Login is through the university single sign-on.
- The system stores bookings in a database. The scenario doesn't say so, and the database rule option depends on it.
- A database rule can enforce no overlap. This depends on how bookings are stored, for example as time ranges or as fixed slots.
- The university has or will choose a code repository. Which one it uses is not stated.
- The configuration items listed (rooms, hours, limits, admin account) are the ones our system needs. This is our scenario need, not textbook content.

**Remaining gaps**
- **Word limit.** You mentioned a limit but not the number. At 505 words, check it before submitting. If it's 450, the easiest cuts are the slide 11 sentence and the "This time comes from features…" sentence.
- **Section 1.1 text.** I only have the slides. If your instructor wants the textbook section itself cited, check whether it says more than slide 7 before changing the configuration-data sentence.
- **Citation style.** I used a simple reference line. Use your course's format if it has one.
- **"Smart Campus."** I kept the name from the earlier draft. Confirm it matches your scenario.
- **AI evidence appendix.** If this assignment needs one like Assignment #01, include this review exchange.
```

## 9. Appendix C — Evidence tables

### Verification table

<!-- At least two complete rows. Source and locator: title + page / slide / section / chapter,
     or title + URL + access date (YYYY-MM-DD). Decision: keep, qualify or reject — one word. -->

| AI claim | Source and locator | Evidence found | Decision |
| --- | --- | --- | --- |
| Sommerville's section 1.1 says software includes (programs plus documentation and configuration data) | Sommerville, Software Engineering 10th ed., Chapter 1 Introduction lecture slides, slide 7, https://software-engineering-book.com/slides/, accessed 2026-10-07 | The slide says software is computer programs and associated documentation. Configuration data is not on the slide. I did not open the book itself, so I can not say if section 1.1 says more. | qualify |
| chapter 1 also discusses essential attributes of good software, such as maintainability and dependability | Sommerville, Software Engineering 10th ed., Chapter 1 Introduction lecture slides, slide 11, https://software-engineering-book.com/slides/, accessed 2026-10-07 | The slide has a table with four attributes: maintainability, dependability and security, efficiency and acceptability. Acceptability means the software is understandable and usable for its users. | keep |

### Change log

<!-- At least two substantive revisions. Your final version must differ from the AI wording,
     and the reason must say which evidence or scenario constraint made you change it. -->

| AI wording / suggestion | Your final version | Reason for change |
| --- | --- | --- |
| the configuration data for our system: the room list, opening hours, booking limits and the administrator account | the configuration data: the room list, the 120 minute limit and the administrator account | Our booking rules have no opening hours rule. The limit is the 120 minute rule from my week-05 lab, so I wrote the real limit and removed opening hours. |
| The existing tests do not test two requests arriving at the same time, so this case is not covered. | The team adds one test where two requests for the same room and time come at the same time, and only one may pass. | The AI only said the case is not covered. The risk in my scenario is exactly double booking, so the gap must be closed with a test, not only described. |
| Security. Good software is maintainable, dependable and secure, efficient and acceptable (slide 11). | Slide 11 says good software is maintainable and acceptable. This is why IT needs maintenance documents and users need short guides. | The AI used slide 11 only for security. Verification row 2 shows maintainability and acceptability (understandable, usable) fit the guides and documents better. |
