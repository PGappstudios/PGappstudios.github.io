import openai
import json
from datetime import datetime
import random
import os
from pathlib import Path

# Your OpenAI API key
openai.api_key = 'sk-Wd6qYPXXXXXXXXXXXXXXXXXX'  # Replace with your actual API key

# Topics and their associated images (using your actual app images)
TOPICS = {
    "iOS Development": ["PG logo no BK.png", "STAR SEEKERS.png", "Baby.png"],
    "SwiftUI Tutorials": ["PG logo no BK.png", "STAR SEEKERS.png"],
    "App Marketing": ["PG logo no BK.png", "Baby.png"],
    "UI/UX Design": ["STAR SEEKERS.png", "Baby.png"],
    "Tech News": ["PG logo no BK.png"]
}

def generate_post():
    # Randomly select a category and image
    category = random.choice(list(TOPICS.keys()))
    image = random.choice(TOPICS[category])

    prompt = f"""Write a detailed blog post about {category} for iOS developers and app creators.
    Focus on practical tips and real-world examples. Include references to SwiftUI, iOS development best practices, 
    and if relevant, mention document scanning (DocyScan), astronomy (Star Seekers), or AI-powered apps (Baby AI).
    
    Format the response as a JSON object with the following structure:
    {{
        "title": "An engaging title",
        "excerpt": "A compelling 150-character summary",
        "content": "The full blog post in markdown format, including code examples if relevant",
        "tags": ["2-4 relevant tags"]
    }}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse the response
        post_data = json.loads(response.choices[0].message.content)
        
        # Load existing posts
        posts_file = Path('posts.json')
        if posts_file.exists():
            with open(posts_file, 'r') as f:
                posts = json.load(f)
        else:
            posts = {"posts": []}

        # Create new post
        new_post = {
            "id": str(len(posts["posts"]) + 1),
            "title": post_data["title"],
            "date": datetime.now().strftime("%Y-%m-%d"),
            "category": category,
            "image": image,
            "excerpt": post_data["excerpt"],
            "content": post_data["content"],
            "tags": post_data["tags"]
        }

        # Add new post to the beginning of the list
        posts["posts"].insert(0, new_post)

        # Save updated posts
        with open(posts_file, 'w') as f:
            json.dump(posts, f, indent=2)

        print(f"Successfully generated and saved post: {new_post['title']}")
        return new_post

    except Exception as e:
        print(f"Error generating post: {str(e)}")
        return None

def main():
    # Create a posts directory if it doesn't exist
    Path('posts').mkdir(exist_ok=True)
    
    # Generate a new post
    new_post = generate_post()
    
    if new_post:
        print("Post generated successfully!")
        print(f"Title: {new_post['title']}")
        print(f"Category: {new_post['category']}")
        print(f"Date: {new_post['date']}")
    else:
        print("Failed to generate post")

if __name__ == "__main__":
    main() 
