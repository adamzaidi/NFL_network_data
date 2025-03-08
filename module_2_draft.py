import requests
from bs4 import BeautifulSoup
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Function to scrape hyperlinks from a given website
def scrape_links(url):
    links = set()
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('http'):
                    links.add(href)
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
    return links

# Define key NFL-related websites to scrape
nfl_sites = [
    'https://www.nfl.com',
    'https://www.espn.com/nfl/',
    'https://www.bleacherreport.com/nfl'
]
network_data = []

# Scraping links from NFL-related websites
for site in nfl_sites:
    linked_sites = scrape_links(site)
    for linked_site in linked_sites:
        network_data.append((site, linked_site))

# Create a directed graph
G = nx.DiGraph()
G.add_edges_from(network_data)

# Calculate importance metrics
pagerank = nx.pagerank(G)
betweenness = nx.betweenness_centrality(G)
degree_centrality = nx.degree_centrality(G)

# Convert metrics to DataFrame
df = pd.DataFrame({
    'Node': list(pagerank.keys()),
    'PageRank': list(pagerank.values()),
    'Betweenness': list(betweenness.values()),
    'Degree Centrality': list(degree_centrality.values())
})

# Sort by PageRank
df_sorted = df.sort_values(by='PageRank', ascending=False).head(5)
print(df_sorted)

# Save results to CSV
df_sorted.to_csv("nfl_network_analysis.csv", index=False)

# Plot the network
plt.figure(figsize=(12, 8))
nx.draw(G, with_labels=True, node_size=50, font_size=8)
plt.title("NFL Web-Based Network")
plt.show()