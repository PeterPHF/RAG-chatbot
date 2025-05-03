import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class RAGSystem:
    def __init__(self):
        # Efficient embedding model (same as original)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load FAISS index and chunks
        self.index = faiss.read_index("D:\\RAG chatbot\\data\\embeddings\\vector_index_CS.faiss")
        self.chunks = np.load("D:\\RAG chatbot\\data\\processed\\text_chunks.npy", allow_pickle=True)
        
        # Smaller text generation model - using GPT-2 small or DistilGPT-2
        # Alternative options you could try:
        # - 'distilgpt2' (smaller version of GPT-2)
        # - 'facebook/opt-125m' (efficient alternative)
        # - 'EleutherAI/gpt-neo-125m' (open alternative)
        model_name = 'facebook/opt-350m'  # default to original, but you can change to smaller model
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        lm_model = AutoModelForCausalLM.from_pretrained(model_name)
        
        self.generator = pipeline(
            'text-generation',
            model=lm_model,
            tokenizer=tokenizer,
            device='cpu'  # remove this if you want to use GPU
        )

    def retrieve_relevant_chunks(self, question, k=1):
        question_embedding = self.model.encode(question, convert_to_tensor=False)
        question_embedding = np.array([question_embedding]).astype('float32')
        faiss.normalize_L2(question_embedding)
        similarities, indices = self.index.search(question_embedding, k)
        return [self.chunks[i] for i in indices[0]]

    def generate_answer(self, question, relevant_chunks):
        context = "\n\n".join(relevant_chunks)
        prompt = f"""Answer the following question using only this context\n\nContext: {context}\n\nQuestion: {question}\n\nAnswer:"""
        
        answer = self.generator(
            prompt,
            max_new_tokens=500,  # more precise than max_length
            num_return_sequences=1,
            temperature=0.7,  # slightly higher for more diversity
            truncation=True,
            do_sample=True,
            pad_token_id=self.generator.tokenizer.eos_token_id  # better stopping condition
        )
        
        # Improved answer extraction
        generated_text = answer[0]['generated_text']
        if "Answer:" in generated_text:
            return generated_text.split("Answer:")[-1].strip()
        return generated_text[len(prompt):].strip()  # fallback

    def query(self, question, k=1):
        relevant_chunks = self.retrieve_relevant_chunks(question, k)
        answer = self.generate_answer(question, relevant_chunks)
        return answer, relevant_chunks