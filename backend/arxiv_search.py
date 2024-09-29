import arxiv
import openai
import os

# Set up your OpenAI API key
OPENAI_API_KEY = os.getenv('GPT_API_KEY')

# Initialize OpenAI API
openai.api_key = OPENAI_API_KEY

def get_arxiv_metadata(query="ubiquitin", max_results=5):
    """
    Function to retrieve metadata from arXiv based on a query.

    Parameters:
    - query: str : Topic to search for in arXiv (default is "ubiquitin").
    - max_results: int : Number of metadata results to retrieve (default is 5).

    Returns:
    - metadata_list: list : A list of metadata dictionaries.
    """
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance
    )
    
    metadata_list = []
    for result in search.results():
        metadata = {
            "title": result.title,
            "authors": [author.name for author in result.authors],
            "summary": result.summary,
            "published": result.published,
            "arxiv_id": result.entry_id.split('/')[-1],  # Extracting arXiv ID
            "url": result.entry_id
        }
        metadata_list.append(metadata)
    
    return metadata_list

def chatbot_with_arxiv_metadata(user_question, metadata_list):
    """
    Function to generate a response to a user question using arXiv metadata as context.

    Parameters:
    - user_question: str : The question posed by the user.
    - metadata_list: list : List of metadata dictionaries to use as context.

    Returns:
    - response: str : The chatbot's generated response.
    """
    # Prepare the context from metadata
    context = ""
    for paper in metadata_list:
        context += f"Title: {paper['title']}\n"
        context += f"Authors: {', '.join(paper['authors'])}\n"
        context += f"Published: {paper['published']}\n"
        context += f"Summary: {paper['summary']}\n"
        context += f"arXiv ID: {paper['arxiv_id']} - URL: {paper['url']}\n\n"

    # Create the prompt for the chat model
    prompt = f"Here is the metadata of recent papers:\n\n{context}\n\nAnswer the question: {user_question}"

    # Generate a response using OpenAI's API
    response = openai.ChatCompletion.create(
        api_key=OPENAI_API_KEY,
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return response['choices'][0]['message']['content']

# Example usage
if __name__ == "__main__":
    # Retrieve arXiv metadata
    metadata_list = get_arxiv_metadata(query="ubiquitin", max_results=5)
    
    # User question
    user_question = "Can you summarize the recent research on ubiquitin?"
    
    # Generate a response using the arXiv metadata as context
    response = chatbot_with_arxiv_metadata(user_question, metadata_list)
    print(f"Chatbot response: {response}")
