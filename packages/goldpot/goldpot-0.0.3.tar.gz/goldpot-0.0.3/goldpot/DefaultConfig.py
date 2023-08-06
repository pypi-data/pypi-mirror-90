from enum import Enum, auto

from goldpot.CompletionEnginesConfig import CompletionEnginesConfigReader, CompletionEngineConfig

class Engines(Enum):
    ADA = auto()
    BABBAGE = auto()
    CURIE = auto()
    DAVINCI = auto()
    INSTRUCT_CURIE_BETA = auto()
    INSTRUCT_DAVINCI_BETA = auto()

    def __str__(self):
        return self.name.lower().replace('_', '-')

class DefaultConfig:
    max_chars: int = 7500
    completion_engine_config: CompletionEngineConfig = CompletionEnginesConfigReader().read("conf/engines.yml").get("TST")
    search_engine_config = Engines.ADA