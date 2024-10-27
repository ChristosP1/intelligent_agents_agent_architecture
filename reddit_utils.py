import os
from dotenv import load_dotenv
import praw
from prawcore.exceptions import NotFound, PrawcoreException
from nlp import *


class RedditAPI:
    def __init__(self):
        """Initialize the Reddit API client using credentials from the .env file."""
        # Load environment variables from the .env file
        load_dotenv()
        
        # Fetch API keys and other credentials
        reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
        reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        user_agent = 'my_reddit_app'  # You can customize this
        
        # Initialize Reddit instance using PRAW
        self.reddit = praw.Reddit(
            client_id=reddit_client_id,
            client_secret=reddit_client_secret,
            user_agent=user_agent
        )
        
    def link_search_reddit(self, query: str, limit: int = 10):
        """
        Search Reddit globally for posts matching the query.

        Args:
            query (str): The search query.
            limit (int): The maximum number of results to return (default is 5).
    
        Returns:
            List[Dict]: A list of dictionaries containing the title, URL, and number of comments for each post.
        """
        # Ensure the limit is passed as an integer
        limit = int(limit)
        
        # Perform the global search on Reddit (using the "all" subreddit for global search)
        search_results = self.reddit.subreddit('all').search(query, limit=limit)
        
        # Collect the results into a list of dictionaries, filter out non-Reddit links
        results = []
        for post in search_results:
            if post.url.startswith("https://www.reddit.com"):
                results.append({
                    'title': post.title,
                    'url': post.url,
                    'comments': post.num_comments
                })

        return results
    
    def fetch_post_content_and_comments(self, post_url: str, comment_limit: int = 10):
        """
        Fetch the post content and the top comments from a Reddit post.
        
        Args:
            post_url (str): The URL of the Reddit post.
            comment_limit (int): The maximum number of comments to retrieve (default is 10).
        
        Returns:
            dict: A dictionary containing the post's content and the top comments.
        """
        try:
            # Extract the submission from the post URL
            submission = self.reddit.submission(url=post_url)
            
            # Get post content (selftext is the body of the post)
            post_content = submission.selftext
            
            # Get the top comments
            submission.comment_sort = 'top'
            submission.comments.replace_more(limit=0)  # Load all comments
            top_comments = submission.comments.list()[:comment_limit]  # Get top N comments

            # Extract the comment bodies
            comments_text = [comment.body for comment in top_comments]

            # Return the post content and comments
            return {
                'title': submission.title,
                'content': post_content,
                'comments': comments_text
            }

        except NotFound:
            return {"error": "Post not found or deleted."}
        except PrawcoreException as e:
            return {"error": f"An error occurred: {str(e)}"}
        
    def get_post_and_comments(self, query: str, post_limit: int = 1, comment_limit: int = 10):
        """
        This function searches Reddit for the given query, fetches posts,
        and retrieves the content and top comments for the first valid post.
        
        Args:
            query (str): The search query for Reddit.
            post_limit (int): The number of posts to retrieve (default is 1).
            comment_limit (int): The number of comments to retrieve (default is 10).
        
        Returns:
            str: A combined string of the post content and the top comments.
        """
        # Search for the query on Reddit
        search_results = self.link_search_reddit(query, limit=post_limit)
        
        # Loop through the search results to find the first valid post
        for result in search_results:
            post_url = result['url']
            post_details = self.fetch_post_content_and_comments(post_url, comment_limit=comment_limit)
            
            # If the post was fetched successfully, return the content and comments
            if "error" not in post_details:
                # Combine the post content and top comments into a single output
                output = f"Title: {post_details['title']}\n"
                output += f"Post Content: {post_details['content']}\n\n"
                output += "Top Comments:\n"
                
                for idx, comment in enumerate(post_details['comments'], 1):
                    output += f"{idx}. {comment}\n"
                
                return output
        
        # If no valid posts were found, return an appropriate message
        return "No valid results found for the query."


    def evaluate_normative_statement(self, normative_statement: str, post_limit: int = 1, comment_limit: int = 10, threshold: float = 0.6):
        """
        Evaluate a normative statement by searching for relevant posts on Reddit and comparing the cosine similarity
        between the normative statement and the Reddit posts.

        Args:
            normative_statement (str): The normative statement to evaluate.
            post_limit (int): The number of posts to retrieve (default is 1).
            comment_limit (int): The number of comments to retrieve (default is 10).
            threshold (float): The similarity threshold to determine if the statement is true or false (default is 0.6).
        
        Returns:
            dict: A dictionary indicating if the statement is true, the reason, and the cosine similarity value.
        """
        # Search for the statement on Reddit
        search_results = self.link_search_reddit(normative_statement, limit=post_limit)
        
        # Initialize variables to track the best match
        best_post = None
        best_similarity = 0
        
        # Loop through the search results to find the post with the highest similarity
        for result in search_results:
            post_url = result['url']
            post_details = self.fetch_post_content_and_comments(post_url, comment_limit=comment_limit)

            if "error" not in post_details:
                # Combine the post title, content, and comments for comparison
                combined_text = f"{post_details['title']} {post_details['content']} {' '.join(post_details['comments'])}"

                # Use the cosine_similarity function from the nlp module
                similarity = cosine_similarity(normative_statement, combined_text)
                
                # If this post has the highest similarity, update the best match
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_post = {
                        'title': post_details['title'],
                        'url': post_url,
                        'similarity': similarity,
                        'content': post_details['content'],
                        'comments': post_details['comments']
                    }

        # Evaluate if the statement is real_information based on the threshold
        if best_post and best_similarity >= threshold:
            return {
                'real_information': True,
                'reason': best_post['content'],
                'reddit_title': best_post['title'],
                'similarity': best_similarity
            }
        else:
            return {
                'real_information': False,
                'reason': best_post['content'] if best_post else "No relevant content found.",
                'reddit_title': best_post['title'] if best_post else "No relevant post title found.",
                'similarity': best_similarity  # Always include similarity, even if no relevant match was found
            }

if __name__ == "__main__":
    reddit_api = RedditAPI()  # Initialize Reddit API

    # Query for a specific topic
    query = "head ache due to lack of water "
    result = reddit_api.get_post_and_comments(query)
    
    # Print the results
    #print(result)
    
    #  a normative statement
    normative_statement = "Drinking water helps with headaches."

    # Evaluate the statement by searching Reddit
    best_match = reddit_api.evaluate_normative_statement(normative_statement, 15 , 5 ,0.35 )
    print(best_match)
