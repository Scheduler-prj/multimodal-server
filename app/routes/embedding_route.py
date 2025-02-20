from flask import Blueprint, request, jsonify
from http import HTTPStatus
from app.utils.embedding_utils import process_pdf_and_save_embedding
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pdf_blueprint = Blueprint('pdf', __name__)

@pdf_blueprint.route('/upload/<member_id>', methods=['POST'])
def upload_pdf(member_id):
    file = request.files.get('file')

    if not member_id or not file:
        return jsonify({"error": "Missing member_id or file"}), HTTPStatus.BAD_REQUEST

    try:
        vector_store_path = process_pdf_and_save_embedding(member_id, file)
        return jsonify({
            "message": "PDF processed successfully",
            "vector_store_path": vector_store_path
        }), HTTPStatus.OK
    except ValueError as e:
        logger.error(f"잘못된 PDF 파일: {repr(e)}")
        return jsonify({"error": "올바르지 않은 PDF 파일입니다."}), HTTPStatus.BAD_REQUEST
    except FileNotFoundError as e:
        logger.error(f"파일이 존재하지 않음: {repr(e)}")
        return jsonify({"error": "처리 중 PDF 파일을 찾을 수 없습니다."}), HTTPStatus.NOT_FOUND
    except Exception as e:
        logger.error(f"서버 내부 오류 발생: {repr(e)}")
        return jsonify({"error": "서버 내부 오류가 발생했습니다."}), HTTPStatus.INTERNAL_SERVER_ERROR
