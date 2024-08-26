import config,json,os
from langtrace_python_sdk import langtrace
langtrace.init(api_key = os.getenv("LANGTRACE_API_KEY"))
from github import GitHubService
from embedding import EmbeddingService
from ingestion import IngestionService

def main():
    github_service = GitHubService(config.GITHUB_TOKEN)
    embedding_service = EmbeddingService(config.EMBEDDING_MODEL, config.DIMENSION)
    ingestion_service = IngestionService(github_service, embedding_service)

    try:
        repo_name = input("Enter the GitHub repository (e.g., 'username/repo'): ")
        pr_number = int(input("Enter the Pull Request number: "))

        filename = ingestion_service.generate_filename(repo_name, pr_number)

        print("Fetching repository and PR information...")
        repo_info = github_service.fetch_repo_info(repo_name)
        pr_info = github_service.fetch_pr_info(repo_name, pr_number)
        file_changes = github_service.fetch_file_changes(repo_name, pr_number)
        readme_content = github_service.fetch_repo_readme(repo_name)
        
        repo_explanation = ingestion_service.generate_safe_explanation(
            f"Summarize the following GitHub repository README in about 150 words: {readme_content[:5000]}"
        )
        print(f"Repository explanation: {repo_explanation[:100]}...")

        pr_explanation = ingestion_service.generate_safe_explanation(f"Summarize the following pull request: {json.dumps(pr_info)}")
        print(f"PR explanation: {pr_explanation[:100]}...")

        all_chunks = ingestion_service.process_file_changes(repo_info, pr_info, file_changes, repo_explanation, pr_explanation, filename)

        print("Ready to answer questions!")
        while True:
            query = input("\nAsk a question about the pull request (or 'quit' to exit):\n")
            if query.lower() == 'quit':
                break

            similar_indices = embedding_service.search_similar_chunks(query)
            relevant_chunks = [all_chunks[i] for i in similar_indices]
            response = ingestion_service.generate_response(query, relevant_chunks)
            print(response)

    except Exception as e:
        print(f"Error in main: {e}")

main()