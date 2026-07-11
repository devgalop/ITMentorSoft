import pytest

from src.features.shared.template_loader import TemplateLoader


def test_load_existing_template():
    loader = TemplateLoader()
    content = loader.load("recovery_password")
    assert "<!DOCTYPE html>" in content
    assert "Recuperación de contraseña" in content


def test_load_nonexistent_template_raises_file_not_found():
    loader = TemplateLoader()
    with pytest.raises(FileNotFoundError, match="Template not found:"):
        loader.load("nonexistent_template")


def test_load_returns_string_content():
    loader = TemplateLoader()
    content = loader.load("recovery_password")
    assert isinstance(content, str)


def test_load_with_custom_base_path(tmp_path):
    template_file = tmp_path / "custom.html"
    template_file.write_text("<html>Custom template</html>", encoding="utf-8")

    loader = TemplateLoader(base_path=str(tmp_path))
    content = loader.load("custom")
    assert content == "<html>Custom template</html>"
