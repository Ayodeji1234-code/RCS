def caesar_encrypt(text, shift):
    result = ""
    for char in text:
      if char.islower():
        result += chr((ord(char) + shift - ord('a')) % 26 + ord('a'))
      elif char.isupper():
        result += chr((ord(char) + shift - ord('A')) % 26 + ord('A'))

      else:
        result += char
    return result

def caesar_decrypt(text, shift):
  result = ""
  for char in text:
    if char.islower():
      result += chr((ord(char) - shift - ord('a')) % 26 + ord('a'))
    elif char.isupper():
      result += chr((ord(char) - shift - ord('A')) % 26 + ord('A'))

    else:
      result += char
  return result

def caesar_cipher():
  while True:
      choice = input("Do you want to (e)ncrypt or (d)ecrypt or (q)uit? ").strip()
      if choice == 'q':
        print("exiting caesar ciper. Goodbye!")
        break
      if choice not in ['e', 'd']:
            print("Invalid choice. Choose 'e' or 'd'.")
            continue

      text = input("Enter the message: ")
      try:
        shift = int(input("Enter shift amount: "))
      except ValueError:
        print("Invalid shift amount. Please enter an integer.")
        continue

      if choice == 'e':
          encrypted = caesar_encrypt(text, shift)
          print("🔐 Encrypted message:", encrypted)
      if choice == 'd':
          decrypted = caesar_decrypt(text,shift)
          print("🔓 Decrypted message:", decrypted)

# Run the cipher
if __name__ == "__main__":
    caesar_cipher()
