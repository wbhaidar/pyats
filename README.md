# pyATS AeTest Framework Demo

This repository demonstrates how to utilize Cisco's [pyATS AeTest](https://developer.cisco.com/pyats/) testing framework to automate network device validation.

The goal is to provide a simple, clear example of using AeTest for:

- Establishing device connections from a YAML testbed
- Writing structured test cases with setup, test, and cleanup phases
- Validating device connectivity and software versions
- Organizing test scripts and jobs for scalable automation

---

## 📦 Features

- Connects to devices defined in a testbed YAML file
- Verifies each device is reachable and connected
- Parses `show version` output to check software version correctness
- Demonstrates best practices for AeTest testcases and job files

---

## ⚙️ Requirements

- Python 3.8+
- Cisco devices or simulators (e.g. VIRL, GNS3)
- Installed Python dependencies (see below)

---

## 🧪 Installation

```bash
git clone https://github.com/your-username/pyats.git
cd pyats

python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

pip install -r requirements.txt

