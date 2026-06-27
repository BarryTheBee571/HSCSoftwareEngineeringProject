# <ins> **SOFTWARE ENGINEERING PROJECT DOCUMENTATION** <ins>
---
## <ins> **1. Identifying and Defining** <ins>

### **1.1 Problem Statement**
Many primary school students struggle to memorise and recall basic mathematical facts quickly, especially multiplication tables. This slows down their progress in more advanced maths topics because they spend too long calculating simple facts instead of applying them. Teachers and parents often lack engaging tools that encourage repeated practice without feeling repetitive or boring. Children themselves may find traditional worksheets unmotivating, leading to reduced practice and weaker long-term recall.

This issue is significant because automatic recall of basic maths facts is a foundational skill. When students cannot answer simple multiplication questions quickly, it affects their confidence, slows their problem-solving, and can create long-term gaps in numeracy.

A software solution is appropriate because digital games can provide instant feedback, timed challenges, and adaptive difficulty features that are difficult to achieve with physical worksheet methods. A speed-based maths game can make practice more enjoyable, encourage repeated attempts, and track performance over time, helping students build fluency in a motivating way.

---
### **1.2 Project Purpose and Boundaries**
The purpose of this project will be to develop a Python based maths game that improves a student's speed and accuracy when answering basic maths questions. The program will present the user with simple questions within a certain period of time (eg. 30 seconds), and the aim will be answer as many questions correctly within this time period. This project will focus on basic mathematical skills suitable for young learners, such as basic addition, subtraction, multiplication, and division. The project has boundaries to my capabilities of coding and the resources/time available.

---
### **1.3 Stakeholder Requirements**
Stakeholders of this project would include teachers, parents and the primary users (Children).
- Teachers would want a tool that supports classroom learning, and be simple to use
- Parents would want a safe and reliable app to help their children improve maths skills at home
- Children need a fun and simple game to motivate them to learn maths

These factors could influence the project direction by identifying the basic needs that this app will need to achieve, such as a simple GUI and the core gameplay.

---
### **1.4 Functional Requirements**
- Generate random simple maths questions
- Have a time limit
- Accept user input for answers
- Check answers and update the score instantly
- Display the final score and accuracy at the end
- A simple menu to choose game mode or difficulty

---
### **1.5 Non-Functional Requirements**
- Performance: the game must load quickly, generate questions instantly, and process answers without lag
- Usability: The UI must be simple, child friendly and easy to navigate
- Security: A username and password will be stored with a random token allowing users to safely access their own account and view high scores and accuracy
- Reliability: The game should run consistently without crashes, and scoring must be accurate every time

---
### **1.6 Constraints**
- Time: The development of this project will be limited to the time period of this assignment
- Technical knowledge: The development will be restricted to my programming skills
- Hardware/software access: The game must run on weak school laptops

---
### **1.7 Requirements Analysis and Prioritisation**
Functional requirements (generating questions, timing, scoring and checking answers) will be prioritised as they relate to the core gameplay and without it, the game would not be able to fulfil its purpose. Non-functional requirements have also been prioritised but to a lesser degree. For example usability and reliability are also needed but not essential to the core functionality of the game, but are still important because the target audience is young children who need a simple, frustration free experience.

Some trade-offs made due to the constraints would be visual elements and potentially a visually appealing graphical user interface. But overall the requirements that are the main focus point align closely with the identified problem of children needing a fun, fast and effective way to practise basic maths, and the game focuses on delivering exactly that.

---
## <ins> **2. Research and Planning**<ins>
---
### **2.1 Development Methodology**
The development approach used for this project will be a waterfall, a linear and structure approach. This method was chosen because it aligns well with the project's clear requirements, simple development and the limited amount of time.

The core idea (a simple time based maths game for practising) has been well defined from the beginning. The essential features (question generation, timer, scoring, simple UI) are unlikely to suffer and significant changes. Waterfall works effectively when requirements are known early and remain stable.

The game is relatively simple compared to larger software systems. Because the project does not require complex systems, databases, or unpredictable user interactions, a linear approach was efficient and manageable

The project needs to be completed before the due date near the end of term 2. Waterfall's structured phases (planning - design - development - testing - evaluations) makes it easier to allocate time and ensure progress stayed on track. Each stage had clear deliverables, reducing the risk of significantly falling behind

Although feedback will still be valuable, the game does not need constant design or major feature changes. Most improvements should be minor such as difficulty or GUI layout. These changes could be handled during the testing phase rather than through ongoing iterative cycles.

---
### **2.2 Tools and Technologies**
**Programming language**\
Python was used to develop this program. Its simple and readable reducing the need for a complex understanding of the language, which is appropriate given the time constraints of this project. Python is also widely supported on low end hardware such as school laptops allowing for more access

**GUI Framework**\
CustomTkinter was used to create the graphical user interface. It is built on top of Tkinter and provides modern widgets such as frames, buttons, labels, entries, and scrollable frames. This suited the project because the game needed a clear login page, menu, timed gameplay screen, results screen, statistics page, and leaderboard without requiring complex graphics. CustomTkinter also supports styling and resizing, which helped make the interface child friendly and usable on different screen sizes.

**Development Environment**\
Visual Studio Code was used to write, test and debug code efficiently. Features such as syntax highlighting, error detection, and debugging tools improve code quality and reduce development time.

**Version Control**\
GitHub was used to track code changes through commits, allowing previous versions to be restored if errors occurred. It also provided access to the project from multiple devices improving organisation and documentation of the development process.

Overall, these tools and technologies supported efficient development by reducing complexity, improving, code reliability, and ensuring the final product meets both functional and non-functional requirements.

---
### **2.3 Gantt Chart / Timeline**
![Gantt Chart](<Theory/Gantt Chart.png>)

Time was allocated in a structured approach to match the waterfall development method. The initial weeks were dedicated to planning, including defining the problem, requirements and methodology. This sets a clear foundation and direction for the overall project before the actual development began. A short period was then used for research and selecting the appropriate tools and technologies that would be used. System design tasks such as diagrams and modelling were completed next to establish how the software would function before coding. Then the majority of the time would be allocated to the development of the project, including the core gameplay, GUI, and user account features, as this is the most complex and time intensive stage. Testing and evaluation would be in the last stages to identify and fix issues. The final weeks were reserved for evaluation, finishing documentation, and reflection to assess how well the project met its requirements and to complete all components.

---
### **2.4 Communication Plan**
Feedback will be obtained primarily from friends and the teacher at key stages of development, particularly after early prototypes and during testing. Demonstrations of the project in used will gather feedback on usability, difficulty, and overall engagement. This feedback was then incorporated by adjusting game features such as difficulty balancing, interface layout and clarity of instructions to better suit the target audience.

---
### **2.5 Resource Allocation Justification**
Time was allocated with the majority dedicated to development, as implementing the core functionality requires the most effort and work. Planning and design were given sufficient time early to plan and provide a foundation for the rest of the project. Testing and evaluation were allocated time towards the end to ensure the software met requirements, fix issues, and reflect on the overall project.

Software resources such as Python, CustomTkinter, and Visual Studio Code were chosen because they are lightweight, accessible, and suitable for the project's scope. Hardware requirements were minimal, ensuring compatibility with a larger range of devices.

Human input from friends and teacher will be used to identify usability issues and guide improvements, ensuring the final product aligns with stakeholder needs.

---
## <ins> **3. System Design** <ins>
---
### **3.1 Context Diagram/Data Flow Diagram Level 0**
![Context/Data Flow Level 0 Diagram](<Theory/Context and Data Flow Lv0.png>)

---
### **3.2 Data Flow Diagrams Level 1)**
![Data Flow Level 1 Diagram](<Theory/Data Flow Lv1.png>)

---
### **3.3 Structure Chart**
![Structure Chart](<Theory/Structure Chart.png>)

---
### **3.4 IPO Chart**
| Input | Process | Output |
| :---- | :------ | :----- |
| Username, password | Validate user details and check account information | Login confirmation or error message |
| New username, new password | Validate details and create a new user account | Account created message |
| Game mode selection | Record chosen mode for the session | Selected game mode |
| Difficulty selection | Record chosen difficulty for the session | Selected difficulty level |
| Start | Begin a timed game session | Active game round |
| Game mode, difficulty level | Generate a suitable maths question | Maths question displayed |
| User answer | Compare answer to correct result | Correct or incorrect feedback |
| Correct answer, current score | Update score | New score displayed |
| Number of correct answers, total questions answered | Calculate accuracy | Accuracy percentage |
| Timer data | Check remaining game time | Time left displayed or round ended |
| Final score, accuracy, round performance | Save results to user records | Updated progress and saved score |
| Saved user records | Retrieve high scores and previous performance | High scores and progress shown |
| End of round data | Prepare summary of performance | Final results screen |

---
### **3.5 Data Dictionary**
| Name | Type | Description |
| :---- | :---- | :---- |
| username | String | Stores the user’s account name for login and score records |
| password | String | Stores the password entered by the user during login or registration |
| sessionToken | String | Stores a random token linked to a user account for secure access |
| gameMode | String | Stores the selected game mode, such as addition, subtraction, multiplication, division, or mixed |
| difficultyLevel | String | Stores the selected difficulty level for the round |
| startCommand | Boolean | Indicates that the player has chosen to begin a game round |
| questionText | String | Stores the maths question shown to the player |
| correctAnswer | Integer | Stores the correct answer for the current question |
| userAnswer | Integer | Stores the answer entered by the player |
| answerStatus | Boolean | Indicates whether the player’s answer is correct or incorrect |
| score | Integer | Stores the player’s current score during a round |
| highScore | Integer | Stores the highest score achieved by a player |
| accuracy | Float | Stores the percentage of correct answers given by the player |
| timeLimit | Integer | Stores the total time allowed for a game round |
| timeRemaining | Integer | Stores the amount of time left in the current round |
| questionsAnswered | Integer | Stores the total number of questions attempted in a round |
| correctAnswers | Integer | Stores the total number of questions answered correctly |
| gamesPlayed | Integer | Stores the total number of rounds played by a user |
| roundResult | Record | Stores the summary data for one completed round, such as score and accuracy |
| performanceHistory | List | Stores previous results for a user across multiple rounds |
| leaderboardData | List | Stores score information used to display rankings or top scores |
| feedbackMessage | String | Stores messages shown to the player, such as correct, incorrect, login success, or error messages |
| accountRecord | Record | Stores the full set of account information for a user |
| scoreRecord | Record | Stores saved score and performance information for a user |

---
### **3.6 UML Class Diagram**
![UML Class Diagram](<Theory/UML Class Diagram.png>)

---
## <ins> **4. Producing and Implementing** <ins>
---
### **4.1 Development Process**
The solution was built as a modular Python desktop application using CustomTkinter. The main file, `main.py`, contains the `App` class, which opens the program window, stores shared state such as the current user, and controls navigation between screens. Each major screen was placed in its own module: `login.py`, `menu.py`, `game.py`, `results.py`, `stats.py`, and `leaderboard.py`. This structure means the login page, menu, gameplay screen, results page, statistics page, and leaderboard each have a clear purpose.

Modular design was appropriate because the project contains several separate responsibilities. For example, `questions.py` generates maths questions, `auth.py` handles login and saved user data, and `styles.py` stores shared colours and sizing constants. This is effective because a change to question generation does not require changes to the login system or user interface. It also makes the program easier to test, debug, and explain in the documentation.

Object-oriented programming was suitable because the application is screen based. `App` inherits from `ctk.CTk`, while each screen inherits from `ctk.CTkFrame`. Classes such as `LoginFrame`, `MenuFrame`, `GameFrame`, `ResultsFrame`, `StatsFrame`, and `LeaderboardFrame` store their own widgets, screen data, and behaviours. This improves organisation because each screen can manage its own layout and actions while still being controlled by the main app.

Code reuse was used through helper methods such as `make_label`, `make_button`, `scale_value`, and `refresh_scaling`. These methods keep the interface consistent and reduce repeated code. Shared functions such as `auth.load_users()`, `auth.save_game_stats()`, and `questions.make_question()` are reused across multiple screens. This was a strong engineering choice because repeated code would make the project harder to maintain and more likely to contain inconsistent behaviour.

Validation and error handling were included to improve reliability and user experience. Registration checks that usernames are at least 4 characters, passwords are at least 6 characters and include a number, duplicate usernames are blocked, and usernames cannot contain spaces. Login checks account details. The game only accepts whole-number answers. Accuracy calculations avoid division by zero, and `auth.load_users()` handles missing or corrupted JSON data by returning an empty dictionary instead of crashing. These techniques are justified because the target users are children, so the program must recover from mistakes clearly rather than fail unexpectedly.

---
### **4.2 Key Features Developed**
| Feature | Description | Justification |
| :---- | :---- | :---- |
| Login, registration, and guest mode | Users can create an account, log in, or continue as a guest. | This was included because registered users need saved progress, while guest mode keeps the app quick and accessible for casual use. |
| Main menu selections | The player selects game mode, difficulty, and time limit before starting. | This is justified because students have different ability levels and may need targeted practice in addition, subtraction, multiplication, division, or mixed mode. |
| Timed gameplay | The game generates random questions, accepts typed answers, checks correctness, updates score, and displays feedback. | This is the most important feature because it directly addresses the problem statement: improving speed and accuracy through repeated maths practice. |
| Results screen | The program displays score, questions answered, correct answers, and accuracy after a round. | This gives immediate feedback, allowing the user to judge their performance and try to improve in the next round. |
| Statistics screen | Logged-in users can view high score, games played, total correct answers, total answered questions, accuracy, time spent, and grouped performance data. | This was included because long-term data helps students, parents, and teachers identify progress and weaknesses. |
| Leaderboard | Users are ranked by high score. | This adds motivation and replay value because students can aim to improve their personal best and compare scores. |

---
### **4.3 Back-End Engineering Contribution**
Back-end engineering contributed to the success of the project by separating data processing, validation, storage, and authentication from the visual interface. This made the software easier to use because the interface could stay simple while the logic was handled by separate modules.

The `questions.py` module explains how data processing supports gameplay. It uses the selected game mode and difficulty to generate appropriate number ranges. For division, the program creates numbers that divide evenly, so the user receives whole-number questions rather than confusing decimal answers. This improves usability because the generated questions match the target audience's skill level.

The `auth.py` module explains how validation and logic support reliability. It checks registration rules, verifies login details, hashes passwords, creates session tokens, records started tests, and saves completed game results. Because this logic is placed in one module, the interface screens can call clear functions such as `auth.login()`, `auth.register()`, and `auth.save_game_stats()` without duplicating account logic.

Storage and retrieval are handled through `users.json`. This file stores password hashes, tokens, high scores, games played, total correct answers, total answered questions, total time spent, mode counts, difficulty statistics, time mode statistics, and game mode statistics. JSON was an appropriate storage method because it is lightweight, readable, and does not require a separate database server.

Overall, the back-end engineering was effective because it allowed the program to save progress, calculate statistics, authenticate users, and generate suitable questions while keeping the user interface clear and child friendly.

---
### **4.4 Screenshots of Interface**
**Login Page**
![Login Page](<Theory/Login Page.png>)

**Sign Up Page**
![Sign Up Page](<Theory/Sign Up Page.png>)

**Main Menu**
![Main Menu](<Theory/Main Menu.png>)

**Account Stats Page**
![Stats Page](<Theory/Stats Page.png>)

**Leaderboard Page**
![Leaderboard Page](<Theory/Leaderboard Page.png>)

**Game Page**
![Game Page](<Theory/Game Page.png>)

---
## **4.5 Version Control Summary**
GitHub was used to track the development of the project through commits. In summary, version control helped organise the project because each major stage could be saved, reviewed, and restored if needed.

The commit history shows a structured development process. Early commits created the project documentation and completed the planning sections. Later commits added system design diagrams, base gameplay, the graphical interface, time selection, improved question generation, saved data, statistics screens, leaderboard features, and final refinements.

---
## <ins> **5. Testing and Evaluation** <ins>
---
### **5.1 Testing Methods Used**
| Testing method | Description | How results were used |
| :---- | :---- | :---- |
| Functional testing | Individual features such as login, registration, menu selection, question generation, answer checking, scoring, results, statistics, and leaderboard display were tested. | This identified whether each feature met its expected output before being tested as part of the full system. |
| Integration testing | Connected modules were tested together. For example, `MenuFrame` passes selected settings to `GameFrame`, `GameFrame` uses `questions.make_question()`, and `ResultsFrame` uses `auth.save_game_stats()` to update saved user data. | This improved reliability because it confirmed that data moved correctly between screens and modules. |
| User testing | Testers used the program like real players by logging in, selecting a game mode, playing a round, viewing results, and checking statistics. | This improved usability because feedback was used to refine navigation, error messages, and the usefulness of game options. |

Testing improved the final solution by revealing practical issues such as invalid inputs, missing selections, non-numeric answers, timer ending behaviour, and safe accuracy calculation when no questions were answered. Fixing these issues made the program more reliable and easier for the target audience to use.

---
### **5.2 Test Cases and Results**

| Test ID | Feature tested | Test steps | Expected result | Actual result | Status |
| :---- | :---- | :---- | :---- | :---- | :---- |
| TC01 | Register new user (valid data) | Open Sign Up, enter username with at least 3 chars and password with at least 4 chars, submit. | Account is created, session token is generated, user is redirected to menu. | Account created successfully and user entered menu. | Pass |
| TC02 | Register with duplicate username | Try to register with an existing username. | Registration is blocked with "Username already taken" message. | Duplicate account was rejected with correct message. | Pass |
| TC03 | Register with invalid username/password | Try username shorter than 3 chars, username containing spaces, or password shorter than 4 chars. | Registration is blocked with validation message for each invalid input. | Invalid inputs were rejected with correct messages. | Pass |
| TC04 | Login with valid credentials | Open Login, enter existing username and correct password, submit. | Login succeeds, token refreshes, user is redirected to menu. | Login succeeded and menu opened. | Pass |
| TC05 | Login with invalid credentials | Try unknown username and wrong password cases. | Login is blocked with "Username not found" or "Incorrect password" message. | Both invalid login cases showed correct error feedback. | Pass |
| TC06 | Guest mode flow | On login screen, click Continue as Guest and start a game. | Guest can play game but no account statistics are saved. | Gameplay worked as guest and no user stats were written. | Pass |
| TC07 | Menu selection validation | Attempt Start Game without selecting mode, difficulty, or time. | Start is blocked and clear error message is shown for missing selection. | Validation prevented start and showed correct message. | Pass |
| TC08 | Question generation by mode/difficulty | Start games across addition, subtraction, multiplication, division, and mixed with easy/medium/hard. | Questions match selected mode and difficulty ranges; division answers are whole numbers. | Generated questions matched mode settings and valid ranges. Division remained whole-number. | Pass |
| TC09 | Answer input validation | Enter letters/symbols in answer field and submit. | Input is rejected with "Enter a whole number!" and score does not update. | Non-numeric entries were rejected and score unchanged. | Pass |
| TC10 | Score and streak logic | Submit several correct answers, then one incorrect answer. | Score increases by 10 per correct answer; streak increases on correct and resets on incorrect. | Score and streak behavior matched expected logic. | Pass |
| TC11 | Timer and end-of-round behavior | Run timed mode until timer expires, then run unlimited mode and press End Game. | Timed game auto-ends at 0 seconds; unlimited mode counts up and ends only when user chooses End Game. | Both timed and unlimited behaviors worked as expected. | Pass |
| TC12 | Result saving, stats, and leaderboard integration | Complete a logged-in game, then open stats and leaderboard pages. | Game results are saved to users.json, high score updates if beaten, stats totals update, leaderboard sorts by high score. | Data saved correctly, high score updated, and leaderboard ranking reflected saved values. | Pass |

---
### **5.3 Evaluation Against Requirements**
| Requirement | Evaluation and evidence |
| :---- | :---- |
| Generate random maths questions | Achieved. The `questions.py` module generates addition, subtraction, multiplication, division, and mixed questions based on the selected difficulty. This meets the core gameplay requirement. |
| Time limit | Achieved. The game supports 30, 60, 90, 120 second modes and unlimited mode. This gives users both timed practice and flexible practice. |
| Accept and check answers | Achieved. The game accepts typed answers, validates whole-number input, checks correctness, and gives immediate feedback. This is effective because it directly supports fast recall practice. |
| Score and accuracy | Achieved. Correct answers increase the score, and the results screen calculates accuracy using correct answers and total answered questions. |
| Menu and difficulty selection | Achieved. The menu allows the user to select game mode, difficulty, and time limit before starting a round. |
| Saved progress | Achieved for logged-in users. Scores, accuracy, high scores, games played, and grouped statistics are saved to `users.json`. This extends the original requirements and supports long-term progress tracking. |
| Usability | Mostly achieved. The interface uses clear screens, large text, simple buttons, and immediate feedback. This is suitable for younger users, although future screenshots and user feedback could further support this judgement. |
| Performance | Achieved. The program runs locally and uses lightweight Python logic and JSON storage, so question generation and scoring occur quickly. |
| Reliability | Mostly achieved. Input validation, safe accuracy calculations, and JSON error handling reduce crashes. |
| Security | Partly achieved. Passwords are hashed and session tokens are generated, but the system does not use salted hashing, encryption, or a secure database. This is acceptable for the project scope but limited for real-world use. |

---
### **5.4 Improvements and Future Development**

| Limitation | Future enhancement | Explanation |
| :---- | :---- | :---- |
| User data is stored in a local JSON file. | Use SQLite or another database. | This would make data storage more structured and reliable, especially if the project grew to support more users. |
| Security is basic. | Add salted password hashing, stronger session management, and protected storage. | This would better protect user data and make the system more suitable for real-world use. |
| Difficulty is selected manually. | Add adaptive difficulty. | The program could automatically adjust question difficulty based on the user's speed and accuracy, making practice more personalised. |
| Progress feedback is useful but limited. | Add weakness reports and practice recommendations. | This would help students, parents, and teachers identify which maths areas need more practice. |
| The interface is functional but could be more engaging. | Add sound effects, achievements, animations, or reward badges. | This could improve motivation for younger users while keeping the core gameplay simple. |
| Testing is mainly manual. | Add automated unit tests. | Automated tests for authentication, question generation, scoring, and statistics would make future changes safer and the whole testing process more efficient. |

---

### **5.5 Evaluation of Social, Ethical, and Communication Issues**

| Area | Evaluation |
| :---- | :---- |
| Social impact | The project has a positive social impact because it supports numeracy practice for younger students in a format that is more engaging than worksheets. Features such as selectable game mode, difficulty, and time settings allow learners with different confidence levels to participate. A limitation is that the current design is mainly practice-based and does not explicitly teach problem-solving strategies, so weaker learners may still need teacher or parent guidance. |
| Accessibility and inclusion | The interface uses large text, simple buttons, and clear screens, which improves accessibility for the target age group. However, accessibility is not fully addressed because there are no audio cues, no dyslexia-focused font option, and no dedicated colour-blind accessibility checks. Future development should include accessibility settings to improve inclusion. |
| Ethical use of data | User accounts store only basic credentials and game performance data needed for functionality. Passwords are hashed rather than stored as plain text, which is an ethical and safer approach to handling user information. A remaining ethical risk is that data is saved locally in a JSON file without advanced protection, so the system should be used with awareness that it is a school-level prototype, not a production security platform. |
| Fairness and wellbeing | Scoring and answer checking are rules-based and consistent for all users, which supports fairness. The leaderboard can increase motivation, but it may also create pressure for some students. To manage wellbeing, future versions could include personal progress goals and optional hiding of comparative rankings. |
| Legal and policy considerations | The project currently operates as an offline educational tool with no online sharing, which reduces privacy and compliance risk. For a wider deployment, legal responsibilities would increase, including parental consent requirements for children, clearer data retention policies, and compliance with school and privacy regulations. |
| Communication with stakeholders | Peer feedback was collected and used to identify practical improvements, including requests for better engagement, more teaching support, and improved progression. This shows effective communication during development and supports iterative refinement. The communication process could be strengthened further by using a structured feedback form with consistent questions for all testers. |

---

## <ins> **6. Feedback, Security and Reflection** <ins>
---
### **6.1 Summary of Client or Peer Feedback**
| Name | Plus | Minus | Implication |
| :---- | :---- | :---- | :---- |
| Chris | The maths is a good idea to help you practice skills that you don't use often. Lets you choose how hard the modes are | Not multiplayer | Add easter eggs in the game |
| Stephen | Barry’s maths application presents different maths types to develop skills, it allows selection of many options | Basic maths for smaller children | Auto select level when login |
| Shawn | Many options to select from, provides answers if you get it wrong, and is easy to use | Too plain and boring | Add more complex topics but with easy questions (factorisation, etc) |
| Miles | Where 2 Numbers are added together, as demonstrated by the game. | Where 2 Numbers are taken away from one another, as demonstrated by the game. | I didn’t reach this level |
| Miles, For Real this time. | The game's UI was really focused, which was a big benefit for this type of educational game, where I am only trying to focus on one task at a time, and reduce the distractions. | I wasn't a fan of the font. And the game sort of fails to ‘teach’ in that sense. It is a practice tool. A way to improve it might be to have lessons or tips for some of the more difficult problems. For example*, notes for “Multiplying by 99, you can multiply by 100 and then take away one of the multiplied values”.* | If I was younger, I would use a tool like this, and I do think it would benefit me in laying a stronger foundation level of Math skills going into high school or even up through parts of high school. But this type of practice does begin to fall short at the much higher level, which is more focused on the process and adjacent thinking of a solution, rather than one calculation. |

---
### **6.2 Secure Software Design and Data Handling**
The secure software design is appropriate for the scope of this project because the application is a small offline maths game, not a large online system. The main user data stored by the program is account login details and performance statistics, such as high score, accuracy, games played, and total time spent.

A key security feature is that passwords are not stored as plain text. Instead, the program converts the password into a SHA-256 hash before saving it in `users.json`. This means that if someone opened the user data file, they would not immediately see the user’s actual password. This improves user trust and shows safer handling of login data.

The program also uses input validation to protect the reliability and integrity of the system. Registration checks for usernames that are too short, passwords that are too short, usernames with spaces, and duplicate usernames. Login checks whether the account exists and whether the entered password matches the saved hash. The game also validates answer input so only whole-number answers are accepted.

User data is stored locally in a JSON file. This is suitable for the size and purpose of the project because the game is designed to run offline on a local computer. A more advanced real-world version could use salted password hashing, encryption, or a database, but for this school project the current security measures are suitable because they protect passwords better than plain-text storage and prevent common invalid inputs.

Overall, the security approach meets the needs of the project by safely handling basic login data, protecting stored passwords, validating user input, and keeping the application reliable for its intended users.

---
### **6.3 Personal Reflection**

**Reflect** on what you learned during the project, including

* Software engineering skills developed

* Challenges encountered and how they were overcome


---
## <ins> **7. Appendices** <ins>

### **7.1 Full Gantt Chart**

### **7.2 Complete Data Dictionary**

### **7.3 Full Test Logs**

### **7.4 Raw Feedback Notes**

### **7.5 Exemplar Code Snippets**