"""
🎬 MovieLens AI - Smart Movie Analytics Pipeline
Author: Gunavant Rumne
"""

import pandas as pd
import matplotlib.pyplot as plt
import random

# ==========================================================
# STEP 1: GENERATE MOVIE DATA
# ==========================================================
print("=" * 50)
print("🚀 STEP 1: Generating Movie Data...")
print("=" * 50)

random.seed(42)

titles = [
    "The Last Storm", "Dark Horizon", "City of Dreams", "Broken Wings",
    "Silent Warrior", "Fire & Ice", "Lost in Time", "Shadow King",
    "Golden Days", "Night Riders", "The Chase", "Blood Moon",
    "Ocean Heart", "Street Fighter", "Dream Catcher", "Iron Will",
    "Love Actually", "Cold Mountain", "Fast Lane", "Deep Blue",
    "Planet X", "Wild Hunt", "Star Child", "River Song",
    "Ghost Ship", "Thunder Road", "Neon Lights", "Red Alert",
    "Sky Fall", "Zero Hour",
]

genres = ["Action", "Comedy", "Drama", "Thriller", "Romance"]
platforms = ["Netflix", "Prime Video", "Hotstar", "Zee5"]
languages = ["Hindi", "English", "Tamil", "Telugu"]

data = []
for i in range(1000):
    cat = random.choice(genres)
    budget = round(random.uniform(1, 100), 1)
    revenue = round(random.uniform(0.5, 200), 1)
        data.append({
        "movie_id": i + 1,
        "title": random.choice(titles),
        "genre": cat,
        "release_year": random.choice(range(2018, 2026)),
        "platform": random.choice(platforms),
        "language": random.choice(languages),
        "rating": round(random.uniform(1.0, 5.0), 1),
        "budget_crore": budget,
        "revenue_crore": revenue,
    })

df = pd.DataFrame(data)
print(f"📊 Generated {len(df)} movie records!\n")
print(df.head())

# ==========================================================
# STEP 2: ETL (Clean & Transform)
# ==========================================================
print("\n" + "=" * 50)
print("🧼 STEP 2: Cleaning Data (ETL)...")
print("=" * 50)

df = df.drop_duplicates(subset=["movie_id"])

df["hit_or_flop"] = df.apply(
    lambda row: "Hit" if row["revenue_crore"] > row["budget_crore"] else "Flop",
    axis=1,
)

def get_rating_cat(r):
    if r >= 4: return "Excellent"
    elif r >= 3: return "Good"
    elif r >= 2: return "Average"
    else: return "Poor"

df["rating_category"] = df["rating"].apply(get_rating_cat)
df["profit_crore"] = round(df["revenue_crore"] - df["budget_crore"], 1)
df.to_csv("movies_data.csv", index=False)

print(f"✅ Cleaned! {len(df)} records")
print(f"✅ Added columns: hit_or_flop, rating_category, profit_crore")
print(f"✅ Saved -> movies_data.csv")

# ==========================================================
# STEP 3: SMART MOVIE AGENT
# ==========================================================
print("\n" + "=" * 50)
print("🤖 STEP 3: AI Agent Answering Questions...")
print("=" * 50)

class SmartMovieAgent:
    """AI Agent that answers movie questions!"""

    def __init__(self, df):
        self.df = df

    def ask(self, question):
        q = question.lower()

        if "top genre" in q or "best genre" in q:
            top = self.df.groupby("genre")["rating"].mean().idxmax()
            val = self.df.groupby("genre")["rating"].mean().max()
            return f"Best Genre: {top} (Avg Rating: {val:.1f})"

        elif "best movie" in q or "top movie" in q:
            idx = self.df["revenue_crore"].idxmax()
            row = self.df.loc[idx]
            return f"Top Movie: {row['title']} (Revenue: Rs.{row['revenue_crore']}Cr)"

        elif "total movies" in q or "how many" in q:
            return f"Total Movies: {len(self.df)}"

        elif "average rating" in q or "avg rating" in q:
            return f"Average Rating: {self.df['rating'].mean():.1f} / 5.0"
                elif "best platform" in q or "top platform" in q:
            top = self.df.groupby("platform")["rating"].mean().idxmax()
            val = self.df.groupby("platform")["rating"].mean().max()
            return f"Best Platform: {top} (Avg Rating: {val:.1f})"

        elif "hit rate" in q or "hit percentage" in q:
            hits = (self.df["hit_or_flop"] == "Hit").sum()
            rate = hits / len(self.df) * 100
            return f"Hit Rate: {rate:.1f}% ({hits} out of {len(self.df)})"

        elif "best language" in q or "top language" in q:
            top = self.df.groupby("language")["revenue_crore"].sum().idxmax()
            return f"Top Language: {top}"

        elif "best year" in q or "top year" in q:
            top = self.df.groupby("release_year")["revenue_crore"].sum().idxmax()
            return f"Best Year: {top}"

        else:
            return "Try: 'top genre', 'best movie', 'hit rate', 'best platform'"

agent = SmartMovieAgent(df)
questions = [
    "What is the top genre by rating?",
    "Which is the best movie by revenue?",
    "How many total movies?",
    "What is the average rating?",
    "What is the hit rate?",
    "Which is the best platform?",
]

for q in questions:
    print(f"\n Q: {q}")
    print(f" A: {agent.ask(q)}")

# ==========================================================
# STEP 4: CREATE 4 CHARTS
# ==========================================================
print("\n\n" + "=" * 50)
print("📊 STEP 4: Creating Charts...")
print("=" * 50)

colors = ["#E74C3C", "#3498DB", "#2ECC71", "#F39C12", "#9B59B6"]

# Chart 1: Average Rating by Genre
fig1, ax1 = plt.subplots(figsize=(8, 5))
genre_data = df.groupby("genre")["rating"].mean().sort_values()
ax1.barh(list(genre_data.index), list(genre_data.values), color=colors)
ax1.set_title("Average Rating by Genre", fontsize=16, fontweight="bold")
ax1.set_xlabel("Average Rating")
plt.tight_layout()
plt.savefig("chart_genre_rating.png", dpi=150)
plt.show()

# Chart 2: Movies per Platform
fig2, ax2 = plt.subplots(figsize=(8, 5))
plat_data = df["platform"].value_counts()
ax2.bar(list(plat_data.index), list(plat_data.values), color=colors[:4])
ax2.set_title("Movies per Platform", fontsize=16, fontweight="bold")
ax2.set_ylabel("Number of Movies")
for i, v in enumerate(plat_data.values):
    ax2.text(i, v + 5, str(v), ha='center', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig("chart_platform.png", dpi=150)
plt.show()

# Chart 3: Hit vs Flop
fig3, ax3 = plt.subplots(figsize=(7, 7))
hf = df["hit_or_flop"].value_counts()
ax3.pie(list(hf.values), labels=list(hf.index), autopct="%1.1f%%",
        colors=["#2ECC71", "#E74C3C"], startangle=90,
        textprops={"fontsize": 14}, explode=(0.05, 0.05))
ax3.set_title("Hit vs Flop Movies", fontsize=16, fontweight="bold")
plt.tight_layout()
plt.savefig("chart_hit_flop.png", dpi=150)
plt.show()
# Chart 4: Yearly Trend
fig4, ax4 = plt.subplots(figsize=(10, 5))
yearly = df.groupby("release_year").size()
ax4.plot(list(yearly.index), list(yearly.values), marker="o",
         color="#3498DB", linewidth=2.5, markersize=9)
ax4.fill_between(list(yearly.index), list(yearly.values), alpha=0.15, color="#3498DB")
ax4.set_title("Movies Released Per Year", fontsize=16, fontweight="bold")
ax4.set_xlabel("Year")
ax4.set_ylabel("Number of Movies")
plt.tight_layout()
plt.savefig("chart_yearly.png", dpi=150)
plt.show()

print("\n🥳 ALL DONE! Download files from 📁 icon on left!")



