import requests
import configparser
from discord import Client, Intents, Embed
from discord_slash import SlashCommand, SlashContext

TOKEN_LOOKUP_TEXT="token"
CONTRACT_ADDRESS=""
COLLECTION_SIZE=1

config = configparser.ConfigParser()
config.read("bot.config")
DISCORD_API_TOKEN=config.get("DISCORD","API_TOKEN")
TOKEN_LOOKUP_TEXT=config.get("BOT_CMDS","TOKEN_LOOKUP_TEXT")
CONTRACT_ADDRESS=config.get('CONTRACT','ADDRESS')
COLLECTION_SIZE=config.get('TOKEN','MAX_SUPPLY')

bot = Client(intents=Intents.default())
slash = SlashCommand(bot)

def format_trait(value, trait_count):
    return str(value) + " (" + str(trait_count) + ")\n" + calc_trait_percent(trait_count) + "%\n \n"

def calc_trait_percent(trait_count):
    trait_percent=(trait_count / float(COLLECTION_SIZE)*100)
    if trait_percent > 10.0:
      return str(int(round(trait_percent,0)))
    else:
      return str(round(trait_percent,2))

def get_activity_section(stats):
     output = "```Range         Volume           Change          Average  \n"
     output = output + "1D".ljust(5, " ") + format_activity_value(stats.get("one_day_volume")) + format_activity_value(stats.get("one_day_change")) + format_activity_value(stats.get("one_day_average_price"))  +"\n"
     output = output + "7D".ljust(5, " ") + format_activity_value(stats.get("seven_day_volume"))  + format_activity_value(stats.get("seven_day_change"))   + format_activity_value(stats.get("seven_day_average_price"))  +"\n"
     output = output + "30D".ljust(5, " ") + format_activity_value(stats.get("thirty_day_volume"))  + format_activity_value(stats.get("thirty_day_change"))  + format_activity_value(stats.get("thirty_day_average_price"))  +"\n"
     output = output + "Total" + format_activity_value(stats.get("total_volume"))  + format_activity_value("") + format_activity_value(stats.get("average_price")) + "```"
     return output

def format_activity_value(value, currency="", padding=17):
    formatted_value="0.0"
    if isinstance(value, float):
      formatted_value = str(round(value, 2))
    else:
        formatted_value = str(value)

    if currency == "DAI":
      formatted_value = formatted_value + " "
    elif currency == "USDC":
      formatted_value = formatted_value + " "
    elif formatted_value != "":
      formatted_value = formatted_value + " ⧫"      
    formatted_value = formatted_value.rjust(padding, " ") 
    
    return formatted_value

def format_int_value(value, padding=17):
    formatted_value="0.0"
    formatted_value = str(int(value)).rjust(padding, " ") 
    return formatted_value

@slash.slash(name=TOKEN_LOOKUP_TEXT)
async def test(ctx: SlashContext, number):
    data_url = "https://api.opensea.io/api/v1/asset/" + str(CONTRACT_ADDRESS) + "/" + str(number)
    response = requests.get(data_url)
    json_data = response.json()
    #print(json_data)
    image_url=json_data.get("image_original_url")
    nft_name = json_data.get("name")
    traits = json_data.get("traits")
    embed=Embed(title="View on Opensea ", type="rich",url="https://opensea.io/assets/" + str(CONTRACT_ADDRESS) + "/" + str(number))
    embed.set_author(name=nft_name, url="", icon_url="")
    embed.set_image(url=image_url)
    for trait in traits:
      formatted_trait=format_trait(trait.get("value"), trait.get("trait_count"))      
      embed.add_field(name="__" + str(trait.get("trait_type")) + "__", value=formatted_trait, inline="true") 
      
    embed.set_footer(text="Data provided by OpenSea", icon_url="https://storage.googleapis.com/opensea-static/Logomark/Logomark-Blue.png")
    await ctx.send(embed=embed)


@slash.slash(name="floor")
async def floor(ctx: SlashContext):
    data_url = "https://api.opensea.io/api/v1/asset/" + str(CONTRACT_ADDRESS) + "/1"
    response = requests.get(data_url)
    json_data = response.json()

    #print(json_data)
    collection_slug=json_data["collection"].get("slug")
    floor_price=json_data["collection"]["stats"].get("floor_price")
    embed=Embed(title="View on Opensea ", type="rich",url="https://opensea.io/assets/" + str(collection_slug))
    embed.set_author(name="Floor Price: " + str(floor_price) + " ETH", url="", icon_url="")   
    embed.set_footer(text="Data provided by OpenSea", icon_url="https://storage.googleapis.com/opensea-static/Logomark/Logomark-Blue.png") 
    await ctx.send(embed=embed)

@slash.slash(name="stats")
async def floor(ctx: SlashContext):
    data_url = "https://api.opensea.io/api/v1/asset/" + str(CONTRACT_ADDRESS) + "/1"
    response = requests.get(data_url)
    json_data = response.json()

    #print(json_data)
    collection=json_data["collection"]
    collection_slug=collection.get("slug")
    collection_name=collection.get("name")
    stats = collection.get("stats")
    embed=Embed(title=str(collection_name) + " Collection (__View__)", type="rich",url="https://opensea.io/assets/" + str(collection_slug))    
    embed.add_field(name="__# of Owners__", value=format_int_value(stats.get("num_owners")), inline="true")  
    embed.add_field(name="__Total Supply__", value=format_int_value(stats.get("total_supply")), inline="true")         
    embed.add_field(name="__Total Sales__", value=format_int_value(stats.get("total_sales")), inline="true")         

    embed.add_field(name="__Floor Price__ ", value=format_activity_value(stats.get("floor_price")), inline="true")
    embed.add_field(name="__Average Price__", value=format_activity_value(stats.get("average_price")), inline="true")    
    embed.add_field(name="__Total Volumne__", value=format_activity_value(stats.get("total_volume")), inline="true")   
    
    activity_section = get_activity_section(stats)
    embed.add_field(name="Sales Activity", value=activity_section, inline="false")
    embed.set_footer(text="Data provided by OpenSea", icon_url="https://storage.googleapis.com/opensea-static/Logomark/Logomark-Blue.png")
    await ctx.send(embed=embed)

bot.run(DISCORD_API_TOKEN)

