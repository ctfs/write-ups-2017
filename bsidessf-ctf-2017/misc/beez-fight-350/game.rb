#!/usr/local/bin/ruby

require 'readline'

require_relative './items.rb'
require_relative './locations.rb'
require_relative './monsters.rb'

# Turns off stdout buffering
$stdout.sync = true

YOU = {
  :weapon_equipped => false,
  :weapon => nil,

  :shield_equipped => false,
  :shield => nil,

  :inventory => (1..3).map() { random_item(ALL_ITEMS) },

  :gold => 10,
  :health => 80,
  :location => :club,
  :experience => 0,
}

MONSTER = {
  :present => false,
  :monster => nil,
}

# Generate a handful of random items for the store, in addition to the flag
STORE = FLAGS + (0..8).map { random_item(ALL_ITEMS) }

class BeezException < StandardError
end

# Get an item from a specific index in the player's inventory
def get_from_inventory(num)
  num = num.to_i()
  if(num < 1 || num > YOU[:inventory].length())
    raise(BeezException, "Itemnum needs to be an integer between 1 and #{YOU[:inventory].length()}")
  end
  return YOU[:inventory][num - 1]
end

# Don't allow certain actions when a monster is present
def ensure_no_monster()
  if(MONSTER[:present])
    raise(BeezException, "That action can't be taken when a monster is present!")
  end
end

# Check if a monster appears
def gen_monster()
  # Don't spawn multiple monsters
  if(MONSTER[:present] == true)
    return
  end

  if(rand() < location()[:monster_chance])
    MONSTER[:present] = true
    MONSTER[:monster] = (MONSTERS.select() { |m| m[:appears_in].include?(YOU[:location]) }).sample().clone()
    MONSTER[:max_health] = MONSTER[:monster][:health].to_a().sample()
    MONSTER[:health] = MONSTER[:max_health]

    puts()
    puts("Uh oh! You just got attacked by #{MONSTER[:monster][:name]}! Better defend yourself!")
    sleep(1)
    raise(BeezException, "You are now in combat!")
  end
end

def location()
  return LOCATIONS[YOU[:location]]
end

# Do the monster's attack, if one is present
def monster_attack()
  if(!MONSTER[:present])
    return
  end

  # Start by randomizing which of the monster's attacks it uses
  monster_attack = MONSTER[:monster][:weapons].sample()

  # Randomly choose a damage from the list of possible damages from the attack
  monster_damage = monster_attack[:damage].to_a().sample().to_f()

  # Scale down the damage based on the monster's health (makes the game a little easier)
  monster_adjusted_damage = (monster_damage * (MONSTER[:health].to_f() / MONSTER[:max_health].to_f())).ceil()

  # Scale down the damage if a shield is equipped
  if(YOU[:shield_equipped] && monster_adjusted_damage > 0)
    monster_adjusted_damage = monster_adjusted_damage * YOU[:shield][:defense]
  end

  # Round the damage up
  monster_adjusted_damage = monster_adjusted_damage.ceil().to_i()

  puts("The #{MONSTER[:monster][:name]} attacks you with its #{monster_attack[:weapon_name]} for #{monster_adjusted_damage} damage!")
  YOU[:health] -= monster_adjusted_damage

  # Check if the player is dead
  if(YOU[:health] <= 0)
    puts()
    puts("You were killed by the #{}! :( :( :(")
    puts("RIP #{YOU[:name]}!")
    1.upto(10) do
      puts(":(")
      sleep(1)
    end
    exit(0)
  end

  puts("You have #{YOU[:health]}hp left!")
  puts()
  sleep(1)
end

# Unequip a weapon or armour
def unequip(which)
  if(which == "weapon")
    if(!YOU[:weapon])
      raise(BeezException, "You aren't using a weapon!")
    end

    YOU[:inventory] << YOU[:weapon]
    YOU[:weapon_equipped] = false
    puts("You unequipped your weapon!")
  elsif(which == "shield")
    if(!YOU[:shield])
      raise(BeezException, "You aren't using a shield!")
    end

    YOU[:inventory] << YOU[:shield]
    YOU[:shield_equipped] = false
    puts("You unequipped your shield!")
  else
    raise(BeezException, "You can only unequip a weapon or shield!")
  end
end

# Do a single 'tick' of hte game
def tick()
  # Print character
  puts()
  puts("  -------------------------------------------------------------------------------")
  puts("  The Brave Sir/Lady #{YOU[:name]}")
  puts("  Gold: #{YOU[:gold]}gp")
  puts("  Health: #{YOU[:health]}hp")
  puts("  Experience: #{YOU[:experience]}")
  puts()

  if(YOU[:weapon_equipped])
    puts("  Left hand: #{YOU[:weapon][:name]}")
  else
    puts("  Left hand: No weapon!");
  end

  if(YOU[:shield_equipped])
    puts("  Right hand: #{YOU[:shield][:name]}")
  else
    puts("  Right hand: No shield!");
  end

  puts()
  puts("  Inventory: #{YOU[:inventory].map() { |i| i[:name] }.join(", ")}")

  puts()
  puts("  Location: #{location()[:name]}")
  puts("  -------------------------------------------------------------------------------")
  puts()

  # If there's a monster present, display it
  if(MONSTER[:present])
    puts("You're in combat with #{MONSTER[:monster][:name]}!")
    puts()
  end

  # If the player is in the store, print its inventory
  if(YOU[:location] == :store)
    puts("For sale:")
    1.upto(STORE.length()) do |i|
      puts("%d :: %s (%dgp)" % [i, STORE[i - 1][:name], STORE[i - 1][:value]])
    end
    puts()
  end

  # Get command
  command = Readline.readline("> ", true)
  if(command.nil?)
    puts("Bye!")
    exit(0)
  end

  # Split the command/args at the space
  command, args = command.split(/ /, 2)
  puts()

  # Process command
  if(command == "look")
    # Print a description of hte locatoin
    puts("#{location()[:description]}. You can see the following:" )

    # Print the attached locations
    1.upto(location()[:connects_to].length()) do |i|
      puts("%2d :: %s" % [i, LOCATIONS[location()[:connects_to][i - 1]][:name]])
    end
  elsif(command == "move")
    # Don't allow moving if there's a monster
    ensure_no_monster()

    # See if a monster apperas
    gen_monster()

    # Make sure it's a valid move
    args = args.to_i
    if(args < 1 || args > location()[:connects_to].length)
      raise(BeezException, "Invalid location")
    end

    # Update the location
    YOU[:location] = location()[:connects_to][args - 1]
    puts("Moved to #{location()[:name]}")
  elsif(command == "search")
    puts("You search the ground around your feet...")
    sleep(1)

    # See if a monster appears
    gen_monster()

    # If no monster appeared, see if an item turns up
    if(rand() < location()[:item_chance])
      item = random_item(ALL_ITEMS)
      puts("...and find #{item[:name]}")
      YOU[:inventory] << item
    else
      puts("...and find nothing!");
    end
    puts()

    # After searching for an item, if there's a monster present, let it attack
    monster_attack()
  elsif(command == "inventory")
    puts "Your inventory:"
    1.upto(YOU[:inventory].length()) do |i|
      item = get_from_inventory(i)
      if(item.nil?)
        return
      end
      puts("%3d :: %s (worth %dgp)" % [i, item[:name], item[:value]])
    end
  elsif(command == "describe")
    # Show the description for an item. Note that this is what you have to do with the flag.txt item to get the flag!
    item = get_from_inventory(args)
    puts("%s -> %s" % [item[:name], item[:description]])
  elsif(command == "equip")
    # Attempt to equip an item
    item = get_from_inventory(args)
    if(item[:type] == :weapon)
      if(YOU[:weapon_equipped])
        unequip('weapon')
      end

      YOU[:weapon_equipped] = true
      YOU[:weapon] = item

      puts("Equipped #{item[:name]} as a weapon!")
    elsif(item[:type] == :shield)
      if(YOU[:shield_equipped])
        unequip('shield')
      end

      YOU[:shield_equipped] = true
      YOU[:shield] = item

      puts("Equipped #{item[:name]} as a shield!")
    else
      raise(BeezException, "#{item[:name]} can't be equipped!")
    end

    # Remove the item from inventory after equipping it
    YOU[:inventory].delete_at(args.to_i - 1)

  elsif(command == "drop")
    # Just remove the item from inventory
    item = get_from_inventory(args)
    YOU[:inventory].delete_at(args.to_i - 1)

    puts("Dropped #{item[:name]} into the eternal void")
  elsif(command == "drink")
    item = get_from_inventory(args)
    if(item[:type] != :potion)
      raise(BeezException, "That item can't be drank!")
    end

    # Remove the item from the inventory
    YOU[:inventory].delete_at(args.to_i - 1)

    # Heal for a random amount
    amount = item[:healing].to_a.sample
    YOU[:health] += amount
    puts("You were healed for #{amount}hp!")
    puts()
    sleep(1)
    monster_attack()
  elsif(command == "sell")
    ensure_no_monster()
    if(YOU[:location] != :store)
      raise(BeezException, "This can only be done at the store!")
    end

    # Remove the item from inventory
    item = get_from_inventory(args)
    YOU[:inventory].delete_at(args.to_i - 1)

    # Increase your gold by the item's value
    YOU[:gold] += item[:value]
    STORE << item

    puts("You sold the #{item[:name]} for #{item[:value]}gp!")
  elsif(command == "buy")
    ensure_no_monster()
    if(YOU[:location] != :store)
      raise(BeezException, "This can only be done at the store!")
    end

    args = args.to_i()
    if(args < 1 || args > STORE.length())
      raise(BeezException, "Itemnum needs to be an integer between 1 and #{STORE.length()}")
    end

    # MAke sure they can afford the item
    item = STORE[args - 1]
    if(item[:value] > YOU[:gold])
      raise(BeezException, "You can't afford that item!")
    end

    # Remove the item from the store
    STORE.delete_at(args - 1)
    YOU[:inventory] << item
    YOU[:gold] -= item[:value]

    puts("You bought %s for %dgp!" % [item[:name], item[:value]])
  elsif(command == "attack")
    if(!MONSTER[:present])
      puts("Only while monster is present!!!")
      return
    end

    # Get the amount of damage
    if(YOU[:weapon_equipped])
      your_attack = YOU[:weapon][:damage].to_a.sample()
      puts("You attack the #{MONSTER[:monster][:name]} with your #{YOU[:weapon][:name]} doing #{your_attack} damage!")
    else
      your_attack = (0..2).to_a.sample
      puts("You attack the #{MONSTER[:monster][:name]} with your fists doing #{your_attack} damage!")
    end

    # Reduce the monster's health
    MONSTER[:health] -= your_attack

    # Check if the monster is dead
    if(MONSTER[:health] <= 0)
      puts("You defeated the #{MONSTER[:monster][:name]}!")

      # If the monster died, have it drop a random item
      item = random_item(ALL_ITEMS)
      puts("It dropped a #{item[:name]}!")
      YOU[:inventory] << item
      MONSTER[:present] = false
    else
      puts("It's still alive!")
    end
    puts()
    sleep(1)

    monster_attack()

  elsif(command == "unequip")
    unequip(args)
  else
    puts("Commands:")
    puts()
    puts("look")
    puts("  Look at the current area. Shows other areas that the current area connects")
    puts("  to.")
    puts()

    puts("move <locationnum>")
    puts("  Move to the selected location. Get the <locationnum> from the 'look' command.")
    puts()
    puts("  Be careful! You might get attacked while you're moving! You can't move when")
    puts("  you're in combat.")
    puts()

    puts("search")
    puts("  Search the area for items. Some areas will have a higher or lower chance")
    puts("  of having items hidden.")
    puts()
    puts("  Be careful! You might get attacked while you're searching!")
    puts()

    puts("inventory")
    puts("  Show the items in your inventory, along with their <itemnum> values, which")
    puts("  you'll need in order to use them!")
    puts()

    puts("describe <itemnum>")
    puts("  Show a description of the item in your inventory. <itemnum> is obtained by")
    puts("  using the 'inventory' command.")
    puts()

    puts("equip <itemnum>")
    puts("  Equip a weapon or shield. Some unexpected items can be used, so try equipping")
    puts("  everything!")
    puts()

    puts("unequip <weapon|shield>")
    puts("  Unequip (dequip?) your weapon or shield.")
    puts()

    puts("drink <itemnum>")
    puts("  Consume a potion. <itenum> is obtained by using the 'inventory' command.")
    puts()

    puts("drop <itemnum>")
    puts("  Consign the selected item to the eternal void. Since you have unlimited")
    puts("  inventory, I'm not sure why you'd want to do that!")
    puts()

    puts("buy <storenum>")
    puts("  Buy the selected item. Has to be done in a store. The list of <storenum>")
    puts("  values will be displayed when you enter the store")
    puts()

    puts("sell <itemnum>")
    puts("  Sell the selected item. Has to be done in a store. Note that unlike other")
    puts("  games, we're fair and items sell for the exact amount they're bought for!")
    puts("  <itemnum> is obtained by using the 'inventory' command.")
    puts()

    puts("attack")
    puts("  Attack the current monster.")
  end
end

puts("Welcome, brave warrior! What's your name?")
print("--> ")
YOU[:name] = gets().strip()

puts()
puts("Welcome, #{YOU[:name]}! Good luck on your quest!!");
puts()
puts("You just woke up. You don't remember what happened to you, but you're somewhere with loud music. You aren't sure what's going on, but you know you need to get out of here!")
puts()
puts("Press <enter> to continue");
gets()

loop do
  begin
    tick()
  rescue BeezException => e
    puts("Error: #{e}")
  end
end
