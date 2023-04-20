# Create a Quine Icon Library with Python

The code in this repo accompanies the blog post [Create a Quine Icon Library with Python](#)

Have you ever wanted to add flair to a graph visualization but are unsure which icons Quine supports? In this blog, we explore a Python script that fetches valid icon names from the web, configures the Exploration UI, then creates a graph of icon nodes for reference. The script uses several popular Python libraries, including Requests, BeautifulSoup, and Halo, along with the `/query-ui` and `/query/cypher` API endpoints.

We will be using the following tools and technologies:

* Quine streaming graph 1.5.0 or later
* Python 3.6 or later
* Requests library to make HTTP requests to the Neo4j server
* BeautifulSoup library to extract data from the webpage
* Halo library to add a spinner animation and updates to the terminal output
* Log-Symbols library to add emojis to the terminal output

First, we need to install the required libraries. We can do this using `pip`. Open a terminal and type the following command:

```
pip install -r requirements.txt
```

Now run the `iconLibray.py` script or optionally, load the included notebook using a Jupyter Lab or Notebook environment.
