WORLD_MAP = {
	"enter_factory": ["factory_hall"],
	"factory_hall": ["factory_stairs", "factory_workshop", "factory_storage"],
	"factory_stairs": ["factory_hall", "factory_catwalk"],
	"factory_catwalk": ["factory_stairs", "factory_engine"],
	"factory_engine": ["factory_catwalk"],
	"factory_workshop": ["factory_hall"],
	"factory_storage": ["factory_hall"]
}
