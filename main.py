import random
import asyncio
from pyscript import document, window

# Jogo do Bicho Data
ANIMALS = [
    {"group": "01", "name": "Avestruz", "numbers": "01-04"},
    {"group": "02", "name": "Águia", "numbers": "05-08"},
    {"group": "03", "name": "Burro", "numbers": "09-12"},
    {"group": "04", "name": "Borboleta", "numbers": "13-16"},
    {"group": "05", "name": "Cachorro", "numbers": "17-20"},
    {"group": "06", "name": "Cabra", "numbers": "21-24"},
    {"group": "07", "name": "Carneiro", "numbers": "25-28"},
    {"group": "08", "name": "Camelo", "numbers": "29-32"},
    {"group": "09", "name": "Cobra", "numbers": "33-36"},
    {"group": "10", "name": "Coelho", "numbers": "37-40"},
    {"group": "11", "name": "Cavalo", "numbers": "41-44"},
    {"group": "12", "name": "Elefante", "numbers": "45-48"},
    {"group": "13", "name": "Galo", "numbers": "49-52"},
    {"group": "14", "name": "Gato", "numbers": "53-56"},
    {"group": "15", "name": "Jacaré", "numbers": "57-60"},
    {"group": "16", "name": "Leão", "numbers": "61-64"},
    {"group": "17", "name": "Macaco", "numbers": "65-68"},
    {"group": "18", "name": "Porco", "numbers": "69-72"},
    {"group": "19", "name": "Pavão", "numbers": "73-76"},
    {"group": "20", "name": "Peru", "numbers": "77-80"},
    {"group": "21", "name": "Touro", "numbers": "81-84"},
    {"group": "22", "name": "Tigre", "numbers": "85-88"},
    {"group": "23", "name": "Urso", "numbers": "89-92"},
    {"group": "24", "name": "Veado", "numbers": "93-96"},
    {"group": "25", "name": "Vaca", "numbers": "97-00"},
]

def init():
    # Populate Animal Select
    select_el = document.getElementById("animal-select")
    grid_el = document.getElementById("bicho-grid")
    
    for animal in ANIMALS:
        # Add to select
        option = document.createElement("option")
        option.value = animal["group"]
        option.innerText = f"{animal['group']} - {animal['name']}"
        select_el.appendChild(option)
        
        # Add to grid
        card = document.createElement("div")
        card.className = "bicho-card"
        card.innerHTML = f"""
            <div class="bicho-num">{animal['numbers']}</div>
            <div class="bicho-name">{animal['name']}</div>
            <div class="bicho-group">{animal['group']}</div>
        """
        grid_el.appendChild(card)

async def make_bet(event):
    btn = document.getElementById("btn-bet")
    val_input = document.getElementById("bet-value")
    animal_select = document.getElementById("animal-select")
    
    bet_value = float(val_input.value)
    chosen_group = animal_select.value
    
    # UI Reset
    btn.disabled = True
    btn.innerText = "Sorteando..."
    document.getElementById("result-content").classList.remove("show")
    
    # Get the "antigravity" element for animation
    orb = document.getElementById("antigravity-orb")
    orb.style.animation = "float 0.5s infinite ease-in-out" # Faster spin/float
    
    # Simulate processing delay
    await asyncio.sleep(2)
    
    # Game Logic
    winning_number = random.randint(0, 9999)
    # The result of Jogo do Bicho is based on the last 2 digits for simple group betting
    last_two = winning_number % 100
    
    # Map last_two to group
    # 01-04 -> 01, 05-08 -> 02, ..., 97-00 -> 25
    # Special case for 00 which is group 25
    if last_two == 0:
        winning_group_idx = 24 # Vaca
    else:
        winning_group_idx = (last_two - 1) // 4
    
    winning_animal = ANIMALS[winning_group_idx]
    
    # UI Update
    status_el = document.getElementById("result-status")
    bicho_el = document.getElementById("result-bicho")
    numbers_el = document.getElementById("result-numbers")
    payout_el = document.getElementById("result-payout")
    
    bicho_el.innerText = winning_animal["name"]
    numbers_el.innerText = f"Número Sorteado: {winning_number:04d} ({last_two:02d})"
    
    if winning_animal["group"] == chosen_group:
        status_el.innerText = "PARABÉNS! VOCÊ GANHOU!"
        status_el.style.color = "#00ff88"
        payout = bet_value * 18 # Group payout multiplier
        payout_el.innerText = f"Ganho: R$ {payout:.2f}"
        payout_el.style.color = "#00ff88"
    else:
        status_el.innerText = "NÃO FOI DESTA VEZ"
        status_el.style.color = "var(--text-dim)"
        payout_el.innerText = "Sorte na próxima!"
        payout_el.style.color = "var(--accent-pink)"

    # Final Reveal
    orb.style.animation = "float 2s infinite ease-in-out" # Back to normal
    document.getElementById("result-content").classList.add("show")
    
    btn.disabled = False
    btn.innerText = "Fazer Aposta"

# Initialize
init()
print("Bicho-Gravity Initialized")
