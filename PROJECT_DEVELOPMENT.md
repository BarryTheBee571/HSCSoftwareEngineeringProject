# <ins> **SOFTWARE ENGINEERING PROJECT DOCUMENTATION** <ins>
---
## <ins> **1. Identifying and Defining** <ins>

### **1.1 Problem Statement**
Many primary school students struggle to memorise basic mathematical facts, especially multiplication tables. This slows down their progress in more advanced maths topics because they spend too long calculating simple facts instead of applying them. Teachers and parents often lack engaging tools that encourage repeated practice without feeling repetitive or boring. Children themselves may find traditional worksheets unmotivating, leading to reduced practice and weaker long‑term recall.

This issue is significant because automatic recall of basic maths facts is a foundational skill. When students cannot answer simple multiplication questions quickly, it affects their confidence, slows their problem‑solving, and can create long‑term gaps in numeracy.

A software solution is appropriate because digital games can provide instant feedback, timed challenges, and adaptive difficulty features that are difficult to achieve with physical worksheet methods. A speed‑based maths game can make practice more enjoyable, encourage repeated attempts, and track performance over time, helping students build fluency in a motivating way.

---
### **1.2 Project Purpose and Boundaries**
The purpose of this project will be to develop a Python based maths game that improves a student's speed and accuracy when answering basic maths questions. The program will present the user with simple questions within a certain period of time (eg. 30 seconds), and the aim will be answer as many questions correctly within this time period. This project will focus on basic mathematical skills suitable for young learners, such as basic addition, subtraction, multiplication, and division. The project has boundaries to my capabilities of coding and the resources available.

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
Pygame was used to develop the graphical user interface and handle game logic. It provides built in functionality for rendering graphics, handling user input, and managing timing, which are essential for this project. This reduced the need to build a system from scratch and increasing development efficiency and reliability. Pygame also allows the creation of a simple and interactive interface suitable for young users.

**Development Environment**\
Visual Studio Code was used to write, test and debug code efficiently. Features such as syntax highlighting, error detection, and debugging tools improve code quality and reduce development time.

**Version Control**\
GitHub was used to track code changes through commits, allowing previous versions to be restored if errors occurred. It also provided access to the project from multiple devices improving organisation and documentation of the development process.

Overall, these tools and technologies supported efficient development by reducing complexity, improving, code reliability, and ensuring the final product meets both functional and non-functional requirements.

---
### **2.3 Gantt Chart / Timeline**
![Gantt Chart](<Theory/Gantt Chart.png>)
SUBJECT TO CHANGE ACCORDING TO DUE DATE

Time was allocated in a structured approach to match the waterfall development method. The initial weeks were dedicated to planning, including defining the problem, requirements and methodology. This sets a clear foundation and direction for the overall project before the actual development began. A short period was then used for research and selecting the appropriate tools and technologies that would be used. System design tasks such as diagrams and modelling were completed next to establish how the software would function before coding. Then the majority of the time would be allocated to the development of the project, including the core gameplay, GUI, and user account features, as this is the most complex and time intensive stage. Testing and evaluation would be in the last stages to identify and fix issues. The final weeks were reserved for evaluation, finishing documentation, and reflection to assess how well the project met its requirements and to complete all components.

---
### **2.4 Communication Plan**
Feedback will be obtained primarily from friends and the teacher at key stages of development, particularly after early prototypes and during testing. Demonstrations of the project in used will gather feedback on usability, difficulty, and overall engagement. This feedback was then incorporated by adjusting game features such as difficulty balancing, interface layout and clarity of instructions to better suit the target audience.

---
### **2.5 Resource Allocation Justification**
Time was allocated with the majority dedicated to development, as implementing the core functionality requires the most effort and work. Planning and design were given sufficient time early to plan and provide a foundation for the rest of the project. Testing and evaluation were allocated time towards the end to ensure the software met requirements, fix issues, and reflect on the overall project.

Software resources such as Python, Pygame, and Visual Studio Code were chosen because they are lightweight, accessible, and suitable for the project's scope. Hardware requirements were minimal, ensuring compatibility with a larger range of devices.

Human input from friends and the teacher will be used to identify usability issues and guide improvements, ensuring the final product aligns with stakeholder needs.
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
Not sure if I will incorporate classes into this project yet unless all the data get's too messy and I want a cleaner way to manage things like user account details or game session data.

---
## <ins> **4. Producing and Implementing** <ins>
---
### **4.1 Development Process**

**Describe** how the solution was built and implemented.

**Justify** the engineering techniques used, such as:

* Modular design

* Object-oriented principles

* Reuse of code

* Validation and error handling

---
### **4.2 Key Features Developed**

**Describe** the core features of the system.

**Justify** their inclusion.

---
### **4.3 Back-End Engineering Contribution**

**Explain** how back-end engineering contributed to the success and ease of use of the software, including

* Data processing

* Validation and logic

* Storage and retrieval

* Authentication (if applicable)

---
### **4.4 Screenshots of Interface**

Include annotated screenshots explaining how the user interacts with the system.

---
## **4.5 Version Control Summary (Optional)**

**Summarise** commits, iterations, or sprints if version control was used.

---
## <ins> **5. Testing and Evaluation** <ins>
---
### **5.1 Testing Methods Used**

Describe testing approaches, such as:

* Unit testing

* Integration testing

* User testing

**Explain** how testing results were used to improve performance, efficiency, or reliability.

---
### **5.2 Test Cases and Results**

| Test ID | Description | Expected Result | Actual Result | Pass/Fail |
| :---- | :---- | :---- | :---- | :---- |
| TC01 | Valid login | Success message | Success message | Pass |
| TC02 | Invalid login | Error message | Error message | Pass |

---
### **5.3 Evaluation Against Requirements**

**Evaluate** how effectively the solution meets the identified functional and non-functional requirements.

---
### **5.4 Improvements and Future Development**

**Outline** your project’s limitations.

**Explain** realistic future enhancements.

---

## <ins> **6. Feedback, Security and Reflection** <ins>
---
### **6.1 Summary of Client or Peer Feedback**

**Summarise** feedback received and explain how it influenced development.


You could collect a **‘PMI’ (Plus, Minus, Implication)** table from **at least three** different people after testing, or **record and summarise an interview** with **at least three** three people who test the software.

---
### **6.2 Secure Software Design and Data Handling**

**Evaluate** the approach undertaken to safely and securely collect, use, and store data.

Your evaluation should address:


* Secure coding practices applied during development

* Input validation and error handling


* Data storage and protection methods


* The impact of secure software design on user trust, data integrity, and system reliability

---
### **6.3 Personal Reflection**

**Reflect** on what you learned during the project, including

* Software engineering skills developed

* Challenges encountered and how they were overcome

---
## <ins> **7. Appendices** <ins>

* Full Gantt Chart

* Complete Data Dictionary


* Full Test Logs

* Raw Feedback Notes

* Exemplar Code Snippets