#  PassFort

### Intelligent Password Security & Attack Simulation Platform

PassFort is an advanced cybersecurity application that analyzes password strength from an **attacker’s perspective**, combining behavioral analysis, breach intelligence, and real-world attack simulation into a single interactive platform.

Unlike traditional password checkers that provide static strength labels, PassFort demonstrates **how and why passwords fail** under modern cyberattack strategies.

---

##  Overview

Modern password systems fail not because encryption is weak, but because **human behavior is predictable**.

PassFort bridges this gap by simulating real attacker workflows while educating users about secure authentication practices through visualization and interaction.

The system transforms password evaluation into a live security analysis experience.

---

##  Core Concept

PassFort introduces the **Human Pattern Index (HPI)**, a behavioral security metric that detects predictable password construction habits commonly exploited by attackers.

Examples include:

* Capitalized first letters
* Birth years and numeric suffixes
* Repeated characters
* Word + symbol patterns

Higher predictability directly reduces effective password security.

---

##  Key Features

###  Deep Strength & HPI Analyzer

* Multi-layer password evaluation
* Behavioral predictability detection
* Entropy-based strength estimation
* Human bias identification

---

###  Attack Path Simulator

Simulates realistic cyberattack progression:

1. Breach database exposure check
2. Dictionary attack analysis
3. Mutation prediction modeling
4. Automated brute-force estimation

Users observe how attackers systematically compromise weak credentials.

---

###  Secure Password Generator

* Cryptographically secure randomness (`secrets` module)
* Customizable character sets
* Adjustable password length (4–64)
* Automatic clipboard copying

---

###  True Ephemeral Mode

Designed for privacy-sensitive environments:

* RAM-only execution principles
* Clipboard self-destruction
* Reduced password persistence
* Temporary sensitive-data handling

---

###  Cybersecurity Learning Module

Integrated educational tools:

* Interactive security quiz
* Practical FAQ explanations
* Attack-awareness training

---

##  System Architecture

```
User Input
   │
   ▼
Human Pattern Index Analysis
   │
   ▼
Breach Intelligence Check (HIBP API)
   │
   ▼
Attack Path Simulation
   │
   ▼
Entropy & Crack-Time Estimation
   │
   ▼
Security Report Output
```

---

##  Privacy & Security

PassFort prioritizes user privacy.

Passwords are **never transmitted in full**.

Breach verification uses the privacy-preserving **k-Anonymity model** provided by the HaveIBeenPwned API:

* SHA-1 hash generated locally
* Only hash prefix transmitted
* Full password never exposed

---

##  Technologies Used

* Python
* CustomTkinter (Modern GUI Framework)
* Cryptographic Random Generation
* Regex-based Pattern Analysis
* SHA-1 Hashing
* HaveIBeenPwned API Integration
* Multithreading for Secure Clipboard Handling

---

##  Installation

```bash
git clone https://github.com/beginnercodervortex/PassFort-Secure-Password-Intelligence.git
cd PassFort-Secure-Password-Intelligence
pip install -r requirements.txt
python passfort.py
```


---

##  Project Objectives

* Demonstrate attacker-perspective password analysis
* Improve cybersecurity awareness through interaction
* Model human behavioral vulnerabilities
* Provide privacy-conscious password tooling

---

##  Real-World Relevance

PassFort reflects modern authentication threats including:

* Credential stuffing attacks
* Automated password mutation engines
* Database breach exploitation
* Human-pattern prediction attacks

The platform functions both as a **security education tool** and a **password intelligence demonstrator**.

---

##  Future Enhancements

* GPU-scale attack modeling
* Password reuse detection
* Local encrypted vault integration
* Machine-learning-based pattern prediction

---

##  Team Members

* **Akshita Singh**

* **Fuzailur Rahman**

* **Yashila Verma**

* **Archana**


---

## 📄 License

This project is licensed under the MIT License.

---

> *Security is rarely broken by mathematics.
> It is broken by predictability.*

