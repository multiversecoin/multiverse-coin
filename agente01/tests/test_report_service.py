"""Tests for report generation service."""

from app.services.report_service import classify_evidences


def test_classify_by_tags():
    evidences = [
        {"tags": ["CASCO", "ANTES"], "filename_original": "img1.jpg", "observacao_operador": ""},
        {"tags": ["CASCO", "DEPOIS"], "filename_original": "img2.jpg", "observacao_operador": ""},
        {"tags": ["HELICE"], "filename_original": "img3.jpg", "observacao_operador": ""},
    ]
    result = classify_evidences(evidences)

    assert "CASCO" in result
    assert len(result["CASCO"]["ANTES"]) == 1
    assert len(result["CASCO"]["DEPOIS"]) == 1
    assert "HELICE" in result
    assert len(result["HELICE"]["NAO_CLASSIFICADO"]) == 1


def test_classify_by_filename_heuristic():
    evidences = [
        {"tags": [], "filename_original": "CASCO_ANTES_001.jpg", "observacao_operador": ""},
        {"tags": [], "filename_original": "CASCO_DEPOIS_001.jpg", "observacao_operador": ""},
    ]
    result = classify_evidences(evidences)

    assert "CASCO" in result
    assert len(result["CASCO"]["ANTES"]) == 1
    assert len(result["CASCO"]["DEPOIS"]) == 1


def test_classify_empty():
    result = classify_evidences([])
    assert result == {}


def test_classify_unknown_area():
    evidences = [
        {"tags": ["ANTES"], "filename_original": "random.jpg", "observacao_operador": ""},
    ]
    result = classify_evidences(evidences)
    assert "OUTROS" in result
    assert len(result["OUTROS"]["ANTES"]) == 1
