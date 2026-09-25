"""
Centralized configuration module for LER Core
Loads and manages all configuration from ler.core.json
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

class LERConfig:
    """Singleton configuration manager for LER Core"""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LERConfig, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._config is None:
            self.load_config()
    
    def load_config(self) -> None:
        """Loads configuration from ler.core.json"""
        config_path = Path(__file__).parent / "ler.core.json"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
            self._setup_paths()
        except json.JSONDecodeError as e:
            raise ValueError(f"Error parsing JSON configuration: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading configuration: {e}")
    
    def _setup_paths(self) -> None:
        """Sets absolute paths based on the project directory"""
        self.base_dir = Path(__file__).parent.parent
        
        # Absolute paths
        self.glyphs_path = self.base_dir / self._config["paths"]["glyphs"]
        self.memory_path = self.base_dir / self._config["paths"]["memory"] 
        self.entities_path = self.base_dir / self._config["paths"]["entities"]
        self.tree_path = self.base_dir / self._config["paths"]["tree"]
        self.docs_path = self.base_dir / self._config["paths"]["docs"]
        
        # Specific files
        self.stable_memory_path = self.base_dir / self._config["files"]["stable_memory"]
        self.ontological_manifest_path = self.base_dir / self._config["files"]["ontological_manifest"]
        self.defense_protocol_path = self.base_dir / self._config["files"]["defense_protocol"]
    
    def ensure_directories(self) -> None:
        """Creates required directories if they don't exist"""
        directories = [
            self.memory_path,
            self.entities_path, 
            self.tree_path,
            self.docs_path
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    # Shortcut properties
    @property
    def version(self) -> str:
        return self._config["version"]
    
    @property 
    def name(self) -> str:
        return self._config["name"]
    
    @property
    def modules(self) -> list:
        return self._config["modules"]
    
    @property
    def mathema_operators(self) -> list:
        return self._config["mathema"]["operators"]
    
    @property
    def mathema_operator_descriptions(self) -> dict:
        return self._config["mathema"]["operator_descriptions"]
    
    @property
    def alert_glyphs(self) -> dict:
        return self._config["security"]["alert_glyphs"]
    
    @property
    def safe_mode(self) -> bool:
        return self._config["security"]["safe_mode"]
    
    @property
    def required_entity_attributes(self) -> list:
        return self._config["entities"]["required_attributes"]
    
    @property
    def max_glyphs_without_node(self) -> int:
        return self._config["syntax"]["max_glyphs_without_node"]
    
    def get(self, key: str, default: Any = None) -> Any:
        """Generic access to any configuration value using dot notation"""
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def get_startup_script(self, platform: Optional[str] = None) -> str:
        """Gets the startup script for the current or specified platform"""
        if platform is None:
            import platform as plt
            platform = "windows" if plt.system() == "Windows" else "linux"
        
        return self._config["execution"]["startup_scripts"].get(platform, "start.sh")
    
    def to_dict(self) -> Dict[str, Any]:
        """Returns the entire configuration as a dictionary"""
        return self._config.copy()
    
    def __str__(self) -> str:
        return f"LERConfig(version={self.version}, name={self.name})"
    
    def __repr__(self) -> str:
        return self.__str__()


# Global instance for easy access
config = LERConfig()

# Convenience functions
def get_config() -> LERConfig:
    """Gets the configuration instance"""
    return config

def reload_config() -> None:
    """Reloads configuration from disk"""
    config.load_config()

def ensure_project_structure() -> None:
    """Ensures the project directory structure exists"""
    config.ensure_directories()


# Example usage
if __name__ == "__main__":
    cfg = get_config()
    print(f"LER Core {cfg.version}")
    print(f"Glyphs path: {cfg.glyphs_path}")
    print(f"Mathema operators: {cfg.mathema_operators}")
    
    # Create project structure
    ensure_project_structure()
    print("\u2713 Project structure verified")
