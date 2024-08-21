import os
import re

wlc_msg = """\33[31;1m

   ____  ________          __          _______           __         
  / __ \/ __/ __/_______  / /______   / ____(_)___  ____/ /__  _____
 / / / / /_/ /_/ ___/ _ \/ __/ ___/  / /_  / / __ \/ __  / _ \/ ___/
/ /_/ / __/ __(__  )  __/ /_(__  )  / __/ / / / / / /_/ /  __/ /    
\____/_/ /_/ /____/\___/\__/____/  /_/   /_/_/ /_/\__,_/\___/_/     

                                         
 \033[32;1m

⊱⋅ ──────────── ⋅⊰
𝖢𝗋𝖾𝖺𝗍𝗈𝗋: 𝖢𝗒𝗅𝗇𝖾 𝖬𝗈𝖽𝗓 
𝖢𝗋𝖾𝖽𝗂𝗍: @HiiCylne                                      
⊱⋅ ──────────── ⋅⊰
                                                        
  \033[33;1m
"""
print(wlc_msg)


directory = input("Input Path file .cs: ").strip()

keywords = [
     "getcoins", "SetClipSize", "IsFreeUser",  "CalculateInAirJumpCount", "CalculateHeadAttackLevel", "GetClipSize", "GetCurrentAmmo", "SetReloadSpeed", "CalculateClipSize",  "ClaimAdsRewards", "get_removeads", "get_invincible", "get_instantresourcekill", "get_freepurchases", "getgems", 
    "getdiamond", "getmoney", "get_dailygoldavailable", "get_cangetdailybonusforads", "getdollar", "get_coins", 
    "get_gems", "get_diamond", "get_money", "get_cash", "get_gold", "get_silver", "CanBulletPierceEnemies", "IsAllowedToGetEndOfLevelPerks", "getTrapCost", "get_exp", 
    "get_premiumrewardavailable", "isvip", "ispurchased", "removeads", "noads", "get_unlimitedhints", "ispro", 
    "get_premiumactive", "get_noads", "get_isadmin", "get_adsavailable", "get_doublerewardavailable", 
    "get_canunlockforgold", "donated", "unlocked", "set_hintscount", "paid", "get_goldenlockpick", "isfull", 
    "get_rateusdisabled", "ispaid", "isnoads", "isremoveads", "haspro", "hasvip", "haspaid", "haspremium", 
    "hasnoads", "hasfull", "hasremoveads", "vip", "premium", "die", "setreloadspeed", "get_power", "get_purchased", 
    "getpurchased", "checkexpired", "getunlocked", "wasbonuscodeconsumed", "isunlocked", "get_isvip", 
    "getarenalock", "get_premiumtimeremaining", "getdiamondnum", "getskinunlock", "isherounlocked", 
    "get_goldcoins", "gearsunlocked", "heroesunlocked", "get_noadspurchased", "get_ispremiumpurchaser", 
    "get_energy", "isimmuneotdamage", "calculateclipsize", "getclipsize", "getcurrentammo", "get_isloggedin", "get_payMoney", "HasProLicense", "get_AutoSolvePictures", "get_IsInvulnerable", "get_maxHealth", "isInfiniteEnergyActive", "isRewardedVideoAvailable", "get_MinDamage", "get_Stealth", "get_TotalWeight", "get_Lockpick", "CalculateInventoryWeight", "set_Health", "set_Stamina","get_Health","get_Damage","get_MaxAmmo","get_FireRate","GetDamage","get_Speed","GetSpeed","IsSubscribed","GetCurrency","GetLevel","get_level",
]

keywords = [keyword.lower() for keyword in keywords]


pattern_offset = re.compile(r"// RVA:\s+(0x[0-9A-Fa-f]+)\s+Offset:\s+(0x[0-9A-Fa-f]+)")
pattern_method = re.compile(r"public\s+(?:static\s+)?(\w+)\s+(\w+)\s*\([^)]*\)")

def search_in_file(file_path):
    results = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
            
            current_offset = None
            
            for line in content:
                offset_match = pattern_offset.search(line)
                if offset_match:
                    current_offset = offset_match.group(2)
                
                method_match = pattern_method.search(line)
                if method_match:
                    return_type, name = method_match.groups()
                    if name.lower() in keywords and current_offset:
                        results.append((name, return_type, current_offset))
                        current_offset = None
                        
    except Exception as e:
        print(f"Error when reading file {file_path}: {e}")
    return results

if not os.path.isdir(directory):
    print(f"The path {directory} does not exist or is not a directory.")
else:
    found_any = False
    results_to_write = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.cs'):
                file_path = os.path.join(root, file)
                results = search_in_file(file_path)
                if results:
                    found_any = True
                    for name, return_type, offset in results:
                        result_line = f"{name} ({return_type}) Offset: {offset}"
                        print(result_line)
                        results_to_write.append(result_line)
    if not found_any:
        print("No result is found.")
    else:
        output_file_path = os.path.join(directory, "result.txt")
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write("\n".join(results_to_write))
        print(f"Results have been saved to {output_file_path}")
