from bedrock_utils import (
    valid_prompt, 
    query_knowledge_base, 
    generate_response
)

def build_rag_prompt(user_prompt, context_chunks):
    """
    Constructs a comprehensive RAG prompt by combining retrieved context 
    with the user's question in a structured format.
    """
    
    # Enhanced prompt template with clearer instructions
    prompt_template = """Human: You are a specialized assistant for heavy machinery and industrial equipment.

Please use the provided technical documentation to answer the question accurately.
If the context doesn't contain relevant information, clearly state that you cannot answer based on the available documents.

<technical_documents>
{context}
</technical_documents>

<user_question>
{question}
</user_question>

Provide a detailed, technical response based solely on the documents above.

Assistant:
"""
    
    # Combine all context chunks into a single context block
    context_text = ""
    for i, chunk in enumerate(context_chunks):
        context_text += f"Document Section {i+1}:\n{chunk['content']['text']}\n\n"
        
    # Build final prompt by inserting context and question
    final_prompt = prompt_template.format(
        context=context_text.strip(),
        question=user_prompt
    )
    
    return final_prompt, context_chunks

def get_rag_response(user_prompt):
    """
    Orchestrates the complete RAG pipeline from query to response generation.
    Handles validation, retrieval, and response formatting with citations.
    """
    
    # Step 1: Validate user input against domain constraints
    print("Bot: Analyzing your question...")
    if not valid_prompt(user_prompt):
        return "I specialize in heavy machinery topics only. Please ask a question about industrial equipment, machinery maintenance, or related technical subjects."

    # Step 2: Retrieve relevant documentation from knowledge base
    print("Bot: Searching technical documentation...")
    context_chunks = query_knowledge_base(user_prompt)
    
    if not context_chunks:
        return "No relevant technical documentation found for your query. Please try rephrasing your question about heavy machinery."
        
    # Step 3: Build enhanced prompt with retrieved context
    final_prompt, sources = build_rag_prompt(user_prompt, context_chunks)
    
    # Step 4: Generate AI response using the contextual prompt
    print("Bot: Generating technical response...")
    answer = generate_response(final_prompt)
    
    # Step 5: Format response with proper source attribution
    response_text = f"{answer}\n\n📚 Reference Documents:\n"
    source_files = set()  # Track unique source documents
    
    # Extract and format source file names
    for chunk in sources:
        try:
            s3_uri = chunk['location']['s3Location']['uri']
            file_name = s3_uri.split('/')[-1]
            source_files.add(file_name)
        except (KeyError, IndexError, TypeError):
            continue
            
    # Add formatted source list
    for i, file_name in enumerate(source_files, 1):
        response_text += f"[{i}] {file_name}\n"

    return response_text


def main_chat_loop():
    """
    Main interactive chat interface for the Heavy Machinery Knowledge Base.
    Provides continuous conversation until user exits.
    """
    print("╔══════════════════════════════════════════════════╗")
    print("║    Heavy Machinery Technical Assistant           ║")
    print("║                                                  ║")
    print("╚══════════════════════════════════════════════════╝")
    print("\n🔧 Specialized in: Construction equipment, industrial machinery,")
    print("   maintenance procedures, and technical specifications")
    print("\n💡 Available commands:")
    print("   • Type your question about heavy machinery")
    print("   • Type 'quit' or 'exit' to end session")
    print("\n" + "─" * 55)
    
    while True:
        try:
            # Get user input
            user_prompt = input("\nYou: ").strip()
            
            # Exit condition check
            if user_prompt.lower() in ['quit', 'exit', 'bye']:
                print("\nThank you for using the Heavy Machinery Assistant. Goodbye!")
                break
                
            # Handle empty input
            if not user_prompt:
                print("Bot: Please enter a question about heavy machinery.")
                continue
                
            # Process query and generate response
            bot_response = get_rag_response(user_prompt)
            
            # Display formatted response
            print(f"\n🤖 Assistant: {bot_response}")
            print("─" * 55)

        except EOFError:
            print("\n\nSession ended. Thank you for using our service!")
            break
        except KeyboardInterrupt:
            print("\n\nSession interrupted. Thank you for your time!")
            break

# Application entry point
if __name__ == "__main__":
    main_chat_loop()