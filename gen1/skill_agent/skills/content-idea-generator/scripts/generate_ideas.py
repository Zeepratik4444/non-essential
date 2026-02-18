import sys

def generate_ideas(topic):
    ideas = []
    if "social media marketing" in topic.lower() or "social media" in topic.lower() or "marketing" in topic.lower():
        ideas.append("5 Instagram Reel Ideas for Small Businesses")
        ideas.append("LinkedIn Strategy: How to Generate Leads in 2024")
        ideas.append("TikTok Trends Explained: A Guide for Brands")
        ideas.append("Facebook Ad Hacks That Actually Work")
        ideas.append("Content Calendar Template for Social Media Managers")
    elif "healthy recipes" in topic.lower() or "recipes" in topic.lower() or "food" in topic.lower():
        ideas.append("Quick & Easy Healthy Weeknight Dinners")
        ideas.append("10 Vegan Meal Prep Ideas for Busy People")
        ideas.append("Gluten-Free Baking: Delicious Desserts You Won't Believe")
        ideas.append("Smoothie Recipes for a Healthy Gut")
        ideas.append("Budget-Friendly Healthy Lunch Ideas")
    elif "youtube" in topic.lower():
        ideas.append("YouTube Channel Growth: 10 Tips for Beginners")
        ideas.append("Video Editing Tutorial: DaVinci Resolve for Newbies")
        ideas.append("My Morning Routine: A Productive Start to the Day")
        ideas.append("Gaming Review: The Latest Indie Hit")
        ideas.append("Travel Vlog: Exploring Hidden Gems in [City Name]")
    elif "instagram" in topic.lower():
        ideas.append("Instagram Photography Tips: Mastering Your Smartphone Camera")
        ideas.append("Reel Ideas for Fashion Influencers")
        ideas.append("How to Grow Your Instagram Following Organically")
        ideas.append("Caption Ideas for Engaging Instagram Posts")
        ideas.append("Behind-the-Scenes: A Day in the Life of a [Profession]")
    elif "blog" in topic.lower():
        ideas.append("Blog Post Ideas for [Niche]")
        ideas.append("SEO Basics for Bloggers: Drive More Traffic")
        ideas.append("How to Write Engaging Blog Introductions")
        ideas.append("Monetizing Your Blog: 5 Proven Strategies")
        ideas.append("Guest Post Opportunities: Expand Your Reach")
    else:
        ideas.append(f"Top 5 {topic} Trends to Watch")
        ideas.append(f"Beginner's Guide to {topic}")
        ideas.append(f"The Future of {topic}: Predictions and Insights")
        ideas.append(f"{topic} Hacks You Need to Know")
        ideas.append(f"Deep Dive: Understanding {topic} Fundamentals")
    
    print(f"### Content Ideas for \"{topic}\"")
    for idea in ideas:
        print(f"- {idea}")

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "general content"
    generate_ideas(topic)
