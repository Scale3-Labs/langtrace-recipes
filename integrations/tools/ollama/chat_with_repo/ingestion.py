import json,tiktoken,os,config
from typing import List, Dict, Any, Tuple
import numpy as np
from github import GitHubService
from embedding import EmbeddingService
from llmservice import LLMService

class IngestionService:
    def __init__(self, github_service: GitHubService, embedding_service: EmbeddingService):
        self.github_service = github_service
        self.embedding_service = embedding_service
        self.llm_service = LLMService()

    def generate_filename(self, repo_name: str, pr_number: int) -> str:
        repo_safe_name = repo_name.replace('/', '_')
        return f"{repo_safe_name}_pr_{pr_number}_chunks.json"

    def load_chunks_from_file(self, filename: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)
                return data.get("chunks", []), data.get("processed_files", [])
        return [], []

    def save_chunks_to_file(self, chunks: List[Dict[str, Any]], processed_files: List[str], filename: str):
        data = {
            "chunks": chunks,
            "processed_files": processed_files
        }
        with open(filename, 'w') as file:
            json.dump(data, file, indent=2)
        print(f"Saved {len(chunks)} chunks and {len(processed_files)} processed files to {filename}")

    def count_tokens(self, text: str) -> int:
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))

    def recursive_chunk(self, text: str, max_tokens: int = config.MAX_TOKENS) -> List[str]:
        if self.count_tokens(text) <= max_tokens:
            return [text]
        mid = len(text) // 2
        left = text[:mid]
        right = text[mid:]
        return self.recursive_chunk(left, max_tokens) + self.recursive_chunk(right, max_tokens)

    def generate_explanation(self, prompt: str) -> str:
        try:
            return self.llm_service.generate_explanation(prompt)
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return f"Error: Unable to generate explanation due to {str(e)}"

    def generate_safe_explanation(self, prompt: str, max_attempts: int = config.MAX_ATTEMPTS) -> str:
        for attempt in range(max_attempts):
            try:
                chunks = self.recursive_chunk(prompt, max_tokens=config.MAX_TOKENS // (2 ** attempt))
                explanations = [self.generate_explanation(chunk) for chunk in chunks]
                return " ".join(explanations).strip()
            except Exception as e:
                print(f"Error generating explanation (attempt {attempt + 1}/{max_attempts}): {e}")
                if attempt == max_attempts - 1:
                    return f"Error: Unable to generate explanation after {max_attempts} attempts. Last error: {str(e)}"
        return "Error: Unable to generate explanation due to unexpected error."

    def chunk_large_file(self, file_patch: str, chunk_size: int = config.CHUNK_SIZE) -> List[str]:
        lines = file_patch.split('\n')
        chunks = []
        current_chunk = []
        current_chunk_size = 0

        for line in lines:
            line_size = len(line)
            if current_chunk_size + line_size > chunk_size and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = []
                current_chunk_size = 0
            current_chunk.append(line)
            current_chunk_size += line_size

        if current_chunk:
            chunks.append('\n'.join(current_chunk))

        return chunks

    def create_chunks_from_patch(self, repo_info, pr_info, file_info, repo_explanation, pr_explanation):
        print(f"Processing file: {file_info['filename']}")

        if 'patch' not in file_info:
            print(f"Skipping file {file_info['filename']} as it does not contain patch information.")
            return []

        file_explanation = self.generate_safe_explanation(f"Explain the purpose and content of this file: {json.dumps(file_info)}")
        print(f"Generated file explanation for {file_info['filename']}")

        code_blocks = self.chunk_large_file(file_info['patch'])
        chunks = []

        for i, block in enumerate(code_blocks):
            chunk_explanation = self.generate_safe_explanation(f"Explain this part of the code and its changes: {block}")
            
            chunk = {
                "code": block,
                "explanations": {
                    "repository": repo_explanation,
                    "pull_request": pr_explanation,
                    "file": file_explanation,
                    "code": chunk_explanation
                },
                "metadata": {
                    "repo": repo_info["name"],
                    "pr_number": pr_info["number"],
                    "file": file_info["filename"],
                    "chunk_number": i + 1,
                    "total_chunks": len(code_blocks),
                    "timestamp": pr_info["updated_at"]
                }
            }
            chunks.append(chunk)

        print(f"Created {len(chunks)} chunks for {file_info['filename']}")
        return chunks

    def process_file_changes(self, repo_info: Dict[str, Any], pr_info: Dict[str, Any],
                             file_changes: List[Dict[str, Any]], repo_explanation: str,
                             pr_explanation: str, filename: str) -> List[Dict[str, Any]]:
        all_chunks, processed_files = self.load_chunks_from_file(filename)

        for file_info in file_changes:
            if file_info['filename'] in processed_files:
                print(f"Skipping already processed file: {file_info['filename']}")
                continue
            try:
                new_chunks = self.create_chunks_from_patch(repo_info, pr_info, file_info, repo_explanation, pr_explanation)
                all_chunks.extend(new_chunks)
                if new_chunks:
                    processed_files.append(file_info['filename'])
                self.save_chunks_to_file(all_chunks, processed_files, filename)
            except Exception as e:
                print(f"Error processing file {file_info['filename']}: {e}")

        self.embedding_service.embed_and_index_chunks(all_chunks)
        print(f"Indexed {len(all_chunks)} chunks in total.")
        return all_chunks

    def generate_response(self, query: str, chunks: List[Dict[str, Any]]) -> str:
        query_vector = self.embedding_service.model.encode([query])[0]
        
        chunk_vectors = []
        for chunk in chunks:
            chunk_id = f"{chunk['metadata']['file']}_{chunk['metadata']['chunk_number']}"
            if chunk_id in self.embedding_service.embedding_cache:
                chunk_vectors.append(self.embedding_service.embedding_cache[chunk_id])
            else:
                text_to_embed = self.embedding_service.get_full_context(chunk)
                embedding = self.embedding_service.model.encode([text_to_embed])[0]
                self.embedding_service.embedding_cache[chunk_id] = embedding
                chunk_vectors.append(embedding)
        
        chunk_vectors = np.array(chunk_vectors)
        
        similarities = np.dot(chunk_vectors, query_vector) / (np.linalg.norm(chunk_vectors, axis=1) * np.linalg.norm(query_vector))
        
        top_indices = np.argsort(similarities)[-2:][::-1]
        top_chunks = [chunks[i] for i in top_indices]
        
        repo_info = top_chunks[0]['explanations']['repository']
        pr_info = top_chunks[0]['explanations']['pull_request']
        
        context_parts = []
        seen_files = set()
        for chunk in top_chunks:
            file_info = f"File: {chunk['metadata']['file']}"
            if file_info not in seen_files:
                seen_files.add(file_info)
                context_parts.append(f"""
    {file_info}
    File Explanation: {chunk['explanations']['file']}
    """)
            
            context_parts.append(f"""
    Chunk {chunk['metadata']['chunk_number']}/{chunk['metadata']['total_chunks']}:

    Code:
    {chunk['code']}

    Code Explanation:
    {chunk['explanations']['code']}
    """)
        
        context = "\n".join(context_parts)

        full_context = f"""
    Repository: {repo_info}

    Pull Request: {pr_info}

    {context}
    """

        full_context = self.truncate_context(full_context, max_tokens=config.MAX_TOKENS)

        prompt = f""" Context: {full_context}
    \nYou are a helpful assistant that explains code changes and file contents. Based on the following context about a repository, pull request, file, and code changes, answer this question: {query}
    """
        #print("-"*100)
        #print(prompt + "\n")
        #print("-"*100)
        try:
            return self.llm_service.generate_explanation(prompt)
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return f"Error: Unable to generate explanation due to {str(e)}"

    def truncate_context(self, context: str, max_tokens: int = config.MAX_TOKENS) -> str:
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(context)
        return encoding.decode(tokens[:max_tokens])