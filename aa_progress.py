import json

biomes_all = [
	"badlands",
	"bamboo_jungle",
	"beach",
	"birch_forest",
	"cherry_grove",
	"cold_ocean",
	"dark_forest",
	"deep_cold_ocean",
	"deep_dark",
	"deep_frozen_ocean",
	"deep_lukewarm_ocean",
	"deep_ocean",
	"desert",
	"dripstone_caves",
	"eroded_badlands",
	"flower_forest",
	"forest",
	"frozen_ocean",
	"frozen_peaks",
	"frozen_river",
	"grove",
	"ice_spikes",
	"jagged_peaks",
	"jungle",
	"lukewarm_ocean",
	"lush_caves",
	"mangrove_swamp",
	"meadow",
	"mushroom_fields",
	"ocean",
	"old_growth_birch_forest",
	"old_growth_pine_taiga",
	"old_growth_spruce_taiga",
	"plains",
	"river",
	"savanna",
	"savanna_plateau",
	"snowy_beach",
	"snowy_plains",
	"snowy_slopes",
	"snowy_taiga",
	"sparse_jungle",
	"stony_peaks",
	"stony_shore",
	"sunflower_plains",
	"swamp",
	"taiga",
	"warm_ocean",
	"windswept_forest",
	"windswept_gravelly_hills",
	"windswept_hills",
	"windswept_savanna",
	"wooded_badlands"]
mobs_all = [
	'blaze',
	'bogged',
	'breeze',
	'cave_spider',
	'creeper',
	'drowned',
	'elder_guardian',
	'ender_dragon',
	'enderman',
	'endermite',
	'evoker',
	'ghast',
	'guardian',
	'hoglin',
	'husk',
	'magma_cube',
	'phantom',
	'piglin',
	'piglin_brute',
	'pillager',
	'ravager',
	'shulker',
	'silverfish',
	'skeleton',
	'slime',
	'spider',
	'stray',
	'vex',
	'vindicator',
	'witch',
	'wither',
	'wither_skeleton',
	'zoglin',
	'zombie',
	'zombified_villager',
	'zombified_piglin']
breed_all = [
	'armadillo',
	'axolotl',
	'bee',
	'camel',
	'cat',
	'chicken',
	'cow',
	'donkey',
	'fox',
	'frog',
	'goat',
	'hoglin',
	'horse',
	'llama',
	'mooshroom',
	'mule',
	'ocelot',
	'panda',
	'pig',
	'rabbit',
	'sheep',
	'sniffer',
	'strider',
	'turtle',
	'wolf']
cats_all = [
	'black',
	'british_shorthair',
	'calico',
	'jellie',
	'persian',
	'ragdoll',
	'red',
	'siamese',
	'tabby',
	'tuxedo',
	'white']
wolves_all = [
	'ashen',
	'black',
	'chestnut',
	'pale',
	'rusty',
	'snowy',
	'spotted',
	'striped',
	'woods']
food_all = [
	'apple',
	'baked_potato',
	'beetroot',
	'beetroot_soup',
	'bread',
	'carrot',
	'chorus_fruit',
	'cooked_chicken',
	'cooked_cod',
	'cooked_mutton',
	'cooked_porkchop',
	'cooked_rabbit',
	'cooked_salmon',
	'cookie',
	'dried_kelp',
	'enchanted_golden_apple',
	'glow_berries',
	'golden_apple',
	'golden_carrot',
	'honey_bottle',
	'melon_slice',
	'mushroom_stew',
	'poisonous_potato',
	'potato',
	'pufferfish',
	'pumpkin_pie',
	'rabbit_stew',
	'raw_beef',
	'raw_chicken',
	'raw_cod',
	'raw_mutton',
	'raw_porkchop',
	'raw_rabbit',
	'raw_salmon',
	'rotten_flesh',
	'spider_eye',
	'steak',
	'suspicious_stew',
	'sweet_berries',
	'tropical_fish']
trims_all = [
	'Rib',
	'Silence',
	'Snout',
	'Spire',
	'Tide',
	'Vex',
	'Ward',
	'Wayfinder',]

def get_uuid(player_name: str) -> str:
	f = open('test_files/usercache.json')
	users = json.load(f)
	f.close()
	for user in users:
		if user['name'] == player_name:
			return user['uuid']
	return None

def get_advancement_progress(player_uuid: str, key: str) -> {str, str}:
	filename = 'test_files/' + player_uuid + '.json'
	f = open(filename)
	aa = json.load(f)
	f.close()

	if key == 'biomes' and 'minecraft:adventure/adventuring_time' in aa:
		progress = aa['minecraft:adventure/adventuring_time']
		list_all = biomes_all
	elif key == 'kill' and 'minecraft:adventure/kill_all_mobs' in aa:
		progress = aa['minecraft:adventure/kill_all_mobs']
		list_all = mobs_all
	elif key == 'eat' and 'minecraft:husbandry/balanced_diet' in aa:
		progress = aa['minecraft:husbandry/balanced_diet']
		list_all = food_all
	elif key == 'breed' and 'minecraft:husbandry/bred_all_animals' in aa:
		progress = aa['minecraft:husbandry/bred_all_animals']
		list_all = breed_all
	elif key == 'cat' and 'minecraft:husbandry/complete_catalogue' in aa:
		progress = aa['minecraft:husbandry/complete_catalogue']
		list_all = cats_all
	elif key == 'wolf' and 'minecraft:husbandry/whole_pack' in aa:
		progress = aa['minecraft:husbandry/whole_pack']
		list_all = wolves_all
	else:
		print("ADVANCEMENT NOT FOUND")
		return None, None

	return compare_with_completed(key, progress, list_all)

def compare_with_completed(key: str, progress: dict, list_all: list) -> {str, str}:
	if progress['done'] == True:
		n_done = len(list_all)
		list_missing = ["Done!"]
	else:
		list_missing = []
		n_done = len(list_all)
		list_done = [b.replace('minecraft:', '') for b in list(progress['criteria'].keys())]
		for x in list_all:
			if x not in list_done:
				list_missing.append(x)
				n_done -= 1
	n_done_str = "("+ str(n_done) + "/" + str(len(list_all)) + ")"
	return n_done_str, list_missing

if __name__ == '__main__':

	from test_files.cfg import player_name

	advancement = "breed" #['biomes','kill','breed','eat','cat','wolf']

	player_uuid = get_uuid(player_name)
	progress, missing = get_advancement_progress(player_uuid, advancement)
	print(progress)
	print(missing)