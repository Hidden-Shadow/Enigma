class Alphabet:
    def __init__(self):
        self.plugboard = {}
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        self.reflectorB = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
        self.keys = ["EKMFLGDQVZNTOWYHXUSPAIBRCJ", "AJDKSIRUXBLHWTMCQGZNPYFVOE", "BDFHJLCPRTXVZNYEIWGAKMUSQO",
                     "ESOVPZJAYQUIRHXLNFTGKDCMWB", "VZBRGITYUPSDNHLXAWMJQOFECK", "JPGVOUMFYQBENHZRDKASXLICTW",
                     "NZJHGRCXMYSWBOUFAIVLPEKQDT", "FKQHTLXOCBJSPDZRAMEWNIUYGV"]
        '''
        - Rotor I is element 0 of self.keys
        - Rotor II is element 1 of self.keys
        - etc.
        '''
        self.turnovers = ['R', 'F', 'W', 'K', 'A']

        self.alphabet_dict = {}

        for i in range(len(self.alphabet)):
            self.alphabet_dict[self.alphabet[i]] = i

    def new_plugboard(self, raw_plugboard):
        for i in range(len(raw_plugboard)):
            if raw_plugboard[i] == '-':
                self.plugboard[raw_plugboard[i - 1]] = raw_plugboard[i + 1]
                self.plugboard[raw_plugboard[i + 1]] = raw_plugboard[i - 1]
                i += 2

        #  print(self.plugboard)

    def run_plugboard(self, letter):
        if letter in self.plugboard.keys():
            return self.plugboard[letter]
        else:
            return letter


a = Alphabet()


class Dial:
    def __init__(self, initial, number, key):
        self.position = a.alphabet_dict[initial]
        self.num_rotations = 0
        self.rotate_next = False

        if key != -1:
            self.number = number
            self.key = a.keys[key]
            self.turnover = a.turnovers[key]

        elif key == -1:
            self.number = number
            self.key = a.reflectorB

    def rotate(self):
        self.position += 1
        if self.position > 25:
            self.position = 0

        if self.position == a.alphabet_dict[self.turnover]:
            self.rotate_next = True

        #  print('Dial', self.number, 'rotated. New position', a.alphabet[self.position])

    def run_dial(self, letter, direction):  # Returns STRING letter

        input_with_offset = a.alphabet_dict[letter] + self.position

        if input_with_offset > 25:
            input_with_offset -= 26

        #  print("Dial " + str(self.number) + " input " + a.alphabet[input_with_offset])

        if direction.upper() == 'FORWARD':
            output = self.key[input_with_offset]
        elif direction.upper() == 'BACKWARD':
            output = a.alphabet[self.key.index(a.alphabet[input_with_offset])]
        else:
            output = 'ERROR'

        # print("Dial " + str(self.number) + " output " + output)

        return output


class DialSet:
    def __init__(self, num_dials, initial_positions, rotors):  # len(initial_positions) has to be equal to num_dials
        #  (rotors)
        assert (num_dials == len(initial_positions) == len(rotors))
        self.dials = []

        for i in range(num_dials):
            self.dials.append(Dial(initial_positions[i], i, rotors[i]))  # This is where the dials are initialized

        self.reflector = Dial('A', -1, -1)

    def run_letter(self, letter_input):
        letter = letter_input
        self.rotate_dials()

        for dial in self.dials:
            letter = dial.run_dial(letter_input, 'FORWARD')
            letter_input_number = a.alphabet_dict[letter] - dial.position
            if letter_input_number > 25:
                letter_input_number -= 26

            letter_input = a.alphabet[letter_input_number]
            letter = a.alphabet[letter_input_number]

        letter = self.reflector.run_dial(letter, 'FORWARD')  # Returns STRING

        for dial in reversed(self.dials):
            letter = a.alphabet[a.alphabet_dict[dial.run_dial(letter, 'BACKWARD')] - dial.position]

        letter = a.alphabet_dict[letter]
        letter = a.alphabet[letter]
        return letter

    def rotate_dials(self):
        new_position = ''
        for i in range(len(self.dials)):
            if i == 0:
                self.dials[i].rotate()
                new_position += a.alphabet[self.dials[i].position]
            elif self.dials[i - 1].rotate_next:
                self.dials[i].rotate()
                self.dials[i - 1].rotate_next = False
                new_position += a.alphabet[self.dials[i].position]

            else:
                new_position += a.alphabet[self.dials[i].position]

        # print(new_position)


class Enigma:
    def __init__(self, num_dials, initial_positions, plugboard, rotors):
        self.dial_set = DialSet(num_dials, initial_positions, rotors)
        a.new_plugboard(plugboard)

    def run_cycle(self, letter):
        #  print("Letter Being Run:", letter)
        new_letter = a.run_plugboard(letter)
        #  print("After plugboard:", new_letter)
        new_letter = self.dial_set.run_letter(new_letter)
        #  print("After dials:", new_letter)
        new_letter = a.run_plugboard(new_letter)
        #  print("Final:", new_letter)
        return new_letter

    def run_full(self, string):
        encoded_string = ''
        for char in string:
            if char in a.alphabet:
                encoded_string += self.run_cycle(char)
            else:
                encoded_string += char
        return encoded_string


rotor_numbers = int(input("Enter rotor quantity: "))
initial_input = input("Enter initial rotor positions in form ABC. Must match rotor number entered above.: ")
initial_list = [char for char in initial_input.upper()]
plugboard_input = input("Enter plugboard connections in form A-B separated by spaces. Ex. A-B F-H O-I: ")
rotor_choices = input("Enter rotors to be used in numerical form, range 1-5. Ex. Rotor V and IV would be 5, 4: ")
rotor_choices = [int(char) - 1 for char in rotor_choices.upper() if char.isdigit()]
#  print(rotor_choices)

active_machine = Enigma(rotor_numbers, initial_list, plugboard_input, rotor_choices)

#  active_machine = Enigma(3, ['A', 'A', 'A'], "A-H U-O P-G M-N Q-W E-R X-C")
message_i = input("Input message: ").upper()
print("Message Input: " + message_i)
encoded = active_machine.run_full(message_i)
print("Message Encoded: " + encoded)
