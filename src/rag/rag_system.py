import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

class PerfectRAGSystem:
    def __init__(self):
        # Initialize with best available embedding model
        self.embedder = SentenceTransformer('all-mpnet-base-v2')  # Higher quality than MiniLM
        
        # Perfect knowledge base with complete, natural statements
        self.knowledge_base = np.load("D:\RAG-chatbot\data\embeddings\gfg_embeddings_mpnet_2.npz")['chunks']
        
        # Create optimized FAISS index with proper normalization
        embeddings = np.load("D:\RAG-chatbot\data\embeddings\gfg_embeddings_mpnet_2.npz")['embeddings']
        embeddings = np.array(embeddings).astype('float32')
        faiss.normalize_L2(embeddings) #  normalize the vectors to unit length (L2 norm = 1) 
        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(np.array(embeddings).astype('float32'))
        
        # Top-quality generator with optimal parameters
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base", truncation_side='left')
        self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
        self.generator = pipeline(
            "text2text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device='cpu',
            truncation=True
        )

    def retrieve(self, question, k, threshold=0.35):
        """Precision retrieval with similarity validation"""
        emb = self.embedder.encode(question, convert_to_tensor=False)
        emb = np.array([emb]).astype('float32')
        faiss.normalize_L2(emb)
        scores, indices = self.index.search(emb, k)
        return self.knowledge_base[indices[0][0]] if scores[0][0] >= threshold else None

    def generate_answer(self, question, context):
        """Generate perfect natural language answers"""
        prompt = f"""Compose a professional, complete answer to the question using the provided context. 
        The answer should:
        - Be a single well-structured paragraph
        - Include all key details from the context
        - Sound natural and authoritative
        - Not contain phrases like "the context says"

        Question: {question}
        Context: {context}

        Professional Answer:"""
        
        answer = self.generator(
            prompt,
            max_length=250,
            num_beams=5,
            temperature=0.6,
            early_stopping=True,
            repetition_penalty=2.5,
            no_repeat_ngram_size=3
        )[0]['generated_text'].strip()
        
        # Final quality check
        if len(answer.split()) < 10 or "don't know" in answer.lower():
            return self._polish_context_extract(context)
        return answer

    def _polish_context_extract(self, context):
        """Create perfect answer from context when generation fails"""
        core_info = context.split(":", 1)[1].strip()
        if not core_info.endswith("."):
            core_info += "."
        return core_info[0].upper() + core_info[1:]  # Ensure proper capitalization

    def query(self, question, k):
        """Flawless query interface"""
        context = self.retrieve(question, k)
        if not context:
            return "I don't have sufficiently detailed information about that topic.", ""
        
        answer = self.generate_answer(question, context)
        return answer, context.split(":")[0]

# Test the perfected system
rag = PerfectRAGSystem()

questions = [
    "What is machine learning?",
    "What is deep learning?",
    "How do researchers measure human cognition?",
    "What capabilities do modern robots have?",
    "Provide a comprehensive definition of artificial intelligence",
    "Explain how nuclear reactors work"  # Unknown topic test
]

print("=== PERFECTED RAG SYSTEM ===")
for q in questions:
    answer, source = rag.query(q, k=3)
    print(f"\nQ: {q}\nA: {answer}\nSource: {source}")

# Without RAG - just using the language model
# tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base", truncation_side='left')
# model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
# generator = pipeline(
#     "text2text-generation",
#     model=model,
#     tokenizer=tokenizer,
#     device='cpu',
#     truncation=True
# )
# question = "answer the following question in detail\n question: What is deep learning?"
# answer = generator(question, max_length=200)[0]['generated_text']
# print("answer:", answer)