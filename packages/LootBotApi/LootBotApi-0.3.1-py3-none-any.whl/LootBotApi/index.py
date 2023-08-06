from LootBotApi import LootBotApi
api = LootBotApi("8JQplLaSFlLYy8pL11690")


elements = api.get_crafting_steps(api.get_exact_item("scudo punta tripla").id)
for element in elements:
    print(element)
