# rag-foundation-exercise

## Installation

**Note:** Prefer `python=3.10.*`

### 1. Clone repo (If you've already done this, jump to step 2)
```sh
git clone https://github.com/Cinnamon/ai-bootcamp-2024
cd ai-bootcamp-2024
```
### 2. Update changes from remote repo
Make sure you have folder `rag-foudation` in `ai-bootcamp-2024`

```sh
git checkout main
git fetch origin
```
### 3. Create a new environment for this week homework
#### Windows
   - **Open Command Prompt.**
   - **Navigate to your project directory:**
```sh
cd C:\Path\To\ai-bootcamp-2024
```
   - **Create a virtual environment using Python 3.10:**

Check your python version first using `py -0` or `where python`

```
python -m venv rag-foundation
or
path/to/python3.10 -m venv rag-foundation
```

   - **Activate the Virtual Environment:**
```sh
rag-foundation\Scripts\activate
```

#### Ubuntu/MacOS

- **Open a terminal.**
- **Create a new Conda environment with Python 3.10:**
```sh
conda create --name rag-foundation python=3.10
```

- **Activate the Conda Environment:**
```sh
conda activate rag-foundation
```

### 4. **Install Required Packages:**
   - Install the required packages from `requirements.txt`:
```sh
pip install -r requirements.txt
```
