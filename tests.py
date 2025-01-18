import unittest
from unittest.mock import patch, MagicMock
from main import main

class TestPokemonApp(unittest.TestCase):

    @patch("pokemon_name_translator.PokemonNameTranslator.translate")
    @patch("pokemon_service.PokemonService.get_pokemon_info")
    @patch("pokemon_report.PokemonReport.generate_report")
    def test_main(self, mock_generate_report, mock_get_pokemon_info, mock_translate):
        mock_get_pokemon_info.return_value = {
            "name": "pikachu",
            "height": 4,
            "weight": 60,
            "abilities": [{"ability": {"name": "static"}}, {"ability": {"name": "lightning-rod"}}]
        }
        mock_translate.return_value = "Pikachu (FR)"
        mock_generate_report.return_value = None
        main()
        mock_get_pokemon_info.assert_called_once_with("pikachu")
        mock_translate.assert_called_once_with("pikachu", target_language="fr")
        mock_generate_report.assert_called_once_with(
            mock_get_pokemon_info.return_value, mock_translate.return_value, "pokemon_report.pdf"
        )

    @patch("pokemon_service.PokemonService.get_pokemon_info")
    def test_pokemon_not_found(self, mock_get_pokemon_info):
        mock_get_pokemon_info.return_value = None
        with self.assertLogs() as log:
            main()
        self.assertIn("Pokemon not found.", log.output[-1])

if __name__ == "__main__":
    unittest.main()
