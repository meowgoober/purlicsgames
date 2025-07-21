

import os
import shutil
from datetime import datetime

def backup_games_page():
    """create a backup of the current games.html file"""
    if os.path.exists('games.html'):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'games_backup_{timestamp}.html'
        shutil.copy2('games.html', backup_name)
        print(f"✓ backup created: {backup_name}")
        return True
    else:
        print("⚠ games.html not found in current directory")
        return False

def get_game_details():
    """prompt user for game details"""
    print("\n--- add new game ---")
    
    game_name = input("enter game name: ").strip()
    if not game_name:
        print("❌ game name cannot be empty")
        return None
    
    icon_name = input("enter icon filename (without .png): ").strip()
    if not icon_name:
        print("❌ icon name cannot be empty")
        return None
    
    folder_name = input("enter game folder name: ").strip()
    if not folder_name:
        print("❌ folder name cannot be empty")
        return None
    
    return {
        'name': game_name,
        'icon': f"{icon_name}.png",
        'folder': folder_name,
        'display_name': game_name.lower()
    }

def create_game_card_html(game_details):
    """generate html for new game card"""
    return f'''            <div class="game-card" onclick="playGame('games/{game_details['folder']}/index.html')">
                <img src="images/games/{game_details['icon']}" alt="{game_details['name']}" class="game-icon">
                <div class="game-name">{game_details['display_name']}</div>
                <a href="games/{game_details['folder']}/index.html" class="play-button">play now</a>
            </div>'''

def update_games_page(game_details):
    """update games.html with new game"""
    try:
        with open('games.html', 'r', encoding='utf-8') as file:
            content = file.read()
        
        # find the games grid section
        grid_start = content.find('<div class="games-grid" id="gamesGrid">')
        grid_end = content.find('</div>', grid_start)
        
        if grid_start == -1 or grid_end == -1:
            print("❌ could not find games grid in html file")
            return False
        
        # find the last game card to insert after it
        insert_point = content.rfind('</div>', grid_start, grid_end)
        
        if insert_point == -1:
            # no existing games, insert after grid opening tag
            insert_point = content.find('>', grid_start) + 1
            new_game_html = f"\n{create_game_card_html(game_details)}\n        "
        else:
            # insert after the last game card
            insert_point = content.find('\n', insert_point) + 1
            new_game_html = f"{create_game_card_html(game_details)}\n"
        
        # insert the new game
        updated_content = content[:insert_point] + new_game_html + content[insert_point:]
        
        # write the updated content
        with open('games.html', 'w', encoding='utf-8') as file:
            file.write(updated_content)
        
        return True
        
    except Exception as e:
        print(f"❌ error updating games page: {e}")
        return False

def display_summary(game_details):
    """display summary of added game"""
    print(f"\n--- game added successfully ---")
    print(f"game name: {game_details['name']}")
    print(f"display name: {game_details['display_name']}")
    print(f"icon path: images/games/{game_details['icon']}")
    print(f"game path: games/{game_details['folder']}/index.html")
    print(f"\n📁 make sure to create the game folder: games/{game_details['folder']}/")
    print(f"🖼️ make sure to add the icon: images/games/{game_details['icon']}")

def main():
    """main function"""
    print("🎮 purlics games - games adder")
    print("=" * 40)
    
    # check if games.html exists and create backup
    if not backup_games_page():
        create_new = input("create a new games.html? (y/n): ").lower().strip()
        if create_new != 'y':
            print("❌ exiting...")
            return
        else:
            print("❌ this script requires an existing games.html file to modify")
            return
    
    # get game details from user
    game_details = get_game_details()
    if not game_details:
        print("❌ invalid game details. exiting...")
        return
    
    # update the games page
    if update_games_page(game_details):
        display_summary(game_details)
        print("\n✅ game successfully added to games.html!")
        
        # ask if user wants to add another game
        add_another = input("\nadd another game? (y/n): ").lower().strip()
        if add_another == 'y':
            main()
    else:
        print("❌ failed to update games page")

def show_current_games():
    """display currently added games"""
    try:
        with open('games.html', 'r', encoding='utf-8') as file:
            content = file.read()
        
        # extract game names from the content
        games = []
        lines = content.split('\n')
        for line in lines:
            if 'class="game-name"' in line:
                start = line.find('>') + 1
                end = line.find('<', start)
                if start > 0 and end > start:
                    games.append(line[start:end].strip())
        
        if games:
            print(f"\n--- current games ({len(games)}) ---")
            for i, game in enumerate(games, 1):
                print(f"{i}. {game}")
        else:
            print("\n--- no games found ---")
            
    except FileNotFoundError:
        print("❌ games.html not found")
    except Exception as e:
        print(f"❌ error reading games: {e}")

if __name__ == "__main__":
    # show menu
    while True:
        print("\n🎮 purlics games - games adder")
        print("1. add new game")
        print("2. show current games")
        print("3. exit")
        
        choice = input("\nselect option (1-3): ").strip()
        
        if choice == '1':
            main()
        elif choice == '2':
            show_current_games()
        elif choice == '3':
            print("👋 goodbye!")
            break
        else:
            print("❌ invalid choice. please select 1, 2, or 3.")