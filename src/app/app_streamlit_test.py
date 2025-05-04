import streamlit as st

# Page config must be first Streamlit command
st.set_page_config(page_title="Perfect RAG System", page_icon="🤖")

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

class PerfectRAGSystem:
    def __init__(self):
        # Initialize with best available embedding model
        self.embedder = SentenceTransformer('all-mpnet-base-v2')  # Higher quality than MiniLM
        
        # Perfect knowledge base with complete, natural statements
        self.knowledge_base = np.array([
            "ML_DEFINITION: Machine learning is a branch of artificial intelligence that develops systems capable of learning from data, identifying patterns, and making decisions with minimal human intervention. Key approaches include supervised learning (using labeled data), unsupervised learning (finding hidden patterns), and reinforcement learning (learning through rewards).",
            "COGNITION_METHODS: Researchers measure human cognition through a combination of standardized psychological tests like the Wechsler Adult Intelligence Scale (WAIS) and Stanford-Binet IQ tests, along with advanced neuroimaging techniques including functional MRI (fMRI) which shows brain activity, electroencephalography (EEG) measuring electrical activity, and positron emission tomography (PET) scans that track metabolic processes.",
            "ROBOT_CAPABILITIES: Contemporary robotics systems can execute both physical operations such as delicate assembly work and microsurgery, as well as cognitive functions including real-time decision-making and environmental interpretation, achieved through sophisticated sensor arrays combined with deep learning algorithms that enable adaptation to dynamic environments.",
            "AI_DEFINITION: Artificial intelligence represents the comprehensive discipline of creating intelligent machines capable of performing tasks that typically require human cognition, including but not limited to machine learning (pattern recognition), natural language processing (communication understanding), computer vision (image interpretation), and robotic control systems (physical interaction)."
        ])
        
        # Create optimized FAISS index with proper normalization
        embeddings = self.embedder.encode(self.knowledge_base)
        faiss.normalize_L2(embeddings)
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

    def retrieve(self, question, threshold=0.35):
        """Precision retrieval with similarity validation"""
        emb = self.embedder.encode(question, convert_to_tensor=False)
        emb = np.array([emb]).astype('float32')
        faiss.normalize_L2(emb)
        scores, indices = self.index.search(emb, 1)
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

    def query(self, question):
        """Flawless query interface"""
        context = self.retrieve(question)
        if not context:
            return "I don't have sufficiently detailed information about that topic.", ""
        
        answer = self.generate_answer(question, context)
        return answer, context.split(":")[0]

# Initialize the RAG system
@st.cache_resource
def load_rag_system():
    return PerfectRAGSystem()

rag = load_rag_system()

# Streamlit UI
st.title("🤖 Perfect RAG System")
st.markdown("""
This system demonstrates a Retrieval-Augmented Generation (RAG) approach to answering questions about AI, machine learning, robotics, and cognition.
""")

# Sidebar with example questions
st.sidebar.header("Example Questions")
example_questions = [
    "What is machine learning?",
    "How do researchers measure human cognition?",
    "What capabilities do modern robots have?",
    "Provide a comprehensive definition of artificial intelligence",
    "What is deep learning?"  # Will show unknown topic handling
]

for q in example_questions:
    if st.sidebar.button(q):
        st.session_state.question = q

# Main question input
question = st.text_input(
    "Ask a question about AI, ML, robotics, or cognition:",
    value=st.session_state.get("question", "")
)

if question:
    st.subheader("Answer")
    with st.spinner("Searching for the best answer..."):
        answer, source = rag.query(question)
    
    st.markdown(f"**{answer}**")
    
    if source:
        st.markdown(f"*Source: {source}*")
    else:
        st.warning("The system couldn't find relevant information in its knowledge base for this question.")
    
    st.divider()
    st.subheader("How this works")
    st.markdown("""
    This system uses:
    1. **Retrieval**: Finds the most relevant information from a curated knowledge base
    2. **Generation**: Creates a natural-sounding answer using a language model
    3. **Quality Control**: Ensures answers are complete and well-structured
    
    Try asking follow-up questions or testing the system's knowledge boundaries!
    """)