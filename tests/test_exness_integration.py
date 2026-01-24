import json
import pytest
from utils.config_manager import ConfigManager

def test_default_config_broker_is_exness():
    """Test that the default configuration specifies Exness as the broker."""
    # Initialize ConfigManager with a non-existent path to trigger default config
    config_manager = ConfigManager("non_existent_config.json")
    config = config_manager.get_config()

    assert config["broker"] == "exness"
    assert "EURUSD" in config["symbols"]

def test_load_exness_config(tmp_path):
    """Test loading a specific Exness configuration file."""
    # Create a temporary config file
    config_data = {
        "broker": "exness",
        "account_id": "12345",
        "server": "Exness-Real2",
        "symbols": ["BTCUSD", "ETHUSD"]
    }
    config_file = tmp_path / "exness_config.json"
    with open(config_file, "w") as f:
        json.dump(config_data, f)

    # Load the config
    config_manager = ConfigManager(str(config_file))
    loaded_config = config_manager.get_config()

    assert loaded_config["broker"] == "exness"
    assert loaded_config["account_id"] == "12345"
    assert "BTCUSD" in loaded_config["symbols"]
