import streamlit as st
from dotenv import load_dotenv
import os
from pdf_processor import process_pdfs, get_pdf_text
from chat_engine import get_conversational_chain

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat com PDFs", page_icon=":books:")
    
    st.header("🤖 Seu Assistente de Documentos PDF")
    st.text_input("Chave da API OpenAI:", key="api_key", type="password")
    
    # Upload de PDFs
    pdf_docs = st.file_uploader(
        "Carregue seus arquivos PDF aqui:", 
        accept_multiple_files=True,
        type=['pdf']
    )
    
    # Botão para processar PDFs
    if st.button("Processar PDFs"):
        with st.spinner("Processando documentos..."):
            # Extrair texto dos PDFs
            raw_text = get_pdf_text(pdf_docs)
            
            # Criar chunks de texto e embeddings
            vector_store = process_pdfs(raw_text)
            
            # Salvar vector store na sessão
            st.session_state.vector_store = vector_store
            st.success("Documentos processados com sucesso!")
    
    # Área de chat
    st.subheader("Conversar com os Documentos")
    user_question = st.text_input("Faça uma pergunta sobre seus documentos:")
    
    if user_question:
        if 'vector_store' not in st.session_state:
            st.warning("Por favor, primeiro carregue e processe seus PDFs.")
        else:
            # Processamento da pergunta
            with st.spinner("Gerando resposta..."):
                conversation_chain = get_conversational_chain(
                    st.session_state.vector_store
                )
                
                response = conversation_chain({
                    'question': user_question,
                    'chat_history': st.session_state.get('chat_history', [])
                })
                
                # Exibir resposta
                st.write(response['answer'])
                
                # Atualizar histórico de chat
                st.session_state.chat_history = response.get('chat_history', [])

if __name__ == "__main__":
    main()