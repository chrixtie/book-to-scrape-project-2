# book-to-scrape-project-2
# How to Run This Project:

Clone the repository
First, copy the project to your local computer using Git.

git https://github.com/chrixtie/book-to-scrape-project-2


Create a Python environment
It’s best to run this project inside a virtual environment so the required libraries don’t conflict with other Python projects on your machine.

Create the environment:

python3 -m venv env

Activate it:
On macOS/Linux: source env/bin/activate

On Windows: .\env\Scripts\activate

Install dependencies
This project lists all the required Python packages in the requirements.txt file. To install them, run:

pip install -r requirements.txt

This will make sure your environment has everything the code needs. 

Run the scraper script:
Decide which script you want to run (for one book, one category, or the full site). From the project folder, type:

python main.py

Check your outputs:
After running the script, you should see CSV files appear in the project directory with the scraped data. If you enabled image downloading, you’ll also see an images/ folder with downloaded images.

Deactivate when finished
Once you’re done, you can deactivate the environment:

deactivate
