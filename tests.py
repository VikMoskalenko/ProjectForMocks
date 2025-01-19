import unittest
from unittest.mock import patch, MagicMock, mock_open
from pokemon_name_translator import PokemonNameTranslator
from pokemon_report import PokemonReport
from pokemon_service import PokemonService
from pokemon_report import config
class TestPokemonNameTranslator(unittest.TestCase):
    @patch("pokemon_name_translator.translate.TranslationServiceClient")
    def test_translate(self, mock_translation_client):
        mock_client = MagicMock()
        mock_translation_response = MagicMock()
        mock_translation_response.translations = [MagicMock(translated_text="Pikachu (FR)")]

        mock_client.translate_text.return_value = mock_translation_response
        mock_client.location_path.return_value = "projects/your-project-id/locations/global"
        mock_translation_client.return_value = mock_client

        translator = PokemonNameTranslator()
        result = translator.translate("pikachu", target_language="fr")
        mock_client.translate_text.assert_called_once_with(
            parent="projects/your-project-id/locations/global",
            contents=["pikachu"],
            target_language_code="fr",
        )
        self.assertEqual(result, "Pikachu (FR)")

class TestPokemonService(unittest.TestCase):
    @patch("pokemon_service.requests.get")
    def test_get_pokemon_info_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "pikachu",
            "height": 4,
            "weight": 60,
            "abilities": [{"ability": {"name": "static"}}, {"ability": {"name": "lightning-rod"}}],
        }
        mock_get.return_value = mock_response

        service = PokemonService()
        result = service.get_pokemon_info("pikachu")

        mock_get.assert_called_once_with("https://pokeapi.co/api/v2/pokemon/pikachu")
        self.assertEqual(result["name"], "pikachu")
        self.assertEqual(result["height"], 4)
        self.assertEqual(result["weight"], 60)

    @patch("pokemon_service.requests.get")
    def test_get_pokemon_info_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        service = PokemonService()
        result = service.get_pokemon_info("unknown_pokemon")
        mock_get.assert_called_once_with("https://pokeapi.co/api/v2/pokemon/unknown_pokemon")
        self.assertIsNone(result)


class TestPokemonReport(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open)
    def test_create_html_report(self, mock_file):
        pokemon_info = {
            "abilities": [{"ability": {"name": "static"}}, {"ability": {"name": "lightning-rod"}}],
            "height": 4,
            "weight": 60,
        }
        translated_name = "Pikachu (FR)"
        report = PokemonReport()

        result = report.create_html_report(pokemon_info, translated_name)

        mock_file.assert_called_once_with("report_template.html", "w", encoding="utf-8")
        mock_file().write.assert_called_once()
        self.assertEqual(result, "report_template.html")



if __name__ == "__main__":
    unittest.main()
