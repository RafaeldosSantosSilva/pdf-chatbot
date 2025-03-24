from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

def get_conversational_chain(vectorstore):
    """
    Cria cadeia de conversação usando retrieval
    """
    # Modelo de linguagem
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.3
    )
    
    # Memória de conversação
    memory = ConversationBufferMemory(
        memory_key='chat_history', 
        return_messages=True
    )
    
    # Cadeia de conversação
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    
    return conversation_chain