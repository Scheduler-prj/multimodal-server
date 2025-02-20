from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_upstage import UpstageEmbeddings
import logging
from config import UPSTAGE_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BASE_DIR = Path(__file__).resolve().parent.parent.parent
VECTOR_DB_PATH = BASE_DIR / "app/vector_databases"
TEMP_DIR = BASE_DIR / "app/temp"

VECTOR_DB_PATH.mkdir(parents=True, exist_ok=True)
TEMP_DIR.mkdir(parents=True, exist_ok=True)

embedding_model = UpstageEmbeddings(api_key=UPSTAGE_API_KEY, model="embedding-query")

def process_pdf(temp_pdf_path):
    try:
        loader = PyPDFLoader(str(temp_pdf_path))
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        texts = text_splitter.split_documents(documents)
        logger.info(f"PDF 로드 및 텍스트 청킹 완료: {temp_pdf_path}")
        return [doc.page_content for doc in texts]
    except Exception as e:
        logger.error(f"PDF 처리 중 오류 발생: {repr(e)}")
        raise ValueError("PDF 파일을 처리하는 중 오류가 발생했습니다.") from e
def save_to_faiss(member_id, doc_list):
    faiss_db_path = VECTOR_DB_PATH / f"{member_id}_faiss"

    # if not os.path.exists(str(faiss_db_path)):
    #     print(f"❌ FAISS 데이터베이스가 존재하지 않음: {faiss_db_path}")
    # else:   
    #     print(f"✅ FAISS 데이터베이스가 존재함: {faiss_db_path}")

    
    # # 데이터베이스 경로 확인    
    # if os.path.exists(str(faiss_db_path)) and os.listdir(str(faiss_db_path)):
    #     print(f"✅ FAISS 데이터베이스가 존재하며 파일이 있음: {faiss_db_path}")
    # else:
    #     print(f"❌ FAISS 데이터베이스가 존재하지 않거나 파일이 없음: {faiss_db_path}")

    
    # try:
    #     faiss_db = FAISS.load_local(faiss_db_path, embeddings=embedding_model)
    #     print("✅ FAISS 데이터베이스 로드 성공:", faiss_db_path)
    # except Exception as e:
    #     print("❌ FAISS 데이터베이스 로드 실패:", repr(e))


    try:
        faiss_db = FAISS.load_local(str(faiss_db_path), embeddings=embedding_model)
        logger.info("기존 FAISS 데이터베이스 불러오기 완료.")
        
        new_db = FAISS.from_texts(doc_list, embedding_model)
        faiss_db.merge_from(new_db)
        
        faiss_db.save_local(str(faiss_db_path))
        logger.info("FAISS DB 업데이트 완료 (새로운 벡터 추가됨).")
        
    except Exception:
        logger.warning("기존 데이터베이스를 찾을 수 없어 새 데이터베이스를 생성합니다.")
        faiss_db = FAISS.from_texts(doc_list, embedding_model)
        faiss_db.save_local(str(faiss_db_path))
        logger.info("FAISS DB 저장 완료.")

    return str(faiss_db_path)


def process_pdf_and_save_embedding(member_id, pdf_file):
    temp_pdf_path = TEMP_DIR / f"{member_id}.pdf"
    pdf_file.save(temp_pdf_path)

    try:
        doc_list = process_pdf(temp_pdf_path)
        faiss_db_path = save_to_faiss(member_id, doc_list)
        temp_pdf_path.unlink()
        return faiss_db_path
    except Exception as e:
        if temp_pdf_path.exists():
            temp_pdf_path.unlink()  # 실패 시 파일 정리
        logger.error(f"임베딩 처리 중 오류 발생: {repr(e)}")
        
        # 특정 예외 유형에 따른 예외 메시지 통합
        error_message = "임베딩 처리 중 오류가 발생했습니다."
        if isinstance(e, ValueError):
            error_message = "올바르지 않은 PDF 파일입니다."
        elif isinstance(e, FileNotFoundError):
            error_message = "처리 중 PDF 파일을 찾을 수 없습니다."
        
        raise RuntimeError(error_message) from e
